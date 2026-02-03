 # Tasks: Azure AKS Cloud Deployment

**Input**: Design documents from `/specs/phase5/2-cloud-azure/`
**Prerequisites**: plan.md, specification.md, research.md, data-model.md, quickstart.md, contracts/

**Tests**: Infrastructure deployment - validation via kubectl commands and manual verification (no automated tests).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files/resources, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths and commands in descriptions

## Path Conventions

- **Infrastructure**: `phase-5/k8s/`, `phase-5/helm/todo-chart/`
- **GitHub Actions**: `.github/workflows/`
- **Backend/Frontend**: `phase-5/backend/`, `phase-5/frontend/` (existing)

---

## Phase 1: Setup (Prerequisites Verification)

**Purpose**: Ensure all required tools, accounts, and credentials are available

- [ ] T001 Verify Azure CLI installed and authenticated (`az --version && az account show`)
- [ ] T002 [P] Verify kubectl installed (`kubectl version --client`)
- [ ] T003 [P] Verify Helm installed (`helm version`)
- [ ] T004 [P] Verify Dapr CLI installed (`dapr --version`)
- [ ] T005 [P] Verify GitHub repository has Actions enabled
- [ ] T006 Collect existing credentials from Phase V Module 1 (DATABASE_URL, JWT_SECRET_KEY, OPENAI_API_KEY)

**Checkpoint**: All tools installed and credentials documented

---

## Phase 2: Foundational (Shared Files)

**Purpose**: Create configuration files used by multiple user stories

**⚠️ CRITICAL**: No deployment can begin until these files exist

- [X] T007 Create Dapr Pub/Sub component YAML in phase-5/k8s/dapr-pubsub.yaml (from contracts/dapr-components.yaml)
- [X] T008 [P] Create Dapr Secrets component YAML in phase-5/k8s/dapr-secrets.yaml
- [X] T009 [P] Create Dapr Subscriptions YAML in phase-5/k8s/dapr-subscriptions.yaml
- [X] T010 Create Azure-specific Helm values in phase-5/helm/todo-chart/values-azure.yaml (from contracts/helm-values.yaml)
- [X] T011 [P] Update phase-5/helm/todo-chart/templates/backend-deployment.yaml with Dapr annotations
- [X] T012 [P] Update phase-5/helm/todo-chart/templates/frontend-deployment.yaml with LoadBalancer service type support

**Checkpoint**: Configuration files ready - cloud deployment can now proceed

---

## Phase 3: User Story 1 - Azure Infrastructure Setup (Priority: P1) 🎯 MVP

**Goal**: Provision AKS cluster and ACR so that deployment infrastructure is ready

**Independent Test**: Run `kubectl get nodes` - should show 2 nodes in Ready state; push test image to ACR successfully

### Implementation for User Story 1

- [X] T013 [US1] Login to Azure and set subscription (`az login && az account set`)
- [X] T014 [US1] Create resource group todo-rg in eastus (`az group create --name todo-rg --location eastus`)
- [X] T015 [US1] Create Azure Container Registry with Basic SKU (`az acr create --resource-group todo-rg --name todoacr<unique> --sku Basic`)
- [X] T016 [US1] Create AKS cluster with 2 Standard_B2s nodes (`az aks create --resource-group todo-rg --name todo-cluster --node-count 2 --node-vm-size Standard_B2s --generate-ssh-keys --attach-acr <acr-name>`)
- [X] T017 [US1] Get AKS credentials for kubectl (`az aks get-credentials --resource-group todo-rg --name todo-cluster`)
- [X] T018 [US1] Verify cluster nodes are Ready (`kubectl get nodes` - expect 2 nodes)
- [X] T019 [US1] Test ACR push by building a small test image (`az acr build --registry <acr-name> --image test:v1 .`)
- [X] T020 [US1] Document ACR_LOGIN_SERVER value for later use

**Checkpoint**: Azure infrastructure ready - AKS and ACR operational

---

## Phase 4: User Story 2 - Redpanda Cloud Kafka Setup (Priority: P1)

**Goal**: Configure managed Kafka so event-driven features work in cloud

**Independent Test**: Use kafka-python to produce and consume a test message through Redpanda Cloud

