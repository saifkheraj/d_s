# AWS Lambda & S3 Setup Guide

## 🎯 Objective
Learn to deploy two types of serverless functions on AWS Lambda:
1. **Simple Echo Function** - Basic serverless function using inline code editor
2. **ML Model Function** - Deploy machine learning models with external dependencies

## 🔧 Prerequisites
- AWS Account with console access
- AWS CLI installed locally
- Python environment

---

## Part 1: Simple Echo Function

### 📋 What We're Building
A basic Lambda function that receives a message and echoes it back - no external libraries needed.

### Quick Steps
1. Create Lambda function in AWS console
2. Write simple Python code inline
3. Test the function

### Implementation
1. **Create Function**
   - AWS Console → Lambda → Create Function
   - Choose "Author from scratch"
   - Name: `echo`, Runtime: Python
   - Click "Create Function"

2. **Write Code** (Replace generated code):
```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': event.get('msg', 'No message provided')
    }
```

3. **Test Function**
   - Create test event:
```json
{
    "msg": "Hello from Lambda!"
}
```

---

## Part 2: S3 Storage Setup

### 📋 What We're Building
S3 bucket to store our ML function's zip file (Lambda needs this for functions with dependencies).

### Why S3?
Lambda's inline editor can't handle external libraries like pandas/sklearn. We need to:
- Package our code + libraries into a zip file
- Store the zip file in S3
- Tell Lambda to load the function from S3

### Quick Steps
1. Create S3 bucket
2. Create IAM user with S3 access
3. Configure AWS CLI

### Implementation
1. **Create Bucket**
```bash
aws s3api create-bucket --bucket your-unique-bucket-name --region us-east-1
```

2. **Setup IAM User**
   - AWS Console → IAM → Users → Add user
   - Username: `s3-user`, Access: Programmatic
   - Policy: `AmazonS3FullAccess`
   - Save Access Key ID & Secret Key

3. **Configure CLI**
```bash
aws configure
# Access Key ID: [your-key]
# Secret Access Key: [your-secret]  
# Region: us-east-1
# Output: json
```

---

## Part 3: ML Model Function

### 📋 What We're Building  
A Lambda function that serves a machine learning model (logistic regression) with predictions via API.

### Why Zip Files?
Unlike the simple echo function, ML models need:
- External libraries (pandas, sklearn)
- Model files (.pkl files)
- Lambda's inline editor can't handle these dependencies
- Solution: Bundle everything into a zip file

### The Process Flow
```
Local Environment → Install Dependencies → Add Model Files → Create Zip → Upload to S3 → Configure Lambda
```

### Quick Steps
1. Create local environment with dependencies
2. Add model files  
3. Package everything into zip file
4. Upload zip to S3
5. Create Lambda function from S3 zip
6. Test the ML predictions

### Detailed Implementation

#### Step 1: Setup Local Environment

**Where to run these commands:**
- **On your local computer** (Windows/Mac/Linux terminal/command prompt)
- **OR on a cloud instance** (EC2, Cloud9, etc.)
- **NOT in AWS Console** - these are terminal/command line operations

**Commands to run:**
```bash
# Navigate to your working directory (e.g., Desktop, Documents, etc.)
cd ~/Desktop  # or wherever you want to work

# Create directory for our function
mkdir lambda && cd lambda

# Install ML libraries locally (not globally)
# -t . means "install in current directory"
# --no-deps means "don't install sub-dependencies"
pip3 install pandas --no-deps -t .
pip3 install pytz --no-deps -t .  
pip3 install scikit-learn==0.22.0 --no-deps -t .
pip3 install joblib --no-deps -t .

# Copy your trained model file (assuming it's in parent directory)
cp ../logit.pkl logit.pkl
```

**Directory structure after these commands:**
```
~/Desktop/lambda/          (your working folder)
├── pandas/               (installed here)
├── sklearn/              (installed here)  
├── joblib/               (installed here)
├── pytz/                 (installed here)
└── logit.pkl             (your model file)
```

**Why install locally?** 
- Lambda needs all dependencies packaged with your code
- Installing with `-t .` puts libraries in current folder
- This folder gets zipped and uploaded

#### Step 2: Create Lambda Function Code

**Where:** Still in your local `~/Desktop/lambda/` directory

Create `lambda_function.py` using any text editor (VS Code, Notepad++, nano, etc.):

```python
from sklearn.externals import joblib
import pandas as pd
import json

# Load model once when function starts (not on every request)
model = joblib.load('logit.pkl')

def lambda_handler(event, context):
    # Parse incoming request
    if "body" in event:
        event = event["body"]
        if event is not None:
            event = json.loads(event)
        else:
            event = {}
    
    # Check if we have the required parameters (G1-G10)
    if "G1" in event:
        # Create DataFrame from input parameters
        new_row = {
            "G1": event["G1"], "G2": event["G2"], "G3": event["G3"],
            "G4": event["G4"], "G5": event["G5"], "G6": event["G6"], 
            "G7": event["G7"], "G8": event["G8"], "G9": event["G9"],
            "G10": event["G10"]
        }
        new_x = pd.DataFrame.from_dict(new_row, orient="index").transpose()
        
        # Make prediction (probability of positive class)
        prediction = str(model.predict_proba(new_x)[0][1])
        return {"body": "Prediction " + prediction}
    
    return {"body": "No parameters provided"}
```

