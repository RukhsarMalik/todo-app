# Feature Specification: Azure AKS Cloud Deployment

**Feature Branch**: `008-azure-aks-deployment`
**Created**: 2026-02-03
**Status**: Draft
**Input**: Phase V Module 2: Cloud Deployment on Azure AKS with CI/CD automation

## Overview

Deploy the Phase V Todo application (with all advanced features) to Azure Kubernetes Service (AKS) with full automation via GitHub Actions CI/CD pipeline. The deployment leverages Azure Container Registry for images, Redpanda Cloud for managed Kafka, and Dapr for event-driven architecture.

### Dependencies

- Module 1 complete (all Phase V features working on Minikube)
- Azure subscription with $200 credit
- GitHub repository with Actions enabled
- Redpanda Cloud account (free tier)

### Scope

**INCLUDED:**
- Azure AKS cluster provisioning and configuration
- Azure Container Registry (ACR) for Docker image storage
- Helm-based deployment to AKS
- Redpanda Cloud Kafka integration
- Dapr installation and configuration on AKS
- GitHub Actions CI/CD pipeline
- Basic monitoring and logging via kubectl
- Cost management and cleanup procedures

**NOT INCLUDED:**
- Advanced monitoring (Prometheus/Grafana stack)
- Custom domain and SSL/TLS certificates
- Auto-scaling policies (HPA/VPA)
- Multi-region deployment
- Disaster recovery configuration

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Azure Infrastructure Setup (Priority: P1)

As a DevOps engineer, I need to provision Azure infrastructure (AKS cluster, ACR, networking) so that I have a cloud environment ready for application deployment.

**Why this priority**: Without infrastructure, no deployment is possible. This is the foundational requirement.

**Independent Test**: Can be fully tested by verifying cluster accessibility via kubectl commands and ACR image push/pull operations.

**Acceptance Scenarios**:

1. **Given** Azure CLI is installed and authenticated, **When** I run the AKS creation commands, **Then** a 2-node Kubernetes cluster is provisioned within 10 minutes
2. **Given** AKS cluster exists, **When** I run `kubectl get nodes`, **Then** I see 2 healthy nodes in Ready state
3. **Given** ACR is created, **When** I push a test image, **Then** the image appears in the ACR repository list
4. **Given** ACR is attached to AKS, **When** I deploy a pod referencing ACR image, **Then** the pod successfully pulls the image without explicit credentials

---

### User Story 2 - Redpanda Cloud Kafka Setup (Priority: P1)

As a DevOps engineer, I need to configure Redpanda Cloud Kafka so that the application's event-driven features (notifications, recurring tasks) function correctly in the cloud.

**Why this priority**: Event architecture is core to Phase V features. Without Kafka, notifications and recurring tasks fail.

**Independent Test**: Can be fully tested by producing and consuming a test message via Kafka client tools.

**Acceptance Scenarios**:

1. **Given** Redpanda Cloud account exists, **When** I create a Serverless cluster, **Then** I receive bootstrap server URL and can create credentials
2. **Given** Redpanda cluster is created, **When** I create topics (task-events, reminders), **Then** topics appear in Redpanda console
3. **Given** credentials are configured, **When** I test connection with kafka-python, **Then** connection succeeds and message can be published

---

### User Story 3 - Dapr Installation on AKS (Priority: P1)

As a DevOps engineer, I need to install and configure Dapr on AKS so that the application can use Pub/Sub and other Dapr building blocks.

**Why this priority**: Dapr provides the event publishing abstraction. Backend depends on Dapr sidecar for Kafka communication.

**Independent Test**: Can be fully tested by deploying a test pod with Dapr annotations and verifying sidecar injection.

**Acceptance Scenarios**:

1. **Given** AKS cluster exists, **When** I run `dapr init -k`, **Then** Dapr system pods are running in dapr-system namespace
2. **Given** Dapr is installed, **When** I apply Pub/Sub component for Redpanda, **Then** component appears in `kubectl get components`
3. **Given** Dapr components exist, **When** I deploy a pod with Dapr annotations, **Then** sidecar container is automatically injected

---

### User Story 4 - Application Deployment to AKS (Priority: P1)

As a DevOps engineer, I need to deploy the Todo application (backend, frontend, microservices) to AKS so that users can access the application via public IP.

**Why this priority**: This is the core deliverable - running application in the cloud.

