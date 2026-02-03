# Data Model: Azure AKS Cloud Deployment

**Feature**: Phase V Module 2 - Azure Cloud Deployment
**Date**: 2026-02-03

## Overview

This module focuses on infrastructure deployment, not application data. The data model describes the **infrastructure resources** and **configuration artifacts** that need to be managed.

---

## Infrastructure Resources

### Azure Resource Group

| Attribute | Type | Description |
|-----------|------|-------------|
| name | string | Resource group name: `todo-rg` |
| location | string | Azure region: `eastus` |
| subscription | string | Azure subscription ID |

### AKS Cluster

| Attribute | Type | Description |
|-----------|------|-------------|
| name | string | Cluster name: `todo-cluster` |
| resource_group | string | Parent resource group |
| node_count | integer | Number of worker nodes: `2` |
| vm_size | string | Node VM SKU: `Standard_B2s` |
| kubernetes_version | string | K8s version (latest stable) |
| identity_type | string | `SystemAssigned` (managed identity) |
| network_plugin | string | `azure` (Azure CNI) |

### Azure Container Registry

| Attribute | Type | Description |
|-----------|------|-------------|
| name | string | Globally unique: `todoacr{random}` |
| resource_group | string | Parent resource group |
| sku | string | `Basic` |
| admin_enabled | boolean | `false` (use managed identity) |

### Container Images

| Image | Repository | Tags |
|-------|------------|------|
| Backend | `todoacr.azurecr.io/backend` | `v1`, `latest`, `{commit-sha}` |
| Frontend | `todoacr.azurecr.io/frontend` | `v1`, `latest`, `{commit-sha}` |
| Notification Service | `todoacr.azurecr.io/notification-service` | `v1`, `{commit-sha}` |
| Recurring Service | `todoacr.azurecr.io/recurring-service` | `v1`, `{commit-sha}` |

---

## Kubernetes Resources

### Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo
```

### Deployments

| Deployment | Replicas | Image | Port | Dapr Sidecar |
|------------|----------|-------|------|--------------|
| backend | 2 | backend:v1 | 8000 | Yes |
| frontend | 2 | frontend:v1 | 3000 | No |
| notification-service | 1 | notification-service:v1 | 8001 | Yes |
| recurring-service | 1 | recurring-service:v1 | 8002 | Yes |

### Services

| Service | Type | Port | Target |
|---------|------|------|--------|
| backend | ClusterIP | 8000 | backend pods |
| frontend | LoadBalancer | 80 | frontend pods |
| notification-service | ClusterIP | 8001 | notification pods |
| recurring-service | ClusterIP | 8002 | recurring pods |

### ConfigMaps

**app-config**:
| Key | Value |
|-----|-------|
| NEXT_PUBLIC_API_URL | `http://backend:8000` |
| FRONTEND_URL | `http://{loadbalancer-ip}` |

### Secrets

**app-secrets**:
| Key | Description |
|-----|-------------|
| database-url | Neon PostgreSQL connection string |
| jwt-secret | JWT signing key |
| openai-api-key | OpenAI API key |

**kafka-secrets**:
| Key | Description |
|-----|-------------|
| username | Redpanda SASL username |
| password | Redpanda SASL password |
| bootstrap-servers | Redpanda broker URL |

---

## Dapr Components

### Pub/Sub Component (Redpanda)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: todo
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "seed-xxx.redpanda.com:9092"
    - name: authType
      value: "password"
    - name: saslUsername
      secretKeyRef:
        name: kafka-secrets
        key: username
    - name: saslPassword
      secretKeyRef:
        name: kafka-secrets
        key: password
```

### State Component (PostgreSQL)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: todo
spec:
  type: state.postgresql
  version: v1
  metadata:
    - name: connectionString
      secretKeyRef:
        name: app-secrets
        key: database-url
```

### Secrets Component

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
  namespace: todo
spec:
  type: secretstores.kubernetes
  version: v1
