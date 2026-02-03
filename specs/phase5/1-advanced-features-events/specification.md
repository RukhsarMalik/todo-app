# Feature Specification: Advanced Features + Event Architecture

**Feature Branch**: `007-advanced-features-events`
**Created**: 2026-02-02
**Status**: Draft
**Input**: User description: "Phase V Module 1: Advanced Features + Kafka + Dapr (Local)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Task Priorities and Due Dates (Priority: P1)

A user assigns priority levels (high, medium, low) and due dates to tasks so they can focus on what matters most and track deadlines.

**Why this priority**: Core value-add that every task management user expects. Enables all downstream features (reminders, sorting, filtering by priority/date).

**Independent Test**: Can be fully tested by creating a task with priority=high and due_date=tomorrow, verifying both display correctly in the task list, and confirming the task can be updated/filtered by these fields.

**Acceptance Scenarios**:

1. **Given** a user creating a new task, **When** they set priority to "high" and due_date to "2026-02-10 15:00", **Then** the task is saved with those values and displayed with visual priority indicators.
2. **Given** a user viewing their task list, **When** tasks have different priorities, **Then** priority badges (high/medium/low) are visually distinct.
3. **Given** a user editing an existing task, **When** they change priority from "low" to "high", **Then** the update persists and the UI reflects the change immediately.
4. **Given** a user creates a task without specifying priority, **When** saved, **Then** the default priority is "medium".

---

### User Story 2 - Search, Filter, and Sort Tasks (Priority: P1)

A user searches by keyword, filters by status/priority/tags/date range, and sorts by due date, priority, or creation date to quickly find relevant tasks.

**Why this priority**: Equally critical as P1 — without search/filter/sort, advanced fields are hard to use at scale.

**Independent Test**: Can be tested by creating 10+ tasks with varied priorities, tags, and due dates, then verifying search returns partial matches, filters combine with AND logic, and sort orders are correct.

**Acceptance Scenarios**:

1. **Given** tasks with titles "Team meeting" and "Meeting prep", **When** user searches "meet", **Then** both tasks appear (case-insensitive partial match).
2. **Given** tasks with priorities high, medium, low, **When** user filters by priority=high, **Then** only high-priority tasks appear.
3. **Given** tasks with various due dates, **When** user sorts by due_date ascending, **Then** tasks appear in chronological order with null due dates last.
4. **Given** user applies filter status=pending AND priority=high AND tags=work, **When** results load, **Then** only tasks matching all three criteria appear.
5. **Given** user filters by due_date_from=2026-02-01 and due_date_to=2026-02-28, **When** results load, **Then** only tasks within that date range appear.

---

### User Story 3 - Tags and Categories (Priority: P2)

A user assigns multiple tags (work, home, personal, urgent) to tasks and filters tasks by tag to organize their workflow.

**Why this priority**: Enhances organization but not blocking for core task management. Requires a many-to-many relationship (tags table + junction table).

**Independent Test**: Can be tested by creating tags, assigning multiple tags to a task, and filtering the task list by a specific tag.

**Acceptance Scenarios**:

1. **Given** a user on the task creation form, **When** they add tags "work" and "urgent", **Then** the task is saved with both tags and they display as badges.
2. **Given** a user viewing their tags, **When** they call the tags endpoint, **Then** they see all tags they have created.
3. **Given** a user filtering by tag "work", **When** results load, **Then** only tasks tagged "work" appear.
4. **Given** a user removing a tag from a task, **When** saved, **Then** the tag association is removed but the tag itself still exists for reuse.

---

### User Story 4 - Recurring Tasks (Priority: P2)

A user creates tasks that recur on a schedule (daily, weekly, monthly). When a recurring task is completed, the system automatically creates the next occurrence.

**Why this priority**: High user value for habitual tasks. Depends on the event architecture to auto-create next occurrences asynchronously.

**Independent Test**: Can be tested by creating a weekly recurring task, marking it complete, and verifying a new task appears with the next due date.

**Acceptance Scenarios**:

1. **Given** a user creates a task with recurrence_rule {"type": "weekly", "days": ["Monday"]}, **When** they mark it complete on Monday, **Then** a new task is automatically created for next Monday.
2. **Given** a daily recurring task, **When** completed today, **Then** next occurrence is created for tomorrow.
3. **Given** a monthly recurring task set for the 1st, **When** completed on Feb 1, **Then** next occurrence is created for Mar 1.
4. **Given** a recurring task is deleted (not completed), **When** the deletion occurs, **Then** no new occurrence is created.

---

### User Story 5 - Due Date Reminders (Priority: P2)

A user sets a reminder offset on a task with a due date. The system sends a notification at the configured time before the deadline.

**Why this priority**: Depends on event architecture and notification service. High value but requires Dapr Jobs API integration.

