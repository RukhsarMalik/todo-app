# Implementation Plan: Azure AKS Cloud Deployment

**Branch**: `008-azure-aks-deployment` | **Date**: 2026-02-03 | **Spec**: [specification.md](./specification.md)
**Input**: Feature specification from `/specs/phase5/2-cloud-azure/specification.md`

## Summary

Deploy the Phase V Todo application with all advanced features (priority, due dates, tags, recurring tasks, notifications) to Azure Kubernetes Service (AKS). The deployment uses Azure Container Registry (ACR) for images, Redpanda Cloud for managed Kafka (event streaming), Dapr for event-driven architecture, and GitHub Actions for CI/CD automation.

## Technical Context

**Language/Version**: N/A (Infrastructure deployment - bash scripts, YAML manifests, Helm charts)
**Primary Dependencies**: Azure CLI, kubectl, Helm, Dapr CLI, GitHub Actions
**Storage**: Neon PostgreSQL (existing from Phase V Module 1), Redpanda Cloud (Kafka)
**Testing**: Manual verification via kubectl, curl, browser
**Target Platform**: Azure AKS (2-node Standard_B2s cluster)
**Project Type**: Infrastructure/DevOps
**Performance Goals**: All pods Running within 5 minutes, CI/CD under 10 minutes
**Constraints**: $200 Azure credit budget, 14-day hackathon timeline
**Scale/Scope**: 4 services (backend, frontend, notification-service, recurring-service), 2 replicas each for backend/frontend

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Maximum 3 projects (we have 4 services but they're microservices in one deployment)
- [x] Direct approach only (using managed services where possible)
- [x] No repository pattern (N/A - infrastructure only)
- [x] Test-first (validation commands documented)
- [x] Explicit error handling (edge cases documented in spec)

## Project Structure

### Documentation (this feature)

```text
specs/phase5/2-cloud-azure/
├── specification.md      # Feature requirements
├── plan.md               # This file
├── research.md           # Phase 0 research decisions
├── data-model.md         # Infrastructure resource model
├── quickstart.md         # Setup guide
├── contracts/            # Configuration contracts
│   ├── azure-resources.md
│   ├── dapr-components.yaml
│   ├── github-actions.yaml
│   └── helm-values.yaml
├── checklists/
│   └── requirements.md   # Spec quality checklist
└── tasks.md              # Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
phase-5/
├── backend/              # FastAPI backend (existing)
│   └── Dockerfile        # Updated for ACR build
├── frontend/             # Next.js frontend (existing)
│   └── Dockerfile        # Updated for ACR build
├── helm/
│   └── todo-chart/
│       ├── Chart.yaml
│       ├── values.yaml         # Local/Minikube values
│       ├── values-azure.yaml   # NEW: Azure-specific values
│       └── templates/
│           ├── backend-deployment.yaml   # Updated with Dapr
│           ├── frontend-deployment.yaml
│           ├── notification-deployment.yaml  # NEW
│           ├── recurring-deployment.yaml     # NEW
│           └── dapr-components.yaml          # NEW
├── k8s/
│   ├── dapr-pubsub.yaml      # NEW: Redpanda Pub/Sub component
│   ├── dapr-secrets.yaml     # NEW: K8s secrets component
│   └── dapr-subscriptions.yaml # NEW: Event subscriptions
└── .github/
    └── workflows/
        └── deploy-azure.yml  # NEW: CI/CD pipeline
```

**Structure Decision**: Extends existing phase-5 structure with Azure-specific Helm values and Dapr components. GitHub Actions workflow added at repository root.

## Implementation Phases

### Phase 1: Azure Infrastructure Setup (US-1)

**Objective**: Provision AKS cluster and ACR

**Tasks**:
1. Create resource group `todo-rg` in `eastus`
2. Create ACR with Basic SKU
3. Create AKS cluster (2 nodes, Standard_B2s)
4. Attach ACR to AKS
5. Verify cluster with `kubectl get nodes`

**Validation**:
- `az aks show` returns cluster details
- `kubectl get nodes` shows 2 Ready nodes
- Test image push/pull to ACR

### Phase 2: Redpanda Cloud Setup (US-2)

**Objective**: Configure managed Kafka

**Tasks**:
1. Create Redpanda Cloud Serverless cluster
2. Create topics: task-events, reminders, task-updates
3. Create SASL credentials
4. Document bootstrap server URL

**Validation**:
- Topics visible in Redpanda console
- Test connection with kafka-python

### Phase 3: Dapr Installation (US-3)

**Objective**: Install and configure Dapr on AKS

**Tasks**:
1. Install Dapr runtime (`dapr init -k`)
2. Create Pub/Sub component for Redpanda
3. Create Secrets component for K8s secrets
4. Verify sidecar injection works

**Validation**:
- `dapr status -k` shows all components running
- Test pod gets Dapr sidecar injected

### Phase 4: Application Deployment (US-4)

**Objective**: Deploy all services to AKS

**Tasks**:
1. Create Kubernetes namespace `todo`
2. Create app-secrets and kafka-secrets
3. Build and push images to ACR
4. Create Azure-specific Helm values
5. Deploy with `helm upgrade --install`
6. Verify LoadBalancer IP assigned

**Validation**:
- All pods in Running state
- Frontend accessible via external IP
- Backend health check returns 200

### Phase 5: CI/CD Pipeline (US-5)

**Objective**: Automate deployments with GitHub Actions

**Tasks**:
1. Create service principal for GitHub
2. Configure GitHub secrets
3. Create workflow file
4. Test with push to main

**Validation**:
- Workflow triggers on push
- Images built and pushed
- Deployment completes successfully

### Phase 6: Verification & Documentation (US-6)

**Objective**: Validate and document

**Tasks**:
1. Run full testing checklist
2. Set budget alerts
3. Document cleanup commands
4. Create demo video

**Validation**:
- All checklist items pass
- Budget alerts configured
- Cleanup script tested

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Azure credit exhaustion | Deployment stops | Set alerts at $50, $100, $150 |
| ACR build timeout | CI/CD fails | Use smaller base images, cache layers |
| Redpanda connection issues | Events fail | Graceful degradation in backend |
| LoadBalancer IP delay | No external access | Wait with polling, use port-forward as fallback |

## Dependencies

```
Phase 1 (Azure Infra)
    └── Phase 2 (Redpanda) [parallel]
    └── Phase 3 (Dapr)
         └── Phase 4 (Deployment)
              └── Phase 5 (CI/CD)
                   └── Phase 6 (Verification)
```

## Complexity Tracking

No constitution violations detected. Using managed services (AKS, ACR, Redpanda Cloud) minimizes operational complexity.
