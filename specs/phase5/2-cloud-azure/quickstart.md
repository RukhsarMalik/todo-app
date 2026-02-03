# Quickstart: Azure AKS Cloud Deployment

**Feature**: Phase V Module 2 - Azure Cloud Deployment
**Date**: 2026-02-03

## Prerequisites

### Required Tools
- Azure CLI (`az`) v2.50+
- kubectl v1.28+
- Helm v3.12+
- Dapr CLI v1.12+
- Git

### Required Accounts
- Azure subscription with $200 credit
- Redpanda Cloud account (free tier)
- GitHub repository with Actions enabled

### Required Secrets/Credentials
- `DATABASE_URL`: Neon PostgreSQL connection string (from Phase V Module 1)
- `JWT_SECRET_KEY`: JWT signing secret (from Phase V Module 1)
- `OPENAI_API_KEY`: OpenAI API key (from Phase V Module 1)
- Redpanda Cloud SASL credentials (to be created)
- Azure service principal (to be created)

---

## Quick Start Steps

### Step 1: Azure Authentication
```bash
# Login to Azure
az login

# Set subscription (if multiple)
az account set --subscription "<subscription-id>"
```

### Step 2: Create Resource Group
```bash
az group create --name todo-rg --location eastus
```

### Step 3: Create Azure Container Registry
```bash
# Create ACR (name must be globally unique)
az acr create --resource-group todo-rg --name todoacr$(date +%s) --sku Basic

# Get ACR login server name
ACR_NAME=$(az acr list --resource-group todo-rg --query "[0].name" -o tsv)
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
```

### Step 4: Create AKS Cluster
```bash
# Create 2-node cluster
az aks create \
  --resource-group todo-rg \
  --name todo-cluster \
  --node-count 2 \
  --node-vm-size Standard_B2s \
  --generate-ssh-keys \
  --attach-acr $ACR_NAME

# Get credentials for kubectl
az aks get-credentials --resource-group todo-rg --name todo-cluster
```

### Step 5: Verify Cluster
```bash
# Check nodes
kubectl get nodes

# Expected output:
# NAME                                STATUS   ROLES   AGE   VERSION
# aks-nodepool1-xxxxx-vmss000000     Ready    agent   2m    v1.28.x
# aks-nodepool1-xxxxx-vmss000001     Ready    agent   2m    v1.28.x
```

### Step 6: Install Dapr
```bash
# Install Dapr on Kubernetes
dapr init -k

# Verify Dapr installation
dapr status -k

# Expected: dapr-operator, dapr-placement, dapr-sidecar-injector, dapr-sentry all running
```

### Step 7: Setup Redpanda Cloud
1. Go to https://cloud.redpanda.com
2. Create a Serverless cluster
3. Create topics: `task-events`, `reminders`, `task-updates`
4. Create SASL credentials (username/password)
5. Note the bootstrap server URL

### Step 8: Create Kubernetes Secrets
```bash
# Create namespace
kubectl create namespace todo

# Create app secrets
kubectl create secret generic app-secrets -n todo \
  --from-literal=database-url="<neon-connection-string>" \
  --from-literal=jwt-secret="<jwt-secret-key>" \
  --from-literal=openai-api-key="<openai-key>"

# Create Kafka secrets
kubectl create secret generic kafka-secrets -n todo \
  --from-literal=username="<redpanda-username>" \
  --from-literal=password="<redpanda-password>" \
  --from-literal=bootstrap-servers="<seed-xxx.redpanda.com:9092>"
```

### Step 9: Deploy Dapr Components
```bash
# Apply Pub/Sub component for Redpanda
kubectl apply -f phase-5/k8s/dapr-pubsub.yaml

# Apply Secrets component
kubectl apply -f phase-5/k8s/dapr-secrets.yaml
```

### Step 10: Build and Push Images
```bash
# Build and push backend
az acr build --registry $ACR_NAME --image backend:v1 ./phase-5/backend

# Build and push frontend
az acr build --registry $ACR_NAME --image frontend:v1 ./phase-5/frontend
```

### Step 11: Deploy Application
```bash
# Deploy with Helm
helm upgrade --install todo ./phase-5/helm/todo-chart \
  --namespace todo \
  --values ./phase-5/helm/todo-chart/values-azure.yaml \
  --set backend.image.repository=$ACR_LOGIN_SERVER/backend \
  --set frontend.image.repository=$ACR_LOGIN_SERVER/frontend \
  --wait
```

### Step 12: Get External IP
```bash
# Wait for LoadBalancer IP
kubectl get svc frontend -n todo --watch

# Once EXTERNAL-IP is assigned, access the application
FRONTEND_IP=$(kubectl get svc frontend -n todo -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "Application URL: http://$FRONTEND_IP"
```

---

## Verification Commands

```bash
# Check all pods are running
kubectl get pods -n todo

# Check services
kubectl get svc -n todo

# View backend logs
kubectl logs -l app=backend -n todo -c backend

# View frontend logs
kubectl logs -l app=frontend -n todo

# Test backend health
kubectl port-forward svc/backend 8000:8000 -n todo &
curl http://localhost:8000/health
```

---

## GitHub Actions Setup

### Required GitHub Secrets
1. `AZURE_CREDENTIALS`: Service principal JSON
2. `ACR_LOGIN_SERVER`: e.g., `todoacr123.azurecr.io`
3. `DATABASE_URL`: Neon connection string
4. `JWT_SECRET_KEY`: JWT signing secret
5. `OPENAI_API_KEY`: OpenAI API key
6. `KAFKA_USERNAME`: Redpanda SASL username
7. `KAFKA_PASSWORD`: Redpanda SASL password
8. `KAFKA_BOOTSTRAP_SERVERS`: Redpanda broker URL

### Create Service Principal
```bash
# Create service principal with contributor access
az ad sp create-for-rbac \
  --name "github-actions-todo" \
  --role contributor \
  --scopes /subscriptions/<subscription-id>/resourceGroups/todo-rg \
  --sdk-auth

# Copy the JSON output to GitHub secret AZURE_CREDENTIALS
```

---

## Cleanup Commands

```bash
# Delete all resources in resource group
az group delete --name todo-rg --yes --no-wait

# Verify deletion
az group show --name todo-rg 2>/dev/null || echo "Resource group deleted"
```

---

## Troubleshooting

### Pods stuck in ImagePullBackOff
```bash
# Verify ACR attachment
az aks check-acr --resource-group todo-rg --name todo-cluster --acr $ACR_NAME
```

### Pods stuck in CrashLoopBackOff
```bash
# Check pod logs
kubectl logs <pod-name> -n todo --previous

# Check Dapr sidecar logs
kubectl logs <pod-name> -n todo -c daprd
```

### LoadBalancer IP not assigned
```bash
# Check service events
kubectl describe svc frontend -n todo
```

### Kafka connection issues
```bash
# Verify Dapr component
kubectl get component kafka-pubsub -n todo -o yaml

# Test from pod
kubectl exec -it <backend-pod> -n todo -c backend -- python -c "
from kafka import KafkaProducer
import os
p = KafkaProducer(bootstrap_servers=os.environ['KAFKA_BOOTSTRAP_SERVERS'])
print('Connected!')
"
```
