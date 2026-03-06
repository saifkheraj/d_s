# Complete Guide: Saving and Serving ML Models with Flask and MLflow

This guide explains how to **train**, **save**, and **serve** machine learning models using:

* 📦 **Scikit-learn** and **Keras**
* 🌐 **Flask** for web APIs
* 🔁 **MLflow** for saving/loading

---

## 🔹 PART 1: Training and Saving Models

### 🧠 Scikit-learn: Logistic Regression Example

```python
import pandas as pd
from sklearn.linear_model import LogisticRegression
import mlflow.sklearn

# Dummy data (10 features)
X = pd.DataFrame({f"G{i}": [0, 1, 0, 1] for i in range(1, 11)})
y = [0, 1, 0, 1]

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save using MLflow
mlflow.sklearn.save_model(model, "models/logit_games_v1")
```

### 🤖 Keras: Simple Neural Network Example

```python
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
import mlflow.keras

# Dummy data
X = np.random.rand(100, 10)
y = np.random.randint(0, 2, size=(100,))

# Define model
model = Sequential([
    Dense(16, activation='relu', input_shape=(10,)),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X, y, epochs=3, verbose=1)

# Save using MLflow
mlflow.keras.save_model(model, "models/keras_games_v1")
```

---

## 🔹 PART 2: Serving Models as Endpoints

### ✅ Scikit-learn Endpoint (`predict.py`)

```python
import pandas as pd
import mlflow.sklearn
import flask

model = mlflow.sklearn.load_model("models/logit_games_v1")
app = flask.Flask(__name__)

@app.route("/", methods=["GET"])
def predict():
    params = flask.request.args
    new_row = {f"G{i}": float(params.get(f"G{i}")) for i in range(1, 11)}
    X = pd.DataFrame([new_row])
    prob = model.predict_proba(X)[0][1]
    return flask.jsonify({"success": True, "response": str(prob)})

if __name__ == '__main__':
    app.run(port=5000)
```

### ✅ Keras Endpoint (`keras_predict.py`)

```python
import pandas as pd
import mlflow.keras
import flask
import tensorflow as tf
from keras import backend as K

# Optional: Custom metric
def auc(y_true, y_pred):
    auc_metric = tf.metrics.auc(y_true, y_pred)[1]
    K.get_session().run(tf.local_variables_initializer())
    return auc_metric

graph = tf.compat.v1.get_default_graph()
model_path = "models/keras_games_v1"
app = flask.Flask(__name__)

@app.route("/", methods=["GET"])
def predict():
    params = flask.request.args
    new_row = {f"G{i}": float(params.get(f"G{i}")) for i in range(1, 11)}
    X = pd.DataFrame([new_row])

    with graph.as_default():
        model = mlflow.keras.load_model(model_path, custom_objects={"auc": auc})
        pred = model.predict(X)[0][0]
        return flask.jsonify({"success": True, "response": str(pred)})

if __name__ == '__main__':
    app.run(port=5000)
```

---

## 🧪 PART 3: Testing the Endpoints

```python
import requests
params = {
    "G1": 0, "G2": 0, "G3": 0, "G4": 0, "G5": 1,
    "G6": 0, "G7": 1, "G8": 0, "G9": 0, "G10": 1
}
res = requests.get("http://localhost:5000/", params=params)
print(res.json())
```

---

## 📦 Folder Structure

```
project/
├── models/
│   ├── logit_games_v1/         # sklearn model saved with MLflow
│   └── keras_games_v1/         # keras model saved with MLflow
├── predict.py                  # scikit-learn API
├── keras_predict.py            # keras API
├── save_sklearn_model.py       # script to train + save sklearn model
├── save_keras_model.py         # script to train + save keras model
├── README.md
```

---

## 🔁 Why MLflow?

* ✅ Portable across environments
* ✅ Format-independent (no `.pkl` or `.h5` issues)
* ✅ Compatible with versioning and model registry
* ✅ Unified interface for saving/loading different model types

---

# Gunicorn and Web Deployment Guide

## What is Gunicorn?

**Gunicorn** (Green Unicorn) is a Python WSGI HTTP Server for UNIX systems. Think of it as a **middleman** that helps your Flask application handle multiple users at the same time, making it production-ready.

### Simple Analogy
Imagine you have a small coffee shop (Flask app):
- **Flask alone**: You have one barista who can only serve one customer at a time
- **Flask + Gunicorn**: You now have multiple baristas who can serve many customers simultaneously

## Why Do We Need Gunicorn?

### Problems with Flask Alone
```python
# This is fine for development
if __name__ == '__main__':
    app.run(debug=True)  # Only handles one request at a time
```

**Issues:**
- ❌ Can only handle one user request at a time
- ❌ Not secure for production
- ❌ Poor performance under load
- ❌ No automatic restart if it crashes

### Benefits of Gunicorn
- ✅ **Multiple Workers**: Handles many requests simultaneously
- ✅ **Load Balancing**: Distributes requests across workers
- ✅ **Process Management**: Automatically restarts crashed workers
- ✅ **Production Ready**: Built for real-world applications
- ✅ **Easy Configuration**: Simple setup and deployment

