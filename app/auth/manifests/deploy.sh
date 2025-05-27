#!/bin/bash

# Deploy to AKS
echo "Deploying Auth Service to AKS..."

# Apply ConfigMap and Secret
kubectl apply -f auth-configmap.yaml
kubectl apply -f auth-secret.yaml

# Apply Deployment and Service
kubectl apply -f auth-deployment.yaml
kubectl apply -f auth-service.yaml

# Apply Ingress
kubectl apply -f ingress.yaml

echo "Deployment complete!"

# Check deployment status
kubectl get deployments
kubectl get services
kubectl get ingress

echo ""
echo "Waiting for Ingress IP address..."
echo "Run: kubectl get ingress clipsify-ingress -w"
echo ""
echo "Once you have the IP, configure your DNS:"
echo "- Create an A record for clipsify.net pointing to the Ingress IP"
echo "- Create an A record for www.clipsify.net pointing to the Ingress IP"