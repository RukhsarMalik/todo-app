# Docker Checklist: Phase IV Module 1

## Part A: Containerization

### US-1: Backend Dockerfile
- [X] Multi-stage build implemented (Python 3.13-slim base)
- [X] Dependencies installed with uv package manager
- [X] Port 8000 exposed
- [X] Health check configured
- [X] Non-root user execution (security)
- [X] .dockerignore file created with appropriate exclusions

### US-2: Frontend Dockerfile
- [X] Multi-stage build implemented (Node 20-alpine base)
- [X] Next.js standalone build configured
- [X] Port 3000 exposed
- [X] Health check configured
- [X] .dockerignore file created with appropriate exclusions

### US-3: Local Docker Testing
- [X] docker-compose.yml created
- [X] Backend service defined with correct ports and env vars
- [X] Frontend service defined with correct ports and env vars
- [X] Services can communicate (frontend -> backend)
- [X] Environment variables properly configured
- [ ] Both containers start successfully with `docker-compose up`

## Build Verification

- [ ] `docker build -t todo-backend ./phase-4/backend` succeeds
- [ ] `docker build -t todo-frontend ./phase-4/frontend` succeeds
- [ ] Backend container starts and responds on port 8000
- [ ] Frontend container starts and serves UI on port 3000
- [ ] Health endpoints return healthy status
