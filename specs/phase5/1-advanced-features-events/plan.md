# Implementation Plan: Advanced Features + Event Architecture

**Branch**: `007-advanced-features-events` | **Date**: 2026-02-02 | **Spec**: `specs/phase5/1-advanced-features-events/specification.md`
**Input**: Feature specification from `/specs/phase5/1-advanced-features-events/specification.md`

## Summary

Extend the existing Phase IV todo application with advanced task fields (priority, due dates, tags, recurrence), search/filter/sort capabilities, and an event-driven architecture using Apache Kafka (Strimzi on Minikube) and Dapr for inter-service communication. Two new microservices (notification, recurring task) consume events asynchronously.

## Technical Context

**Language/Version**: Python 3.13+ (backend, new microservices), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI, SQLModel, Dapr SDK (Python), Strimzi Kafka Operator, Dapr CLI, Next.js 16+, Tailwind CSS 4
**Storage**: Neon PostgreSQL (external) — schema extended with new columns and tables
**Testing**: Manual + curl/httpie for API, `kubectl` verification for K8s, Dapr CLI for pub/sub verification
**Target Platform**: Minikube (local Kubernetes cluster)
**Project Type**: Web application (monorepo: phase-5/backend, phase-5/frontend, phase-5/services/notification, phase-5/services/recurring-task)
**Performance Goals**: Task CRUD < 1s response, search < 2s, recurring task creation < 10s after completion, reminders within 1 min of scheduled time
**Constraints**: Kafka broker unavailability must not block CRUD operations (graceful degradation)
**Scale/Scope**: Single-user demo on Minikube; all pods running simultaneously

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. AI-Native Development | PASS | All code generated via Claude Code + Spec-Kit Plus |
| II. Specification-First | PASS | Spec complete, plan in progress |
| III. Clean Code & Python Standards | PASS | Type hints, docstrings, SRP enforced |
| IX. API-First Design | PASS | All new features exposed via REST endpoints |
| X. Database Persistence | PASS | Neon PostgreSQL, schema extended |
| XI. Multi-User Support | PASS | All queries scoped by user_id |
| XII. Authentication Required | PASS | JWT auth on all endpoints |
| XIV. MCP Architecture | PASS | MCP tools extended for new features |
| XVII. Agent Tool Safety | PASS | All tools validate user_id |
| XVIII. Container-First | PASS | All services Dockerized |
| XIX. Kubernetes Orchestration | PASS | Deployed on Minikube |
| XXII. Infrastructure as Code | PASS | All manifests in repo |
| XXIII. Event-Driven Architecture | PASS | Kafka via Strimzi + Dapr Pub/Sub |
| XXIV. Distributed Runtime | PASS | Dapr sidecars on all services |
| XXVII. Advanced Task Features | PASS | Priority, due dates, tags, recurrence |

No violations. No complexity justifications needed.

## Project Structure

### Documentation (this feature)

```text
specs/phase5/1-advanced-features-events/
├── specification.md     # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 research
├── data-model.md        # Phase 1 data model
├── quickstart.md        # Phase 1 quickstart
├── contracts/           # Phase 1 API contracts
│   ├── tasks-api-v2.yaml
│   ├── notifications-api.yaml
│   └── dapr-components.yaml
├── checklists/
│   └── requirements.md  # Requirements checklist
└── tasks.md             # Phase 2 task breakdown
```

### Source Code (repository root)

```text
phase-5/
├── backend/
│   ├── Dockerfile
│   ├── main.py                  # FastAPI app (extended)
│   ├── models.py                # SQLModel models (Task extended, Tag, TaskTag, Notification added)
│   ├── schemas.py               # Pydantic schemas (extended)
│   ├── db.py                    # Database connection
│   ├── init_db.py               # DB init (extended for new tables)
│   ├── events.py                # NEW: Dapr event publisher
│   ├── mcp_server.py            # MCP server (tools extended)
│   ├── agent.py                 # OpenAI agent
│   ├── auth/                    # Auth module (unchanged)
│   ├── routes/
│   │   ├── tasks.py             # Task routes (extended: search, filter, sort, new fields)
│   │   ├── tags.py              # NEW: Tag CRUD routes
│   │   ├── notifications.py     # NEW: Notification list route
│   │   ├── auth.py              # Auth routes (unchanged)
│   │   └── chat.py              # Chat routes (unchanged)
│   ├── requirements.txt
│   └── pyproject.toml
├── frontend/
│   ├── Dockerfile
│   ├── src/
│   │   ├── app/                 # Pages (tasks page extended)
│   │   ├── components/
│   │   │   ├── tasks/           # Task components (extended: priority, due date, tags UI)
│   │   │   └── ui/              # UI components (unchanged)
│   │   └── lib/
│   │       ├── api.ts           # API client (extended)
│   │       └── types.ts         # Types (extended)
│   └── package.json
├── services/
│   ├── notification/
│   │   ├── Dockerfile
│   │   ├── main.py              # NEW: FastAPI app subscribing to reminder events
│   │   ├── requirements.txt
│   │   └── pyproject.toml
│   └── recurring-task/
│       ├── Dockerfile
│       ├── main.py              # NEW: FastAPI app subscribing to task.completed events
│       ├── requirements.txt
│       └── pyproject.toml
├── k8s/
│   ├── backend-deployment.yaml  # Updated with Dapr annotations
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml # Updated with Dapr annotations
│   ├── frontend-service.yaml
│   ├── notification-deployment.yaml   # NEW
│   ├── notification-service.yaml      # NEW
│   ├── recurring-task-deployment.yaml # NEW
│   ├── recurring-task-service.yaml    # NEW
│   ├── secrets.yaml             # Extended
│   └── strimzi/                 # NEW: Kafka manifests
│       ├── kafka-namespace.yaml
│       ├── strimzi-operator.yaml
│       └── kafka-cluster.yaml
├── dapr/
│   ├── components/
│   │   ├── pubsub-kafka.yaml    # Dapr Pub/Sub component (Kafka backend)
│   │   ├── statestore-redis.yaml # Dapr State Store (optional)
│   │   └── secretstore-k8s.yaml # Dapr Secret Store (K8s Secrets)
│   └── subscriptions/
│       ├── notification-sub.yaml
│       └── recurring-task-sub.yaml
├── helm/
│   └── todo-chart/              # Helm chart (extended)
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── backend-deployment.yaml
│           ├── frontend-deployment.yaml
│           ├── notification-deployment.yaml  # NEW
│           ├── recurring-task-deployment.yaml # NEW
│           ├── dapr-components.yaml          # NEW
│           └── ...
└── docker-compose.yml           # Updated for local dev
```

