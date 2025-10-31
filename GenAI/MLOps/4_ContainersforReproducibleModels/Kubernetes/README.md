# Kubernetes Deployment on Google Cloud Platform (GCP)

This guide walks you through deploying a containerized service using Google Kubernetes Engine (GKE) on Google Cloud Platform.

## Overview

**Kubernetes** is a container orchestration system originally developed by Google, now open source. **Google Kubernetes Engine (GKE)** is GCP's managed Kubernetes service that simplifies container deployment, management, and scaling.

## Prerequisites

- Google Cloud Platform account with billing enabled
- GCP project created
- Docker installed on your local machine
- GCP credentials JSON file (service account key)
- A Docker container/service ready for deployment (e.g., `echo_service`)

## Architecture

```
Local Docker Image → GCP Container Registry → GKE Cluster → Load Balancer → Public Internet
```

---

## Step 1: Prepare Your GCP Environment

### 1.1 Set up GCP Credentials
Ensure you have your GCP service account JSON file ready:
```bash
# Your credentials file should look like:
# creds.json (or your-service-account-key.json)
```

### 1.2 Enable Required APIs
Make sure the following APIs are enabled in your GCP project:
- Kubernetes Engine API
- Container Registry API
- Compute Engine API

---

## Step 2: Push Docker Image to Container Registry

### 2.1 Authenticate Docker with GCP
```bash
# Login to GCP Container Registry using your credentials
cat creds.json | sudo docker login -u _json_key --password-stdin https://us.gcr.io
```

### 2.2 Tag Your Docker Image
```bash
# Tag your local image for GCP Container Registry
# Replace [gcp_project_id] with your actual GCP project ID
sudo docker tag echo_service us.gcr.io/[gcp_project_id]/echo_service
```

### 2.3 Push Image to Registry
```bash
# Push the tagged image to Container Registry
sudo docker push us.gcr.io/[gcp_project_id]/echo_service
```

### 2.4 Verify Upload
- Go to GCP Console → Container Registry
- Verify your image appears in the registry

---

## Step 3: Deploy to Google Kubernetes Engine

### 3.1 Navigate to Kubernetes Engine
1. Open [Google Cloud Console](https://console.cloud.google.com)
2. Search for and select **"Kubernetes Engine"**
3. If prompted, enable the Kubernetes Engine API

### 3.2 Deploy Container
1. Click **"Deploy Container"** (or **"Create Deployment"**)
2. Select **"Existing Container Image"**
3. Choose your image: `us.gcr.io/[gcp_project_id]/echo_service:latest`
4. Configure deployment settings:
   - **Application name**: `echo-gke`
   - **Cluster**: Create new or select existing
   - **Namespace**: default (or create custom)
5. Click **"Deploy"**

### 3.3 Wait for Deployment
- The deployment process typically takes 3-5 minutes
- Monitor progress in the GKE dashboard
- Once complete, you'll see your cluster listed under "Clusters"

---

## Step 4: Expose Service to Internet

### 4.1 Access Your Workload
1. From the **GKE menu**, select your cluster
2. Click on **"Workloads"** in the left sidebar
3. Find and select the **"echo-gke"** workload

### 4.2 Expose the Service
1. Click the **"Actions"** menu (three dots)
2. Select **"Expose"**
3. Configure exposure settings:
   - **Service type**: `Load Balancer`
   - **Protocol**: `HTTP`
   - **Port**: `80` (or your service port)
   - **Target port**: Your container's internal port
4. Click **"Expose"**

### 4.3 Get External IP
1. Navigate to **Services & Ingress**
2. Find your service (usually named `echo-gke-service`)
3. Wait for **External IP** to be assigned (may take 2-3 minutes)
4. Note the external IP address (e.g., `35.238.43.63`)

---

## Step 5: Test Your Deployment

### 5.1 Test the Service
```bash
# Example API call using curl
curl "http://[EXTERNAL_IP]/predict?msg=Hello_from_GKE"

# Expected response:
# {"response":"Hello_from_GKE","success":true}
```

### 5.2 Verify in Browser
Navigate to: `http://[EXTERNAL_IP]/predict?msg=Hi_from_GKE`

---

## Key Features of GKE Deployment

### ✅ **Automatic Benefits**
- **Load Balancing**: Traffic distributed across multiple pods
- **Auto-scaling**: Pods scale based on demand
- **Health Monitoring**: Automatic restart of failed containers
- **Rolling Updates**: Zero-downtime deployments
- **SSL Termination**: HTTPS support (when configured)

---

## Management Commands

### View Cluster Information
```bash
# List clusters
gcloud container clusters list

# Get cluster credentials
gcloud container clusters get-credentials [CLUSTER_NAME] --zone [ZONE]

# View pods
kubectl get pods

# View services
kubectl get services

# View deployments
kubectl get deployments
```

### Scaling Your Service
```bash
# Scale deployment to 3 replicas
kubectl scale deployment echo-gke --replicas=3

# View horizontal pod autoscaler (if configured)
kubectl get hpa
```

---

## Troubleshooting

### Common Issues

**1. Image Pull Errors**
```bash
# Check if image exists in Container Registry
gcloud container images list

# Verify image tag
gcloud container images list-tags us.gcr.io/[PROJECT_ID]/echo_service
```

**2. Service Not Accessible**
```bash
# Check service status
kubectl get services
kubectl describe service [SERVICE_NAME]

# Check pod status
kubectl get pods
kubectl describe pod [POD_NAME]
```

**3. Deployment Stuck**
```bash
# Check deployment status
kubectl get deployments
kubectl describe deployment echo-gke

# View events
kubectl get events --sort-by=.metadata.creationTimestamp
```

---

## Clean Up Resources

### Delete Service and Deployment
```bash
# Delete service (removes load balancer)
kubectl delete service echo-gke-service

# Delete deployment
kubectl delete deployment echo-gke

# Delete cluster (if no longer needed)
gcloud container clusters delete [CLUSTER_NAME] --zone [ZONE]
```

---

## Cost Optimization Tips

1. **Use Preemptible Nodes**: Reduce costs by up to 80%
2. **Right-size Your Cluster**: Start small and scale as needed
3. **Enable Autoscaling**: Automatically adjust resources based on demand
4. **Monitor Usage**: Use GCP's monitoring tools to track resource utilization
5. **Set up Alerts**: Get notified of unusual spending

---

## Security Best Practices

1. **Use Private Clusters**: Isolate nodes from public internet
2. **Enable Network Policy**: Control pod-to-pod communication
3. **Regularly Update**: Keep GKE and node images updated
4. **Use Workload Identity**: Secure access to GCP services
5. **Scan Images**: Use Container Analysis API for vulnerability scanning

---

## Next Steps

- **Set up CI/CD Pipeline**: Automate deployments using Cloud Build
- **Configure Monitoring**: Use Google Cloud Operations (formerly Stackdriver)
- **Implement SSL/TLS**: Add HTTPS support with Google-managed certificates
- **Add Custom Domains**: Use Cloud DNS for custom domain mapping
- **Implement Blue-Green Deployments**: Zero-downtime update strategies

---

## Support Resources

- [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Google Cloud Support](https://cloud.google.com/support)
- [GKE Best Practices](https://cloud.google.com/kubernetes-engine/docs/best-practices)

---

*For questions or issues, refer to the official GCP documentation or contact your system administrator.*