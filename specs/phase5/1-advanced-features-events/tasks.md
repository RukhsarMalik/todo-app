# Tasks: Advanced Features + Event Architecture

**Feature**: 007-advanced-features-events | **Branch**: `007-advanced-features-events` | **Date**: 2026-02-02
**Spec**: `specs/phase5/1-advanced-features-events/specification.md`
**Plan**: `specs/phase5/1-advanced-features-events/plan.md`

## User Story Mapping

| Story | Title | Priority | Spec Reference |
|-------|-------|----------|----------------|
| US1 | Task Priorities and Due Dates | P1 | User Story 1 |
| US2 | Search, Filter, and Sort Tasks | P1 | User Story 2 |
| US3 | Tags and Categories | P2 | User Story 3 |
| US4 | Recurring Tasks | P2 | User Story 4 |
| US5 | Due Date Reminders | P2 | User Story 5 |
| US6 | Event-Driven Task Events via Kafka | P3 | User Story 6 |
| US7 | Notification Service | P3 | User Story 7 |
| US8 | Dapr Integration | P3 | User Story 8 |
| US9 | Minikube Deployment | P3 | User Story 9 |

---

## Phase 1: Setup

**Goal**: Copy phase-4 baseline to phase-5 and verify existing functionality.

- [x] T001 Copy phase-4 directory to phase-5 as baseline at `phase-5/`
- [x] T002 Verify phase-5 backend starts locally with `uv run uvicorn main:app --port 8000` in `phase-5/backend/`
- [x] T003 Verify phase-5 frontend starts locally with `npm run dev` in `phase-5/frontend/`
- [x] T004 Add new Python dependencies (httpx for Dapr HTTP calls) to `phase-5/backend/requirements.txt` and `phase-5/backend/pyproject.toml`

---

## Phase 2: Foundational — Extended Task Model & Database

**Goal**: Extend the Task model and database schema with new columns. All user stories depend on this.

- [x] T005 Add Priority enum and extend Task model with priority, due_date, reminder_offset, recurrence_rule, next_occurrence, parent_task_id fields in `phase-5/backend/models.py`
- [x] T006 Add Tag model (id, user_id, name, created_at) with unique constraint on (user_id, name) in `phase-5/backend/models.py`
- [x] T007 Add TaskTag junction model (task_id, tag_id composite PK) in `phase-5/backend/models.py`
- [x] T008 Add Notification model (id, user_id, task_id, message, read, created_at) in `phase-5/backend/models.py`
- [x] T009 Update init_db.py to create new tables (tags, task_tags, notifications) and add new columns to tasks table in `phase-5/backend/init_db.py`
- [x] T010 Extend TaskCreate schema with optional priority, due_date, reminder_offset, recurrence_rule, tag_ids fields in `phase-5/backend/schemas.py`
- [x] T011 Extend TaskUpdate schema with optional priority, due_date, reminder_offset, recurrence_rule, tag_ids fields in `phase-5/backend/schemas.py`
- [x] T012 Extend TaskResponse schema with priority, due_date, reminder_offset, recurrence_rule, next_occurrence, parent_task_id, tags fields in `phase-5/backend/schemas.py`
- [x] T013 Add TagCreate, TagResponse, NotificationResponse schemas in `phase-5/backend/schemas.py`
- [x] T014 Add Priority, SortField enum extensions (due_date, priority values) in `phase-5/backend/schemas.py`
- [ ] T015 Run init_db.py against Neon PostgreSQL to apply schema changes, verify with test_db.py in `phase-5/backend/`

---

## Phase 3: User Story 1 — Task Priorities and Due Dates (P1)

**Goal**: Users can set priority levels and due dates on tasks; visual priority indicators in UI.

**Independent Test**: Create a task with priority=high and due_date=tomorrow, verify both display correctly, update priority, filter by priority.

