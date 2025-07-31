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

### 4. Keras/TensorFlow Model Serving

Deploy deep learning models with custom metrics handling for modern TensorFlow.

**requirements.txt**
```
google-cloud-storage
pandas
flask
tensorflow>=2.0
```

#### Understanding Keras Serverless Challenges

**The Custom Metrics Problem (AUC)**
When you train a Keras model with custom metrics like AUC, the model file stores a reference to that function. When loading the model in Cloud Functions, Python doesn't know what `auc` means anymore - you need to "teach" the new environment by redefining the function.

#### TensorFlow Version Considerations

**TensorFlow 1.x (Legacy - Graph Mode)**
Required explicit graph management with `tf.get_default_graph()` and `with graph.as_default():` because TensorFlow used static computation graphs.

**TensorFlow 2.x (Modern - Eager Execution)**
Uses eager execution by default, eliminating the need for explicit graph management in most cases. The graph handling is automatic.

**Modern Keras Model Implementation (TF 2.x)**
```python
model = None

def predict(request):
    global model
            
    from google.cloud import storage
    import pandas as pd
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    from flask import jsonify
    
    # Redefine custom function that was used during training
    def auc(y_true, y_pred):
        return tf.keras.metrics.AUC()(y_true, y_pred)
    
    data = {"success": False}
    params = request.get_json()
    
    # Download model if not cached (lazy loading)
    if not model:
        bucket_name = "dsp_model_store"
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob("serverless/keras/v1")
        blob.download_to_filename("/tmp/games.h5")
        
        # Load model with custom function definition
        model = load_model('/tmp/games.h5', 
                          custom_objects={'auc': auc})
    
    # Apply the model (no graph context needed in TF 2.x)
    if "G1" in params: 
        new_row = { 
            "G1": params.get("G1"), "G2": params.get("G2"), 
            "G3": params.get("G3"), "G4": params.get("G4"), 
            "G5": params.get("G5"), "G6": params.get("G6"), 
            "G7": params.get("G7"), "G8": params.get("G8"), 
            "G9": params.get("G9"), "G10": params.get("G10")
        }
        new_x = pd.DataFrame.from_dict(new_row, 
                                      orient="index").transpose()               
     
        # Direct prediction - eager execution handles everything
        prediction = model.predict(new_x)
        data["response"] = str(prediction[0][0])
        data["success"] = True
    
    return jsonify(data)
```

**Legacy Implementation (TF 1.x) - For Reference Only**
```python
# Only needed for TensorFlow 1.x - DO NOT USE with TF 2.x
model = None    
graph = None

def predict_legacy(request):
    global model, graph
    
    if not model:
        graph = tf.get_default_graph()  # TF 1.x only
        model = load_model('/tmp/games.h5', custom_objects={'auc': auc})
    
    with graph.as_default():  # TF 1.x only
        prediction = model.predict(new_x)
```

#### Key Differences Between Versions

**TensorFlow 1.x Requirements:**
- ❌ Manual graph management with `tf.get_default_graph()`
- ❌ Graph context with `with graph.as_default():`
- ❌ Session management
- ❌ Complex setup for serverless environments

**TensorFlow 2.x Benefits:**
- ✅ Eager execution by default
- ✅ No manual graph management needed
- ✅ Simpler, cleaner code
- ✅ Better serverless compatibility
- ✅ Modern Keras API (`tf.keras` instead of separate `keras`)

#### What You Still Need

**Custom Metrics (Still Required):**
- Must redefine custom functions like AUC
- Use `custom_objects` parameter in `load_model()`
- Modern syntax: `tf.keras.metrics.AUC()` instead of legacy approaches

**Model Caching (Still Beneficial):**
- Cache model in global variable for performance
- Lazy loading from Cloud Storage
- Reduces cold start impact

**Testing Modern Keras Model**
```python
import requests

result = requests.post(
    "https://your-region-project.cloudfunctions.net/predict",
    json={
        'G1':'1', 'G2':'0', 'G3':'0', 'G4':'0', 'G5':'0',
        'G6':'0', 'G7':'0', 'G8':'0', 'G9':'0', 'G10':'0'
    }
)
print(result.json())
# Output: {'response': '0.8234567', 'success': True}
```

