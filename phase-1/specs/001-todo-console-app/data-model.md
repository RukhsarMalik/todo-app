# Data Model: Todo Console App (Phase I)

**Date**: 2025-12-25
**Context**: In-memory CLI todo application with 5 core operations

## Overview

This document defines the data structures, validation rules, and state transitions for the Phase I todo application. The model is intentionally simple: a single Task entity managed by an in-memory collection.

## Entity: Task

### Purpose
Represents a single todo item that users want to track and manage through the CLI application.

### Structure

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    """A single todo item with title, description, and completion status.

    Attributes:
        id: Unique sequential identifier (auto-generated, never reused)
        title: Short descriptive text (required, 1-200 characters)
        description: Optional detailed information (max 1000 characters)
        completed: Completion status (default False, toggleable)
        created_at: Timestamp when task was created (auto-generated)
    """
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
```

### Field Specifications

| Field | Type | Required | Default | Validation | Notes |
|-------|------|----------|---------|------------|-------|
| `id` | int | Yes | Auto-generated | Must be unique, sequential, > 0 | Never reused after deletion |
| `title` | str | Yes | None | 1-200 chars (after trim), non-empty | Trimmed before storage |
| `description` | str | No | "" | Max 1000 chars (after trim) | Empty string if not provided |
| `completed` | bool | Yes | False | Must be True or False | Toggleable via user action |
| `created_at` | datetime | Yes | Auto-generated | Valid datetime object | Set on task creation |

### Validation Rules

#### Title Validation
**Purpose**: Ensure tasks have meaningful, readable titles

**Rules**:
1. **Non-empty**: After trimming whitespace, title must have ≥ 1 character
2. **Maximum length**: After trimming, title must have ≤ 200 characters
3. **Whitespace handling**: Leading and trailing whitespace automatically trimmed
4. **Character preservation**: Unicode, special chars, quotes preserved after trim
5. **Case preservation**: Exact case as entered by user

**Error Messages**:
- Empty/whitespace-only: `"Title cannot be empty. Please enter a task title (1-200 characters)."`
- Too long: `"Title too long. Maximum 200 characters allowed. Current length: {len}"`

**Examples**:
- ✅ Valid: `"Buy groceries"` → Stored as-is
- ✅ Valid: `"  Call dentist  "` → Stored as `"Call dentist"` (trimmed)
- ✅ Valid: `"Finish report 📝"` → Stored with emoji (unicode preserved)
- ✅ Valid: `"Review "Project X" document"` → Stored with quotes
- ❌ Invalid: `""` (empty string)
- ❌ Invalid: `"   "` (whitespace only)
- ❌ Invalid: 201-character title (exceeds max)

#### Description Validation
**Purpose**: Allow optional detailed task information

**Rules**:
1. **Optional**: Empty string allowed (description not required)
2. **Maximum length**: After trimming, description must have ≤ 1000 characters
3. **Whitespace handling**: Leading and trailing whitespace automatically trimmed
4. **Newlines allowed**: Multiline descriptions supported (displayed as-is)
5. **Character preservation**: Unicode, special chars preserved

**Error Messages**:
- Too long: `"Description too long. Maximum 1000 characters allowed. Current length: {len}"`

**Examples**:
- ✅ Valid: `""` (empty, description optional)
- ✅ Valid: `"Milk, eggs, bread"` → Stored as-is
- ✅ Valid: `"Line 1\nLine 2\nLine 3"` → Multiline preserved
- ✅ Valid: 1000-character description (exactly at max)
- ❌ Invalid: 1001-character description (exceeds max)

#### ID Validation
**Purpose**: Ensure valid task references for operations

**Rules**:
1. **Numeric**: Must parse to integer
2. **Positive**: Must be > 0
3. **Existence**: Must correspond to existing task in collection (for update/delete/toggle)
4. **Uniqueness**: Auto-generated IDs guaranteed unique by TaskManager

**Error Messages**:
- Non-numeric: `"Invalid task ID. Please enter a numeric ID."`
- Not found: `"Task #{id} not found. Use 'View Tasks' to see valid task IDs."`

**Examples**:
- ✅ Valid: `"1"`, `"5"`, `"100"` (if tasks exist)
- ❌ Invalid: `"abc"` (non-numeric)
- ❌ Invalid: `"1.5"` (not an integer)
- ❌ Invalid: `"0"` (IDs start at 1)
- ❌ Invalid: `"-5"` (negative)
- ❌ Invalid: `"999"` (ID doesn't exist in collection)

#### Completed Status
**Purpose**: Track task completion state

**Rules**:
1. **Binary**: Only True (completed) or False (pending) allowed
2. **Default**: New tasks created with `completed = False`
3. **Toggleable**: Can switch between True ↔ False repeatedly
4. **Independent**: Status changes don't affect other fields

**Display Representation**:
- `completed = False` → Display as `[ ]` (pending)
- `completed = True` → Display as `[✓]` (completed)

---

## State Transitions

### Task Lifecycle

```
┌─────────────────────────────────────────────────┐
│              Task Lifecycle                     │
└─────────────────────────────────────────────────┘

   [User Action: Add Task]
            ↓
   ┌─────────────────────┐
   │  Task Created       │
   │  completed = False  │
   │  id = auto-gen      │
   │  created_at = now   │
   └──────────┬──────────┘
              │
              ↓
   ┌─────────────────────┐
   │  Pending State      │
   │  [ ] displayed      │
   └──────────┬──────────┘
              │
              │ [User Action: Toggle Status]
              ↓
   ┌─────────────────────┐
   │  Completed State    │
   │  [✓] displayed      │
   └──────────┬──────────┘
              │
              │ [User Action: Toggle Status]
              ↓
   ┌─────────────────────┐
   │  Pending State      │
   │  [ ] displayed      │
   │  (repeatable cycle) │
   └──────────┬──────────┘
              │
              │ [User Action: Update Task]
              ↓
   ┌─────────────────────┐
   │  Same State         │
   │  title/desc changed │
   │  completed unchanged│
   └──────────┬──────────┘
              │
              │ [User Action: Delete Task]
              ↓
   ┌─────────────────────┐
   │  Task Removed       │
   │  ID NOT REUSED      │
   └─────────────────────┘
