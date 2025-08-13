# Complete MLOps Deployment Guide

**Deploy Your ML Models to Production on AWS - Step by Step**

## Overview

This guide takes you from a Python ML model on your laptop to a production web service handling thousands of users on AWS. No Docker or AWS experience required!

### What You'll Build

```
Local ML Model → Web API → Docker Container → AWS Cloud → Production Service
```

### Prerequisites

**Required:**
- Computer with internet connection
- Basic Python knowledge
- A trained ML model (any simple model works)
- AWS account (free tier is sufficient)

### Journey Overview

We'll build this in 6 clear stages:

1. **Create Web API** - Turn your ML model into a web service
2. **Test Locally** - Verify everything works on your computer
3. **Containerize** - Package everything with Docker
4. **Upload to Cloud** - Store your container in AWS
5. **Deploy to Production** - Run your service on AWS
6. **Add Production Features** - Load balancing, monitoring, auto-scaling

---

## Stage 1: Create Your Web API

### Step 1.1: Create the Main Application File

Create a file named `app.py`:

```python
from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# TODO: Replace this with your actual model loading
# model = pickle.load(open('your_model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def home():
    """Homepage - shows API info"""
    return jsonify({
        'service': 'ML Prediction API',
        'status': 'running',
        'version': '1.0',
        'endpoints': {
            'predict': 'POST /predict',
            'health': 'GET /health'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check - AWS uses this to know if service is working"""
    return jsonify({
        'status': 'healthy',
        'service': 'running'
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    try:
        # Get input data
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({
                'error': 'Missing features in request',
                'example': {'features': [1, 2, 3, 4]}
            }), 400
        
        features = data['features']
        
        # TODO: Replace with your actual model prediction
        # prediction = model.predict([features])
        
        # Demo prediction (replace this)
        mock_prediction = sum(features) * 100
        
        return jsonify({
            'prediction': mock_prediction,
            'input_features': features,
            'model_version': '1.0',
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'failed'
        }), 500

if __name__ == '__main__':
    # Only for local testing
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Step 1.2: Create Requirements File

Create a file named `requirements.txt`:

```txt
flask==2.3.3
gunicorn==21.2.0
numpy==1.24.3
scikit-learn==1.3.0
requests==2.31.0
```

### Step 1.3: Add Your Model (Optional)

If you have a trained model:

1. Save it as `model.pkl` in the same folder
2. Uncomment the model loading lines in `app.py`
3. Replace the mock prediction with real prediction

---

## Stage 2: Test Locally

### Step 2.1: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 2.2: Run Your Service

```bash
python app.py
```

**Expected output:**
```
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://[your-ip]:5000
```

### Step 2.3: Test Your API

Open a new terminal and run these tests:

**Test 1: Health Check**
```bash
curl http://localhost:5000/health
```

**Expected response:**
```json
{"status": "healthy", "service": "running"}
```

**Test 2: Homepage**
```bash
curl http://localhost:5000/
```

**Test 3: Prediction**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1, 2, 3, 4]}'
```

**Expected response:**
```json
{
  "prediction": 1000,
  "input_features": [1, 2, 3, 4],
  "model_version": "1.0",
  "status": "success"
}
```

**✅ Success Check:** All three tests should work before proceeding.

---

## Stage 3: Containerize with Docker

### What is Docker?

Docker packages your entire application (code + dependencies + environment) into a single "container" that runs the same way everywhere.

### Step 3.1: Install Docker

**Windows/Mac:**
1. Download Docker Desktop from [docker.com](https://docker.com)
2. Install and start it
3. Verify installation: `docker --version`

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and back in
```

### Step 3.2: Create Dockerfile

Create a file named `Dockerfile` (no extension):

```dockerfile
# Use Python 3.9 as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# If you have a model file, uncomment this:
# COPY model.pkl .

# Expose port 80 (standard web port)
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/health || exit 1

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "2", "--timeout", "60", "app:app"]
```

### Step 3.3: Build Your Container

```bash
# Build the Docker image
docker build -t my-ml-service .
```

**Understanding the naming:**
- `my-ml-service` is just the name you're giving to your container
- You could call it anything: `pizza-app`, `house-predictor`, etc.
- Docker automatically adds `:latest` (meaning "newest version")

### Step 3.4: Test Your Container

```bash
# Run container locally
docker run -p 8080:80 my-ml-service
```

**In another terminal, test it:**
```bash
# Health check
curl http://localhost:8080/health