```

---

## Redpanda Cloud Resources

### Cluster

| Attribute | Value |
|-----------|-------|
| Type | Serverless |
| Tier | Free |
| Storage | 1GB |
| Throughput | 50MB/s |

### Topics

| Topic | Partitions | Retention |
|-------|------------|-----------|
| task-events | 3 | 24h |
| reminders | 3 | 24h |
| task-updates | 3 | 24h |

### Credentials

| Type | Value |
|------|-------|
| SASL Mechanism | SCRAM-SHA-256 |
| Username | (generated) |
| Password | (generated) |
| Bootstrap Server | seed-xxx.cloud.redpanda.com:9092 |

---

## GitHub Actions Secrets

| Secret Name | Description | Used By |
|-------------|-------------|---------|
| AZURE_CREDENTIALS | Service principal JSON | azure/login action |
| ACR_LOGIN_SERVER | `todoacr.azurecr.io` | Docker push |
| DATABASE_URL | Neon connection string | K8s secret creation |
| JWT_SECRET_KEY | JWT signing secret | K8s secret creation |
| OPENAI_API_KEY | OpenAI key | K8s secret creation |
| KAFKA_USERNAME | Redpanda username | K8s secret creation |
| KAFKA_PASSWORD | Redpanda password | K8s secret creation |
| KAFKA_BOOTSTRAP_SERVERS | Redpanda broker URL | K8s secret creation |

---

## Helm Values Structure

### values-azure.yaml

```yaml
# Global
namespace: todo

# Backend
backend:
  image:
    repository: todoacr.azurecr.io/backend
    tag: v1
  replicas: 2
  service:
    type: ClusterIP
    port: 8000
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 128Mi
  env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: database-url
  dapr:
    enabled: true
    appId: backend
    appPort: 8000

# Frontend
frontend:
  image:
    repository: todoacr.azurecr.io/frontend
    tag: v1
  replicas: 2
  service:
    type: LoadBalancer
    port: 80
  resources:
    limits:
      cpu: 300m
      memory: 256Mi
    requests:
      cpu: 50m
      memory: 64Mi

# Notification Service
notificationService:
  image:
    repository: todoacr.azurecr.io/notification-service
    tag: v1
  replicas: 1
  dapr:
    enabled: true
    appId: notification-service

# Recurring Service
recurringService:
  image:
    repository: todoacr.azurecr.io/recurring-service
    tag: v1
  replicas: 1
  dapr:
    enabled: true
    appId: recurring-service
```

---

## Entity Relationships

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Azure Subscription                           │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    Resource Group: todo-rg                   │    │
│  ├─────────────────────────────────────────────────────────────┤    │
│  │  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐    │    │
│  │  │  AKS Cluster │   │     ACR      │   │ Load Balancer│    │    │
│  │  │  todo-cluster│   │  todoacr123  │   │   (auto)     │    │    │
│  │  └──────────────┘   └──────────────┘   └──────────────┘    │    │
│  │         │                  │                   │            │    │
│  │         ▼                  ▼                   ▼            │    │
│  │  ┌────────────────────────────────────────────────────┐    │    │
│  │  │              Kubernetes Cluster                     │    │    │
│  │  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────┐   │    │    │
│  │  │  │backend │ │frontend│ │notif-  │ │recurring-  │   │    │    │
│  │  │  │  (2)   │ │  (2)   │ │service │ │service     │   │    │    │
│  │  │  └────────┘ └────────┘ └────────┘ └────────────┘   │    │    │
│  │  │  ┌───────────────────────────────────────────────┐ │    │    │
│  │  │  │                 Dapr System                    │ │    │    │
│  │  │  └───────────────────────────────────────────────┘ │    │    │
│  │  └────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                              │                │
                              ▼                ▼
               ┌──────────────────┐  ┌──────────────────┐
               │  Neon PostgreSQL │  │  Redpanda Cloud  │
               │   (external)     │  │   (external)     │
               └──────────────────┘  └──────────────────┘
```
