# Phase IV Module 1: Deployment Guide

## Overview

This guide covers three deployment methods for the Todo application:
1. **Docker Compose** - Local development
2. **Kubernetes (kubectl)** - Direct K8s deployment
3. **Helm** - Managed K8s deployment

## Prerequisites

- Docker Desktop installed and running
- Minikube installed (for K8s deployment)
- kubectl installed
- Helm 3.x installed

### Verify Prerequisites

```bash
# Check Docker
docker --version
docker ps

# Check kubectl
kubectl version --client

# Check Helm
helm version

# Check Minikube
minikube version
```

---

## Step 1: Docker (Local Development)

### Build Images

```bash
# Build backend image
docker build -t todo-backend ./phase-4/backend

# Build frontend image
docker build -t todo-frontend ./phase-4/frontend
```

### Run with Docker Compose

```bash
# Start all services
cd phase-4
docker-compose up

# Or run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Test
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Health Check: http://localhost:8000/health

---

## Step 2: Kubernetes (kubectl)

### Start Minikube

```bash
# Start cluster
minikube start

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

### Build Images to Minikube

```bash
# Point Docker to Minikube's registry
eval $(minikube docker-env)

# Build images directly to Minikube
docker build -t todo-backend:latest ./phase-4/backend
docker build -t todo-frontend:latest ./phase-4/frontend

# Verify images
docker images | grep todo
```

### Update Secrets

Before deploying, update the secrets in `k8s/secrets.yaml`:

```bash
# Encode your actual values
echo -n 'your-database-url' | base64
echo -n 'your-jwt-secret' | base64
echo -n 'your-openai-key' | base64
```

### Deploy

```bash
# Apply all manifests
kubectl apply -f phase-4/k8s/

# Or apply individually
kubectl apply -f phase-4/k8s/secrets.yaml
kubectl apply -f phase-4/k8s/backend-deployment.yaml
kubectl apply -f phase-4/k8s/backend-service.yaml
kubectl apply -f phase-4/k8s/frontend-deployment.yaml
kubectl apply -f phase-4/k8s/frontend-service.yaml

# Check status
kubectl get pods
kubectl get services
kubectl get deployments
```

### Access Application

```bash
# Get Minikube IP and NodePort
minikube service frontend-service --url

# Or open in browser
minikube service frontend-service
```

### Useful Commands

```bash
# View logs
kubectl logs deployment/backend-deployment
kubectl logs deployment/frontend-deployment

# Scale deployments
kubectl scale deployment backend-deployment --replicas=3

# Describe resources
kubectl describe pod <pod-name>

# Delete all resources
kubectl delete -f phase-4/k8s/
```

---

## Step 3: Helm (Managed Deployment)

### Install with Helm

```bash
# Install the chart
helm install todo ./phase-4/helm/todo-chart

# Install with custom values
helm install todo ./phase-4/helm/todo-chart \
  --set secrets.databaseUrl="postgresql://..." \
  --set secrets.jwtSecretKey="your-jwt-secret" \
  --set secrets.openaiApiKey="sk-..."
```

### Verify Deployment

```bash
# Check Helm release
helm list
helm status todo

# Check pods
kubectl get pods

# Access application
minikube service todo-frontend
```

### Upgrade

```bash
# Upgrade with new values
helm upgrade todo ./phase-4/helm/todo-chart

# Upgrade with specific value changes
helm upgrade todo ./phase-4/helm/todo-chart \
  --set backend.replicaCount=3
```

### Uninstall

```bash
# Remove all resources
helm uninstall todo

# Verify cleanup
kubectl get all
```

### Helm Lint

```bash
# Validate chart
helm lint ./phase-4/helm/todo-chart

# Dry-run to see rendered templates
helm template todo ./phase-4/helm/todo-chart
```

---

## File Structure

```
phase-4/
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── ... (application code)
├── frontend/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── ... (application code)
├── docker-compose.yml
├── k8s/
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   └── secrets.yaml
├── helm/
│   └── todo-chart/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── .helmignore
│       └── templates/
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── frontend-deployment.yaml
│           ├── frontend-service.yaml
│           ├── secrets.yaml
│           └── configmap.yaml
└── DEPLOYMENT.md
```

---

## Troubleshooting

### Images Not Found

```bash
# Ensure Docker is pointing to Minikube
eval $(minikube docker-env)

# Rebuild images
docker build -t todo-backend:latest ./phase-4/backend
docker build -t todo-frontend:latest ./phase-4/frontend
```

### Pod CrashLoopBackOff

```bash
# Check logs
kubectl logs <pod-name>

# Describe pod for events
kubectl describe pod <pod-name>
```

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints

# Port forward for debugging
kubectl port-forward service/frontend-service 8080:80
```

### Database Connection Issues

- Verify DATABASE_URL is correct in secrets
- Ensure Neon PostgreSQL allows connections from your IP
- Check SSL requirements in connection string
