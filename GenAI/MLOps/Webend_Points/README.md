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

## 📫 Contact

