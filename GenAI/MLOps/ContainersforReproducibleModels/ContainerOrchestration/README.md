# Container Orchestration for Data Science

## Overview

Container orchestration systems manage the lifecycle of containers in a cluster environment, providing essential services for scalable and reliable application deployment.

## What is Container Orchestration?

Container orchestration platforms handle:
- **Provisioning** - Deploying containers across cluster nodes
- **Scaling** - Automatically adjusting container instances based on demand
- **Failover** - Recovering from container or node failures
- **Load Balancing** - Distributing traffic across container instances
- **Service Discovery** - Enabling containers to find and communicate with each other

## Benefits for Data Scientists

Container orchestration enables robust model deployment with:

- **Scalable Infrastructure** - Automatically scale resources to match demand
- **Fault Tolerance** - System recovers from errors without manual intervention
- **Static URLs** - Load balancers provide consistent service endpoints
- **Flexible Runtime** - Use any programming language or runtime environment

## Trade-offs

**Advantages:**
- Greater flexibility compared to serverless functions
- Support for any programming language/runtime
- Robust, production-ready deployment solution

**Considerations:**
- Higher operational overhead than serverless alternatives
- Initial setup complexity
- Requires container and orchestration knowledge

## Platform Options

### Google Cloud Platform (GCP)
- **Fully managed Kubernetes** solution
- Minimal setup required
- **Recommended for learning** Kubernetes

### Amazon Web Services (AWS)
- **ECS (Elastic Container Service)** - AWS-native solution, easier setup
- **EKS (Elastic Kubernetes Service)** - Managed Kubernetes, more complex
- **Fargate** - Serverless container option within ECS

## Recommendations

- **Learning**: Start with GCP's managed Kubernetes for easiest onboarding
- **AWS Production**: Use ECS for path of least friction
- **General**: Learn Kubernetes fundamentals for long-term orchestration skills

## Conclusion

Container orchestration provides a powerful middle ground between serverless simplicity and infrastructure flexibility, making it an excellent choice for scalable data science model deployments.


# Docker to AWS ECR Deployment Guide

<img width="1912" height="640" alt="image" src="https://github.com/user-attachments/assets/5ae8b94a-62dc-464e-9780-3d6ecd59ea88" />


## Overview

This guide walks you through the process of pushing Docker images to AWS Elastic Container Registry (ECR). ECR is a managed Docker registry that integrates seamlessly with AWS services like ECS and EKS.

## Prerequisites

- AWS account with appropriate permissions
- Docker installed on your local machine or EC2 instance
- AWS CLI installed and configured
- IAM user with ECR permissions

## Table of Contents