**Structure Decision**: Extends the existing phase-4 monorepo pattern. Two new microservices under `services/`. Dapr config and Strimzi manifests under dedicated directories. Helm chart extended with new templates.

## Architecture Overview

### Event Flow

```
User Action (CRUD) → Backend API → Database Write
                                  → Dapr Pub/Sub → Kafka Topic
                                                      ↓
                                    ┌─────────────────┴──────────────────┐
                                    ↓                                    ↓
                           Notification Service              Recurring Task Service
                           (subscribes: reminders)           (subscribes: task.completed)
                                    ↓                                    ↓
                           Store notification record         Create next task occurrence
```

### Dapr Sidecar Architecture

```
┌─────────────────────────────┐
│       Backend Pod            │
│  ┌──────────┐ ┌───────────┐ │
│  │ FastAPI   │ │ Dapr      │ │
│  │ App       │←→│ Sidecar  │ │
│  └──────────┘ └───────────┘ │
└─────────────────────────────┘
        ↓ Dapr Pub/Sub API
┌─────────────────────────────┐
│    Kafka (Strimzi)           │
│    Topics: task-events,      │
│            reminders         │
└─────────────────────────────┘
        ↓
┌──────────────┐  ┌────────────────────┐
│ Notification │  │ Recurring Task     │
│ Service +    │  │ Service +          │
│ Dapr Sidecar │  │ Dapr Sidecar       │
└──────────────┘  └────────────────────┘
```

### Database Schema Changes

**Extended Task table** (add columns to existing `tasks` table):
- `priority` VARCHAR(10) DEFAULT 'medium' — enum: low, medium, high, urgent
- `due_date` TIMESTAMP nullable
- `reminder_offset` INTEGER DEFAULT 60 — minutes before due date
- `recurrence_rule` JSONB nullable — e.g., `{"type": "weekly", "days": ["Monday"]}`
- `next_occurrence` TIMESTAMP nullable — computed field for recurring tasks
- `parent_task_id` INTEGER nullable FK(tasks.id) — links recurrence chain

**New tables**:
- `tags` (id, user_id, name, created_at) — user-owned tags
- `task_tags` (task_id, tag_id) — junction table
- `notifications` (id, user_id, task_id, message, read, created_at) — reminder records

### Key Technical Decisions

1. **Dapr Pub/Sub over direct Kafka SDK**: Abstracts broker; switch between Strimzi (local) and Redpanda Cloud (prod) by changing a component YAML, no code changes.

2. **Dapr Jobs API for reminders**: Schedules one-time callbacks at `due_date - reminder_offset`. Simpler than running a cron polling loop.

3. **Tags as separate table (not JSONB array)**: Enables proper indexing, reusable tags per user, and standard many-to-many patterns.

4. **New microservices as separate FastAPI apps**: Lightweight consumers with their own Dockerfiles. Share the same database (Neon PostgreSQL) via Dapr Secrets for connection string.

5. **Graceful degradation**: Event publishing wrapped in try/except; CRUD succeeds even if Dapr/Kafka is down. Failed events logged for manual retry.

## Implementation Phases

### Phase A: Database & Backend Extensions (P1 features)
1. Copy phase-4 to phase-5 as baseline
2. Extend Task model with priority, due_date, reminder_offset, recurrence_rule, next_occurrence, parent_task_id
3. Add Tag, TaskTag, Notification models
4. Run init_db.py to create new tables/columns
5. Extend schemas (TaskCreate, TaskUpdate, TaskResponse) with new fields
6. Extend routes/tasks.py with search, filter, sort query params
7. Add routes/tags.py for tag CRUD
8. Add routes/notifications.py for notification listing
9. Update MCP tools to support new fields
10. Update frontend task components with priority badges, due date picker, tag input

### Phase B: Event Architecture (P2-P3 features)
1. Install Strimzi operator on Minikube, create Kafka cluster
2. Install Dapr on Minikube
3. Configure Dapr Pub/Sub component (Kafka backend)
4. Add events.py to backend — publish task events via Dapr HTTP API
5. Create notification service (subscribes to reminders topic)
6. Create recurring task service (subscribes to task.completed topic)
7. Configure Dapr Jobs API for reminder scheduling
8. Dockerize new services
9. Create K8s manifests with Dapr annotations
10. Update Helm chart

### Phase C: Integration & Testing
1. Deploy all services to Minikube
2. End-to-end test: create task with due date → event published → reminder triggered → notification logged
3. End-to-end test: complete recurring task → next occurrence created
4. Verify graceful degradation (stop Kafka, CRUD still works)
5. Verify all Phase IV features still work

## Complexity Tracking

No constitution violations. No complexity justifications needed.