## How Does It Work?

### The Flow
```
User Request → Gunicorn → Flask App → Response → User
```

1. **User** sends a request to your web service
2. **Gunicorn** receives the request
3. **Gunicorn** forwards it to an available Flask worker
4. **Flask** processes the request and generates a response
5. **Gunicorn** sends the response back to the user

### Architecture Diagram
```
┌─────────────────┐
│     Internet    │
└─────────┬───────┘
          │
┌─────────▼───────┐
│    Gunicorn     │  ← WSGI Server
│   (Port 8000)   │
└─────┬─┬─┬───────┘
      │ │ │
   ┌──▼─▼─▼──┐
   │  Flask  │  ← Your Application
   │ Workers │
   └─────────┘
```

## Setting Up Gunicorn

### Installation
```bash
pip install gunicorn
```

### Basic Usage

#### Before (Flask Development Server)
```bash
python app.py
# Runs on http://localhost:5000
```

#### After (Gunicorn Production Server)
```bash
gunicorn --bind 0.0.0.0:8000 app:app
# Runs on http://localhost:8000
```

### Command Breakdown
```bash
gunicorn --bind 0.0.0.0:8000 app:app
│        │                   │   │
│        │                   │   └── Flask app variable name
│        │                   └────── Python file name (app.py)
│        └────────────────────────── Listen on all interfaces, port 8000
└─────────────────────────────────── Gunicorn command
```

## Configuration Options

### Common Gunicorn Settings
```bash
# Basic configuration
gunicorn --bind 0.0.0.0:8000 --workers 4 app:app

# With more options
gunicorn \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --worker-class sync \
  --timeout 120 \
  --keepalive 5 \
  app:app
```

### Configuration File (gunicorn.conf.py)
```python
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
```

Run with config file:
```bash
gunicorn -c gunicorn.conf.py app:app
```

## Example Flask Application

### app.py
```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify({
        'message': data.get('message', 'No message provided'),
        'status': 'success'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

# Remove this for production
if __name__ == '__main__':
    app.run(debug=True)  # Only for development
```

### Running with Gunicorn
```bash
# Start the server
gunicorn --bind 0.0.0.0:8000 --workers 4 app:app

# Test the endpoint
curl -X POST http://localhost:8000/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, Gunicorn!"}'
```

## Key Differences: Flask vs Gunicorn

| Aspect | Flask Development Server | Gunicorn Production Server |
|--------|-------------------------|---------------------------|
| **Purpose** | Development & Testing | Production Deployment |
| **Performance** | Single-threaded | Multi-worker |
| **Port** | Usually 5000 | Usually 8000+ |
| **Concurrency** | 1 request at a time | Multiple simultaneous requests |
| **Security** | Basic | Production-grade |
| **Monitoring** | Limited | Process management |

## Production Deployment Options

### 1. Gunicorn (Self-Managed)
- **Pros**: Full control, customizable
- **Cons**: Need to manage infrastructure, scaling, monitoring

### 2. Heroku (Platform-as-a-Service)
- **Pros**: Easy deployment, managed infrastructure
- **Cons**: Limited customization, can be expensive

### 3. AWS Lambda (Serverless)
- **Pros**: Auto-scaling, pay-per-use
- **Cons**: Cold starts, execution time limits

### 4. Docker + Kubernetes
- **Pros**: Containerized, highly scalable
- **Cons**: Complex setup, requires DevOps knowledge

## Best Practices

### 1. Worker Configuration
```python
# Calculate workers: (2 x CPU cores) + 1
import multiprocessing
workers = (2 * multiprocessing.cpu_count()) + 1
```

### 2. Environment Variables
```bash
# Use environment variables for configuration
export GUNICORN_WORKERS=4
export GUNICORN_PORT=8000
```

### 3. Logging
```python
# gunicorn.conf.py
import logging

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
```

### 4. Health Checks
```python
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })
```

## Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
```

#### 2. Workers Dying
- Check error logs
- Increase timeout settings
- Monitor memory usage

#### 3. Slow Response Times
- Increase worker count
- Check for blocking operations
- Consider async workers

### Monitoring Commands
```bash
# Check running processes
ps aux | grep gunicorn

# Monitor real-time logs
tail -f /var/log/gunicorn/error.log

# Test endpoint performance
curl -w "@curl-format.txt" -s -o /dev/null http://localhost:8000/health
```

## Summary

**Gunicorn transforms your Flask app from a development toy into a production-ready service.** It's the bridge between your code and the real world, handling multiple users, managing processes, and ensuring your application stays running smoothly.

### Key Takeaways
1. **Flask alone** = Development only (single user)
2. **Flask + Gunicorn** = Production ready (multiple users)
3. **Easy transition** = Just change how you start the server
4. **Better performance** = Multiple workers handle concurrent requests
5. **Production features** = Process management, load balancing, monitoring

Start with Gunicorn for production deployments, then consider more advanced solutions like Docker, Kubernetes, or serverless functions as your needs grow.