- [x] T016 [US1] Update POST /api/{user_id}/tasks handler to accept and persist priority, due_date, reminder_offset fields in `phase-5/backend/routes/tasks.py`
- [x] T017 [US1] Update PUT /api/{user_id}/tasks/{id} handler to accept and persist priority, due_date, reminder_offset fields in `phase-5/backend/routes/tasks.py`
- [x] T018 [US1] Update GET task list and GET single task handlers to return new fields in response in `phase-5/backend/routes/tasks.py`
- [x] T019 [P] [US1] Add Priority type and due_date to Task interface in `phase-5/frontend/src/lib/types.ts`
- [x] T020 [P] [US1] Update API client createTask and updateTask functions to send priority, due_date, reminder_offset in `phase-5/frontend/src/lib/api.ts`
- [x] T021 [US1] Add priority select dropdown (low/medium/high/urgent) and due date picker to TaskForm component in `phase-5/frontend/src/components/tasks/TaskForm.tsx`
- [x] T022 [US1] Add priority select and due date picker to TaskEditForm component in `phase-5/frontend/src/components/tasks/TaskEditForm.tsx`
- [x] T023 [US1] Add priority badge (color-coded: urgent=red, high=orange, medium=blue, low=gray) to TaskItem component in `phase-5/frontend/src/components/tasks/TaskItem.tsx`
- [x] T024 [US1] Display due date with relative time (e.g., "Due in 2 days", "Overdue") on TaskItem in `phase-5/frontend/src/components/tasks/TaskItem.tsx`

---

## Phase 4: User Story 2 — Search, Filter, and Sort Tasks (P1)

**Goal**: Users can search by keyword, filter by status/priority/tags/date range, and sort by various fields.

**Independent Test**: Create 10+ tasks with varied attributes, verify search returns partial matches, filters combine with AND logic, sort orders are correct.

- [x] T025 [US2] Add search, priority, tags, due_date_from, due_date_to, sort, order query parameters to GET /api/{user_id}/tasks in `phase-5/backend/routes/tasks.py`
- [x] T026 [US2] Implement case-insensitive partial match search on title and description using SQL ILIKE in `phase-5/backend/routes/tasks.py`
- [x] T027 [US2] Implement filter logic: status, priority, due_date range with AND combination in `phase-5/backend/routes/tasks.py`
- [x] T028 [US2] Implement tag filter: join task_tags and tags tables, filter by comma-separated tag names in `phase-5/backend/routes/tasks.py`
- [x] T029 [US2] Implement sort logic: created_at, due_date (nulls last), priority (urgent>high>medium>low), title in `phase-5/backend/routes/tasks.py`
- [x] T030 [P] [US2] Add search input field, priority filter dropdown, status filter dropdown to tasks page in `phase-5/frontend/src/app/tasks/page.tsx`
- [x] T031 [P] [US2] Add due date range filter (from/to date pickers) to tasks page in `phase-5/frontend/src/app/tasks/page.tsx`
- [x] T032 [US2] Add sort dropdown (by due date, priority, created, title) with asc/desc toggle to tasks page in `phase-5/frontend/src/app/tasks/page.tsx`
- [x] T033 [US2] Update API client getTasks function to pass search, filter, sort query params in `phase-5/frontend/src/lib/api.ts`

---

## Phase 5: User Story 3 — Tags and Categories (P2)

**Goal**: Users can create tags, assign multiple tags to tasks, and filter by tag.

**Independent Test**: Create tags, assign to tasks, filter by tag, remove tag from task.

