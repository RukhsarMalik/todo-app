# Research: Azure AKS Cloud Deployment

**Feature**: Phase V Module 2 - Azure Cloud Deployment
**Date**: 2026-02-03
**Status**: Complete

## Research Questions

### RQ-1: Azure AKS Configuration for Todo Application

**Context**: Deploying a containerized Node.js/Python application with 2 microservices

**Decision**: Use Standard_B2s VM size with 2 nodes

**Rationale**:
- Standard_B2s: 2 vCPUs, 4GB RAM - sufficient for dev/demo workload
- 2 nodes provide basic high availability
- Cost-effective at ~$30/month
- Can scale up later if needed

**Alternatives Considered**:
| Option | Cost | Reason Rejected |
|--------|------|-----------------|
| Standard_D2s_v3 | ~$70/month | Overkill for hackathon demo |
| Single node | ~$15/month | No redundancy, single point of failure |
| AKS Free tier | Free control plane | Selected - provides free cluster management |

---

### RQ-2: Container Registry Strategy

**Context**: Need to store Docker images for backend and frontend services

**Decision**: Use Azure Container Registry (ACR) Basic tier

**Rationale**:
- ACR integrates natively with AKS (no credential management)
- Basic tier: 10GB storage, sufficient for demo
- ~$5/month cost
- Can attach ACR to AKS for seamless pulls

**Alternatives Considered**:
| Option | Cost | Reason Rejected |
|--------|------|-----------------|
| Docker Hub | Free/Pro | Rate limits, requires image pull secrets |
| GitHub Container Registry | Free | Requires additional credential setup |
| ACR Standard | ~$20/month | More storage than needed |

---

### RQ-3: Kafka/Event Streaming in Cloud

**Context**: Phase V uses Kafka for event-driven architecture

**Decision**: Use Redpanda Cloud Serverless (free tier)

**Rationale**:
- Free tier: 1GB storage, 50MB/s throughput
- Kafka-compatible API (no code changes)
- Managed service (no operator installation)
- SASL authentication for security

**Alternatives Considered**:
| Option | Cost | Reason Rejected |
|--------|------|-----------------|
| Confluent Cloud | Pay-as-go | More complex pricing, overkill |
| Azure Event Hubs (Kafka) | ~$11/month | Additional Azure cost |
| Self-hosted Strimzi on AKS | Free (compute) | Operational overhead, resource usage |

---

### RQ-4: Dapr Configuration for Cloud

**Context**: Dapr provides Pub/Sub, State, and Secrets abstractions

**Decision**: Deploy Dapr via CLI with cloud-optimized components

**Rationale**:
- `dapr init -k` installs Dapr on any K8s cluster
- Reconfigure Pub/Sub component for Redpanda (same Kafka API)
- Use Kubernetes secrets for secret storage
- State store: Neon PostgreSQL (existing database)

**Configuration Changes from Minikube**:
| Component | Minikube | Azure AKS |
|-----------|----------|-----------|
| Pub/Sub broker | localhost:9092 | seed-xxx.redpanda.com:9092 |
| Auth | None | SASL_SSL + username/password |
| Secrets | K8s secrets | K8s secrets (same) |
| State | Redis | Neon PostgreSQL (same) |

---

### RQ-5: CI/CD Pipeline Architecture

**Context**: Need automated build and deployment on push to main

**Decision**: GitHub Actions with ACR build and helm upgrade

**Rationale**:
- GitHub Actions: Free for public repos, integrated with GitHub
- ACR Tasks: Build images in Azure (no local Docker required)
- helm upgrade --install: Idempotent deployment
- Commit SHA tagging for traceability

**Workflow Steps**:
1. Checkout code
2. Azure Login (service principal)
3. Build backend image (az acr build)
4. Build frontend image (az acr build)
5. Get AKS credentials
6. Helm upgrade with new tags
7. Verify rollout status

---

### RQ-6: Networking and External Access

**Context**: Frontend needs public access, backend internal only

**Decision**: LoadBalancer for frontend, ClusterIP for backend

**Rationale**:
- Azure LoadBalancer: ~$20/month, provides public IP
- Frontend: Public internet access via LoadBalancer
- Backend: Internal only (ClusterIP), accessed via service name
- CORS configured for LoadBalancer IP

**Architecture**:
```
Internet → LoadBalancer (frontend:80) → Frontend Pods
                ↓
         Frontend → ClusterIP (backend:8000) → Backend Pods
                                    ↓
                              Neon PostgreSQL (external)
                              Redpanda Cloud (external)
```

---

### RQ-7: Secret Management

**Context**: Multiple sensitive values (DATABASE_URL, JWT_SECRET, Kafka credentials)

**Decision**: Kubernetes Secrets with GitHub Secrets for CI/CD

**Rationale**:
- K8s Secrets: Native, no additional cost
- Base64 encoded, mounted as env vars
- GitHub Secrets: Secure storage for CI/CD variables
- AZURE_CREDENTIALS: Service principal JSON for az login

**Secret Distribution**:
| Secret | Storage | Used By |
|--------|---------|---------|
| DATABASE_URL | K8s Secret | Backend |
| JWT_SECRET_KEY | K8s Secret | Backend |
| OPENAI_API_KEY | K8s Secret | Backend |
| KAFKA_USERNAME | K8s Secret | Backend, Dapr |
| KAFKA_PASSWORD | K8s Secret | Backend, Dapr |
| AZURE_CREDENTIALS | GitHub Secret | CI/CD |
| ACR_CREDENTIALS | GitHub Secret | CI/CD |

---

### RQ-8: Cost Optimization

**Context**: Must stay within $200 Azure credit for 14-day hackathon

**Decision**: Minimal resources with documented cleanup

**Cost Breakdown**:
| Resource | Monthly | 14-Day |
|----------|---------|--------|
| AKS (2 × B2s) | $30 | $15 |
| Load Balancer | $20 | $10 |
| Public IP | $3 | $1.50 |
| Storage | $5 | $2.50 |
| ACR Basic | $5 | $2.50 |
| **Total** | $63 | **~$31** |

**Budget Alerts**: Set at $50, $100, $150 via Azure Portal

**Cleanup**: All resources deletable via `az group delete --name todo-rg`

---

## Summary of Decisions

| Area | Decision | Key Reason |
|------|----------|------------|
| Compute | AKS 2-node Standard_B2s | Cost/performance balance |
| Registry | ACR Basic | Native AKS integration |
| Events | Redpanda Cloud Serverless | Free tier, Kafka-compatible |
| Runtime | Dapr on AKS | Existing Phase V integration |
| CI/CD | GitHub Actions | Free, integrated |
| Frontend Access | LoadBalancer | Public IP |
| Backend Access | ClusterIP | Internal only |
| Secrets | K8s Secrets + GitHub Secrets | Native, no cost |
| Budget | ~$31 for 14 days | Within $200 credit |

## Unresolved Items

None - all technical decisions finalized.

## References

- [AKS Documentation](https://docs.microsoft.com/en-us/azure/aks/)
- [Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/)
- [Redpanda Cloud](https://docs.redpanda.com/docs/deploy/deployment-option/cloud/)
- [Dapr on Kubernetes](https://docs.dapr.io/operations/hosting/kubernetes/)
- [GitHub Actions Azure](https://docs.github.com/en/actions/deployment/deploying-to-your-cloud-provider/deploying-to-azure)
