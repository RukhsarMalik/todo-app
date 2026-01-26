# Phase IV: Cloud Native Deployment of AI-Powered Todo Application

A cloud-native deployment of the AI-powered task management application using Docker, Kubernetes, and Helm for scalable infrastructure.

## Deployment Options

- **Docker Compose**: Local development and testing
- **Kubernetes (kubectl)**: Direct cluster deployment
- **Helm Charts**: Managed deployment with configurable parameters

## Technology Stack

| Layer | Technology |
|-------|------------|
| Containerization | Docker with multi-stage builds |
| Orchestration | Kubernetes (Minikube for local) |
| Package Management | Helm 3.x |
| Frontend | Next.js 16, React 19, TypeScript 5.x, Tailwind CSS |
| Backend | Python 3.13+, FastAPI, SQLModel |
| Database | Neon Serverless PostgreSQL |
| Auth | JWT with python-jose, bcrypt password hashing |
| AI Integration | OpenAI GPT-4o-mini with function calling |
| AI Tools | Anthropic MCP (Model Context Protocol) Server |
| Deployment | Docker, Kubernetes, Helm |

## Features

- Complete containerization of frontend and backend services
- Kubernetes-ready deployments with health checks
- Helm charts for easy deployment management
- Scalable infrastructure with replica controls
- Secure configuration management with Kubernetes Secrets
- Resource optimization with CPU/Memory limits
- Network isolation with dedicated service mesh
- **AI Chatbot**: Natural language interaction for task management
- **Conversation History**: Persistent chat sessions with AI assistant
- **AI Task Tools**: Direct integration with task management via function calls
- **MCP Server**: Model Context Protocol support for AI tools

## Project Structure

```
hackathon-2/
├── phase-1/                  # Console app (Module 0)
├── phase-2/                  # Basic full-stack app
├── phase-3/                  # AI chatbot integration
├── phase-4/                  # Cloud native deployment
│   ├── backend/              # Containerized FastAPI app
│   │   ├── Dockerfile        # Multi-stage build for backend
│   │   ├── .dockerignore     # Docker ignore rules
│   │   └── ...               # Backend application code
│   ├── frontend/             # Containerized Next.js app
│   │   ├── Dockerfile        # Multi-stage build for frontend
│   │   ├── .dockerignore     # Docker ignore rules
│   │   └── ...               # Frontend application code
│   ├── docker-compose.yml    # Local development orchestration
│   ├── k8s/                  # Kubernetes manifests
│   │   ├── backend-deployment.yaml
│   │   ├── backend-service.yaml
│   │   ├── frontend-deployment.yaml
│   │   ├── frontend-service.yaml
│   │   └── secrets.yaml
│   ├── helm/                 # Helm chart for managed deployment
│   │   └── todo-chart/
│   │       ├── Chart.yaml    # Chart definition
│   │       ├── values.yaml   # Default configuration values
│   │       └── templates/    # Kubernetes resource templates
│   ├── DEPLOYMENT.md         # Comprehensive deployment guide
│   └── README.md             # This file
├── specs/                    # Feature specifications
└── README.md                 # Project overview
```

## Local Development Setup

### Prerequisites

- Docker Desktop installed and running
- Minikube installed (for Kubernetes)
- kubectl installed
- Helm 3.x installed
- uv (Python package manager)
- npm

### Option 1: Docker Compose (Recommended for Local Development)

```bash
cd phase-4

# Copy environment template
cp backend/.env.example .env
cp frontend/.env.example .env.local

# Build and start services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 2: Kubernetes with Minikube

```bash
cd phase-4

# Start Minikube cluster
minikube start

# Configure Docker to build images directly to Minikube
eval $(minikube docker-env)

# Build container images
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend

# Deploy to Kubernetes
kubectl apply -f k8s/

# Access the application
minikube service frontend-service
```

### Option 3: Helm Deployment

```bash
cd phase-4