**Independent Test**: Can be fully tested by accessing frontend via LoadBalancer IP and performing CRUD operations.

**Acceptance Scenarios**:

1. **Given** images are in ACR, **When** I run helm install with Azure values, **Then** all pods reach Running state within 5 minutes
2. **Given** services are deployed, **When** I check LoadBalancer service, **Then** external IP is assigned to frontend
3. **Given** application is running, **When** I access frontend via external IP, **Then** login page loads successfully
4. **Given** backend is running, **When** I call /health endpoint, **Then** response returns {"status": "ok"}
5. **Given** user is logged in, **When** I create a task with due date, **Then** task is created and event is published to Kafka

---

### User Story 5 - GitHub Actions CI/CD Pipeline (Priority: P2)

As a developer, I need automated deployment via GitHub Actions so that code changes are automatically built, tested, and deployed to AKS.

**Why this priority**: Automation improves deployment speed and reliability but can be done after manual deployment works.

**Independent Test**: Can be fully tested by pushing a commit to main branch and verifying deployment completes.

**Acceptance Scenarios**:

1. **Given** GitHub secrets are configured, **When** I push to main branch, **Then** workflow triggers automatically
2. **Given** workflow is running, **When** build step executes, **Then** images are built and pushed to ACR with commit SHA tag
3. **Given** images are pushed, **When** deploy step executes, **Then** helm upgrade applies new images to AKS
4. **Given** deployment completes, **When** I check pod images, **Then** pods are running with new image tags
5. **Given** deployment fails, **When** workflow fails, **Then** rollback preserves previous working version

---

### User Story 6 - Cost Management and Cleanup (Priority: P2)

As a project owner, I need visibility into Azure costs and documented cleanup procedures so that I stay within budget and properly decommission resources after submission.

**Why this priority**: Critical for hackathon budget compliance but not blocking deployment functionality.

**Independent Test**: Can be fully tested by checking Azure Cost Management and running cleanup commands in non-production subscription.

**Acceptance Scenarios**:

1. **Given** Azure resources exist, **When** I check Cost Management, **Then** I see itemized costs by resource
2. **Given** budget alerts are set, **When** spend reaches threshold, **Then** email notification is sent
3. **Given** hackathon is complete, **When** I run cleanup commands, **Then** all resources are deleted and no charges continue

---

### Edge Cases

- What happens when AKS node fails? Kubernetes reschedules pods to healthy node.
- What happens when ACR is temporarily unavailable? Existing pods continue running; new deployments fail until ACR recovers.
- What happens when Redpanda Cloud has connectivity issues? Backend graceful degradation - CRUD operations succeed, events queue locally.
- What happens when GitHub Actions secret expires? Deployment fails with auth error; requires secret rotation.
- What happens when Azure credit is exhausted? Services stop; cleanup cannot proceed via CLI.

---

## Requirements *(mandatory)*

### Functional Requirements

#### Part A: Azure Infrastructure

- **FR-001**: System MUST provision an AKS cluster with 2 worker nodes using cost-effective VM sizes (Standard_B2s or equivalent)
- **FR-002**: System MUST create an Azure Container Registry (ACR) with Basic SKU
- **FR-003**: System MUST attach ACR to AKS for seamless image pulls without explicit credentials
- **FR-004**: System MUST generate and store SSH keys for cluster access
- **FR-005**: System MUST use managed identity for AKS authentication

#### Part B: Redpanda Cloud Kafka

- **FR-006**: System MUST create Kafka topics: task-events, reminders, task-updates
- **FR-007**: System MUST configure SASL authentication for Kafka connections
- **FR-008**: System MUST document bootstrap server URL and credentials securely

#### Part C: Dapr Configuration

- **FR-009**: System MUST install Dapr runtime on AKS cluster
- **FR-010**: System MUST configure Pub/Sub component for Redpanda Cloud Kafka
- **FR-011**: System MUST configure Secrets component for Kubernetes secrets
- **FR-012**: System MUST enable sidecar injection for application pods

#### Part D: Application Deployment

- **FR-013**: System MUST build and push Docker images (backend, frontend) to ACR
- **FR-014**: System MUST deploy application using Helm charts with Azure-specific values
- **FR-015**: System MUST expose frontend via LoadBalancer with public IP
- **FR-016**: System MUST configure backend as ClusterIP (internal only)
- **FR-017**: System MUST inject environment variables from Kubernetes secrets
- **FR-018**: System MUST configure liveness and readiness probes for all pods
- **FR-019**: System MUST maintain 2 replicas for frontend and backend services

