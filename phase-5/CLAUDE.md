# Claude Code Rules for Phase V: Advanced Features & Event Architecture

## Technologies in Use

### Primary Technologies
- Docker for containerization
- Kubernetes for orchestration (Minikube for local)
- Helm for package management
- Apache Kafka (Strimzi) for event streaming
- Dapr for Pub/Sub, Jobs API, Secrets
- Python 3.13+ with FastAPI for backend
- Next.js 16+ with TypeScript for frontend
- Neon PostgreSQL for database
- OpenAI Agents SDK for AI chatbot
- Model Context Protocol (MCP) for AI tools

### Phase V New Features
- Task priorities (low/medium/high/urgent)
- Due dates with reminders
- Tags (many-to-many with junction table)
- Recurring tasks (daily/weekly/monthly)
- Notifications via event-driven architecture
- Advanced search, filter, and sort
- Dapr Pub/Sub event publishing with graceful degradation

### New Backend Files (Phase V)
- `backend/events.py` - Dapr event publisher
- `backend/routes/tags.py` - Tag CRUD endpoints
- `backend/routes/notifications.py` - Notification listing
- `backend/models.py` - Extended with Tag, TaskTag, Notification models
- `services/notification/` - Notification microservice (Dapr consumer)
- `services/recurring-task/` - Recurring task microservice (Dapr consumer)

### New K8s Manifests (Phase V)
- `k8s/strimzi-kafka.yaml` - Strimzi Kafka cluster + topics
- `k8s/dapr-components.yaml` - Dapr Pub/Sub component (Kafka backend)
- `k8s/notification-deployment.yaml` - Notification service with Dapr sidecar
- `k8s/recurring-task-deployment.yaml` - Recurring task service with Dapr sidecar

## Development Guidelines

### Event Architecture
- Backend publishes events via Dapr HTTP API (localhost:3500)
- Events use CloudEvents format via Dapr Pub/Sub
- Graceful degradation: CRUD succeeds even if Kafka/Dapr is down
- Notification service and recurring-task service consume events

### Database Schema (Phase V additions)
- `tags` table: id, user_id, name, created_at
- `task_tags` junction table: task_id, tag_id (composite PK)
- `notifications` table: id, user_id, task_id, message, read, created_at
- `tasks` table extended: priority, due_date, reminder_offset, recurrence_rule (JSON), next_occurrence, parent_task_id

### MCP Tools (Phase V)
| Tool | Parameters |
|------|-----------|
| add_task | user_id, title, description, priority, due_date, tag_names |
| list_tasks | user_id, status, priority, search |
| complete_task | user_id, task_id |
| delete_task | user_id, task_id |
| update_task | user_id, task_id, title, description, priority, due_date |
| list_tags | user_id |
