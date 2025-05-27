# Local Kubernetes Testing Guide

## Prerequisites

1. Docker Desktop with Kubernetes enabled OR Minikube
2. kubectl configured to connect to your local cluster
3. Auth0 application configured for local testing

## Setup Steps

### 1. Prepare Auth0 Configuration

Update your Auth0 application settings:
- Allowed Callback URLs: `http://localhost:30080/callback, http://localhost:8080/callback`
- Allowed Logout URLs: `http://localhost:30080, http://localhost:8080`

### 2. Encode Your Secrets

Get the values from your `.env` file and base64 encode them:

```bash
# Windows PowerShell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("your-secret-value"))

# Or using Git Bash / Linux
echo -n 'your-secret-value' | base64
```

Update `auth-secret.yaml` with the encoded values.

### 3. Build and Deploy

Run the deployment script:

```bash
# Make the script executable (Linux/Mac)
chmod +x deploy-local.sh

# Run the deployment
./deploy-local.sh
```

Or manually:

```bash
# Build Docker image
cd ../
docker build -t clipsify-auth:local .
cd manifests

# Apply Kubernetes manifests
kubectl apply -f auth-configmap.yaml
kubectl apply -f auth-secret.yaml
kubectl apply -f auth-deployment.yaml
kubectl apply -f auth-service.yaml
```

### 4. Access the Application

You have three options to access the application:

#### Option 1: NodePort (Easiest)
The service is exposed on port 30080:
```
http://localhost:30080
```

#### Option 2: Port Forwarding
```bash
kubectl port-forward service/auth-service 8080:80
```
Then access:
```
http://localhost:8080
```

#### Option 3: Port Forward to Pod (for debugging)
```bash
# Get pod name
kubectl get pods -l app=auth-service

# Port forward to the pod
kubectl port-forward pod/<pod-name> 3000:3000
```
Then access:
```
http://localhost:3000
```

### 5. Verify Deployment

Check if everything is running:

```bash
# Check pods
kubectl get pods -l app=auth-service

# Check service
kubectl get service auth-service

# Check logs
kubectl logs -l app=auth-service

# Describe pod for troubleshooting
kubectl describe pod -l app=auth-service
```

## Troubleshooting

### Pod not starting
1. Check logs: `kubectl logs -l app=auth-service`
2. Check events: `kubectl describe pod -l app=auth-service`
3. Verify image exists: `docker images | grep clipsify-auth`

### Can't access the application
1. Check service: `kubectl get service auth-service`
2. Check endpoints: `kubectl get endpoints auth-service`
3. Try port-forwarding instead of NodePort

### Auth0 redirect issues
1. Make sure callback URLs in Auth0 match your access method
2. Check AUTH0_DOMAIN in ConfigMap matches your Auth0 domain
3. Verify secrets are properly base64 encoded

## Clean Up

To remove the deployment:

```bash
kubectl delete -f auth-deployment.yaml
kubectl delete -f auth-service.yaml
kubectl delete -f auth-secret.yaml
kubectl delete -f auth-configmap.yaml
```