**Current directory structure:**
```
~/Desktop/lambda/
├── lambda_function.py        (just created)
├── logit.pkl                 (your model)
├── pandas/                   (libraries)
├── sklearn/
├── joblib/
└── pytz/
```

#### Step 3: Package and Deploy

**Where:** Still in your local terminal, in the `~/Desktop/lambda/` directory

```bash
# Make sure you're in the lambda directory
pwd  # Should show: /Users/yourname/Desktop/lambda (or similar)

# Create zip file with everything
zip -r logitFunction.zip .

# Upload to S3 bucket (requires AWS CLI configured)
aws s3 cp logitFunction.zip s3://your-bucket-name/logitFunction.zip

# Verify upload
aws s3 ls s3://your-bucket-name/
```

**Understanding the zip command:**
- `zip` = Command to create zip archives
- `-r` = **Recursive flag** - includes all subdirectories and their contents
- `logitFunction.zip` = Name of the zip file being created
- `.` = **Current directory** - means "zip everything in the current folder"

**What gets zipped:**
```
logitFunction.zip contains:
├── lambda_function.py          (your code)
├── logit.pkl                   (your model file)
├── pandas/                     (folder with pandas library)
│   ├── __init__.py
│   ├── core/
│   └── ... (all pandas files)
├── sklearn/                    (folder with sklearn library)
│   ├── __init__.py
│   ├── linear_model/
│   └── ... (all sklearn files)  
├── joblib/                     (joblib library folder)
├── pytz/                       (timezone library folder)
└── ... (any other files/folders in current directory)
```

**Why recursive (-r) is needed:**
- Without `-r`: Only gets files, ignores library folders → Lambda fails with import errors
- With `-r`: Gets everything (files + all library folders + subfolders) → Lambda works properly

#### Step 4: Configure Lambda Function

**Where:** AWS Console (web browser)

1. **Create Function**
   - Go to AWS Console → Lambda → Create Function
   - Choose "Author from scratch"
   - Name: `logit-model`

2. **Upload from S3**
   - Code entry type: "Upload from S3"
   - S3 URL: `s3://your-bucket-name/logitFunction.zip`
   - Handler: `lambda_function.lambda_handler`

3. **Add Required Layer**
   - Scroll to Layers section → Add Layer
   - Choose "AWS Layers" → Select SciPy layer
   - This provides additional math libraries sklearn needs

#### Step 5: Test the Function

**Where:** AWS Console Lambda function page

Create test event:
```json
{
  "G1": "1", "G2": "1", "G3": "1", "G4": "1", "G5": "1",
  "G6": "1", "G7": "1", "G8": "1", "G9": "1", "G10": "1"
}
```

Expected output: `{"body": "Prediction 0.85"}`

---

## Part 4: API Gateway Setup

### 📋 What We're Building
An API Gateway that allows external services to call your Lambda function via HTTP requests (instead of just testing in AWS console).

### Why API Gateway?
- Lambda functions are isolated by default
- API Gateway creates a public HTTP endpoint
- External applications can send POST/GET requests to your model
- Enables real-world usage of your ML model

### Quick Steps
1. Add API Gateway trigger to Lambda function
2. Configure REST API with open security
3. Test via API Gateway console
4. Get endpoint URL for external calls

### Implementation

#### Step 1: Add API Gateway Trigger
**Where:** AWS Console - Your Lambda function page

1. **Add Trigger**
   - In Lambda function → "Function Overview" tab
   - Click "Add Trigger"
   - Select "API Gateway"

2. **Configure API**
   - Select "Create a new API"
   - Choose "REST API" 
   - Security: "Open" (no authentication required)
   - Click "Add"

**Result:** API Gateway appears in the Designer layout connected to your Lambda function

#### Step 2: Test API Gateway
**Where:** AWS Console - API Gateway section

1. **Access Test Interface**
   - Click on "API Gateway" in the Designer
   - Click on your API name (e.g., "logit-API")
   - Click "Test"

2. **Test with JSON Body**
   ```json
   {
     "G1": "1", "G2": "0", "G3": "0", "G4": "0", "G5": "0",
     "G6": "0", "G7": "0", "G8": "0", "G9": "0", "G10": "0"
   }
   ```

**Important:** API Gateway requests have different structure than console tests - this is why our Lambda function checks for `"body"` in the event object.

#### Step 3: Get API Endpoint URL
**Where:** AWS Console - Designer section

- Click on "API Gateway" in the Designer
- Copy the API endpoint URL (looks like: `https://xyz123.execute-api.us-east-1.amazonaws.com/default/your-function-name`)