# Prediction test
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1, 2, 3, 4]}'
```

**✅ Success Check:** Your containerized service should respond the same as before.

---

## Stage 4: Upload to AWS

### Step 4.1: Set Up AWS CLI

**Install AWS CLI:**

**Mac:**
```bash
brew install awscli
```

**Windows:**
Download installer from [aws.amazon.com/cli/](https://aws.amazon.com/cli/)

**Linux:**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**Configure AWS:**
```bash
aws configure
```

**Enter these details:**
- **Access Key ID**: Get from AWS Console → IAM → Users → Your User → Security Credentials
- **Secret Access Key**: From same place
- **Default region**: `us-east-1` (or your preferred region)
- **Output format**: `json`

### Step 4.2: Create Container Registry

Choose either command line (faster) or web console (visual):

#### Option A: Command Line

```bash
# Create ECR repository
aws ecr create-repository --repository-name my-ml-service

# Save the output! You'll need the "repositoryUri"
# Example: 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-ml-service
```

#### Option B: AWS Web Console

1. **Access AWS Console**
   - Go to [aws.amazon.com](https://aws.amazon.com)
   - Click "Sign In to Console"
   - Log in with your AWS account

2. **Find ECR Service**
   - In the search bar, type "ECR"
   - Click "Elastic Container Registry"

3. **Create Repository**
   - Click "Create repository"
   - Repository name: `my-ml-service`
   - Keep defaults
   - Click "Create repository"

4. **Save Repository URI**
   - Copy the URI (looks like: `123456789.dkr.ecr.us-east-1.amazonaws.com/my-ml-service`)
   - **Save this URI!** You'll need it next

### Step 4.3: Login to AWS Container Registry

```bash
# Get your account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=us-east-1  # Change if using different region

# Login to ECR
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
```

### Step 4.4: Tag and Push Your Container

**Understanding container naming:**

Your container is currently named `my-ml-service:latest` on your computer. AWS needs a specific naming format to store it.

```bash
# Step 1: Rename your container for AWS
docker tag my-ml-service:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/my-ml-service:latest

# Step 2: Upload to AWS
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/my-ml-service:latest
```

**Why the long AWS name?**

Think of it like file storage:
- **Local:** `my-ml-service:latest` (just the name)
- **AWS:** `123456789.dkr.ecr.us-east-1.amazonaws.com/my-ml-service:latest` (AWS storage location + same name)

The parts of the AWS name:
```
123456789.dkr.ecr.us-east-1.amazonaws.com / my-ml-service : latest
↑                                         ↑              ↑
AWS storage address                    your app name    version
```

**✅ Success Check:** You should see "latest: digest: sha256:..." when push completes.

---

## Stage 5: Deploy to Production

### Step 5.1: Create ECS Cluster

Choose either command line or web console:

#### Option A: Command Line

```bash
# Create cluster
aws ecs create-cluster --cluster-name ml-production

# Create task execution role
aws iam create-role --role-name ecsTaskExecutionRole --assume-role-policy-document file://trust-policy.json
```

**Create `trust-policy.json`:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

```bash
# Attach required policies
aws iam attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
aws iam attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
```

#### Option B: AWS Web Console

1. **Create ECS Cluster**
   - AWS Console → Search "ECS"
   - Click "Elastic Container Service"
   - Click "Create Cluster"
   - Choose "Networking only (Powered by AWS Fargate)"
   - Cluster name: `ml-production`
   - Click "Create"

2. **Create IAM Role**
   - AWS Console → Search "IAM"
   - Click "Roles" → "Create role"
   - Choose "AWS service" → "Elastic Container Service" → "Elastic Container Service Task"
   - Click "Next"
   - Search and select these policies:
     - `AmazonECSTaskExecutionRolePolicy`
     - `AmazonEC2ContainerRegistryReadOnly`
   - Click "Next"
   - Role name: `ecsTaskExecutionRole`
   - Click "Create role"

### Step 5.2: Create Task Definition

#### Option A: Command Line

**Create `task-definition.json`:**
```json
{
  "family": "my-ml-service-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::YOUR_ACCOUNT_ID:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "ml-service",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/my-ml-service:latest",
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/my-ml-service",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**Important:** Replace `YOUR_ACCOUNT_ID` with your actual AWS account ID

```bash
# Create log group
aws logs create-log-group --log-group-name /ecs/my-ml-service

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

#### Option B: AWS Web Console

1. **Create Task Definition**
   - ECS Console → "Task Definitions"
   - Click "Create new Task Definition"
   - Select "Fargate" → "Next step"

2. **Configure Task**
   - Task Definition Name: `my-ml-service-task`
   - Task execution IAM role: `ecsTaskExecutionRole`
   - Task memory (GB): 1GB
   - Task CPU (vCPU): 0.5 vCPU

3. **Add Container**
   - Click "Add container"
   - Container name: `ml-service`
   - Image: `123456789.dkr.ecr.us-east-1.amazonaws.com/my-ml-service:latest` (use your URI)
   - Memory Limits (MiB): Soft limit: 1024
   - Port mappings: Container port: 80

4. **Configure Logging**
   - Log driver: awslogs
   - awslogs-group: `/ecs/my-ml-service`
   - awslogs-region: `us-east-1`
   - Click "Add"

5. **Create Log Group**
   - CloudWatch → Logs → Log groups
   - Click "Create log group"
   - Log group name: `/ecs/my-ml-service`
   - Click "Create"

### Step 5.3: Create ECS Service

```bash
# Get your default VPC and subnets
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text)
SUBNET_IDS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query 'Subnets[0:2].SubnetId' --output text | tr '\t' ',')

