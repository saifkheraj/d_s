# Serverless ML on AWS Lambda

Deploy ML models as HTTP APIs using Lambda and API Gateway.

---

## Architecture

```
Client Request
    ↓
API Gateway (HTTP)
    ↓
Lambda (Python runtime)
    ├─ Load model (cached globally)
    ├─ Parse JSON
    └─ Predict
    ↓
JSON Response
```

---

## When to Use Lambda

✅ **Good**
- MVP/prototype serving
- Low traffic (<1K req/min)
- Batch jobs
- Quick iteration

❌ **Not Good**
- Large models (>250MB)
- Sub-100ms latency needed
- GPU required
- Complex infrastructure

---

## Setup Overview

```
1. Create IAM role (Lambda execution permission)
2. Package code + model + dependencies locally → zip
3. Deploy zip to Lambda
4. Add API Gateway trigger
5. Test via HTTP
```

---

## Step 1: IAM Role

```bash
# Create role
aws iam create-role \
  --role-name lambda-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach policy
aws iam attach-role-policy \
  --role-name lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Get ARN (save this!)
aws iam get-role --role-name lambda-role --query 'Role.Arn'
```

---

## Step 2: Package Locally

**On your computer:**

```bash
mkdir lambda-ml && cd lambda-ml

# Install dependencies to current directory
pip3 install scikit-learn joblib pandas --no-deps -t .

# Copy your model
cp /path/to/model.pkl .

# Create function
cat > lambda_function.py << 'EOF'
import json
import joblib
import pandas as pd

model = joblib.load('model.pkl')

def lambda_handler(event, context):
    try:
        # API Gateway wraps JSON in 'body'
        body = json.loads(event.get('body', '{}'))
        
        # Prepare features
        X = pd.DataFrame([{
            'f1': float(body.get('f1', 0)),
            'f2': float(body.get('f2', 0)),
        }])
        
        # Predict
        pred = float(model.predict(X)[0])
        
        return {
            'statusCode': 200,
            'body': json.dumps({'prediction': pred})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
EOF

# Verify structure
ls -la
# Should have: lambda_function.py, model.pkl, sklearn/, pandas/, joblib/
```

---

## Step 3: Create Zip & Deploy

**Still on your computer:**

```bash
# Create zip with everything
zip -r function.zip .

# Deploy
aws lambda create-function \
  --function-name predict \
  --runtime python3.11 \
  --role arn:aws:iam::123456789012:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip \
  --timeout 60 \
  --memory-size 512
```

**To update:** 
```bash
zip -r function.zip .
aws lambda update-function-code \
  --function-name predict \
  --zip-file fileb://function.zip
```

---

## Step 4: API Gateway

**AWS Console → API Gateway → Create API:**

1. Choose **REST API**
2. Create resource `/predict`
3. POST method → Integration: Lambda Function
4. Select `predict` function
5. Deploy → Stage: `prod`
6. Copy **Invoke URL**

---

## Step 5: Test

```bash
API_URL="https://abc123.execute-api.us-east-1.amazonaws.com/prod/predict"

# Test with curl
curl -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d '{"f1": 1.5, "f2": 2.3}'

# Response: {"prediction": 0.87}
```

**Python test:**
```python
import requests

url = "https://abc123.execute-api.us-east-1.amazonaws.com/prod/predict"
resp = requests.post(url, json={'f1': 1.5, 'f2': 2.3})
print(resp.json())
```

---

## Keras/TensorFlow Model

```python
import json
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np

model = None

def lambda_handler(event, context):
    global model
    
    if not model:
        model = tf.keras.models.load_model('model.h5')
    
    body = json.loads(event.get('body', '{}'))
    X = np.array([[float(body.get('i1', 0)), float(body.get('i2', 0))]])
    pred = float(model.predict(X, verbose=0)[0][0])
    
    return {
        'statusCode': 200,
        'body': json.dumps({'prediction': pred})
    }
```

⚠️ **Warning:** TensorFlow is 200+ MB. May exceed Lambda 250MB limit. Use S3 for model storage.

---

## S3-Based Model Loading (For Large Models)

```python
import boto3
import joblib

s3 = boto3.client('s3')
model = None

def lambda_handler(event, context):
    global model
    
    if not model:
        # Download model on first call
        s3.download_file('your-bucket', 'model.pkl', '/tmp/model.pkl')
        model = joblib.load('/tmp/model.pkl')
    
    # ... prediction logic ...
```

**Setup:**
```bash
# Upload model to S3
aws s3 cp model.pkl s3://your-bucket/model.pkl

# Add S3 read permission to Lambda role
aws iam attach-role-policy \
  --role-name lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

---

## Performance

| Factor | Impact |
|--------|--------|
| **Cold Start** | 2-5s (first invocation) |
| **Warm** | 100-200ms (subsequent) |
| **Memory** | 128MB-10GB (higher = faster) |
| **Timeout** | 15-900 seconds |

**Optimization:**
- Global model caching (already done in examples)
- Increase memory: `aws lambda update-function-configuration --memory-size 1024`
- Minimize dependencies (use `--no-deps` flag)

---

## Security

⚠️ **Default: API open to world**

**Disable public access:**
```bash
# In AWS Console:
# API Gateway → Settings → Resource Policy
# Add restriction or use IAM authentication
```

**Simple: API Key**
```bash
# Create API key
aws apigatewayv2 create-api-key --name ml-key

# Require key in requests
curl -X POST "$API_URL" \
  -H "x-api-key: YOUR-KEY" \
  -d '{"f1": 1.5}'
```

---

## Limits

| Item | Limit |
|------|-------|
| Package size | 250MB |
| Memory | 128-10,240MB |
| Timeout | 900 seconds |
| /tmp storage | 512MB |

---

## Cost Estimate

```
100K requests/month × 1 second × 512MB ≈ $20/month
(+ ~$3.50 for API Gateway)
```

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| "Unable to import module" | Check zip has libraries: `unzip -l function.zip \| head` |
| "Model not found" | Model must be in zip or S3 |
| "Task timed out" | Increase timeout: `--timeout 120` |
| "Out of memory" | Increase memory or use S3 model loading |

---

## Quick Commands

```bash
# View logs
aws logs tail /aws/lambda/predict --follow

# View function details
aws lambda get-function --function-name predict

# Delete function
aws lambda delete-function --function-name predict

# Invoke directly
aws lambda invoke \
  --function-name predict \
  --payload '{"f1":1.5}' \
  response.json
```

---

## Key Concepts

- **Global variables persist** between invocations in same container
- **Global model loading = performance boost** (3s → 100ms)
- **API Gateway wraps request in 'body'** field
- **Local testing with --no-deps** keeps package small
- **/tmp is writable**, rest of filesystem is read-only