- [x] T034 [P] [US3] Create routes/tags.py with GET /api/{user_id}/tags (list), POST /api/{user_id}/tags (create), DELETE /api/{user_id}/tags/{tag_id} (delete with cascade) in `phase-5/backend/routes/tags.py`
- [x] T035 [US3] Register tags router in main.py app in `phase-5/backend/main.py`
- [x] T036 [US3] Update POST /api/{user_id}/tasks to accept tag_ids array and create task_tags associations in `phase-5/backend/routes/tasks.py`
- [x] T037 [US3] Update PUT /api/{user_id}/tasks/{id} to accept tag_ids and sync task_tags (replace existing) in `phase-5/backend/routes/tasks.py`
- [x] T038 [US3] Update GET task responses to include tags array (join task_tags + tags) in `phase-5/backend/routes/tasks.py`
- [x] T039 [P] [US3] Add Tag type and tag-related API functions (getTags, createTag, deleteTag) to frontend in `phase-5/frontend/src/lib/api.ts` and `phase-5/frontend/src/lib/types.ts`
- [x] T040 [US3] Add tag input component (create/select tags, display as badges, remove) to TaskForm and TaskEditForm in `phase-5/frontend/src/components/tasks/TaskForm.tsx` and `phase-5/frontend/src/components/tasks/TaskEditForm.tsx`
- [x] T041 [US3] Add tag filter chips to tasks page (click tag to filter) in `phase-5/frontend/src/app/tasks/page.tsx`

---

## Phase 6: User Story 4 — Recurring Tasks (P2)

**Goal**: Users create tasks with recurrence rules. Completing a recurring task auto-creates the next occurrence.

**Independent Test**: Create weekly recurring task, mark complete, verify new task created with next due date.

**Note**: The auto-creation logic is implemented here at the API level. Phase 8 (US6) will move this to an async event consumer.

- [x] T042 [US4] Add recurrence_rule JSON validation (type: daily|weekly|monthly, optional days/day_of_month) in `phase-5/backend/schemas.py`
- [x] T043 [US4] Enforce due_date required when recurrence_rule is set (validation in TaskCreate/TaskUpdate) in `phase-5/backend/schemas.py`
- [x] T044 [US4] Implement next_occurrence calculator: given recurrence_rule and current due_date, compute next due date in `phase-5/backend/routes/tasks.py` (helper function)
- [x] T045 [US4] Update PATCH /api/{user_id}/tasks/{id}/complete: when completing a recurring task, create next occurrence with updated due_date and parent_task_id link in `phase-5/backend/routes/tasks.py`
- [x] T046 [P] [US4] Add recurrence rule selector (daily/weekly/monthly + day picker for weekly) to TaskForm in `phase-5/frontend/src/components/tasks/TaskForm.tsx`
- [x] T047 [US4] Display recurrence indicator icon and next occurrence date on TaskItem in `phase-5/frontend/src/components/tasks/TaskItem.tsx`

---

## Phase 7: User Story 5 — Due Date Reminders (P2)

**Goal**: Users set reminder offsets; system generates notifications at the configured time before deadline.

**Independent Test**: Create task due in 2 minutes with 1-minute reminder offset, verify notification record created.

**Note**: For now, reminders use a simple polling or synchronous check. Phase 8-9 (US8) will migrate to Dapr Jobs API.

- [x] T048 [P] [US5] Create routes/notifications.py with GET /api/{user_id}/notifications (list, sorted by created_at desc) in `phase-5/backend/routes/notifications.py`
- [x] T049 [US5] Register notifications router in main.py in `phase-5/backend/main.py`
- [x] T050 [US5] Implement reminder check logic: when task with due_date is created/updated, if due_date - reminder_offset is in the future, schedule a notification creation (inline for now) in `phase-5/backend/routes/tasks.py`
- [x] T051 [P] [US5] Add Notification type and getNotifications API function in `phase-5/frontend/src/lib/api.ts` and `phase-5/frontend/src/lib/types.ts`
- [x] T052 [US5] Add notifications bell icon with count badge and dropdown panel to Sidebar or header in `phase-5/frontend/src/components/ui/Sidebar.tsx`

---

## Phase 8: User Story 6 — Event-Driven Task Events via Kafka (P3)

**Goal**: Task CRUD operations publish events to Kafka topics via Dapr Pub/Sub. Graceful degradation when broker is unavailable.

**Independent Test**: Create/complete a task, verify events appear on task-events topic with correct payloads.