# Create security group
SECURITY_GROUP_ID=$(aws ec2 create-security-group \
  --group-name ml-service-sg \
  --description "Security group for ML service" \
  --vpc-id $VPC_ID \
  --query 'GroupId' --output text)

# Allow HTTP traffic
aws ec2 authorize-security-group-ingress \
  --group-id $SECURITY_GROUP_ID \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

# Create service
aws ecs create-service \
  --cluster ml-production \
  --service-name my-ml-service \
  --task-definition my-ml-service-task:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_IDS],securityGroups=[$SECURITY_GROUP_ID],assignPublicIp=ENABLED}"
```

### Step 5.4: Verify Your Service

```bash
# Check service status
aws ecs describe-services --cluster ml-production --services my-ml-service

# Get task details
aws ecs list-tasks --cluster ml-production --service-name my-ml-service
```

**✅ Success Check:** Service should show "RUNNING" status with 2 tasks.

---

## Stage 6: Add Production Features

### Step 6.1: Create Load Balancer

```bash
# Create Application Load Balancer
ALB_ARN=$(aws elbv2 create-load-balancer \
  --name my-ml-service-alb \
  --subnets $SUBNET_IDS \
  --security-groups $SECURITY_GROUP_ID \
  --query 'LoadBalancers[0].LoadBalancerArn' --output text)

# Create target group
TARGET_GROUP_ARN=$(aws elbv2 create-target-group \
  --name ml-service-targets \
  --protocol HTTP \
  --port 80 \
  --vpc-id $VPC_ID \
  --target-type ip \
  --health-check-path /health \
  --query 'TargetGroups[0].TargetGroupArn' --output text)

# Create listener
aws elbv2 create-listener \
  --load-balancer-arn $ALB_ARN \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=$TARGET_GROUP_ARN
```

### Step 6.2: Update Service with Load Balancer

```bash
# Update service to use load balancer
aws ecs update-service \
  --cluster ml-production \
  --service my-ml-service \
  --load-balancers targetGroupArn=$TARGET_GROUP_ARN,containerName=ml-service,containerPort=80
```

### Step 6.3: Get Your Public URL

```bash
# Get load balancer DNS name
ALB_DNS=$(aws elbv2 describe-load-balancers \
  --load-balancer-arns $ALB_ARN \
  --query 'LoadBalancers[0].DNSName' --output text)

echo "Your ML service is available at: http://$ALB_DNS"
```

### Step 6.4: Test Your Production Service

```bash
# Test health check
curl http://$ALB_DNS/health

# Test prediction
curl -X POST http://$ALB_DNS/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1, 2, 3, 4]}'
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check service events
aws ecs describe-services --cluster ml-production --services my-ml-service

# Check logs
aws logs get-log-events --log-group-name /ecs/my-ml-service --log-stream-name LOG_STREAM_NAME
```

### Can't Connect to Service

1. **Check security group:** Ensure it allows port 80
2. **Verify health check:** Ensure `/health` endpoint works
3. **Check subnet configuration:** Ensure tasks run in public subnets

### Common Issues

- **Port conflicts:** Make sure your app listens on port 80
- **Health check fails:** Verify `/health` endpoint returns HTTP 200
- **Memory issues:** Increase memory allocation in task definition
- **Permission errors:** Check IAM roles have correct policies

---

## Success! 🎉

You now have:

- ✅ ML model running as web service
- ✅ Containerized application
- ✅ Production deployment on AWS
- ✅ Load balancer for high availability
- ✅ Auto-scaling and monitoring

**Your ML service can now handle thousands of users!**

## Next Steps

1. **Set up CI/CD** - Automate deployments
2. **Add authentication** - Secure your API
3. **Monitor performance** - Track predictions and errors
4. **Version your models** - A/B test different models
5. **Scale globally** - Deploy to multiple regions

## Cost Management

- Use AWS Free Tier for learning
- Monitor costs in AWS Billing Dashboard
- Consider Spot instances for non-critical workloads
- Set up billing alerts

**Estimated completion time:** 2-4 hours  
**Monthly cost:** $10-50 for basic setup

---

*You've just built production-grade MLOps infrastructure used by major companies! 🚀*