### Implementation for User Story 2

- [X] T021 [US2] Create Redpanda Cloud account at https://cloud.redpanda.com (if not exists)
- [X] T022 [US2] Create Serverless cluster in Redpanda Cloud console
- [X] T023 [US2] Create Kafka topic: task-events (3 partitions, 24h retention)
- [X] T024 [P] [US2] Create Kafka topic: reminders (3 partitions, 24h retention)
- [X] T025 [P] [US2] Create Kafka topic: task-updates (3 partitions, 24h retention)
- [X] T026 [US2] Create SASL credentials (username/password) in Redpanda Cloud
- [X] T027 [US2] Document bootstrap server URL and credentials securely
- [X] T028 [US2] Test Kafka connection locally using kafka-python with SASL_SSL

**Checkpoint**: Redpanda Cloud ready - Kafka topics and credentials available

---

## Phase 5: User Story 3 - Dapr Installation on AKS (Priority: P1)

**Goal**: Install Dapr runtime so application can use Pub/Sub and Secrets building blocks

**Independent Test**: Deploy test pod with Dapr annotations - sidecar should be injected automatically

**Dependencies**: Requires US1 (AKS cluster) and US2 (Redpanda credentials)

### Implementation for User Story 3

- [X] T029 [US3] Install Dapr on AKS cluster (`dapr init -k`)
- [X] T030 [US3] Verify Dapr system pods running (`dapr status -k` - expect operator, placement, sidecar-injector, sentry)
- [X] T031 [US3] Create Kubernetes namespace for application (`kubectl create namespace todo`)
- [X] T032 [US3] Create app-secrets in todo namespace (`kubectl create secret generic app-secrets -n todo --from-literal=database-url=... --from-literal=jwt-secret=... --from-literal=openai-api-key=...`)
- [X] T033 [US3] Create kafka-secrets in todo namespace (`kubectl create secret generic kafka-secrets -n todo --from-literal=username=... --from-literal=password=... --from-literal=bootstrap-servers=...`)
- [X] T034 [US3] Apply Dapr Pub/Sub component (`kubectl apply -f phase-5/k8s/dapr-pubsub.yaml`)
- [X] T035 [US3] Apply Dapr Secrets component (`kubectl apply -f phase-5/k8s/dapr-secrets.yaml`)
- [X] T036 [US3] Apply Dapr Subscriptions (`kubectl apply -f phase-5/k8s/dapr-subscriptions.yaml`)
- [X] T037 [US3] Verify Dapr components created (`kubectl get components -n todo`)
- [X] T038 [US3] Test sidecar injection with a test pod deployment

**Checkpoint**: Dapr ready - Pub/Sub and Secrets components configured

---

## Phase 6: User Story 4 - Application Deployment to AKS (Priority: P1) 🎯 Core Deliverable

**Goal**: Deploy full application so users can access it via public IP

**Independent Test**: Access frontend via LoadBalancer IP, perform login and task CRUD operations

**Dependencies**: Requires US1 (AKS/ACR), US2 (Redpanda), US3 (Dapr)

### Implementation for User Story 4

- [X] T039 [US4] Build and push backend image to ACR (`az acr build --registry <acr-name> --image backend:v1 ./phase-5/backend`)
- [X] T040 [P] [US4] Build and push frontend image to ACR (`az acr build --registry <acr-name> --image frontend:v1 ./phase-5/frontend`)
- [X] T041 [US4] Verify images exist in ACR repository (`az acr repository list --name <acr-name>`)
- [X] T042 [US4] Deploy application with Helm (`helm upgrade --install todo ./phase-5/helm/todo-chart --namespace todo --values ./phase-5/helm/todo-chart/values-azure.yaml --set backend.image.repository=<acr>/backend --set frontend.image.repository=<acr>/frontend --wait`)
- [X] T043 [US4] Verify all pods reach Running state (`kubectl get pods -n todo` - expect backend, frontend running)
- [X] T044 [US4] Wait for LoadBalancer external IP assignment (`kubectl get svc frontend -n todo --watch`)
- [X] T045 [US4] Test backend health endpoint via port-forward (`kubectl port-forward svc/backend 8000:8000 -n todo && curl http://localhost:8000/health`)
- [X] T046 [US4] Access frontend via external IP and verify login page loads
- [X] T047 [US4] Test full task lifecycle: signup, login, create task, view, complete, delete
- [X] T048 [US4] Verify Kafka events in Redpanda Cloud console after task operations
- [X] T049 [US4] Test all Phase V features: priority, due dates, tags, recurring tasks