#### Part E: CI/CD Pipeline

- **FR-020**: System MUST trigger deployment on push to main branch
- **FR-021**: System MUST build images using ACR build (no local Docker required)
- **FR-022**: System MUST tag images with git commit SHA for traceability
- **FR-023**: System MUST perform helm upgrade with --wait flag for rollout verification
- **FR-024**: System MUST preserve previous deployment on failure (no automatic rollback)
- **FR-025**: System MUST store Azure credentials, ACR credentials, and application secrets as GitHub secrets

#### Part F: Monitoring and Management

- **FR-026**: System MUST provide kubectl-based log access for all pods
- **FR-027**: System MUST configure /health endpoints for all services
- **FR-028**: System MUST document cleanup commands for all Azure resources
- **FR-029**: System MUST set budget alerts at $50, $100, and $150 thresholds

### Key Entities

- **AKS Cluster**: Kubernetes control plane and worker nodes; manages pod scheduling and networking
- **ACR Repository**: Docker image storage; stores backend:tag and frontend:tag images
- **Dapr Component**: Configuration for building blocks (Pub/Sub, Secrets); connects to external services
- **Kafka Topic**: Message channel in Redpanda; stores task events and reminders
- **Kubernetes Secret**: Encrypted configuration; stores DATABASE_URL, JWT_SECRET, Kafka credentials
- **LoadBalancer Service**: Azure Load Balancer; provides external IP for frontend access
- **GitHub Workflow**: CI/CD definition; orchestrates build and deploy steps

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: AKS cluster is provisioned and accessible within 15 minutes of running creation command
- **SC-002**: All application pods (backend, frontend, notification-service, recurring-service) reach Running state within 5 minutes of helm install
- **SC-003**: Frontend is accessible via public IP address and login page loads successfully
- **SC-004**: User can complete full task lifecycle (create, view, complete, delete) through cloud-hosted application
- **SC-005**: Task events are successfully published to Redpanda Cloud (verified via Redpanda console)
- **SC-006**: GitHub Actions deployment completes end-to-end in under 10 minutes
- **SC-007**: All Phase V features (priority, due dates, tags, recurring tasks, notifications) function correctly in cloud environment
- **SC-008**: Azure resource costs remain under $50 for 14-day hackathon period
- **SC-009**: All resources can be deleted via documented cleanup commands with zero residual charges
- **SC-010**: Demo video successfully records complete feature walkthrough

---

## Assumptions

1. Azure subscription has $200 free credit available
2. Neon PostgreSQL database from Phase V Module 1 remains accessible
3. GitHub repository has Actions enabled and sufficient minutes
4. Redpanda Cloud free tier provides adequate Kafka capacity
5. Network policies allow outbound connections to Azure, Redpanda, and Neon services
6. Team has Azure CLI, kubectl, and helm installed locally
7. Docker images from Phase V Module 1 are compatible with Azure deployment

---

## Cost Estimates

| Resource | Monthly Cost | 14-Day Cost |
|----------|-------------|-------------|
| AKS (2 × Standard_B2s) | ~$30 | ~$15 |
| Load Balancer | ~$20 | ~$10 |
| Public IP | ~$3 | ~$1.50 |
| Storage | ~$5 | ~$2.50 |
| ACR Basic | ~$5 | ~$2.50 |
| **Total** | ~$63/month | **~$31** |

Budget allocation: $31 estimated from $200 credit (15.5% utilization)

---

## Testing Checklist

- [ ] Frontend accessible at http://<external-ip>
- [ ] Backend health check returns 200 OK
- [ ] User signup and login working
- [ ] Task CRUD operations functional
- [ ] Priority and due date features working
- [ ] Tags can be created and assigned
- [ ] Recurring tasks create next occurrence on completion
- [ ] Kafka events visible in Redpanda console
- [ ] GitHub Actions workflow succeeds on push
- [ ] kubectl logs show no errors
- [ ] Cost under budget threshold

---

## Submission Artifacts

- GitHub repository URL with all code
- Deployed frontend URL (Azure LoadBalancer IP)
- Demo video URL (YouTube/Loom)
- Submission form completion
