# Data Model: Advanced Features + Event Architecture

**Feature**: 007-advanced-features-events | **Date**: 2026-02-02

## Entity Relationship

```
users 1──* tasks
users 1──* tags
users 1──* notifications
tasks *──* tags (via task_tags)
tasks 1──* notifications
tasks 1──* tasks (parent_task_id self-reference for recurrence chain)
```

## Table: tasks (EXTENDED)

Existing columns unchanged. New columns added:

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| priority | VARCHAR(10) | NO | 'medium' | low, medium, high, urgent |
| due_date | TIMESTAMP | YES | NULL | Task deadline |
| reminder_offset | INTEGER | NO | 60 | Minutes before due_date for reminder |
| recurrence_rule | JSONB | YES | NULL | e.g., {"type":"weekly","days":["Monday"]} |
| next_occurrence | TIMESTAMP | YES | NULL | Computed next due date for recurring tasks |
| parent_task_id | INTEGER | YES | NULL | FK to tasks.id — links recurrence chain |

**New indexes**:
- `idx_tasks_priority` on (priority)
- `idx_tasks_due_date` on (due_date)
- `idx_tasks_parent_task_id` on (parent_task_id)

**Validation rules**:
- `priority` must be one of: low, medium, high, urgent
- `reminder_offset` must be >= 0
- `recurrence_rule` must be valid JSON matching schema: `{"type": "daily"|"weekly"|"monthly", ...}`
- If `recurrence_rule` is set, `due_date` MUST be set (enforced at API layer)

## Table: tags (NEW)

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | INTEGER | NO | auto-increment | Primary key |
| user_id | VARCHAR(255) | NO | — | FK to users.id |
| name | VARCHAR(100) | NO | — | Tag name |
| created_at | TIMESTAMP | NO | NOW() | Creation timestamp |

**Indexes**:
- `idx_tags_user_id` on (user_id)
- `uq_tags_user_name` UNIQUE on (user_id, name) — no duplicate tag names per user

## Table: task_tags (NEW)

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| task_id | INTEGER | NO | — | FK to tasks.id ON DELETE CASCADE |
| tag_id | INTEGER | NO | — | FK to tags.id ON DELETE CASCADE |

**Primary key**: (task_id, tag_id) — composite
**Indexes**: Composite PK serves as index

## Table: notifications (NEW)

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | INTEGER | NO | auto-increment | Primary key |
| user_id | VARCHAR(255) | NO | — | FK to users.id |
| task_id | INTEGER | YES | NULL | FK to tasks.id ON DELETE SET NULL |
| message | TEXT | NO | — | Notification message |
| read | BOOLEAN | NO | false | Whether user has read it |
| created_at | TIMESTAMP | NO | NOW() | Creation timestamp |

**Indexes**:
- `idx_notifications_user_id` on (user_id)
- `idx_notifications_created_at` on (created_at)

## SQLModel Definitions

```python
from enum import Enum

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

# Extended Task model — new fields added to existing Task class
class Task(SQLModel, table=True):
    # ... existing fields ...
    priority: str = Field(default="medium", max_length=10)
    due_date: Optional[datetime] = Field(default=None)
    reminder_offset: int = Field(default=60)
    recurrence_rule: Optional[dict] = Field(default=None, sa_type=JSON)
    next_occurrence: Optional[datetime] = Field(default=None)
    parent_task_id: Optional[int] = Field(default=None, foreign_key="tasks.id")

class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(max_length=255, index=True, nullable=False)
    name: str = Field(max_length=100, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskTag(SQLModel, table=True):
    __tablename__ = "task_tags"
    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)

class Notification(SQLModel, table=True):
    __tablename__ = "notifications"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(max_length=255, index=True, nullable=False)
    task_id: Optional[int] = Field(default=None, foreign_key="tasks.id")
    message: str = Field(nullable=False)
    read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
```

## Event Schemas (CloudEvents via Dapr)

### TaskEvent (published to topic: task-events)

```json
{
  "specversion": "1.0",
  "type": "task.created",
  "source": "/api/tasks",
  "id": "uuid",
  "time": "2026-02-02T12:00:00Z",
  "data": {
    "task_id": 1,
    "user_id": "uuid-string",
    "title": "Buy groceries",
    "priority": "high",
    "due_date": "2026-02-10T15:00:00Z",
    "recurrence_rule": null,
    "completed": false
  }
}
```

### ReminderEvent (published to topic: reminders)

```json
{
  "specversion": "1.0",
  "type": "reminder.schedule",
  "source": "/api/tasks",
  "id": "uuid",
  "time": "2026-02-02T12:00:00Z",
  "data": {
    "task_id": 1,
    "user_id": "uuid-string",
    "title": "Buy groceries",
    "due_date": "2026-02-10T15:00:00Z",
    "reminder_time": "2026-02-10T14:00:00Z"
  }
}
```