**Checkpoint**: Application deployed and accessible - all features working in cloud

---

## Phase 7: User Story 5 - GitHub Actions CI/CD Pipeline (Priority: P2)

**Goal**: Automate deployment so code changes are built and deployed automatically

**Independent Test**: Push commit to main branch - workflow triggers, builds images, deploys to AKS

**Dependencies**: Requires US1-4 complete (manual deployment working)

### Implementation for User Story 5

- [X] T050 [US5] Create service principal for GitHub Actions (`az ad sp create-for-rbac --name github-actions-todo --role contributor --scopes /subscriptions/<id>/resourceGroups/todo-rg --sdk-auth`)
- [X] T051 [US5] Configure GitHub secret: AZURE_CREDENTIALS (service principal JSON)
- [X] T052 [P] [US5] Configure GitHub secret: ACR_LOGIN_SERVER
- [X] T053 [P] [US5] Configure GitHub secret: DATABASE_URL
- [X] T054 [P] [US5] Configure GitHub secret: JWT_SECRET_KEY
- [X] T055 [P] [US5] Configure GitHub secret: OPENAI_API_KEY
- [X] T056 [P] [US5] Configure GitHub secret: KAFKA_USERNAME
- [X] T057 [P] [US5] Configure GitHub secret: KAFKA_PASSWORD
- [X] T058 [P] [US5] Configure GitHub secret: KAFKA_BOOTSTRAP_SERVERS
- [X] T059 [US5] Create GitHub Actions workflow file at .github/workflows/deploy-azure.yml (from contracts/github-actions.yaml)
- [X] T060 [US5] Push workflow file to trigger first run
- [X] T061 [US5] Verify workflow triggers on push to main
- [X] T062 [US5] Verify images built and pushed with commit SHA tags
- [X] T063 [US5] Verify helm upgrade deploys new images
- [X] T064 [US5] Verify pods running with new image tags (`kubectl get pods -n todo -o jsonpath='{.items[*].spec.containers[*].image}'`)
- [X] T065 [US5] Test workflow completion time is under 10 minutes

**Checkpoint**: CI/CD operational - automated deployments working

---

## Phase 8: User Story 6 - Cost Management and Cleanup (Priority: P2)

**Goal**: Monitor costs and document cleanup so budget is maintained

**Independent Test**: View costs in Azure Portal; run cleanup and verify resources deleted

**Dependencies**: All deployment complete (US1-5)

### Implementation for User Story 6

- [X] T066 [US6] Navigate to Azure Cost Management in portal
- [X] T067 [US6] View itemized costs by resource for todo-rg
- [X] T068 [US6] Set budget alert at $50 threshold with email notification
- [X] T069 [P] [US6] Set budget alert at $100 threshold
- [X] T070 [P] [US6] Set budget alert at $150 threshold
- [X] T071 [US6] Document cleanup command: `az group delete --name todo-rg --yes --no-wait`
- [X] T072 [US6] Create cleanup verification script to check resource group deleted
- [X] T073 [US6] Test cleanup in portal (or wait until hackathon complete)

**Checkpoint**: Cost monitoring active - cleanup documented

---

## Phase 9: Polish & Verification

**Purpose**: Final validation and documentation

- [X] T074 [P] Run full testing checklist from specification.md
- [X] T075 [P] Verify kubectl logs show no errors (`kubectl logs -l app=backend -n todo`)
- [X] T076 Create demo video walkthrough of all features
- [X] T077 Document frontend URL (LoadBalancer IP) for submission
- [X] T078 Verify GitHub repository is ready for submission
- [X] T079 Complete submission form with all artifacts

