# Quickstart Guide: Phase IV Module 1 - Containerization & Kubernetes Deployment

## Overview
This guide will help you containerize the Todo application and deploy it to a local Kubernetes cluster using Minikube and Helm.

## Three-Step Deployment Process

### Step 1: Docker (Local)
```bash
docker build -t todo-backend ./phase-4/backend
docker build -t todo-frontend ./phase-4/frontend
docker-compose up
# Test: http://localhost:3000
```

### Step 2: Kubernetes (Plain)
```bash
minikube start
eval $(minikube docker-env)
docker build -t todo-backend ./phase-4/backend
docker build -t todo-frontend ./phase-4/frontend
kubectl apply -f k8s/
minikube service frontend-service
# Test: http://192.168.49.2:30000
```

### Step 3: Helm (Managed)
```bash
helm install todo ./helm/todo-chart
kubectl get pods
minikube service todo-frontend
# Test: Same URL as Step 2
```

## File Structure
```
phase-4/
├── backend/
│   └── Dockerfile
├── frontend/
│   └── Dockerfile
├── docker-compose.yml
├── k8s/
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   └── secrets.yaml
└── helm/
    └── todo-chart/
        ├── Chart.yaml
        ├── values.yaml
        └── templates/
            ├── backend-deployment.yaml
            ├── backend-service.yaml
            ├── frontend-deployment.yaml
            ├── frontend-service.yaml
            ├── secrets.yaml
            └── configmap.yaml
```

## Prerequisites
- Docker Desktop installed and running
- Minikube installed and configured
- kubectl installed and configured
- Helm 3.x installed
- Git (for cloning/configuring)

## Step 1: Prepare Your Environment

### Verify Prerequisites
```bash
# Check Docker
docker --version
docker ps

# Check kubectl
kubectl version --client

# Check Helm
helm version

# Check Minikube
minikube version
```

### Start Minikube Cluster
```bash
# Start a local Kubernetes cluster
minikube start

# Verify cluster is running
kubectl cluster-info

# Enable ingress addon (optional, for advanced routing)
minikube addons enable ingress
```

## Step 2: Containerize the Application

### Backend Dockerfile
Create `phase-4/backend/Dockerfile`:

```dockerfile
# Build stage
FROM python:3.13-slim as builder
WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.13-slim
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY . .

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile
Create `phase-4/frontend/Dockerfile`:

```dockerfile
# Build stage
FROM node:20-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000

CMD ["node", "server.js"]
```

### Build Docker Images
```bash
# Navigate to backend directory
cd backend

# Build backend image
docker build -t todo-backend:latest .

# Navigate to frontend directory
cd ../frontend

# Build frontend image
docker build -t todo-frontend:latest .

# Verify images were created
docker images | grep todo-
```

## Step 3: Test with Docker Compose (Optional)
Create `docker-compose.yml` for local testing:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/todo_db
      - FRONTEND_URL=http://localhost:3000
    depends_on:
      - db
    networks:
      - app-network

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    networks:
      - app-network

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: todo_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

Test the compose setup:
```bash
docker-compose up
```

## Step 4: Deploy to Kubernetes with kubectl

### Create Kubernetes Manifests (5 files)

#### 1. Backend Deployment
Create `k8s/backend-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: todo-backend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database_url
        - name: FRONTEND_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: frontend_url
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### 2. Backend Service
Create `k8s/backend-service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
```

#### 3. Frontend Deployment
Create `k8s/frontend-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: todo-frontend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: backend_url
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### 4. Frontend Service
Create `k8s/frontend-service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  selector:
    app: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
      nodePort: 30000
  type: NodePort
```

#### 5. Secrets (and ConfigMap)
Create `k8s/secrets.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  frontend_url: "http://localhost:30000"
  backend_url: "http://backend-service:80"
---
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  database_url: cG9zdGdyZXNxbDovL3VzZXI6cGFzc3dvcmRAZGI6NTQzMi90b2RvX2Ri  # Base64 encoded
```

### Apply Kubernetes Manifests
```bash
# Apply all manifests at once
kubectl apply -f k8s/

# Or apply individually in order
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml

# Check deployment status
kubectl get pods
kubectl get services

# Access the application
minikube service frontend-service
```

## Step 5: Deploy with Helm

### Create Helm Chart Structure
```bash
# Create single Helm chart directory for the entire application
mkdir -p helm/todo-chart/templates
```

### Helm Chart Files
Create `helm/todo-chart/Chart.yaml`:

```yaml
apiVersion: v2
name: todo-chart
description: Todo Application - Full Stack Deployment (Backend + Frontend)
type: application
version: 1.0.0
appVersion: "1.0.0"
```

Create `helm/todo-chart/values.yaml`:

```yaml
# Backend configuration
backend:
  replicaCount: 2
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 80
    targetPort: 8000
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 200m
      memory: 256Mi

# Frontend configuration
frontend:
  replicaCount: 2
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: NodePort
    port: 80
    targetPort: 3000
    nodePort: 30000
  resources:
    limits:
      cpu: 200m
      memory: 256Mi
    requests:
      cpu: 100m
      memory: 128Mi

# Secrets (base64 encoded values should be provided)
secrets:
  databaseUrl: ""
  jwtSecret: ""
  openaiApiKey: ""