# Install the Helm chart
helm install todo ./helm/todo-chart

# Install with custom values
helm install todo ./helm/todo-chart \
  --set secrets.databaseUrl="postgresql://..." \
  --set secrets.jwtSecretKey="your-jwt-secret" \
  --set secrets.openaiApiKey="sk-..."

# Access the application
minikube service todo-frontend
```

## Configuration

### Environment Variables

#### Backend (via Kubernetes Secrets)

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | Neon PostgreSQL connection string | `postgresql+asyncpg://user:pass@host/db?ssl=require` |
| JWT_SECRET_KEY | JWT signing secret (min 32 chars) | Generate with `secrets.token_urlsafe(32)` |
| FRONTEND_URL | Production frontend URL (for CORS) | `https://your-frontend.example.com` |
| OPENAI_API_KEY | OpenAI API key for chat functionality | `sk-...` |

#### Frontend (via ConfigMap)

| Variable | Description | Example |
|----------|-------------|---------|
| NEXT_PUBLIC_API_URL | Backend API URL | `http://backend-service:8000` (internal) or `http://localhost:8000` (local) |

## Deployment Strategies

### Docker Compose
- Best for local development and testing
- Single command deployment with `docker-compose up`
- Built-in service dependencies and health checks
- Easy scaling with `docker-compose up --scale`

### Kubernetes (kubectl)
- Direct control over Kubernetes resources
- Supports advanced networking and security policies
- Enables horizontal pod autoscaling
- Integrates with cloud provider services

### Helm Charts
- Parameterized deployments with configurable values
- Versioned releases with rollback capability
- Template-based resource generation
- Dependency management for complex applications

## Scaling Considerations

### Horizontal Scaling
- Backend: Scale based on API request volume
- Frontend: Scale based on concurrent user sessions
- Database: Leverage Neon's serverless scaling

### Resource Management
- CPU/Memory requests and limits defined in deployments
- Quality of Service (QoS) classification for resource allocation
- Resource quotas for namespace-level control

## Monitoring and Logging

### Health Checks
- Liveness and readiness probes for all services
- Application-level health endpoints
- Infrastructure monitoring via Kubernetes

### Logging
- Structured logging in JSON format
- Centralized logging via Kubernetes logging drivers
- Log aggregation with ELK or similar stacks

## CI/CD Pipeline Integration

The deployment configurations are designed to work with popular CI/CD platforms:

- **GitHub Actions**: Pre-configured workflows for building and deploying
- **Docker Hub**: Automated image building and tagging
- **Helm Repositories**: Chart publishing and versioning
- **Infrastructure as Code**: Declarative Kubernetes manifests

## Troubleshooting

### Common Issues
1. **ImagePullBackOff**: Ensure images are built and available in the target registry
2. **CrashLoopBackOff**: Check application logs and environment variables
3. **Service Unavailable**: Verify service networking and ingress configuration

### Useful Commands
```bash
# Check pod status
kubectl get pods
kubectl describe pod <pod-name>

# View application logs
kubectl logs deployment/backend-deployment
kubectl logs deployment/frontend-deployment

# Port forward for local testing
kubectl port-forward service/frontend-service 8080:80

# Scale deployments
kubectl scale deployment backend-deployment --replicas=3
```

## Specifications

All feature specifications are in the `/specs/` folder:
- `specs/phase2/1-database/` - Database module spec
- `specs/phase2/2-backend-api/` - Backend API spec
- `specs/phase2/3-jwt-auth/` - Authentication spec
- `specs/005-frontend-web-app/` - Frontend spec
- `specs/006-chat-database/` - AI chatbot spec
- `specs/phase-4/1-deployment/` - Deployment spec

## Deployment Guide

For detailed deployment instructions, refer to [DEPLOYMENT.md](./DEPLOYMENT.md).

## Author

RukhsarMalik - Hackathon 2, Phase 4 Submission

## License

This project is for educational purposes as part of the Hackathon 2 program.