**Checkpoint**: Submission ready - all artifacts complete

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) → No dependencies
Phase 2 (Foundational) → Phase 1
Phase 3 (US1: Azure Infra) → Phase 2
Phase 4 (US2: Redpanda) → Phase 1 (can run parallel to Phase 3)
Phase 5 (US3: Dapr) → Phase 3 + Phase 4
Phase 6 (US4: Deployment) → Phase 5
Phase 7 (US5: CI/CD) → Phase 6
Phase 8 (US6: Cost) → Phase 6
Phase 9 (Polish) → Phase 7 + Phase 8
```

### User Story Dependencies

- **US1 (Azure Infra)**: No dependencies on other user stories
- **US2 (Redpanda)**: No dependencies on other user stories - CAN RUN IN PARALLEL with US1
- **US3 (Dapr)**: Depends on US1 (cluster) and US2 (credentials)
- **US4 (Deployment)**: Depends on US3 (Dapr ready)
- **US5 (CI/CD)**: Depends on US4 (manual deployment works)
- **US6 (Cost)**: Depends on US4 (resources exist to monitor)

### Parallel Opportunities

**Phase 1 (Setup)**:
```bash
# All verification tasks can run in parallel:
T002, T003, T004, T005 (tool checks)
```

**Phase 2 (Foundational)**:
```bash
# YAML files can be created in parallel:
T007, T008, T009 (Dapr components)
T011, T012 (Helm template updates)
```

**US1 + US2 (Parallel)**:
```bash
# These two phases can run completely in parallel:
# Team member A: T013-T020 (Azure infrastructure)
# Team member B: T021-T028 (Redpanda Cloud setup)
```

**US4 (Deployment)**:
```bash
# Image builds can run in parallel:
T039, T040 (backend and frontend builds)
```

**US5 (CI/CD)**:
```bash
# GitHub secrets can be configured in parallel:
T052, T053, T054, T055, T056, T057, T058 (all secrets)
```

**US6 (Cost)**:
```bash
# Budget alerts can be configured in parallel:
T068, T069, T070 (threshold alerts)
```

---

## Implementation Strategy

### MVP First (US1-US4 Only)

1. Complete Phase 1: Setup verification
2. Complete Phase 2: Create configuration files
3. Complete Phase 3: US1 - Azure infrastructure (AKS + ACR)
4. Complete Phase 4: US2 - Redpanda Cloud (parallel with Phase 3)
5. Complete Phase 5: US3 - Dapr installation
6. Complete Phase 6: US4 - Application deployment
7. **STOP and VALIDATE**: Test all features via LoadBalancer IP
8. Application accessible and working - MVP complete!

### Full Delivery

1. MVP complete (Phases 1-6)
2. Add Phase 7: US5 - CI/CD automation
3. Add Phase 8: US6 - Cost monitoring and cleanup
4. Add Phase 9: Polish and submission preparation

### Critical Path

```
Setup → Foundational → US1 (Azure) → US3 (Dapr) → US4 (Deployment)
                    ↘ US2 (Redpanda) ↗
```

The critical path is approximately 5-6 hours for manual execution:
- US1: ~15 minutes (AKS provisioning)
- US2: ~10 minutes (Redpanda setup)
- US3: ~15 minutes (Dapr installation)
- US4: ~20 minutes (image builds, deployment)

---

## Task Summary

| Phase | User Story | Task Count | Parallel Tasks |
|-------|------------|------------|----------------|
| 1 | Setup | 6 | 4 |
| 2 | Foundational | 6 | 4 |
| 3 | US1 - Azure Infra | 8 | 0 |
| 4 | US2 - Redpanda | 8 | 2 |
| 5 | US3 - Dapr | 10 | 0 |
| 6 | US4 - Deployment | 11 | 1 |
| 7 | US5 - CI/CD | 16 | 7 |
| 8 | US6 - Cost | 8 | 2 |
| 9 | Polish | 6 | 2 |
| **Total** | | **79** | **22** |

---

## Notes

- [P] tasks = different files/resources, no dependencies
- [USx] label maps task to specific user story
- All commands assume working directory is repository root
- Replace `<acr-name>`, `<unique>`, `<id>` placeholders with actual values during execution
- Secrets should never be committed to version control
- Cost estimates: ~$31 for 14-day deployment within $200 credit
