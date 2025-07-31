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

Deploy deep learning models with proper TensorFlow graph management and custom metrics handling.

**requirements.txt**
```
google-cloud-storage
pandas
flask
tensorflow
keras
```

#### Understanding Keras Serverless Challenges

**The Custom Metrics Problem (AUC)**
When you train a Keras model with custom metrics like AUC, the model file stores a reference to that function. When loading the model in Cloud Functions, Python doesn't know what `auc` means anymore - you need to "teach" the new environment by redefining the function.

**The TensorFlow Graph Problem**
TensorFlow uses "graphs" (blueprints) to organize computations. In serverless environments, each request might create a new blueprint, but your model was built with the original blueprint. You need to ensure you always use the same blueprint for consistent predictions.

**Keras Model Implementation**
```python
model = None    
graph = None  # Cache both model and TensorFlow graph

def predict(request):
    global model
    global graph
            
    from google.cloud import storage
    import pandas as pd
    import flask
    import tensorflow as tf
    import keras as k
    from keras.models import load_model
    from flask import jsonify
    
    # Redefine custom function that was used during training
    def auc(y_true, y_pred):
        auc = tf.metrics.auc(y_true, y_pred)[1]
        k.backend.get_session().run(
                      tf.local_variables_initializer())
        return auc
    
    data = {"success": False}
    params = request.get_json()
    
    # Download model if not cached (lazy loading)
    if not model:
        # Capture the graph when we first load the model
        graph = tf.get_default_graph()  # Save this blueprint!
        
        bucket_name = "dsp_model_store"
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob("serverless/keras/v1")
        blob.download_to_filename("/tmp/games.h5")
        
        # Load model with custom function definition
        model = load_model('/tmp/games.h5', 
                          custom_objects={'auc': auc})  # Tell Keras about AUC
    
    # Apply the model with proper graph context
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
     
        # Always use the original graph for predictions
        with graph.as_default():  # Switch to the correct blueprint        
            data["response"] = str(model.predict_proba(new_x)[0][0])
            data["success"] = True
    
    return jsonify(data)
```

#### Why This Pattern is Essential

**Without Proper Handling:**
- ❌ "ValueError: Unknown metric function: auc"
- ❌ "Cannot use the default session to evaluate tensor"  
- ❌ Inconsistent predictions across requests
- ❌ Model fails on second+ requests

**With Proper Handling:**
- ✅ Custom functions work in new environment
- ✅ Consistent predictions across all requests
- ✅ No graph context errors
- ✅ Reliable serverless deployment

**Key Components Explained:**
- **AUC Redefinition** - "Teach the new environment what AUC means"
- **Graph Caching** - "Remember which blueprint we used to build the model"  
- **Graph Context** - "Always use the same blueprint for predictions"
- **Custom Objects** - Tell `load_model()` about your custom functions

**Testing Keras Model**
```python
import requests

result = requests.post(
    "https://us-central1-gameanalytics.cloudfunctions.net/predict",
    json={
        'G1':'1', 'G2':'0', 'G3':'0', 'G4':'0', 'G5':'0',
        'G6':'0', 'G7':'0', 'G8':'0', 'G9':'0', 'G10':'0'
    }
)
print(result.json())
# Output: {'response': '0.8234567', 'success': True}
```

**Mental Model:**
Think of custom metrics like a recipe calling for "Mom's special sauce" - when someone else tries to make it, they need the recipe for the special sauce too! The graph is like ensuring you always drive on the correct side of the road for your car.

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

## Next Steps
- Add authentication for production use
- Implement model versioning and A/B testing
- Set up monitoring and logging
- Integrate with CI/CD pipelines
- Explore advanced deployment patterns
