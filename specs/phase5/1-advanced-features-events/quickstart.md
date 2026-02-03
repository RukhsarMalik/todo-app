# Quickstart: Advanced Features + Event Architecture

**Feature**: 007-advanced-features-events | **Date**: 2026-02-02

## Prerequisites

- Minikube running (`minikube start --memory=8192 --cpus=4`)
- kubectl configured
- Helm 3.x installed
- Dapr CLI installed (`dapr init -k`)
- Docker daemon accessible to Minikube (`eval $(minikube docker-env)`)

## Step 1: Install Strimzi Kafka

```bash
kubectl create namespace kafka
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
kubectl wait --for=condition=ready pod -l name=strimzi-cluster-operator -n kafka --timeout=300s
kubectl apply -f phase-5/k8s/strimzi/kafka-cluster.yaml -n kafka
kubectl wait kafka/todo-kafka --for=condition=Ready -n kafka --timeout=300s
```

## Step 2: Install Dapr

```bash
dapr init -k
dapr status -k
kubectl apply -f phase-5/dapr/components/
```

## Step 3: Build Docker Images

```bash
eval $(minikube docker-env)
docker build -t todo-backend:latest phase-5/backend/
docker build -t todo-frontend:latest phase-5/frontend/
docker build -t todo-notification:latest phase-5/services/notification/
docker build -t todo-recurring-task:latest phase-5/services/recurring-task/
```

## Step 4: Deploy

```bash
kubectl apply -f phase-5/k8s/secrets.yaml
kubectl apply -f phase-5/k8s/
kubectl apply -f phase-5/dapr/subscriptions/
```

Or via Helm:
```bash
helm install todo phase-5/helm/todo-chart/
```

## Step 5: Verify

```bash
kubectl get pods
# All pods should be Running with 2/2 (app + Dapr sidecar)

# Port forward frontend
kubectl port-forward svc/frontend 3000:3000

# Port forward backend
kubectl port-forward svc/backend 8000:8000
```

## Step 6: Test End-to-End

```bash
# Create a task with priority and due date
curl -X POST http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","priority":"high","due_date":"2026-02-10T15:00:00Z"}'

# Search tasks
curl http://localhost:8000/api/{user_id}/tasks?search=test&priority=high&sort=due_date&order=asc \
  -H "Authorization: Bearer {token}"

# Check notifications (after reminder fires)
curl http://localhost:8000/api/{user_id}/notifications \
  -H "Authorization: Bearer {token}"
```

## Local Development (without K8s)

For development without Minikube, run services directly:

```bash
# Backend
cd phase-5/backend && uv run uvicorn main:app --reload --port 8000

# Frontend
cd phase-5/frontend && npm run dev

# Dapr standalone (optional, for pub/sub testing)
dapr run --app-id backend --app-port 8000 -- uv run uvicorn main:app --port 8000
```
