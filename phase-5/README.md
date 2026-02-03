# Phase V: Advanced Features & Event Architecture

A feature-rich task management application extended with priorities, due dates, tags, recurring tasks, notifications, and an event-driven architecture using Dapr and Apache Kafka.

## What's New in Phase V

- **Task Priorities**: Low, Medium, High, Urgent with color-coded badges
- **Due Dates**: Date picker with overdue/today/tomorrow indicators
- **Tags**: Many-to-many tagging system with create/assign/filter
- **Recurring Tasks**: Daily, weekly, monthly recurrence with auto-creation on completion
- **Notifications**: Task reminders and event-driven notifications
- **Advanced Search**: Full-text search across title and description (server-side ILIKE)
- **Filter & Sort**: Filter by priority, tags, due date range; sort by date, title, priority, due date
- **Event-Driven Architecture**: Dapr Pub/Sub with Apache Kafka (Strimzi) for inter-service communication
- **Graceful Degradation**: CRUD operations succeed even when Kafka/Dapr is unavailable

## Technology Stack

| Layer | Technology |
|-------|------------|
| Containerization | Docker with multi-stage builds |
| Orchestration | Kubernetes (Minikube for local) |
| Package Management | Helm 3.x |
| Event Streaming | Apache Kafka (Strimzi on K8s) |
| Event Framework | Dapr Pub/Sub, Jobs API |
| Frontend | Next.js 16, React 19, TypeScript 5.x, Tailwind CSS |
| Backend | Python 3.13+, FastAPI, SQLModel |
| Database | Neon Serverless PostgreSQL |
| Auth | JWT with python-jose, bcrypt password hashing |
| AI Integration | OpenAI GPT-4o-mini with function calling |
| AI Tools | Anthropic MCP (Model Context Protocol) Server |

## Project Structure

```
phase-5/
├── backend/
│   ├── models.py            # Extended: Priority, Tags, Notifications, Recurrence
│   ├── schemas.py           # Extended: priority/due_date/tags request/response
│   ├── events.py            # NEW: Dapr event publisher (graceful degradation)
│   ├── routes/
│   │   ├── tasks.py         # Extended: search, filter, sort, tags, recurrence
│   │   ├── tags.py          # NEW: Tag CRUD endpoints
│   │   ├── notifications.py # NEW: Notification listing endpoint
│   │   ├── auth.py          # Auth endpoints
│   │   └── chat.py          # AI chat endpoints
│   ├── main.py              # FastAPI app with all routers
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/tasks/
│   │   │   ├── TaskForm.tsx     # Extended: priority, due date, tags, recurrence
│   │   │   ├── TaskEditForm.tsx # Extended: edit all new fields
│   │   │   ├── TaskItem.tsx     # Extended: priority badge, due date, tags display
│   │   │   └── TaskList.tsx     # Extended: filter bar, server-side search/sort
│   │   └── lib/
│   │       ├── types.ts         # Extended: Priority, Tag, RecurrenceRule types
│   │       └── api.ts           # Extended: tags, notifications, filter params
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── k8s/                     # Kubernetes manifests
├── helm/                    # Helm charts
└── README.md
```

## API Endpoints

### New Endpoints (Phase V)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /api/{user_id}/tags | List user's tags |
| POST | /api/{user_id}/tags | Create a tag |
| DELETE | /api/{user_id}/tags/{tag_id} | Delete a tag |
| GET | /api/{user_id}/notifications | List notifications |

### Extended Task Endpoints

| Method | Endpoint | Changes |
|--------|----------|---------|
| GET | /api/{user_id}/tasks | +search, priority, tags, due_date_from/to, sort params |
| POST | /api/{user_id}/tasks | +priority, due_date, tag_ids, recurrence_rule fields |
| PUT | /api/{user_id}/tasks/{id} | +priority, due_date, tag_ids, recurrence_rule fields |
| PATCH | /api/{user_id}/tasks/{id}/complete | Auto-creates next occurrence for recurring tasks |