1. [Setting up an ECR Repository](#1-setting-up-an-ecr-repository)
2. [Creating IAM Role for ECR](#2-creating-iam-role-for-ecr)
3. [Authenticating with Docker Login](#3-authenticating-with-docker-login)
4. [Building and Tagging Images](#4-building-and-tagging-images)
5. [Pushing Images to ECR](#5-pushing-images-to-ecr)
6. [Verifying the Push](#6-verifying-the-push)

---

## 1. Setting up an ECR Repository

### Steps:

1. **Navigate to ECR in AWS Console**
   - Search for "ECR" in the AWS console
   - Click on the ECR service

2. **Create a New Repository**
   - In the left panel, click "Repositories"
   - Click "Create Repository"
   - Enter repository name (e.g., `models`)
   - Select "Private" repository type
   - Click "Create Repository"

### Result:
You now have an empty ECR repository ready to store Docker images.

---

## 2. Creating IAM Role for ECR

### Generate Login Token:

```bash
sudo aws ecr get-login-password --region us-east-1
```

**Note:** Replace `us-east-1` with your preferred AWS region.

---

## 3. Authenticating with Docker Login

### Authentication Command:

```bash
sudo docker login --username AWS --password [password] [account_id].dkr.ecr.us-east-1.amazonaws.com
```

### Parameters:
- `[password]`: Output from the previous `get-login-password` command
- `[account_id]`: Your AWS account ID (found in "My Account" section)

### Success Indicator:
You should see: `Login Succeeded`

---

## 4. Building and Tagging Images

### Build Your Docker Image:

```bash
sudo docker image build -t "echo_service" .
```

### Tag for ECR:

```bash
sudo docker tag echo_service [account_id].dkr.ecr.us-east-1.amazonaws.com/models:echo
```

### Verify Tags:

```bash
sudo docker images
```

This command will show all your local images with their tags.

---

## 5. Pushing Images to ECR

### Push Command:

```bash
sudo docker push [account_id].dkr.ecr.us-east-1.amazonaws.com/models:echo
```

---

## 6. Verifying the Push

### Option A: Using AWS CLI

1. **Set Default Region:**
   ```bash
   aws configure set default.region [region]
   ```

2. **List Images in Repository:**
   ```bash
   aws ecr list-images --repository-name models
   ```

### Option B: Using AWS Console

1. Navigate to ECR in AWS Console
2. Click on your repository (e.g., "models")
3. Click "Images" tab
4. You should see your pushed image with tag `models:echo`

---

## Command Reference

### Complete Workflow Example:

```bash
# 1. Get login token
sudo aws ecr get-login-password --region us-east-1

# 2. Docker login (use output from step 1 as password)
sudo docker login --username AWS --password [token] [account_id].dkr.ecr.us-east-1.amazonaws.com

# 3. Build image
sudo docker image build -t "echo_service" .

# 4. Tag image
sudo docker tag echo_service [account_id].dkr.ecr.us-east-1.amazonaws.com/models:echo

# 5. Push image
sudo docker push [account_id].dkr.ecr.us-east-1.amazonaws.com/models:echo

# 6. Verify push
aws ecr list-images --repository-name models
```

---

## Important Notes

- **Replace Placeholders:** Always replace `[account_id]`, `[password]`, and `[region]` with your actual values
- **Permissions:** Ensure your IAM user has the necessary ECR permissions
- **Region Consistency:** Use the same region throughout the process
- **Image Names:** Repository names must be lowercase and can contain letters, numbers, hyphens, and underscores
- **Authentication:** Docker login tokens are temporary and will need to be refreshed periodically

---

## Troubleshooting

### Common Issues:

1. **Authentication Failed**
   - Verify your AWS credentials are configured correctly
   - Check if your IAM user has ECR permissions
   - Ensure you're using the correct region

2. **Repository Not Found**
   - Verify the repository name matches exactly
   - Check that you're pushing to the correct region

3. **Permission Denied**
   - Confirm your IAM user has `ecr:GetAuthorizationToken`, `ecr:BatchCheckLayerAvailability`, `ecr:PutImage`, and `ecr:InitiateLayerUpload` permissions

---

## Next Steps

The outcome of this process is that we now have a Docker image pushed to ECR that can be used by an orchestration system. 

Once your image is successfully pushed to ECR, you can:
- Use it with AWS ECS for container orchestration
- Deploy it with AWS EKS (Kubernetes)
- Reference it in your infrastructure as code templates
- Set up automated CI/CD pipelines for continuous deployment

---

## Additional Resources

- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)


# ECS Guide Steps

# MLOps Container Deployment Pipeline

Complete end-to-end guide for deploying ML models from development to production using AWS ECS.

## 🎯 MLOps Workflow Overview

```
Local Development → Containerization → Registry → Orchestration → Production
     (Model)     →   (Dockerfile)   →  (ECR)   →    (ECS)    →  (Service)
```

## Prerequisites

- Python ML model/service ready for deployment
- AWS CLI configured (`aws configure`)
- Docker installed locally
- AWS account with appropriate permissions

---

## Phase 1: Prepare Your ML Application

### Step 1: Create Your Model Service

Create a simple API service for your ML model:

```python
# app.py
from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load your trained model
# model = pickle.load(open('model.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        # prediction = model.predict(data['features'])
        
        # Mock response for demo
        return jsonify({
            'prediction': 'sample_prediction',
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

### Step 2: Create Requirements File

```bash
# requirements.txt
flask==2.3.3
numpy==1.24.3
scikit-learn==1.3.0
pandas==2.0.3
gunicorn==21.2.0
```

---

## Phase 2: Containerization

### Step 3: Create Dockerfile

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY model.pkl .  # Your trained model file

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/health || exit 1

# Run application with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "2", "app:app"]
```

### Step 4: Build and Test Locally

```bash
# Build Docker image
docker build -t ml-service:latest .

# Test locally
docker run -p 8080:80 ml-service:latest

# Test the endpoints
curl http://localhost:8080/health
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1,2,3,4]}'
```

---

## Phase 3: Container Registry (ECR)

### Step 5: Create ECR Repository

```bash
# Create ECR repository
aws ecr create-repository --repository-name ml-service

# Get login command
aws ecr get-login-password --region us-east-1 | \
docker login --username AWS --password-stdin \
<account-id>.dkr.ecr.us-east-1.amazonaws.com
```

### Step 6: Push to ECR

- ml-service is the local image name (before the colon).
- :latest is the tag for that local image.


```bash
# Tag your image
docker tag ml-service:latest \
<account-id>.dkr.ecr.us-east-1.amazonaws.com/ml-service:latest

# Push to ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ml-service:latest

# Note the image URI for next steps
echo "<account-id>.dkr.ecr.us-east-1.amazonaws.com/ml-service:latest"
```

---

## Phase 4: ECS Cluster Setup

### Step 7: Create ECS Cluster

**Via AWS Console:**
1. Navigate to **ECS** → **Clusters** → **Create Cluster**
2. Select **EC2 Linux + Networking**
3. Configure:
   ```
   Cluster Name: ml-production
   EC2 Instance Type: t3.medium (or larger for ML workloads)
   Number of instances: 1-3
   VPC: Default or existing VPC
   Subnets: Select 2+ subnets for HA
   Security Group: Allow HTTP (80) and HTTPS (443)
   ```

**Via AWS CLI:**
```bash
aws ecs create-cluster --cluster-name ml-production
```

---

## Phase 5: Task Definition

### Step 8: Create Task Definition

**Via AWS Console:**
1. **ECS** → **Task Definitions** → **Create new Task Definition**
2. Select **EC2**
3. Configure:
   ```
   Family: ml-service-task
   Task Role: ecsTaskExecutionRole
   Network Mode: bridge
   Task Memory: 2048 MB
   Task CPU: 1024 units
   ```

4. **Add Container:**
   ```
   Container Name: ml-service
   Image: <your-ecr-uri>/ml-service:latest
   Memory: 1024 MB
   Port Mappings: Host:0 → Container:80 (dynamic port)
   Environment Variables:
     - MODEL_VERSION=v1.0
     - LOG_LEVEL=INFO
   ```

**Via JSON (Alternative):**
```json
{
  "family": "ml-service-task",
  "taskRoleArn": "arn:aws:iam::<account>:role/ecsTaskExecutionRole",
  "executionRoleArn": "arn:aws:iam::<account>:role/ecsTaskExecutionRole",
  "networkMode": "bridge",
  "memory": "2048",
  "cpu": "1024",
  "containerDefinitions": [
    {
      "name": "ml-service",
      "image": "<ecr-uri>",
      "memory": 1024,
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "MODEL_VERSION", "value": "v1.0"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ml-service",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

---

## Phase 6: Testing Deployment

### Step 9: Run Single Task (Testing)

```bash
# Run a single task for testing
aws ecs run-task \
  --cluster ml-production \
  --task-definition ml-service-task:1 \
  --count 1

# Check task status
aws ecs describe-tasks \
  --cluster ml-production \
  --tasks <task-arn>
```

### Step 10: Find and Test Your Service

1. **Get Task Details:**
   - Go to ECS Console → Clusters → ml-production → Tasks
   - Click on running task → Find public IP

2. **Test Endpoints:**
   ```bash
   # Health check
   curl http://<public-ip>:<port>/health
   
   # Model prediction
   curl -X POST http://<public-ip>:<port>/predict \
     -H "Content-Type: application/json" \
     -d '{"features": [1.0, 2.0, 3.0, 4.0]}'
   ```

---

## Phase 7: Production Service

### Step 11: Create ECS Service

```bash
aws ecs create-service \
  --cluster ml-production \
  --service-name ml-service \
  --task-definition ml-service-task:1 \
  --desired-count 2 \
  --launch-type EC2 \
  --deployment-configuration maximumPercent=200,minimumHealthyPercent=50
```

### Step 12: Setup Load Balancer (Production)

1. **Create Application Load Balancer:**
   ```bash
   aws elbv2 create-load-balancer \
     --name ml-service-alb \
     --subnets subnet-12345 subnet-67890 \
     --security-groups sg-12345
   ```

2. **Create Target Group:**
   ```bash
   aws elbv2 create-target-group \
     --name ml-service-targets \
     --protocol HTTP \
     --port 80 \
     --vpc-id vpc-12345 \
     --health-check-path /health
   ```

3. **Update ECS Service with Load Balancer:**
   ```bash
   aws ecs update-service \
     --cluster ml-production \
     --service ml-service \
     --load-balancers targetGroupArn=<target-group-arn>,containerName=ml-service,containerPort=80
   ```

---

## Phase 8: Monitoring & Logging

### Step 13: Setup CloudWatch Logging

```bash
# Create log group
aws logs create-log-group --log-group-name /ecs/ml-service

# Logs will automatically appear in CloudWatch
```

### Step 14: Setup Monitoring

```python
# Add to your app.py for custom metrics
import boto3
cloudwatch = boto3.client('cloudwatch')

def put_custom_metric(metric_name, value):
    cloudwatch.put_metric_data(
        Namespace='MLService',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': 'Count'
            }
        ]
    )
```

---

## MLOps Best Practices Implemented

✅ **Containerization**: Consistent environment across dev/prod  
✅ **Image Registry**: Centralized, versioned container storage  
✅ **Orchestration**: Automated container management  
✅ **Health Checks**: Built-in service monitoring  
✅ **Scaling**: Auto-scaling based on demand  
✅ **Load Balancing**: High availability and traffic distribution  
✅ **Logging**: Centralized log aggregation  
✅ **Monitoring**: Real-time performance metrics  

## Production Checklist

- [ ] Model artifacts included in container
- [ ] Environment variables configured
- [ ] Health checks implemented
- [ ] Resource limits set appropriately
- [ ] Load balancer configured
- [ ] Auto-scaling policies defined
- [ ] Monitoring and alerting setup
- [ ] CI/CD pipeline for updates
- [ ] Security groups configured
- [ ] IAM roles properly scoped

## Next Steps: CI/CD Pipeline

1. **GitHub Actions** or **Jenkins** for automated builds
2. **Model versioning** with MLflow or DVC
3. **Blue-green deployments** for zero-downtime updates
4. **A/B testing** infrastructure for model comparison
5. **Model monitoring** for drift detection

## Troubleshooting Common Issues

**Container won't start:**
```bash
# Check logs
aws logs get-log-events --log-group-name /ecs/ml-service --log-stream-name <stream>
```

**Service unhealthy:**
- Verify health check endpoint returns 200
- Check security group allows traffic on container port
- Ensure sufficient memory/CPU allocation

**Model performance issues:**
- Monitor CloudWatch metrics
- Check container resource utilization
- Consider scaling up instance types for ML workloads
- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/)
- [AWS CLI ECR Commands](https://docs.aws.amazon.com/cli/latest/reference/ecr/)
