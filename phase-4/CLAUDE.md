# Claude Code Rules for Phase IV: Cloud Native Deployment

## Task context

**Surface**: You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Technologies in Use

### Primary Technologies
- Docker for containerization
- Kubernetes for orchestration
- Minikube for local cluster
- Helm for package management
- kubectl for cluster management

### Existing Application Stack (from previous phases)
- Python 3.13+ with FastAPI for backend
- Next.js 16+ with TypeScript for frontend
- Neon PostgreSQL for database
- OpenAI Agents SDK for AI chatbot
- Model Context Protocol (MCP) for AI tools

## Development Guidelines

### Containerization Guidelines
- Use multi-stage Docker builds for optimized images
- Use minimal base images (python:3.13-slim, node:20-alpine)
- Include health checks in Dockerfiles
- Follow security best practices (non-root users where possible)

### Kubernetes Guidelines
- Deploy backend as ClusterIP service (internal access)
- Deploy frontend as NodePort service (external access)
- Use ConfigMaps for non-sensitive configuration
- Use Secrets for sensitive data (encoded in base64)
- Define resource requests and limits for all deployments

### Helm Guidelines
- Create separate charts for frontend and backend
- Use values.yaml for configurable parameters
- Template all Kubernetes resources properly
- Follow Helm best practices for chart structure

### Integration Guidelines
- Preserve all Phase III functionality in containerized deployment
- Maintain existing authentication flows
- Ensure database connectivity from containerized app
- Preserve AI chatbot functionality