## Database Schema Changes

New tables: `tags`, `task_tags` (junction), `notifications`

Extended `tasks` table columns:
- `priority` (VARCHAR, default 'medium')
- `due_date` (DATE, nullable)
- `reminder_offset` (INTEGER, default 30 minutes)
- `recurrence_rule` (JSON, nullable)
- `next_occurrence` (DATE, nullable)
- `parent_task_id` (FK to tasks.id, self-referencing)

## Local Development

```bash
cd phase-5

# Backend
cd backend
cp .env.example .env   # Configure DATABASE_URL, JWT_SECRET_KEY, OPENAI_API_KEY
uv run python init_db.py
uv run uvicorn main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
cp .env.example .env.local
npm installwsl

npm run dev
```

## Cloud Deployment (Azure AKS)

### Prerequisites
- Azure subscription with AKS and ACR
- Redpanda Cloud account with Kafka topics
- Neon PostgreSQL database

### Deployment Steps

1. **Create Azure Infrastructure**:
   ```bash
   # Create resource group and AKS cluster
   az group create --name todo-rg --location eastus
   az aks create --resource-group todo-rg --name todo-cluster --node-count 2 --node-vm-size Standard_B2s --generate-ssh-keys

   # Create Azure Container Registry
   az acr create --resource-group todo-rg --name todoacr$(date +%s) --sku Basic

   # Attach ACR to AKS
   ACR_NAME=$(az acr list --resource-group todo-rg --query "[0].name" -o tsv)
   az aks update -n todo-cluster -g todo-rg --attach-acr $ACR_NAME

   # Get AKS credentials
   az aks get-credentials --resource-group todo-rg --name todo-cluster
   ```

2. **Install Dapr**:
   ```bash
   dapr init -k
   ```

3. **Create Kubernetes Secrets**:
   ```bash
   kubectl create namespace todo

   kubectl create secret generic app-secrets -n todo \
     --from-literal=database-url="<neon-db-url>" \
     --from-literal=jwt-secret="<jwt-secret>" \
     --from-literal=openai-api-key="<openai-key>"

   kubectl create secret generic kafka-secrets -n todo \
     --from-literal=username="<redpanda-username>" \
     --from-literal=password="<redpanda-password>" \
     --from-literal=bootstrap-servers="<redpanda-bootstrap-servers>"
   ```

4. **Deploy Dapr Components**:
   ```bash
   kubectl apply -f k8s/dapr-pubsub.yaml
   kubectl apply -f k8s/dapr-secrets.yaml
   kubectl apply -f k8s/dapr-subscriptions.yaml
   ```

5. **Build and Deploy Application**:
   ```bash
   # Build and push images to ACR
   az acr build --registry $ACR_NAME --image backend:v1 ./backend
   az acr build --registry $ACR_NAME --image frontend:v1 ./frontend

   # Deploy with Helm using Azure values
   ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
   helm upgrade --install todo ./helm/todo-chart \
     --namespace todo \
     --values ./helm/todo-chart/values-azure.yaml \
     --set backend.image.repository=$ACR_LOGIN_SERVER/backend \
     --set frontend.image.repository=$ACR_LOGIN_SERVER/frontend \
     --wait
   ```

### CI/CD Pipeline

The deployment includes a GitHub Actions workflow in `.github/workflows/deploy-azure.yml` that automates:
- Building container images
- Pushing to Azure Container Registry
- Deploying to AKS using Helm
- Verifying rollout status

## Specifications

- `specs/phase5/1-advanced-features-events/specification.md` - Feature spec
- `specs/phase5/1-advanced-features-events/plan.md` - Architecture plan
- `specs/phase5/1-advanced-features-events/tasks.md` - Implementation tasks
- `specs/phase5/1-advanced-features-events/data-model.md` - Data model

## Author

RukhsarMalik - Hackathon 2, Phase 5 Submission

## License

This project is for educational purposes as part of the Hackathon 2 program.
