# Data Model: Backend API

**Feature**: 003-backend-api
**Date**: 2026-01-18
**Status**: Complete

## Entity Overview

This module uses the Task entity from Module 1 and adds Pydantic schemas for API request/response validation.

## Existing Entity (Module 1)

### Task (SQLModel)

**Source**: `phase-2/backend/models.py`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | int | Primary Key, auto-increment | Unique task identifier |
| user_id | str | Required, indexed, max 255 | Owner reference |
| title | str | Required, 1-200 chars | Task title |
| description | str | Optional, max 1000 chars | Task details |
| completed | bool | Default: False | Completion status |
| created_at | datetime | Auto-set, UTC | Creation timestamp |
| updated_at | datetime | Auto-set, UTC | Last modification |

**Table Name**: `tasks`
**Indexes**: `user_id`, `completed`

## API Schemas (New in Module 2)

### TaskCreate (Request)

**Purpose**: Input for POST /api/{user_id}/tasks

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| title | str | Yes | min_length=1, max_length=200 |
| description | str | No | max_length=1000 |

```python
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
```

### TaskUpdate (Request)

**Purpose**: Input for PUT /api/{user_id}/tasks/{id}

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| title | str | No | min_length=1, max_length=200 |
| description | str | No | max_length=1000 |

**Note**: At least one field should be provided (validated in endpoint logic)

```python
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
```

### TaskToggle (Request)

**Purpose**: Input for PATCH /api/{user_id}/tasks/{id}/complete

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| completed | bool | Yes | Must be boolean |

```python
class TaskToggle(BaseModel):
    completed: bool
```

### TaskResponse (Response)

**Purpose**: Output for all task endpoints

| Field | Type | Source |
|-------|------|--------|
| id | int | Task.id |
| user_id | str | Task.user_id |
| title | str | Task.title |
| description | str | None | Task.description |
| completed | bool | Task.completed |
| created_at | datetime | Task.created_at |
| updated_at | datetime | Task.updated_at |

```python
class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

## Query Parameters Schema

### TaskListParams

**Purpose**: Query parameters for GET /api/{user_id}/tasks

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| status | str | "all" | "all", "pending", "completed" |
| sort | str | "created" | "created", "title" |
| order | str | "desc" | "asc", "desc" |

```python
class StatusFilter(str, Enum):
    all = "all"
    pending = "pending"
    completed = "completed"

class SortField(str, Enum):
    created = "created"
    title = "title"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"
```

## State Transitions

### Task Lifecycle

```
Created (completed=False)
    │
    ├── Toggle → Completed (completed=True)
    │               │
    │               └── Toggle → Incomplete (completed=False)
    │
    ├── Update → Modified (updated_at changes)
    │
    └── Delete → Removed (permanent)
```

## Relationships

```
User (external, Better Auth)
  │
  └── 1:N ──> Task
              │
              └── All operations filtered by user_id
                  Deleting user cascades task deletion
```

**Note**: User entity managed by Better Auth in Module 3. Currently user_id is accepted without verification.

## Validation Rules Summary

| Rule | Enforced By | Error Code |
|------|-------------|------------|
| Title required | Pydantic | 422 |
| Title 1-200 chars | Pydantic | 422 |
| Description max 1000 | Pydantic | 422 |
| Task ownership | Endpoint logic | 404 |
| Task exists | Endpoint logic | 404 |
| Completed is boolean | Pydantic | 422 |