**Independent Test**: Can be tested by creating a task due in 2 minutes with a 1-minute reminder offset, then verifying a notification is generated 1 minute before the due time.

**Acceptance Scenarios**:

1. **Given** a task due at 3:00 PM with reminder_offset=60 minutes, **When** the clock reaches 2:00 PM, **Then** a notification is generated for the user.
2. **Given** a task with no due_date, **When** saved, **Then** no reminder is scheduled.
3. **Given** a task's due_date is updated, **When** saved, **Then** the existing reminder is rescheduled to the new time.
4. **Given** the default reminder_offset, **When** a user creates a task with due_date but no explicit offset, **Then** the offset defaults to 60 minutes.

---

### User Story 6 - Event-Driven Task Events via Kafka (Priority: P3)

When tasks are created, updated, deleted, or completed, the system publishes events to a message broker. Downstream services (notification, recurring task) consume these events asynchronously.

**Why this priority**: Infrastructure story — enables US-4 and US-5 automation but is not directly user-facing.

**Independent Test**: Can be tested by creating/completing a task and verifying events appear on the appropriate topics with correct payloads.

**Acceptance Scenarios**:

1. **Given** a user creates a task, **When** saved, **Then** an event `{event_type: "created", task_id, task_data, user_id, timestamp}` is published to the task-events topic.
2. **Given** a user completes a task, **When** status changes to complete, **Then** an event `{event_type: "completed", ...}` is published.
3. **Given** a task with a due_date is created, **When** saved, **Then** a reminder event is published to the reminders topic.
4. **Given** the message broker is temporarily unavailable, **When** an event fails to publish, **Then** the task operation still succeeds and the event is retried or logged.

---

### User Story 7 - Notification Service (Priority: P3)

A microservice consumes reminder events and generates user notifications. For the hackathon scope, notifications are logged to console and stored in a notifications table.

**Why this priority**: Consumer service that depends on Kafka and Dapr being operational. Demonstrates the event architecture end-to-end.

**Independent Test**: Can be tested by publishing a reminder event and verifying the notification service logs it and stores a record in the notifications table.

**Acceptance Scenarios**:

1. **Given** a reminder event on the reminders topic, **When** the notification service consumes it, **Then** a notification record is created with task title, user_id, and timestamp.
2. **Given** a user queries their notifications, **When** they call the notifications endpoint, **Then** they see a list of their recent notifications.

---

### User Story 8 - Dapr Integration for Pub/Sub, State, Jobs, and Secrets (Priority: P3)

All inter-service communication uses Dapr sidecars. The backend publishes events via Dapr Pub/Sub (backed by Kafka). Reminders are scheduled via Dapr Jobs API. Secrets are accessed via Dapr Secrets API (backed by K8s Secrets).

**Why this priority**: Infrastructure layer that simplifies service communication but is transparent to end users.

**Independent Test**: Can be tested by verifying Dapr components are configured, events flow through Dapr pub/sub, and secrets are accessible via the Dapr API.

**Acceptance Scenarios**:

1. **Given** Dapr is initialized on Minikube, **When** the backend publishes to topic "task-events", **Then** the event is delivered via Dapr pub/sub to subscribing services.
2. **Given** a scheduled reminder via Dapr Jobs API, **When** the trigger time arrives, **Then** Dapr calls the configured callback endpoint.
3. **Given** secrets stored in K8s Secrets, **When** a service requests them via Dapr Secrets API, **Then** the secret values are returned without direct K8s API access.

---

### User Story 9 - Minikube Deployment (Priority: P3)

All services (frontend, backend, notification service, recurring task service), Kafka (Strimzi), and Dapr run on a local Minikube cluster.

**Why this priority**: Deployment concern — needed for demo but not for feature logic development.

**Independent Test**: Can be tested by running `kubectl get pods` and verifying all services are running, then performing an end-to-end flow (create task with due date → event published → reminder triggered → notification logged).

**Acceptance Scenarios**:

1. **Given** Minikube is running, **When** all manifests are applied, **Then** frontend, backend, notification service, recurring task service, Kafka, and Dapr sidecars are all in Running state.
2. **Given** the full stack is deployed, **When** a user creates a recurring task with a due date via the frontend, **Then** the complete flow works end-to-end (event published, reminder scheduled, notification generated, next occurrence created on completion).

---

### Edge Cases