# ConfigMap values
config:
  frontendUrl: "http://localhost:30000"
  backendUrl: "http://backend-service:80"
```

Create `helm/todo-chart/templates/backend-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-backend
  labels:
    app: backend
    release: {{ .Release.Name }}
spec:
  replicas: {{ .Values.backend.replicaCount }}
  selector:
    matchLabels:
      app: backend
      release: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app: backend
        release: {{ .Release.Name }}
    spec:
      containers:
        - name: backend
          image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}"
          imagePullPolicy: {{ .Values.backend.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.backend.service.targetPort }}
              protocol: TCP
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: {{ .Release.Name }}-secrets
                  key: database_url
            - name: FRONTEND_URL
              valueFrom:
                configMapKeyRef:
                  name: {{ .Release.Name }}-config
                  key: frontend_url
          resources:
            {{- toYaml .Values.backend.resources | nindent 12 }}
          livenessProbe:
            httpGet:
              path: /health
              port: {{ .Values.backend.service.targetPort }}
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: {{ .Values.backend.service.targetPort }}
            initialDelaySeconds: 5
            periodSeconds: 5
```

Create `helm/todo-chart/templates/backend-service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-backend
  labels:
    app: backend
    release: {{ .Release.Name }}
spec:
  type: {{ .Values.backend.service.type }}
  ports:
    - port: {{ .Values.backend.service.port }}
      targetPort: {{ .Values.backend.service.targetPort }}
      protocol: TCP
      name: http
  selector:
    app: backend
    release: {{ .Release.Name }}
```

Create `helm/todo-chart/templates/frontend-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-frontend
  labels:
    app: frontend
    release: {{ .Release.Name }}
spec:
  replicas: {{ .Values.frontend.replicaCount }}
  selector:
    matchLabels:
      app: frontend
      release: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app: frontend
        release: {{ .Release.Name }}
    spec:
      containers:
        - name: frontend
          image: "{{ .Values.frontend.image.repository }}:{{ .Values.frontend.image.tag }}"
          imagePullPolicy: {{ .Values.frontend.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.frontend.service.targetPort }}
              protocol: TCP
          env:
            - name: NEXT_PUBLIC_API_URL
              valueFrom:
                configMapKeyRef:
                  name: {{ .Release.Name }}-config
                  key: backend_url
          resources:
            {{- toYaml .Values.frontend.resources | nindent 12 }}
          livenessProbe:
            httpGet:
              path: /
              port: {{ .Values.frontend.service.targetPort }}
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /
              port: {{ .Values.frontend.service.targetPort }}
            initialDelaySeconds: 5
            periodSeconds: 5
```

Create `helm/todo-chart/templates/frontend-service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-frontend
  labels:
    app: frontend
    release: {{ .Release.Name }}
spec:
  type: {{ .Values.frontend.service.type }}
  ports:
    - port: {{ .Values.frontend.service.port }}
      targetPort: {{ .Values.frontend.service.targetPort }}
      nodePort: {{ .Values.frontend.service.nodePort }}
      protocol: TCP
      name: http
  selector:
    app: frontend
    release: {{ .Release.Name }}
```

Create `helm/todo-chart/templates/secrets.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ .Release.Name }}-secrets
type: Opaque
data:
  database_url: {{ .Values.secrets.databaseUrl | b64enc | quote }}
  jwt_secret: {{ .Values.secrets.jwtSecret | b64enc | quote }}
  openai_api_key: {{ .Values.secrets.openaiApiKey | b64enc | quote }}
```

Create `helm/todo-chart/templates/configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-config
data:
  frontend_url: {{ .Values.config.frontendUrl | quote }}
  backend_url: {{ .Values.config.backendUrl | quote }}
```

### Install with Helm
```bash
# Install the todo application chart
helm install todo ./helm/todo-chart \
  --set secrets.databaseUrl="postgresql://user:password@neon-db-url" \
  --set secrets.jwtSecret="your-jwt-secret" \
  --set secrets.openaiApiKey="your-openai-api-key"

# Upgrade the chart (for configuration changes)
helm upgrade todo ./helm/todo-chart

# Uninstall the chart
helm uninstall todo
```

## Step 6: Access the Application

### With kubectl
```bash
# Get frontend service NodePort
kubectl get service frontend-service

# Access via minikube IP
minikube ip
# Then access: http://<minikube-ip>:<nodeport>
```

### With Minikube Service
```bash
# Open service in browser
minikube service frontend-service
```

## Troubleshooting

### Common Issues
1. **Images not found**: Ensure images are built and available to Minikube:
   ```bash
   # For Minikube, use the Minikube Docker environment
   eval $(minikube docker-env)
   docker build -t todo-backend:latest .
   docker build -t todo-frontend:latest .
   ```

2. **Database connectivity**: Ensure Neon PostgreSQL connection string is correct in secrets

3. **Service communication**: Check that backend service name matches the one used in frontend configuration

### Useful Commands
```bash
# Check pod status
kubectl get pods
kubectl describe pod <pod-name>

# Check logs
kubectl logs deployment/backend-deployment
kubectl logs deployment/frontend-deployment

# Port forward for testing
kubectl port-forward service/frontend-service 8080:80

# Helm operations
helm list
helm status todo
helm upgrade todo ./helm/todo-chart
helm uninstall todo
```