```

### Operation Effects

| Operation | Fields Modified | Fields Unchanged | ID Reuse |
|-----------|----------------|------------------|----------|
| **Add** | All fields set (id auto-gen, created_at now, completed False) | N/A (new task) | Next sequential ID assigned |
| **View** | None (read-only) | All | N/A |
| **Update** | title and/or description | id, completed, created_at | N/A |
| **Toggle** | completed (inverted) | id, title, description, created_at | N/A |
| **Delete** | Task removed from collection | N/A | ID NEVER reused |

### State Invariants

**Must always be true**:
1. All task IDs in collection are unique
2. All task IDs are positive integers > 0
3. All task IDs are sequential from creation order (gaps allowed after deletion)
4. All task titles are non-empty strings (1-200 chars)
5. All task descriptions are strings (0-1000 chars, empty allowed)
6. All task `completed` values are boolean (True or False)
7. All task `created_at` values are valid datetime objects
8. Tasks are stored in creation order (oldest first)

**Violations indicate bugs** - should be caught during implementation testing.

---

## Data Storage

### In-Memory Collection

**Structure**:
```python
class TaskManager:
    def __init__(self) -> None:
        self._tasks: list[Task] = []      # Ordered collection
        self._next_id: int = 1            # Never decremented
```

**Storage Characteristics**:
- **Type**: Python list (preserves insertion order)
- **Capacity**: Unlimited (Python memory limit), practical limit <1000 tasks
- **Persistence**: None (data lost on program exit per Phase I constraints)
- **Concurrency**: Single-threaded (one user, no concurrent access)

### ID Management

**ID Assignment**:
```python
def add_task(self, title: str, description: str = "") -> Task:
    task = Task(
        id=self._next_id,
        title=title,
        description=description,
        completed=False,
        created_at=datetime.now()
    )
    self._tasks.append(task)
    self._next_id += 1  # Increment ALWAYS (never reuse)
    return task
```

**Key Points**:
- `_next_id` starts at 1 (first task gets ID 1)
- `_next_id` increments on every add (even if previous IDs deleted)
- Deleted IDs create "gaps" in sequence (e.g., 1, 2, 4, 5 if ID 3 deleted)
- This prevents confusion (user sees ID 5 deleted, then ID 6 created, not ID 5 reused)

### Task Retrieval

**By ID** (for update/delete/toggle):
```python
def get_task_by_id(self, task_id: int) -> Task | None:
    for task in self._tasks:
        if task.id == task_id:
            return task
    return None  # Not found
```

**All Tasks** (for view):
```python
def get_all_tasks(self) -> list[Task]:
    return self._tasks.copy()  # Return copy to prevent external modification
```

---

## Display Format

### Task List Display

**Format Specification**:
```
=== Your Tasks ===