- What happens when a recurring task has a due_date in the past? The next occurrence should be calculated from today, not from the past date.
- How does the system handle a task with recurrence_rule but no due_date? The system should require due_date when recurrence_rule is set.
- What happens when a user deletes a tag that is assigned to tasks? The tag-task associations are removed (cascade), but tasks remain.
- What if two filters return contradictory results (e.g., status=completed AND status=pending)? Return empty results — AND logic means both must match.
- What happens when Kafka is down? Task CRUD operations succeed; events are logged as failed and can be retried. The system degrades gracefully.
- What if reminder_offset is larger than the time until due_date? The reminder fires immediately (or is skipped if due_date is already past).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to set task priority as high, medium, or low (default: medium).
- **FR-002**: System MUST allow users to set a due_date (datetime, nullable) on tasks.
- **FR-003**: System MUST allow users to set a reminder_offset (minutes before due, default: 60) on tasks with due dates.
- **FR-004**: System MUST allow users to define recurrence rules (daily, weekly, monthly) on tasks as a JSON structure.
- **FR-005**: System MUST automatically create the next occurrence of a recurring task when the current one is marked complete.
- **FR-006**: System MUST support creating, listing, and assigning multiple tags per task via a many-to-many relationship.
- **FR-007**: System MUST support keyword search across task title and description (case-insensitive, partial match).
- **FR-008**: System MUST support filtering tasks by status, priority, tags, and due_date range with AND logic.
- **FR-009**: System MUST support sorting tasks by due_date, priority, created_at, or title in ascending or descending order (default: created_at desc).
- **FR-010**: System MUST publish events to a message broker when tasks are created, updated, deleted, or completed.
- **FR-011**: System MUST publish reminder events for tasks with due dates, scheduled at due_time minus reminder_offset.
- **FR-012**: A notification service MUST consume reminder events and store notification records.
- **FR-013**: A recurring task service MUST consume task completion events and create next occurrences for recurring tasks.
- **FR-014**: All inter-service event communication MUST use Dapr Pub/Sub backed by Kafka.
- **FR-015**: Reminder scheduling MUST use Dapr Jobs API for time-based triggers.
- **FR-016**: Sensitive configuration (database URLs, API keys) MUST be accessed via Dapr Secrets API backed by K8s Secrets.
- **FR-017**: All services MUST be deployable on a local Minikube cluster.
- **FR-018**: Task CRUD operations MUST succeed even if the event broker is temporarily unavailable (graceful degradation).

### Key Entities

- **Task** (extended): Existing task entity gains due_date, priority, recurrence_rule, and reminder_offset fields. Core entity for all features.
- **Tag**: A label (name) owned by a user. Many-to-many relationship with tasks via a junction table.
- **TaskTag**: Junction entity linking tasks to tags.
- **Notification**: A record of a triggered reminder, containing task reference, user, message, and timestamp.
- **TaskEvent**: An event payload published to the message broker, containing event_type, task_id, task_data, user_id, and timestamp.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a task with priority, due date, tags, and recurrence in a single form submission.
- **SC-002**: Search returns relevant results for partial keyword matches within 2 seconds.
- **SC-003**: Filters (status, priority, tags, date range) correctly narrow results with AND logic — zero false positives.
- **SC-004**: Sorting by any supported field produces correctly ordered results in ascending or descending order.
- **SC-005**: Completing a recurring task automatically creates the next occurrence within 10 seconds.
- **SC-006**: Reminders fire within 1 minute of the scheduled reminder time.
- **SC-007**: Notification records are persisted for all triggered reminders — zero missed notifications under normal operation.
- **SC-008**: All services (frontend, backend, notification, recurring task, Kafka, Dapr) run simultaneously on Minikube with all pods in Running state.
- **SC-009**: Task CRUD operations succeed with sub-second response times even when the event broker is temporarily unavailable.
- **SC-010**: End-to-end demo: create recurring task with due date → complete it → verify next occurrence created AND reminder notification logged.

## Assumptions

- Phase IV (K8s on Minikube) is complete and the existing frontend/backend are deployable on Minikube.
- Neon PostgreSQL (external) remains the database — no local PostgreSQL needed.
- For hackathon scope, notifications are console logs + database records (no email/SMS/push integration).
- Dapr Jobs API is available in the Dapr version installed on Minikube.
- Strimzi operator supports single-replica ephemeral Kafka suitable for local development.
- The existing task API uses the pattern `/api/{user_id}/tasks` and this is preserved.

## Scope

### In Scope

- Advanced task fields: priority, due_date, reminder_offset, recurrence_rule
- Tags/categories with many-to-many relationship
- Search, filter, and sort on the tasks endpoint
- Kafka cluster (Strimzi) on Minikube with topics: task-events, reminders
- Event publishing on task CRUD operations
- Notification microservice (consumer)
- Recurring task microservice (consumer)
- Dapr integration: Pub/Sub, State (optional), Jobs API, Secrets
- Frontend updates for new fields, search, filter, sort UI
- Full Minikube deployment of all services

### Out of Scope

- Cloud deployment (Phase V Module 2)
- CI/CD pipelines (Phase V Module 2)
- Real email/SMS/push notifications (hackathon: console + DB only)
- Task sharing or collaboration between users
- File attachments on tasks
- Subtasks or task dependencies