- [x] T053 [US6] Create events.py with publish_task_event and publish_reminder_event functions using Dapr HTTP API (POST to localhost:3500/v1.0/publish/pubsub/{topic}) in `phase-5/backend/events.py`
- [x] T054 [US6] Implement graceful degradation: wrap publish calls in try/except, log failures, never fail the HTTP request in `phase-5/backend/events.py`
- [x] T055 [US6] Add event publishing calls to POST /api/{user_id}/tasks (task.created event) in `phase-5/backend/routes/tasks.py`
- [x] T056 [US6] Add event publishing calls to PUT /api/{user_id}/tasks/{id} (task.updated event) in `phase-5/backend/routes/tasks.py`
- [x] T057 [US6] Add event publishing calls to DELETE /api/{user_id}/tasks/{id} (task.deleted event) in `phase-5/backend/routes/tasks.py`
- [x] T058 [US6] Add event publishing calls to PATCH /api/{user_id}/tasks/{id}/complete (task.completed event) in `phase-5/backend/routes/tasks.py`
- [x] T059 [US6] Add reminder event publishing when task with due_date is created/updated (reminder.schedule event) in `phase-5/backend/routes/tasks.py`

---

## Phase 9: User Story 7 — Notification Service (P3)

**Goal**: A standalone microservice consumes reminder events from Kafka and creates notification records in the database.

**Independent Test**: Publish a reminder event, verify notification service logs it and stores a record in notifications table.

- [x] T060 [US7] Create notification service project structure: main.py, requirements.txt, pyproject.toml in `phase-5/services/notification/`
- [x] T061 [US7] Implement FastAPI app with POST /events/reminder endpoint (Dapr subscription callback) that creates Notification records in DB in `phase-5/services/notification/main.py`
- [x] T062 [US7] Add health check endpoint GET /health in `phase-5/services/notification/main.py`
- [x] T063 [P] [US7] Create Dockerfile for notification service (multi-stage Python build) in `phase-5/services/notification/Dockerfile`

---

## Phase 10: User Story 4+7 — Recurring Task Service (P3)

**Goal**: A standalone microservice consumes task.completed events and creates next occurrences for recurring tasks.

**Independent Test**: Complete a recurring task, verify the service creates a new task with updated due_date.

- [x] T064 [US4] Create recurring task service project structure: main.py, requirements.txt, pyproject.toml in `phase-5/services/recurring-task/`
- [x] T065 [US4] Implement FastAPI app with POST /events/task-completed endpoint that checks recurrence_rule and creates next task occurrence in DB in `phase-5/services/recurring-task/main.py`
- [x] T066 [US4] Add health check endpoint GET /health in `phase-5/services/recurring-task/main.py`
- [x] T067 [P] [US4] Create Dockerfile for recurring task service (multi-stage Python build) in `phase-5/services/recurring-task/Dockerfile`
- [ ] T068 [US4] Remove inline recurrence logic from PATCH complete handler (now handled by async consumer) in `phase-5/backend/routes/tasks.py`

---

## Phase 11: User Story 8 — Dapr Integration (P3)

**Goal**: All services use Dapr sidecars. Pub/Sub, Secrets, and Jobs API configured.

**Independent Test**: Verify Dapr components configured, events flow through Dapr pub/sub, secrets accessible via Dapr API.

- [x] T069 [US8] Create Dapr Pub/Sub component YAML (pubsub-kafka.yaml) pointing to Strimzi Kafka bootstrap in `phase-5/dapr/components/pubsub-kafka.yaml`
- [x] T070 [P] [US8] Create Dapr Secret Store component YAML (secretstore-k8s.yaml) for K8s Secrets in `phase-5/dapr/components/secretstore-k8s.yaml`
- [x] T071 [P] [US8] Create Dapr subscription for notification service (reminders topic → POST /events/reminder) in `phase-5/dapr/subscriptions/notification-sub.yaml`
- [x] T072 [P] [US8] Create Dapr subscription for recurring task service (task-events topic, filter task.completed → POST /events/task-completed) in `phase-5/dapr/subscriptions/recurring-task-sub.yaml`
- [ ] T073 [US8] Update backend events.py to use Dapr Secrets API to fetch DATABASE_URL and OPENAI_API_KEY instead of env vars (optional enhancement) in `phase-5/backend/events.py`