#### Step 4: Call from External Code
**Where:** Your local computer or any system with Python

```python
import requests

# Replace with your actual API endpoint URL
api_url = "https://3z5btf0ucb.execute-api.us-east-1.amazonaws.com/default/logit"

# Send POST request with JSON data
result = requests.post(api_url, 
    json = { 
        'G1':'1', 'G2':'0', 'G3':'0', 'G4':'0', 'G5':'0', 
        'G6':'0', 'G7':'0', 'G8':'0', 'G9':'0', 'G10':'0' 
    })

# Print the prediction result
print(result.text)  # Output: {"body": "Prediction 0.23"}
```

### Model Updates & Deployment Options

**Current Approach (Manual):**
- Update model file locally → Rebuild zip → Upload to S3 → Deploy new version
- Good for infrequent updates

**Scalable Approaches:**
1. **S3-based Model Loading:** Function fetches model from S3 at runtime
2. **Trigger-based Updates:** Set up S3 triggers to notify function of new models
3. **Version Management:** Use Lambda versions/aliases for A/B testing

---

## 🚀 Quick Reference

### Common S3 Commands
```bash
aws s3 ls                                    # List buckets
aws s3 cp file.txt s3://bucket-name/         # Upload file  
aws s3 cp s3://bucket-name/file.txt ./       # Download file
```

### Key Concepts
- **Inline Editor**: For simple functions with no dependencies
- **S3 Deployment**: For functions with external libraries
- **Zip Packaging**: Bundle code + dependencies + model files
- **Lambda Layers**: Pre-built libraries (like SciPy) from AWS
- **Handler**: Tells Lambda which function to call (`filename.function_name`)

### Troubleshooting
- **Import errors**: Check if layer is added (SciPy for sklearn)
- **File not found**: Ensure model file is in zip package
- **Timeout**: Increase Lambda timeout in configuration
- **Memory**: Increase memory allocation for large models

# 🧠 ML API Endpoint on AWS (Lambda + API Gateway)

This project demonstrates how to deploy a **serverless API** that serves predictions from a Machine Learning model using:

* **AWS Lambda** (backend logic)
* **API Gateway** (public HTTP endpoint)
* **S3 (optional)** for model storage

---

## 📦 Folder Structure

```
├── lambda_function.py   # Lambda code for prediction
├── model.pkl            # Trained ML model (optional)
├── requirements.txt     # Python dependencies (e.g., scikit-learn, numpy)
├── function.zip         # Zipped deployment package (code + model)
└── README.md            # You're here!
```

---

## ✅ Prerequisites

* AWS CLI configured (`aws configure`)
* Python 3.8+
* IAM role with Lambda execution + (optional) S3 read access
* Trained model saved as `model.pkl` (or use `joblib`, `h5`, etc.)

---

## 🚀 Deployment Steps

### 1. Install Dependencies & Package Code

```bash
pip install -r requirements.txt -t ./package
cp lambda_function.py model.pkl ./package/
cd package && zip -r ../function.zip . && cd ..
```

> This zips everything (code + dependencies) into `function.zip`.

---

### 2. Create IAM Role

Create an IAM role named `lambda-ml-role` with:

* **AWSLambdaBasicExecutionRole**
* (Optional) **AmazonS3ReadOnlyAccess**

Copy the **Role ARN** (looks like: `arn:aws:iam::123456789012:role/lambda-ml-role`)

---

### 3. Deploy Lambda Function

```bash
aws lambda create-function \
  --function-name mlPredictor \
  --runtime python3.12 \
  --role arn:aws:iam::123456789012:role/lambda-ml-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip
```

---

### 4. Create API Gateway

* Go to AWS Console → API Gateway → **Create HTTP API**
* **Integration type**: Lambda
* Select `mlPredictor`
* Deploy → Copy the public **Invoke URL**

---

### 5. Test the Endpoint

Send a test request (replace the URL with yours):

```bash
curl -X POST https://abc123.execute-api.us-east-1.amazonaws.com/predict \
  -H "Content-Type: application/json" \
  -d '{"feature1": 1.5, "feature2": 3.7}'
```

---

## 🧠 Example `lambda_function.py`

```python
import json
import joblib

model = joblib.load('model.pkl')  # Load model on cold start

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        features = [[body['feature1'], body['feature2']]]
        prediction = model.predict(features).tolist()

        return {
            'statusCode': 200,
            'body': json.dumps({'prediction': prediction})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

---

## 📁 Optional: Load Model from S3 (Instead of bundling)

```python
import boto3
import joblib

def load_model_from_s3():
    s3 = boto3.client('s3')
    s3.download_file('your-bucket-name', 'model.pkl', '/tmp/model.pkl')
    return joblib.load('/tmp/model.pkl')
```

---

## 🔒 Notes

* Lambda has a **250MB deployment limit** including dependencies.
* `/tmp` directory inside Lambda can be used for temporary file storage (up to 512MB).
* Use **Amazon SageMaker** for large models or more control.

---

