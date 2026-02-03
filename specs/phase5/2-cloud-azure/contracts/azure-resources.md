# Contract: Azure Resource Configuration

**Feature**: Phase V Module 2 - Azure Cloud Deployment
**Date**: 2026-02-03
**Type**: Infrastructure Contract

## Resource Group

| Field | Value | Constraint |
|-------|-------|------------|
| Name | `todo-rg` | Required, alphanumeric with hyphens |
| Location | `eastus` | Any Azure region |
| Subscription | User's subscription | Must have $200 credit |

---

## Azure Kubernetes Service (AKS)

| Field | Value | Constraint |
|-------|-------|------------|
| Name | `todo-cluster` | Required, alphanumeric with hyphens |
| Resource Group | `todo-rg` | Must exist |
| Node Count | `2` | Minimum 1, maximum 3 for cost |
| VM Size | `Standard_B2s` | Cost-effective, 2 vCPU, 4GB RAM |
| Kubernetes Version | Latest stable | Auto-selected by Azure |
| Identity | `SystemAssigned` | Managed identity |
| Network Plugin | `azure` | Azure CNI for pod networking |
| SSH Keys | Auto-generated | `--generate-ssh-keys` flag |

### AKS Scaling Limits
- Min nodes: 1
- Max nodes: 3 (budget constraint)
- Auto-scaling: Disabled (manual only)

---

## Azure Container Registry (ACR)

| Field | Value | Constraint |
|-------|-------|------------|
| Name | `todoacr{random}` | Must be globally unique |
| Resource Group | `todo-rg` | Must exist |
| SKU | `Basic` | 10GB storage, sufficient |
| Admin Enabled | `false` | Use managed identity |
| Attached to AKS | `true` | `--attach-acr` flag |

### Image Naming Convention
```
{acr-name}.azurecr.io/{service}:{tag}

Examples:
- todoacr123.azurecr.io/backend:v1
- todoacr123.azurecr.io/backend:abc1234  (commit SHA)
- todoacr123.azurecr.io/frontend:latest
```

### Tag Policy
| Tag | Usage |
|-----|-------|
| `v1` | Initial release |
| `latest` | Most recent build |
| `{commit-sha}` | CI/CD builds (first 7 chars) |

---

## Azure Load Balancer

| Field | Value | Constraint |
|-------|-------|------------|
| Type | Standard | Created by AKS |
| SKU | Standard | Required for AKS |
| Public IP | Dynamic | Assigned on service creation |

### Exposed Services
| Service | External Port | Internal Port |
|---------|---------------|---------------|
| Frontend | 80 | 3000 |

---

## Service Principal (GitHub Actions)

| Field | Value | Constraint |
|-------|-------|------------|
| Name | `github-actions-todo` | Descriptive name |
| Role | `Contributor` | Required for deployments |
| Scope | Resource Group | `/subscriptions/{id}/resourceGroups/todo-rg` |

### Required Permissions
- Create/update deployments in AKS
- Push images to ACR
- Read resource group metadata

### Output Format (AZURE_CREDENTIALS)
```json
{
  "clientId": "<app-id>",
  "clientSecret": "<password>",
  "subscriptionId": "<subscription-id>",
  "tenantId": "<tenant-id>",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

---

## Budget Configuration

| Threshold | Alert Type | Action |
|-----------|------------|--------|
| $50 | Email | Warning notification |
| $100 | Email | Review resources |
| $150 | Email | Consider cleanup |

### Budget Scope
- Resource Group: `todo-rg`
- Time Period: Monthly
- Start Date: Deployment date
