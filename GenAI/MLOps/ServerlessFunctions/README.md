# Serverless Technologies & Managed Services

## Overview
Serverless technologies and managed services enable data scientists to build scalable data pipelines without infrastructure management overhead.

## Key Considerations

### Decision Factors
- **Iteration Speed** - Rapid prototyping vs production stability
- **Latency Requirements** - Multi-second delays vs real-time needs
- **Scale Demands** - Peak workload handling capabilities
- **Cost Structure** - Serverless pricing vs dedicated infrastructure

## Use Cases

### Ideal for Serverless
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

## Benefits
- Rapid deployment and iteration
- Automatic scaling capabilities
- Reduced infrastructure management
- Pay-per-use cost model
- Separation of model training and deployment concerns

## Trade-offs
- Higher per-request costs at scale
- Cold start latency issues
- Limited control over infrastructure
- Vendor lock-in considerations

# Google Cloud Functions (GCP)

## Overview
Google Cloud Functions provides a serverless environment for running Python code with Flask-like development patterns and elastic scaling capabilities.

## Key Features
- **Flask-Compatible Development** - Write code using familiar Flask patterns
- **Managed Infrastructure** - Automatic scaling and resource management
- **Standard Python Ecosystem** - Uses requirements.txt and standard project structure
- **Elastic Computing** - Scales automatically based on demand

## Use Cases
- **Model Serving Endpoints** - Deploy sklearn and Keras models as REST APIs
- **Data Processing Functions** - Event-driven data transformations
- **Microservice APIs** - Lightweight service endpoints
- **Webhook Handlers** - Process incoming HTTP requests

## Important Limitations

### Storage Constraints
- **Read-Only Environment** - Function filesystem is immutable
- **Temporary Storage** - Only `/tmp` directory is writable
- **No Persistent Storage** - Use Cloud Storage for file persistence

### Development Considerations
- **Indentation Issues** - Spaces vs tabs can cause deployment failures
- **Web Editor Limitations** - IDE tools like Sublime Text recommended for development
- **Package Dependencies** - Careful distinction between `sklearn` vs `scikit-learn` in requirements

## Best Practices
- Use local development environment instead of web editor
- Test functions locally before deployment
- Keep dependencies minimal for faster cold starts
- Use Cloud Storage for model artifacts and large files
- Implement proper error handling and logging

## Supported Models
- **scikit-learn Models** - Classification, regression, clustering
- **Keras/TensorFlow Models** - Deep learning model serving
- **Custom Python Models** - Any pickle-serializable model


# 1. Echo Service - GCP Cloud Functions

## Overview
Basic HTTP echo service built with Google Cloud Functions to demonstrate serverless deployment fundamentals.

## Setup Steps

### Console Configuration
1. Search "Cloud Function" in GCP Console
2. Click "Create Function"
3. Select "HTTP" trigger
4. Enable "Allow unauthenticated invocations"
5. Choose "Inline Editor" for source code
6. Select Python 3.7 runtime
7. Name your function

### Code Structure
- **main.py** - Function implementation with Flask-like syntax
- **requirements.txt** - Dependencies (flask >= 1.1.1)

## Functionality
- Accepts HTTP requests with `msg` parameter
- Returns JSON response echoing the input parameter
- No endpoint annotations needed (handled by Cloud Functions UI)

## Testing Options

### Built-in Testing
- Use "Testing" tab in GCP Console
- Pass JSON payload to test function
- View output in console interface

### External Testing
- Get function URL from "Trigger" tab
- Use Python `requests` library for HTTP calls
- Function accessible via public URL (unauthenticated)

## Key Benefits
- No server management required
- Automatic scaling and load handling
- Simple Flask-like development experience
- Built-in testing and monitoring tools

## Code Example

### requirements.txt
```
flask>=1.1.1
```

### main.py
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

### Testing with Python
```python
import requests
import json

# Function URL from GCP Console Trigger tab
url = "https://YOUR-REGION-YOUR-PROJECT.cloudfunctions.net/echo_service"

# Test payload
payload = {"msg": "Hello Cloud Functions!"}

# Make request
response = requests.post(url, json=payload)
print(response.json())
# Output: {'echo': 'Hello Cloud Functions!'}
```

## Next Steps
- Integrate with Cloud Storage for model persistence
- Expand to serve machine learning models
- Add authentication for production use



# GCP Cloud Functions - Model Serving

## Overview
Deploy machine learning models as serverless HTTP endpoints using Google Cloud Functions, from basic echo services to production ML APIs.

## Setup Steps

### Console Configuration
1. Search "Cloud Function" in GCP Console
2. Click "Create Function"
3. Select "HTTP" trigger
4. Enable "Allow unauthenticated invocations"
5. Choose "Inline Editor" for source code
6. Select Python 3.7 runtime
7. Name your function

### Code Structure
- **main.py** - Function implementation with Flask-like syntax
- **requirements.txt** - Dependencies (flask >= 1.1.1)

## Functionality
- Accepts HTTP requests with `msg` parameter
- Returns JSON response echoing the input parameter
- No endpoint annotations needed (handled by Cloud Functions UI)

## Testing Options

### Built-in Testing
- Use "Testing" tab in GCP Console
- Pass JSON payload to test function
- View output in console interface

### External Testing
- Get function URL from "Trigger" tab
- Use Python `requests` library for HTTP calls
- Function accessible via public URL (unauthenticated)

## Key Benefits
- No server management required
- Automatic scaling and load handling
- Simple Flask-like development experience
- Built-in testing and monitoring tools

## Code Example

### requirements.txt
```
flask>=1.1.1
```

### main.py
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

### Model Serving with GCS Integration

### Dependencies (requirements.txt)
```
google-cloud-storage
sklearn
pandas
flask
```

### Model Function Implementation
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
        new_row = {"G1": params.get("G1"), "G2": params.get("G2"), 
                   "G3": params.get("G3"), "G4": params.get("G4")}
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

### Performance Optimization - Model Caching
```python
model = None

def pred(request):
    global model
    
    # Load model only once (lazy loading)
    if not model:
        # Download and load model from GCS
        storage_client = storage.Client()
        bucket = storage_client.get_bucket("your-bucket-name")
        blob = bucket.blob("models/logit.pkl")
        blob.download_to_filename("/tmp/local_logit.pkl")
        model = pk.load(open("/tmp/local_logit.pkl", 'rb'))
    
    # Use cached model for prediction
    # ... rest of function logic
    return jsonify(data)
```

### Client Usage
```python
import requests

url = "https://YOUR-REGION-PROJECT.cloudfunctions.net/pred"
payload = {'G1':'1', 'G2':'0', 'G3':'0', 'G4':'0', 'G5':'0'}

response = requests.post(url, json=payload)
print(response.json())
# Output: {'response': '0.067451', 'success': True}
```

## Key Features
- **GCS Integration** - Models stored in Cloud Storage, downloaded at runtime
- **Performance Caching** - Global variables for model persistence across invocations  
- **Lazy Loading** - Models loaded only when first needed
- **JSON API** - RESTful interface for model predictions
- **Automatic Scaling** - Handles varying request loads

## Performance Benefits
- **First Call**: ~2-3 seconds (model download + prediction)
- **Subsequent Calls**: ~100-200ms (cached model + prediction)
- **Global Caching**: Maintains model in memory between function invocations

## Next Steps
- Integrate with Cloud Storage for model persistence
- Expand to serve machine learning models
- Add authentication for production use