**Migration Summary:**
- **Remove**: Graph management code (`tf.get_default_graph()`, `with graph.as_default():`)
- **Update**: Use `tf.keras` instead of separate `keras` imports
- **Modernize**: Custom metrics with current TensorFlow 2.x syntax
- **Keep**: Model caching and custom objects handling

## Supported Models
- **scikit-learn Models** - Classification, regression, clustering
- **Keras/TensorFlow Models** - Deep learning model serving with graph management
- **Custom Python Models** - Any pickle-serializable model

## Key Features
- **GCS Integration** - Models stored in Cloud Storage, downloaded at runtime
- **Performance Caching** - Global variables for model persistence across invocations
- **Lazy Loading** - Models loaded only when first needed
- **JSON API** - RESTful interface for model predictions
- **Automatic Scaling** - Handles varying request loads

## Security Considerations

### Production Security Warning

⚠️ **Important**: The Cloud Functions examples in this guide use "Allow unauthenticated invocations" for demonstration purposes. This makes your endpoints open to the web, meaning anyone can access them and potentially abuse your model serving endpoints.

### Security Risks of Open Endpoints
- **Unauthorized Usage** - Anyone can make requests to your model
- **Cost Abuse** - Malicious users can generate expensive compute costs
- **Rate Limiting Issues** - Uncontrolled traffic can overwhelm your function
- **Data Privacy** - Sensitive model predictions exposed to public access

### Recommended Security Practices

#### 1. Disable Unauthenticated Access
The most important step is to disable "Allow unauthenticated invocations" during function setup:

**During Function Creation:**
1. In GCP Console, when creating your Cloud Function
2. **Uncheck** "Allow unauthenticated invocations"
3. This prevents hosting the function on the open web

#### 2. Authentication Methods
Once unauthenticated access is disabled, you'll need to set up proper authentication:

**Options Include:**
- **IAM Roles** - Control access through Google Cloud IAM
- **Service Accounts** - For service-to-service authentication
- **API Keys** - For controlled client access
- **OAuth 2.0** - For user-based authentication

#### 3. Implementation Steps
Setting up authentication involves several steps that may change as GCP evolves:

1. **Create IAM Roles** - Define who can access your function
2. **Set up Service Accounts** - For automated access
3. **Configure Credentials** - Proper authentication tokens
4. **Update Client Code** - Include authentication in requests

**Reference Documentation:**
For current, step-by-step authentication setup instructions, refer to the official [GCP Cloud Functions Authentication Documentation](https://cloud.google.com/functions/docs/securing/authenticating) as the process may change over time.

#### 4. Additional Security Measures

**Network Security:**
- Use **VPC** (Virtual Private Cloud) for internal-only access
- Implement **private IP** restrictions similar to AWS private IPs
- Set up **firewall rules** for additional network-level protection

**Function-Level Security:**
- **Input Validation** - Validate all incoming request parameters
- **Rate Limiting** - Implement request throttling
- **Logging & Monitoring** - Track usage and detect abuse
- **Error Handling** - Don't expose sensitive information in error messages

### Example Authenticated Request

Once authentication is set up, your client requests will need to include credentials:

```python
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Load service account credentials
credentials = service_account.Credentials.from_service_account_file(
    'path/to/service-account-key.json',
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# Get access token
credentials.refresh(Request())
access_token = credentials.token

# Make authenticated request
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.post(
    'https://your-region-project.cloudfunctions.net/predict',
    json={'G1': '1', 'G2': '0', 'G3': '0', 'G4': '0', 'G5': '0'},
    headers=headers
)
```

### Security Checklist for Production

Before deploying to production, ensure:

- [ ] **Disabled** unauthenticated invocations
- [ ] **Configured** appropriate IAM roles
- [ ] **Set up** service account authentication
- [ ] **Implemented** input validation
- [ ] **Added** rate limiting
- [ ] **Enabled** logging and monitoring
- [ ] **Tested** authentication flow
- [ ] **Documented** access procedures for your team

### Development vs Production

**Development/Testing:**
- ✅ Unauthenticated access acceptable for rapid prototyping
- ✅ Public endpoints OK for demos and testing
- ⚠️ Always use test data, never production data

**Production:**
- ❌ Never use unauthenticated access
- ✅ Always implement proper authentication
- ✅ Use private networks when possible
- ✅ Monitor and log all access

Remember: Security should be planned from the beginning, not added as an afterthought. The convenience of open endpoints during development can become a serious vulnerability in production.
