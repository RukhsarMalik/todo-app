# Research: Advanced Features + Event Architecture

**Feature**: 007-advanced-features-events | **Date**: 2026-02-02

## Research Topics

### 1. Strimzi Kafka on Minikube

**Decision**: Use Strimzi operator with a single-replica ephemeral Kafka cluster.

**Rationale**: Strimzi is the standard Kubernetes operator for Apache Kafka. Single-replica ephemeral mode is sufficient for local development and avoids PVC requirements on Minikube.

**Alternatives considered**:
- **Confluent Platform Helm chart**: Heavier, designed for production. Overkill for local dev.
- **Kafka Docker container outside K8s**: Defeats the purpose of running everything on Minikube.
- **Redpanda on K8s**: Lighter than Kafka but less ecosystem tooling. Better suited for cloud (Module 2).

**Setup**:
```bash
# Install Strimzi operator
kubectl create namespace kafka
kubectl apply -f https://strimzi.io/install/latest?namespace=kafka -n kafka

# Create ephemeral Kafka cluster
kubectl apply -f kafka-cluster.yaml -n kafka
```

### 2. Dapr on Minikube

**Decision**: Use Dapr CLI (`dapr init -k`) for Kubernetes installation. Use Pub/Sub, Secrets, and Jobs building blocks.

**Rationale**: Dapr provides a uniform API layer over infrastructure. Pub/Sub abstracts Kafka; Secrets abstracts K8s Secrets; Jobs API provides scheduled callbacks without custom cron code.

**Alternatives considered**:
- **Direct Kafka SDK (confluent-kafka-python)**: Tighter coupling; code changes needed when switching brokers.
- **Celery + Redis for scheduling**: More complex; doesn't integrate with K8s natively.
- **CloudEvents SDK directly**: Lower-level than Dapr; Dapr adds routing, retries, and dead-letter support.

**Key Dapr components needed**:
- `pubsub-kafka`: Pub/Sub backed by Strimzi Kafka
- `secretstore-kubernetes`: Reads K8s Secrets via Dapr API
- Dapr Jobs API: Scheduled one-time callbacks for reminders

### 3. Event Schema Design

**Decision**: Use CloudEvents-compatible JSON payloads published via Dapr Pub/Sub HTTP API.

**Rationale**: Dapr Pub/Sub uses CloudEvents by default. This provides standardized envelope with `type`, `source`, `id`, `time`, and `data` fields.

**Event types**:
| Event Type | Topic | Published When | Consumer |
|------------|-------|----------------|----------|
| `task.created` | task-events | Task created | (future analytics) |
| `task.updated` | task-events | Task updated | (future analytics) |
| `task.completed` | task-events | Task marked complete | Recurring Task Service |
| `task.deleted` | task-events | Task deleted | (future cleanup) |
| `reminder.schedule` | reminders | Task with due_date created/updated | Notification Service |

### 4. Tags Implementation Pattern

**Decision**: Separate `tags` table with `task_tags` junction table (many-to-many).

**Rationale**: Proper relational modeling enables: indexed queries by tag, tag reuse across tasks, user-scoped tags, and clean deletion semantics.

**Alternatives considered**:
- **JSONB array on tasks**: Simpler but no indexing, no tag reuse, harder to query "all tasks with tag X".
- **PostgreSQL array type**: Better than JSONB for simple lists but still no FK integrity.

### 5. Recurring Task Strategy

**Decision**: On task completion, a consumer service creates the next occurrence by copying the task with an updated due_date calculated from the recurrence_rule.

**Rationale**: Separating recurrence logic into its own service keeps the main backend simple. The consumer pattern means recurrence happens asynchronously and doesn't slow down the completion request.

**Recurrence rule format**:
```json
{"type": "daily"}
{"type": "weekly", "days": ["Monday", "Wednesday"]}
{"type": "monthly", "day_of_month": 1}
```

**Next occurrence calculation**:
- `daily`: due_date + 1 day
- `weekly`: next matching weekday from today
- `monthly`: same day next month (handle month-end edge cases)

### 6. Graceful Degradation Pattern

**Decision**: Wrap all Dapr publish calls in try/except. Log failures but do not fail the HTTP request.

**Rationale**: Constitution principle FR-018 requires CRUD to succeed even if the event broker is unavailable.

**Implementation**:
```python
async def publish_event(topic: str, event: dict) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"http://localhost:3500/v1.0/publish/pubsub/{topic}",
                json=event,
                timeout=5.0
            )
            return resp.status_code == 204
    except Exception as e:
        logger.warning(f"Failed to publish event to {topic}: {e}")
        return False
```

### 7. Dapr Jobs API for Reminders

**Decision**: Use Dapr Jobs API to schedule one-time callbacks at `due_date - reminder_offset`.

**Rationale**: Dapr Jobs provides a simple HTTP API for scheduling callbacks. No need for a separate scheduler service or cron system.

**Flow**:
1. Backend creates task with due_date and reminder_offset
2. Backend calls Dapr Jobs API to schedule callback at `due_date - reminder_offset_minutes`
3. When triggered, Dapr calls the notification service endpoint
4. Notification service creates a notification record

**Alternative considered**:
- **Polling loop**: Check every minute for upcoming reminders. Simpler but wastes resources and has up to 1-minute delay.
- **Dapr Bindings with cron**: Only for recurring schedules, not one-time.
