# Research Findings: Phase IV Module 1 - Containerization & Kubernetes Deployment

## Decision: Application Structure Analysis
**Rationale**: Need to understand the current application architecture to properly containerize it
**Findings**:
- Backend: FastAPI application (Python 3.13+) with SQLModel for database operations
- Frontend: Next.js 16+ application with TypeScript and Tailwind CSS
- Database: Neon PostgreSQL (external, not containerized)
- AI Chatbot: OpenAI Agents SDK with MCP server for tool integration
- Authentication: JWT-based using Better Auth

## Decision: Dockerfile Approach
**Rationale**: Multi-stage builds provide optimized container images with security benefits
**Alternatives considered**:
1. Single-stage build - simpler but larger images
2. Multi-stage build - optimized images, security (selected)
3. Buildpacks - abstracts complexity but less control

**Selected**: Multi-stage builds for both services
- Backend: python:3.13-slim as base, separate build stage for dependencies
- Frontend: node:20-alpine as base, separate build stage for Next.js compilation

## Decision: Base Images
**Rationale**: Minimal, secure base images reduce attack surface and image size
**Options evaluated**:
1. python:3.13-slim - minimal Python with package manager access
2. python:3.13-alpine - smaller but potential compatibility issues
3. node:20-alpine - lightweight Node.js base image

**Selected**: python:3.13-slim for backend, node:20-alpine for frontend

## Decision: Kubernetes Service Types
**Rationale**: Different access patterns required for frontend vs backend services
**Options evaluated**:
1. ClusterIP for both - internal only access
2. NodePort for frontend, ClusterIP for backend (selected) - external access for UI, internal for API
3. LoadBalancer for both - external access but resource intensive

**Selected**: NodePort for frontend (external access), ClusterIP for backend (internal)

## Decision: Configuration Management
**Rationale**: Need to separate sensitive from non-sensitive configuration
**Approach**:
- ConfigMaps for non-sensitive environment variables (FRONTEND_URL, API paths)
- Secrets for sensitive data (DATABASE_URL, JWT secrets, API keys)
- Mounted as volumes or environment variables in pods

## Decision: Health Checks
**Rationale**: Essential for Kubernetes liveness/readiness probes
**Backend**: `/health` endpoint or similar health check
**Frontend**: Port availability or simple HTTP response

## Decision: Helm Chart Structure
**Rationale**: Single chart simplifies deployment and version management
**Structure**:
- Single chart (helm/todo-chart/) containing templates for both services
- Combined values.yaml with backend/frontend configuration sections
- Template files for K8s resources (deployments, services, configmaps, secrets)
- Proper versioning in Chart.yaml
- Single `helm install todo ./helm/todo-chart` command deploys entire application

## Decision: Resource Requirements
**Rationale**: Proper resource allocation ensures stability and performance
**Backend**:
- Request: 200m CPU, 256Mi memory
- Limit: 500m CPU, 512Mi memory

**Frontend**:
- Request: 100m CPU, 128Mi memory
- Limit: 200m CPU, 256Mi memory

## Decision: Deployment Strategy
**Rationale**: Rolling updates ensure zero-downtime deployments
**Strategy**: RollingUpdate with maxSurge=1 and maxUnavailable=0 for smooth transitions