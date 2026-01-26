# Kubernetes Checklist: Phase IV Module 1

## Part B: Kubernetes Deployment

### US-4: Minikube Setup
- [ ] Minikube installed and configured
- [ ] Cluster starts successfully with `minikube start`
- [ ] `kubectl get nodes` shows node(s) as Ready
- [ ] Docker environment configured with `eval $(minikube docker-env)`
- [ ] Images can be built directly to Minikube registry

### US-5: Kubernetes Manifests (5 files required)
- [X] k8s/backend-deployment.yaml created
  - [X] 2 replicas configured
  - [X] Resource requests/limits set (256Mi/200m request, 512Mi/500m limit)
  - [X] Liveness probe configured
  - [X] Readiness probe configured
  - [X] Environment variables from ConfigMap/Secret
- [X] k8s/backend-service.yaml created
  - [X] ClusterIP type
  - [X] Port 80 -> 8000
- [X] k8s/frontend-deployment.yaml created
  - [X] 2 replicas configured
  - [X] Resource requests/limits set (128Mi/100m request, 256Mi/200m limit)
  - [X] Liveness probe configured
  - [X] Readiness probe configured
  - [X] Environment variables from ConfigMap
- [X] k8s/frontend-service.yaml created
  - [X] NodePort type
  - [X] Port 80 -> 3000
  - [X] NodePort 30000
- [X] k8s/secrets.yaml created
  - [X] ConfigMap with non-sensitive config
  - [X] Secret with DATABASE_URL, API keys (base64 encoded)

### US-6: Deploy with kubectl
- [ ] `kubectl apply -f k8s/` succeeds without errors
- [ ] All pods reach Running state
- [ ] Backend pods: 2 replicas running
- [ ] Frontend pods: 2 replicas running
- [ ] `minikube service frontend-service` opens application
- [ ] All Phase III features work in K8s deployment
- [ ] Scaling works: `kubectl scale deployment backend-deployment --replicas=3`

## Manifest Validation

- [ ] `kubectl apply -f k8s/ --dry-run=client` passes
- [ ] No syntax errors in YAML files
- [X] Labels and selectors match correctly
- [X] Service selectors match pod labels
