from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# Sample data for demonstration
sample_data = {
    "model_version": "1.0.0",
    "last_updated": "2024-08-02",
    "status": "active"
}

@app.route('/')
def home():
    """Root endpoint - basic welcome message"""
    return jsonify({
        "message": "Welcome to Reproducible ML Model API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "model_info": "/model/info"
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "running",
        "model_loaded": True
    })

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    """Prediction endpoint - echo service for testing"""
    if request.method == 'GET':
        # Handle GET request with query parameter
        message = request.args.get('msg', 'No message provided')
        return jsonify({
            "input": message,
            "prediction": f"Processed: {message}",
            "method": "GET",
            "timestamp": datetime.now().isoformat()
        })
    
    elif request.method == 'POST':
        # Handle POST request with JSON data
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No JSON data provided"}), 400
            
            # Simple echo prediction for demonstration
            prediction = {
                "input_data": data,
                "prediction": f"Processed input with {len(str(data))} characters",
                "model_version": sample_data["model_version"],
                "timestamp": datetime.now().isoformat()
            }
            
            return jsonify(prediction)
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/model/info')
def model_info():
    """Model information endpoint"""
    return jsonify({
        "model_name": "Reproducible Demo Model",
        "model_version": sample_data["model_version"],
        "framework": "Flask",
        "python_version": "3.9+",
        "last_updated": sample_data["last_updated"],
        "status": sample_data["status"],
        "description": "Demo model for containerized ML deployment"
    })

@app.route('/test')
def test_endpoint():
    """Test endpoint for CI/CD validation"""
    return jsonify({
        "test": "success",
        "message": "Container is working correctly",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Get port from environment variable, default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run on all interfaces for container accessibility
    app.run(host='0.0.0.0', port=port, debug=False)