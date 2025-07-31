# Serverless Machine Learning with Google Cloud Functions

## Overview

This guide covers deploying machine learning models as serverless HTTP endpoints using Google Cloud Functions. Learn how to build scalable data pipelines without infrastructure management overhead, from basic echo services to production ML APIs.

## When to Use Serverless

### Ideal Use Cases
- **Startup MVP Development** - Low traffic, quick iterations
- **Model Serving Demos** - Proof of concept deployments
- **Batch Processing Jobs** - Periodic data transformations
- **Event-Driven Workflows** - Trigger-based data processing
- **Prototype Model APIs** - Testing model endpoints

### Consider Alternatives When
- **High-Volume Streaming** - Large continuous data flows
- **Ultra-Low Latency** - Sub-second response requirements
- **Cost-Sensitive at Scale** - High traffic with budget constraints
- **Complex Dependencies** - Heavy computational requirements

### Decision Factors
- **Iteration Speed** - Rapid prototyping vs production stability
- **Latency Requirements** - Multi-second delays vs real-time needs
- **Scale Demands** - Peak workload handling capabilities
- **Cost Structure** - Serverless pricing vs dedicated infrastructure

## Google Cloud Functions Features

### Benefits
- Rapid deployment and iteration
- Automatic scaling capabilities
- Flask-compatible development patterns
- Pay-per-use cost model
- No server management required

### Trade-offs
- Higher per-request costs at scale
- Cold start latency issues
- Limited control over infrastructure
- Vendor lock-in considerations

### Important Limitations
- **Read-Only Environment** - Function filesystem is immutable
- **Temporary Storage** - Only `/tmp` directory is writable
- **No Persistent Storage** - Use Cloud Storage for file persistence
- **Package Dependencies** - Careful distinction between `sklearn` vs `scikit-learn`

## Setup Instructions

### Console Configuration
1. Search "Cloud Function" in GCP Console
2. Click "Create Function"
3. Select "HTTP" trigger
4. Enable "Allow unauthenticated invocations"
5. Choose "Inline Editor" for source code
6. Select Python 3.7+ runtime
7. Name your function

### Project Structure
- **main.py** - Function implementation with Flask-like syntax
- **requirements.txt** - Dependencies specification

### Testing Options
- **Built-in Testing** - Use "Testing" tab in GCP Console with JSON payload
- **External Testing** - Get function URL from "Trigger" tab, use `requests` library

## Implementation Examples

### 1. Basic Echo Service

Test your serverless setup with a simple echo function.

**requirements.txt**
```
flask>=1.1.1
```

**main.py**
```python
from flask import jsonify

def echo_service(request):
    """Simple echo service that returns the msg parameter"""
    request_json = request.get_json()
    
    if request_json and 'msg' in request_json:
        message = request_json['msg']
        return jsonify({'echo': message})
    else:
        return jsonify({'error': 'No msg parameter provided'})
```

**Testing**
```python
import requests

url = "https://YOUR-REGION-YOUR-PROJECT.cloudfunctions.net/echo_service"
payload = {"msg": "Hello Cloud Functions!"}
response = requests.post(url, json=payload)
print(response.json())
# Output: {'echo': 'Hello Cloud Functions!'}
```

### 2. ML Model Serving with Cloud Storage

Deploy trained models with GCS integration for production use.

**requirements.txt**
```
google-cloud-storage
scikit-learn
pandas
flask
```

**Basic Model Serving**
```python
def pred(request):
    from google.cloud import storage
    import pickle as pk
    import pandas as pd 
    from flask import jsonify
    
    data = {"success": False}
    params = request.get_json()
    
    if "G1" in params:
        # Create dataframe from request parameters
        new_row = {
            "G1": params.get("G1"), 
            "G2": params.get("G2"), 
            "G3": params.get("G3"), 
            "G4": params.get("G4")
        }
        new_x = pd.DataFrame.from_dict(new_row, orient="index").transpose()
        
        # Download model from GCS
        bucket_name = "your-bucket-name"
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob("models/logit.pkl")
        blob.download_to_filename("/tmp/local_logit.pkl")
        
        # Load and apply model
        model = pk.load(open("/tmp/local_logit.pkl", 'rb'))
        data["response"] = str(model.predict_proba(new_x)[0][1])
        data["success"] = True
    
    return jsonify(data)
```

### 3. Optimized Model Serving with Caching

Improve performance by caching models between function invocations.

```python
# Global variable for model caching
model = None

def pred_cached(request):
    from google.cloud import storage
    import pickle as pk
    import pandas as pd 
    from flask import jsonify
    
    global model
    
    # Load model only once (lazy loading)
    if not model:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket("your-bucket-name")
        blob = bucket.blob("models/logit.pkl")
        blob.download_to_filename("/tmp/local_logit.pkl")
        model = pk.load(open("/tmp/local_logit.pkl", 'rb'))
    
    data = {"success": False}
    params = request.get_json()
    
    if "G1" in params:
        new_row = {
            "G1": params.get("G1"),
            "G2": params.get("G2"),
            "G3": params.get("G3"),
            "G4": params.get("G4")
        }
        new_x = pd.DataFrame.from_dict(new_row, orient="index").transpose()
        
        # Use cached model for prediction
        data["response"] = str(model.predict_proba(new_x)[0][1])
        data["success"] = True
    
    return jsonify(data)
```

**Client Usage**
```python
import requests

url = "https://YOUR-REGION-PROJECT.cloudfunctions.net/pred"
payload = {'G1':'1', 'G2':'0', 'G3':'0', 'G4':'0'}

response = requests.post(url, json=payload)
print(response.json())
# Output: {'response': '0.067451', 'success': True}
```

## Performance Optimization

### Model Caching Benefits
- **First Call**: ~2-3 seconds (model download + prediction)
- **Subsequent Calls**: ~100-200ms (cached model + prediction)
- **Global Caching**: Maintains model in memory between function invocations

### Best Practices
- Use local development environment instead of web editor
- Test functions locally before deployment
- Keep dependencies minimal for faster cold starts
- Use Cloud Storage for model artifacts and large files
- Implement proper error handling and logging
- Cache models using global variables for better performance

## Supported Models
- **scikit-learn Models** - Classification, regression, clustering
- **Keras/TensorFlow Models** - Deep learning model serving  
- **Custom Python Models** - Any pickle-serializable model

## Key Features
- **GCS Integration** - Models stored in Cloud Storage, downloaded at runtime
- **Performance Caching** - Global variables for model persistence across invocations
- **Lazy Loading** - Models loaded only when first needed
- **JSON API** - RESTful interface for model predictions
- **Automatic Scaling** - Handles varying request loads

## Next Steps
- Add authentication for production use
- Implement model versioning and A/B testing
- Set up monitoring and logging
- Integrate with CI/CD pipelines
- Explore advanced deployment patterns