---

## Phase 12: User Story 9 — Minikube Deployment (P3)

**Goal**: All services, Kafka (Strimzi), and Dapr run on local Minikube cluster.

**Independent Test**: `kubectl get pods` shows all services Running with 2/2 (app + Dapr sidecar). End-to-end flow works.

- [x] T074 [US9] Create Strimzi Kafka manifests: kafka-namespace.yaml, kafka-cluster.yaml (single-replica ephemeral) in `phase-5/k8s/strimzi/`
- [x] T075 [US9] Update backend-deployment.yaml with Dapr annotations (dapr.io/enabled, dapr.io/app-id, dapr.io/app-port) in `phase-5/k8s/backend-deployment.yaml`
- [x] T076 [P] [US9] Create notification-deployment.yaml and notification-service.yaml with Dapr annotations in `phase-5/k8s/notification-deployment.yaml` and `phase-5/k8s/notification-service.yaml`
- [x] T077 [P] [US9] Create recurring-task-deployment.yaml and recurring-task-service.yaml with Dapr annotations in `phase-5/k8s/recurring-task-deployment.yaml` and `phase-5/k8s/recurring-task-service.yaml`
- [ ] T078 [US9] Update secrets.yaml with any new secrets needed in `phase-5/k8s/secrets.yaml`
- [x] T079 [US9] Update backend Dockerfile to include new files (events.py, routes/tags.py, routes/notifications.py) in `phase-5/backend/Dockerfile`
- [x] T080 [US9] Update frontend Dockerfile if needed in `phase-5/frontend/Dockerfile`
- [ ] T081 [US9] Build all Docker images in Minikube docker env (`eval $(minikube docker-env)` then docker build)
- [ ] T082 [US9] Apply Strimzi operator and Kafka cluster manifests, wait for Kafka Ready
- [ ] T083 [US9] Install Dapr on Minikube (`dapr init -k`), apply Dapr component and subscription YAMLs
- [ ] T084 [US9] Apply all K8s manifests (secrets, deployments, services) and verify all pods Running

---

## Phase 13: User Story 8+9 — Helm Chart Updates (P3)

**Goal**: Helm chart extended with new services, Dapr components, and Strimzi resources.

- [x] T085 [US9] Add notification-deployment.yaml template to Helm chart in `phase-5/helm/todo-chart/templates/notification-deployment.yaml`
- [x] T086 [P] [US9] Add recurring-task-deployment.yaml template to Helm chart in `phase-5/helm/todo-chart/templates/recurring-task-deployment.yaml`
- [x] T087 [P] [US9] Add dapr-components.yaml template to Helm chart in `phase-5/helm/todo-chart/templates/dapr-components.yaml`
- [x] T088 [US9] Update values.yaml with notification and recurring-task image configs, Kafka settings in `phase-5/helm/todo-chart/values.yaml`
- [x] T089 [US9] Update Chart.yaml version to 2.0.0 in `phase-5/helm/todo-chart/Chart.yaml`
- [ ] T090 [US9] Verify `helm install todo phase-5/helm/todo-chart/` creates all resources and `helm uninstall todo` cleans up

---

## Phase 14: MCP Tools Update

**Goal**: Update MCP tools to support new task fields so the AI chatbot can set priorities, tags, due dates via chat.

- [x] T091 Update add_task MCP tool to accept priority, due_date, reminder_offset, tag_ids parameters in `phase-5/backend/mcp_server.py`
- [x] T092 Update update_task MCP tool to accept priority, due_date, reminder_offset, tag_ids parameters in `phase-5/backend/mcp_server.py`
- [x] T093 Update list_tasks MCP tool to accept search, priority, tags filter parameters in `phase-5/backend/mcp_server.py`
- [x] T094 Add list_tags MCP tool to return user's tags in `phase-5/backend/mcp_server.py`
- [x] T095 Add list_notifications MCP tool to return user's notifications in `phase-5/backend/mcp_server.py`

