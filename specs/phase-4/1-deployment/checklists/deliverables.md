# Deliverables Checklist: Phase IV Module 1

## Required Files

### Dockerfiles
- [X] phase-4/backend/Dockerfile
- [X] phase-4/frontend/Dockerfile
- [X] phase-4/backend/.dockerignore
- [X] phase-4/frontend/.dockerignore

### Docker Compose
- [X] phase-4/docker-compose.yml

### Kubernetes Manifests (5 files)
- [X] phase-4/k8s/backend-deployment.yaml
- [X] phase-4/k8s/backend-service.yaml
- [X] phase-4/k8s/frontend-deployment.yaml
- [X] phase-4/k8s/frontend-service.yaml
- [X] phase-4/k8s/secrets.yaml

### Helm Chart
- [X] phase-4/helm/todo-chart/Chart.yaml
- [X] phase-4/helm/todo-chart/values.yaml
- [X] phase-4/helm/todo-chart/templates/backend-deployment.yaml
- [X] phase-4/helm/todo-chart/templates/backend-service.yaml
- [X] phase-4/helm/todo-chart/templates/frontend-deployment.yaml
- [X] phase-4/helm/todo-chart/templates/frontend-service.yaml
- [X] phase-4/helm/todo-chart/templates/secrets.yaml
- [X] phase-4/helm/todo-chart/templates/configmap.yaml

### Documentation
- [X] phase-4/DEPLOYMENT.md with deployment commands

## File Structure Verification

```
phase-4/
├── backend/
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── Dockerfile
│   └── .dockerignore
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
│       └── templates/
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── frontend-deployment.yaml
│           ├── frontend-service.yaml
│           ├── secrets.yaml
│           └── configmap.yaml
└── DEPLOYMENT.md
```

## Three-Step Deployment Verification

### Step 1: Docker (Local)
- [ ] `docker build -t todo-backend ./phase-4/backend` works
- [ ] `docker build -t todo-frontend ./phase-4/frontend` works
- [ ] `docker-compose -f phase-4/docker-compose.yml up` works
- [ ] Application accessible at http://localhost:3000

### Step 2: Kubernetes (Plain)
- [ ] `minikube start` works
- [ ] Images built to Minikube registry
- [ ] `kubectl apply -f phase-4/k8s/` works
- [ ] `minikube service frontend-service` opens app

### Step 3: Helm (Managed)
- [ ] `helm install todo ./phase-4/helm/todo-chart` works
- [ ] `kubectl get pods` shows all pods running
- [ ] `helm upgrade todo ./phase-4/helm/todo-chart` works
- [ ] `helm uninstall todo` cleans up all resources