[✓] 1. Buy groceries
    Milk, eggs, bread
    Created: 2025-12-25 10:30:45

[ ] 2. Call dentist
    Schedule annual checkup
    Created: 2025-12-25 10:31:12

[✓] 5. Finish report
    Include Q4 metrics and analysis
    Created: 2025-12-25 10:35:00

---
Total: 3 tasks (2 completed, 1 pending)
```

**Display Rules**:
1. **Status indicator**: `[✓]` for completed, `[ ]` for pending
2. **Task line**: Status + ID + period + title
3. **Description line**: Indented (4 spaces), shown if non-empty
4. **Created timestamp**: Indented, formatted as "Created: YYYY-MM-DD HH:MM:SS"
5. **Separator**: Blank line between tasks
6. **Summary**: Total count + breakdown (completed/pending)

**Empty List Display**:
```
=== Your Tasks ===

No tasks found. Add your first task to get started!
```

### Single Task Display (for confirmations)

**Format** (used in delete confirmation):
```
Task #5: Finish report
Description: Include Q4 metrics and analysis
Status: Completed
```

---

## Data Relationships

### Entity Relationship Diagram

```
┌─────────────────────────────────────────┐
│           TaskManager                   │
│  - _tasks: list[Task]                   │
│  - _next_id: int                        │
│                                         │
│  + add_task(title, desc) -> Task       │
│  + get_all_tasks() -> list[Task]       │
│  + get_task_by_id(id) -> Task | None   │
│  + update_task(id, ...) -> bool        │
│  + delete_task(id) -> bool             │
│  + toggle_task_status(id) -> bool      │
└──────────────┬──────────────────────────┘
               │
               │ contains (1:N)
               │
               ↓
      ┌─────────────────┐
      │      Task       │
      │  - id: int      │
      │  - title: str   │
      │  - description  │
      │  - completed    │
      │  - created_at   │
      └─────────────────┘
```

**Relationship Type**: Composition (TaskManager owns Tasks)
- TaskManager created → empty task list
- TaskManager destroyed → all tasks destroyed (in-memory only)
- Tasks cannot exist outside TaskManager context (no global task registry)

**Cardinality**: One-to-Many (1:N)
- One TaskManager manages N tasks (0 to unlimited)
- Each Task belongs to exactly one TaskManager instance

---

## Validation Summary

### Pre-Storage Validation (in validators module)

All user inputs validated BEFORE creating/modifying Task objects:

```python
# Title validation
is_valid, error_msg, trimmed_title = validate_title(user_input)
if not is_valid:
    print(error_msg)
    # Re-prompt user

# Description validation
is_valid, error_msg, trimmed_desc = validate_description(user_input)
if not is_valid:
    print(error_msg)
    # Re-prompt user
```

### Post-Storage Invariants (TaskManager enforces)

TaskManager guarantees:
- No duplicate IDs (auto-generation ensures uniqueness)
- IDs never reused (counter never decrements)
- All stored tasks pass field validation (validated before storage)
- List ordering preserved (tasks in creation order)

---

## Future Considerations (Out of Scope for Phase I)

**Phase II/III Enhancements** (not implemented now):
- **Categories/Tags**: Add `tags: list[str]` field for organization
- **Priority**: Add `priority: int` (1-5) field for importance ranking
- **Due Dates**: Add `due_date: datetime | None` for deadlines
- **Persistence**: Serialize to JSON/SQLite for data retention
- **Relationships**: Parent/child tasks for subtasks hierarchy
- **Audit Trail**: Track all changes (who, when, what changed)
- **Search**: Full-text search across titles and descriptions
- **Archival**: Soft delete (is_archived) instead of hard delete

**Data Model Evolution**:
- Phase I: Simple Task dataclass (5 fields, in-memory)
- Phase II: Add persistence (same fields, file-based storage)
- Phase III: Add relationships and metadata (expanded fields, relational DB)

---

## Summary

**Core Entity**: Task with 5 fields (id, title, description, completed, created_at)

**Validation**: Title (1-200 chars), Description (0-1000 chars), ID (positive int, exists)

**Storage**: In-memory list, sequential IDs never reused, creation order preserved

**Operations**: Add, View, Update (title/desc), Delete, Toggle (status)

**State Transitions**: pending ↔ completed (toggleable), update preserves status

**Display**: Status indicators [✓]/[ ], indented descriptions, creation timestamps

**Constitutional Compliance**: ✅ Zero external dependencies, in-memory only, clean data model