---

## Phase 15: Polish & Cross-Cutting Concerns

**Goal**: Final integration verification, edge cases, documentation.

- [ ] T096 Verify all Phase IV features still work (auth, basic CRUD, chat) on phase-5 codebase
- [ ] T097 Verify graceful degradation: stop Kafka pod, confirm task CRUD still works, events logged as failed
- [ ] T098 Verify edge case: recurring task with past due_date calculates next occurrence from today
- [ ] T099 Verify edge case: recurrence_rule without due_date returns validation error
- [x] T100 Update phase-5 backend CLAUDE.md with new models, routes, events documentation in `phase-5/backend/CLAUDE.md`
- [x] T101 Update phase-5 CLAUDE.md with Dapr, Strimzi, new services documentation in `phase-5/CLAUDE.md`
- [x] T102 Update docker-compose.yml for local development (optional, non-K8s dev) in `phase-5/docker-compose.yml`

---

## Dependencies

```
Phase 1 (Setup)
  └→ Phase 2 (Foundational: models + schemas)
       ├→ Phase 3 (US1: Priority + Due Dates) ──┐
       ├→ Phase 4 (US2: Search/Filter/Sort)     │ (P1 features, can run in parallel)
       ├→ Phase 5 (US3: Tags)                   │
       └→ Phase 6 (US4: Recurring Tasks) ───────┤
           └→ Phase 7 (US5: Reminders) ─────────┤
                                                 │
       Phase 8 (US6: Kafka Events) ◄────────────┘ (depends on P1+P2 features existing)
         ├→ Phase 9 (US7: Notification Service)
         └→ Phase 10 (US4+7: Recurring Task Service)
              └→ Phase 11 (US8: Dapr Integration)
                   └→ Phase 12 (US9: Minikube Deploy)
                        └→ Phase 13 (Helm Charts)

       Phase 14 (MCP Tools) — can run after Phase 5 (US3: Tags)
       Phase 15 (Polish) — runs last
```

## Parallel Execution Opportunities

| Tasks | Why Parallel |
|-------|-------------|
| T019, T020 | Frontend types and API client — independent files |
| T030, T031 | Search input and date filter — different UI sections |
| T034, T039 | Backend tags route and frontend tags API — independent |
| T048, T051 | Backend notifications route and frontend notifications API — independent |
| T063, T067 | Notification and recurring task Dockerfiles — independent services |
| T070, T071, T072 | Dapr component YAMLs — independent files |
| T076, T077 | K8s manifests for new services — independent |
| T085, T086, T087 | Helm templates for new services — independent |

## Implementation Strategy

**MVP (Phase 1-4)**: Setup + foundational models + US1 (priorities/due dates) + US2 (search/filter/sort). This delivers the core P1 user-facing value.

**Increment 2 (Phase 5-7)**: US3 (tags) + US4 (recurring tasks) + US5 (reminders). P2 features building on the foundation.

**Increment 3 (Phase 8-13)**: US6-US9 (Kafka events, microservices, Dapr, Minikube). Infrastructure/P3 features.

**Increment 4 (Phase 14-15)**: MCP tools update + polish. Cross-cutting and verification.

## Summary

| Metric | Value |
|--------|-------|
| Total tasks | 102 |
| Setup tasks | 4 |
| Foundational tasks | 11 |
| US1 tasks | 9 |
| US2 tasks | 9 |
| US3 tasks | 8 |
| US4 tasks | 10 |
| US5 tasks | 5 |
| US6 tasks | 7 |
| US7 tasks | 4 |
| US8 tasks | 5 |
| US9 tasks | 17 |
| Helm tasks | 6 |
| MCP tasks | 5 |
| Polish tasks | 7 |
| Parallelizable tasks | 22 |
| Independent story phases | 4 (US1, US2, US3 can be parallel after Phase 2) |
