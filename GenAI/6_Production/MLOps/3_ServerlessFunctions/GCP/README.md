# Serverless Machine Learning with Google Cloud Functions

A concise guide to deploying ML models as serverless HTTP APIs using Google Cloud Functions, with production-ready examples.

---

## Table of Contents
1. [Quick Start](#quick-start)
2. [When to Use](#when-to-use)
3. [Architecture](#architecture)
4. [Implementation Guide](#implementation-guide)
5. [Security](#security)

---

## Quick Start

### GCP Components Needed
- **Google Cloud Functions** - Serverless compute
- **Cloud Storage (GCS)** - Model artifact storage
- **IAM** - Access control
- **Cloud Logging** - Monitoring

### Setup (5 minutes)
```bash
# 1. Create Cloud Function via GCP Console
gcloud functions create predict \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated

# 2. Enable required APIs
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable storage-api.googleapis.com
```

---

## When to Use

### ✅ Good Fit
- MVP/prototype model serving
- Low to medium traffic (<1000 req/min)
- Batch processing jobs
- Event-driven ML pipelines
- Quick iteration needed

### ❌ Consider Alternatives
- High-volume streaming (use Vertex AI)
- Sub-100ms latency (use Compute Engine)
- GPU-heavy inference (use Vertex AI)
- Complex ML infrastructure

### Key Trade-offs

| Factor | Serverless | Compute Engine |
|--------|-----------|-----------------|
| **Cost at Scale** | Higher per-request | Lower per-hour |
| **Setup Time** | Minutes | Hours |
| **Cold Start** | 2-5 seconds | Instant |
| **Scaling** | Automatic | Manual |

---

## Architecture

### Data Flow
```
Client Request
    ↓
HTTP Trigger
    ↓
Cloud Function
    ├─ Download Model (GCS)
    ├─ Cache in Memory
    └─ Run Inference
    ↓
JSON Response
```

### GCP Components Interaction
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP POST (JSON)
       ▼
┌──────────────────────────┐
│  Cloud Functions         │
│  ┌────────────────────┐  │
│  │ Trigger: HTTP      │  │
│  │ Runtime: Python    │  │
│  │ Memory: 256MB-8GB  │  │
│  └────────────────────┘  │
└──────┬───────────────────┘
       │ GCS Client
       ▼
┌──────────────────────────┐
│  Cloud Storage           │
│  ├─ Model files         │
│  └─ Artifacts           │
└──────────────────────────┘
```

---

## Implementation Guide

![alt text](<Screenshot 2025-10-31 at 1.51.16 PM.png>)

### 1. Basic Echo Service (Test Setup)

**`main.py`**
```python
def echo_service(request):
    """Test endpoint to verify setup"""
    from flask import jsonify
    
    request_json = request.get_json()
    message = request_json.get('msg', 'No message')
    
    return jsonify({'echo': message})
```

**`requirements.txt`**
```
flask>=1.1.1
```

**Test**
```bash
curl -X POST https://REGION-PROJECT.cloudfunctions.net/echo_service \
  -H "Content-Type: application/json" \
  -d '{"msg": "Hello"}'

# Response: {"echo": "Hello"}
```

---

### 2. scikit-learn Model Serving

**`main.py`**
```python
from google.cloud import storage
from flask import jsonify
import pickle
import pandas as pd

# Global cache
model = None

def predict_sklearn(request):
    global model
    
    params = request.get_json()
    
    # Lazy load model on first request
    if not model:
        client = storage.Client()
        bucket = client.bucket('your-bucket')
        blob = bucket.blob('models/model.pkl')
        blob.download_to_filename('/tmp/model.pkl')
        
        with open('/tmp/model.pkl', 'rb') as f:
            model = pickle.load(f)
    
    # Prepare input
    features = pd.DataFrame([{
        'feature1': float(params.get('f1', 0)),
        'feature2': float(params.get('f2', 0)),
    }])
    
    # Predict
    prediction = model.predict(features)[0]
    
    return jsonify({
        'prediction': float(prediction),
        'success': True
    })
```

**`requirements.txt`**
```
google-cloud-storage
scikit-learn
pandas
flask
```

**Test**
```python
import requests

url = "https://REGION-PROJECT.cloudfunctions.net/predict_sklearn"
response = requests.post(url, json={'f1': 1.5, 'f2': 2.3})
print(response.json())
# {"prediction": 0.87, "success": true}
```

---

### 3. TensorFlow/Keras Model Serving

**Key Difference: Custom Metrics**
- Train-time metric definitions don't exist at inference time
- Must redefine custom functions

**`main.py`**
```python
from google.cloud import storage
from tensorflow.keras.models import load_model
from flask import jsonify
import pandas as pd

model = None

def predict_keras(request):
    global model
    
    # Define custom metric (must match training)
    import tensorflow as tf
    def auc(y_true, y_pred):
        return tf.keras.metrics.AUC()(y_true, y_pred)
    
    params = request.get_json()
    
    # Lazy load
    if not model:
        client = storage.Client()
        bucket = client.bucket('your-bucket')
        blob = bucket.blob('models/keras_model.h5')
        blob.download_to_filename('/tmp/model.h5')
        
        # Load with custom objects
        model = load_model(
            '/tmp/model.h5',
            custom_objects={'auc': auc}
        )
    
    # Prepare input
    features = pd.DataFrame([{
        'input1': float(params.get('i1', 0)),
        'input2': float(params.get('i2', 0)),
    }])
    
    # Predict (TensorFlow 2.x handles eager execution automatically)
    prediction = model.predict(features, verbose=0)[0][0]
    
    return jsonify({
        'prediction': float(prediction),
        'success': True
    })
```

**`requirements.txt`**
```
google-cloud-storage
tensorflow>=2.10
pandas
flask
```

---

### 4. Performance Optimization

#### Model Caching Impact
```
First Call:  3-4 seconds (download + inference)
Later Calls: 100-200ms (cached + inference)
```

#### Best Practices
```python
# ✅ Cache globally
model = None

def predict(request):
    global model
    if not model:
        # Download once
        model = load_model(...)
    # Use on every call
```

```python
# ❌ Don't reload each time
def predict(request):
    model = load_model(...)  # Reloads every time!
```

#### Memory Optimization
```python
# Keep models small
# Quantize: float32 → int8 (saves 75%)
# Remove unnecessary layers
# Use model compression tools

# Typical sizes:
# scikit-learn model: 1-50MB
# Keras CNN: 50-200MB
# BERT-style: 300-600MB
```

---

## Security

### ⚠️ Production Warning

**Never use unauthenticated access in production.**

Default setup is **open to the world** and anyone can:
- Make unlimited predictions
- Incur costs on your account
- Extract model behavior

### Disable Public Access

```bash
# Step 1: Edit Cloud Function
# Uncheck "Allow unauthenticated invocations"

# Step 2: Set IAM roles
gcloud functions add-iam-policy-binding predict \
  --member=serviceAccount:my-service@PROJECT.iam.gserviceaccount.com \
  --role=roles/cloudfunctions.invoker
```

### Authenticate Requests

**Option A: Service Account (Recommended for services)**
```python
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import requests

credentials = service_account.Credentials.from_service_account_file(
    'key.json',
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)
credentials.refresh(Request())

headers = {'Authorization': f'Bearer {credentials.token}'}
response = requests.post(
    'https://REGION-PROJECT.cloudfunctions.net/predict',
    json={'f1': 1.5},
    headers=headers
)
```

**Option B: API Key (Simple, development only)**
```bash
# Generate in GCP Console → APIs & Services → Credentials
gcloud functions describe predict --gen-login-url
```

### Monitoring & Logging

```bash
# View logs
gcloud functions logs read predict --limit 50

# Enable detailed logging in function
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def predict(request):
    logger.info(f"Received: {request.get_json()}")
    # ... inference ...
    logger.info("Prediction complete")
```

---

## Deployment Checklist

### Development
- [ ] Test locally with sample data
- [ ] Use `gcloud functions deploy --source=. --runtime=python311`
- [ ] Keep unauthenticated for rapid testing

### Production
- [ ] Disable unauthenticated access
- [ ] Set up IAM authentication
- [ ] Enable Cloud Logging
- [ ] Add input validation
- [ ] Set memory limits (256MB-8GB)
- [ ] Configure timeouts (60-540 seconds)
- [ ] Document API schema
- [ ] Test with production data (sample only)

---

## Deployment Commands

```bash
# Deploy new function
gcloud functions deploy predict \
  --runtime python311 \
  --trigger-http \
  --entry-point predict_keras \
  --memory 512MB \
  --timeout 120

# Update function
gcloud functions deploy predict --update-build-config

# View function details
gcloud functions describe predict

# View real-time logs
gcloud functions logs read predict --follow

# Delete function
gcloud functions delete predict
```

---

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| **"scikit-learn not found"** | Use `scikit-learn` in requirements.txt, not `sklearn` |
| **Model not loading** | Use `/tmp` only; GCS integration required for permanent storage |
| **Cold starts too slow** | Cache model in global variable; keep dependencies minimal |
| **Out of memory** | Reduce model size or increase memory allocation (up to 8GB) |
| **Timeout errors** | Increase timeout; consider async processing for long jobs |

---

## Cost Estimation

```
Monthly cost = (Requests × Time × Memory) + Storage

Example (100K requests/month, 1 second each, 512MB):
- Compute: 100K × 1s × 512MB ≈ $15-20/month
- Storage: 100GB ≈ $2/month
- Total: ~$20/month (much cheaper than always-on server)
```

---

## Next Steps

- **High Volume?** → Migrate to Vertex AI Prediction
- **Complex ML?** → Use Vertex AI Pipelines
- **Real-time?** → Use Compute Engine for lower latency
- **Async?** → Use Cloud Tasks or Pub/Sub

---

## References

- [GCP Cloud Functions Docs](https://cloud.google.com/functions/docs)
- [Authentication Guide](https://cloud.google.com/functions/docs/securing/authenticating)
- [Limits & Quotas](https://cloud.google.com/functions/quotas)
- [Pricing Calculator](https://cloud.google.com/products/calculator)