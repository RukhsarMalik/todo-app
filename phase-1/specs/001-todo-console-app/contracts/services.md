# Module Contract: services/task_manager.py

**Purpose**: Manage in-memory task collection and implement CRUD operations

**Dependencies**: models.Task, datetime

## TaskManager Class

### Class Signature

```python
from models import Task
from datetime import datetime

class TaskManager:
    """Manages in-memory collection of tasks with CRUD operations."""

    def __init__(self) -> None:
        """Initialize empty task list and ID counter."""
        ...

    def add_task(self, title: str, description: str = "") -> Task:
        """Create and store a new task with auto-generated ID."""
        ...

    def get_all_tasks(self) -> list[Task]:
        """Return copy of all tasks in creation order."""
        ...

    def get_task_by_id(self, task_id: int) -> Task | None:
        """Find and return task by ID, or None if not found."""
        ...

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None
    ) -> bool:
        """Update task fields. Returns True if found, False if not."""
        ...

    def delete_task(self, task_id: int) -> bool:
        """Remove task from collection. Returns True if found, False if not."""
        ...

    def toggle_task_status(self, task_id: int) -> bool:
        """Toggle completed status. Returns True if found, False if not."""
        ...
```

### Method Contracts

#### `__init__() -> None`

**Purpose**: Initialize task manager with empty collection

**Parameters**: None

**Returns**: None

**Side Effects**:
- Creates empty `_tasks` list
- Sets `_next_id` to 1

**Guarantees**:
- TaskManager ready to accept tasks
- No tasks in collection initially

---

#### `add_task(title: str, description: str = "") -> Task`

**Purpose**: Create new task with auto-generated ID and add to collection

**Parameters**:
- `title` (str): Validated task title (1-200 chars, already trimmed)
- `description` (str, optional): Validated description (≤1000 chars, already trimmed), defaults to ""

**Returns**: Task object with generated ID and timestamp

**Side Effects**:
- Increments `_next_id` counter (never decremented)
- Appends new task to `_tasks` list
- Sets `created_at` to current time
- Sets `completed` to False

**Guarantees**:
- Task has unique ID (never reused)
- Task stored in creation order
- ID counter advanced for next task

**Example**:
```python
manager = TaskManager()
task = manager.add_task("Buy groceries", "Milk, eggs")
print(task.id)  # 1
print(task.completed)  # False
```

---

#### `get_all_tasks() -> list[Task]`

**Purpose**: Retrieve all tasks for display

**Parameters**: None

**Returns**: Copy of task list (prevents external modification)

**Side Effects**: None (read-only operation)

**Guarantees**:
- Tasks returned in creation order (oldest first)
- Returns copy (modifications don't affect internal list)
- Empty list if no tasks exist

**Example**:
```python
tasks = manager.get_all_tasks()
for task in tasks:
    print(f"{task.id}. {task.title}")
```

---

#### `get_task_by_id(task_id: int) -> Task | None`

**Purpose**: Find specific task for update/delete/toggle operations

**Parameters**:
- `task_id` (int): Validated task ID (positive integer)

**Returns**:
- Task object if found
- None if task with given ID doesn't exist

**Side Effects**: None (read-only operation)

**Guarantees**:
- Returns exact task or None (no exceptions)
- Task reference allows direct modification (used internally)

**Example**:
```python
task = manager.get_task_by_id(5)
if task:
    print(f"Found: {task.title}")
else:
    print("Task #5 not found")
```

---

#### `update_task(task_id: int, title: str | None = None, description: str | None = None) -> bool`

**Purpose**: Modify title and/or description of existing task

**Parameters**:
- `task_id` (int): Validated task ID
- `title` (str | None, optional): New validated title, or None to keep current
- `description` (str | None, optional): New validated description, or None to keep current

**Returns**:
- True if task found and updated
- False if task ID doesn't exist

**Side Effects**:
- Modifies task's title and/or description fields
- Does NOT modify: id, completed, created_at

**Guarantees**:
- At least one of title or description must be provided
- Only provided fields are modified
- Status (completed) unchanged
- Returns False without error if task not found

**Example**:
```python
success = manager.update_task(1, title="Buy groceries and supplies")
if success:
    print("Task updated")
else:
    print("Task not found")
```

---

#### `delete_task(task_id: int) -> bool`

**Purpose**: Remove task from collection (ID never reused)

**Parameters**:
- `task_id` (int): Validated task ID

**Returns**:
- True if task found and deleted
- False if task ID doesn't exist

**Side Effects**:
- Removes task from `_tasks` list
- Creates "gap" in ID sequence (ID not reused)
- `_next_id` NOT decremented (continues incrementing)

**Guarantees**:
- Task completely removed (not soft delete)
- ID never reused even after deletion
- Returns False without error if task not found

**Example**:
```python
success = manager.delete_task(3)
if success:
    print("Task deleted")
# Next added task gets ID 4, 5, etc. (NOT 3)
```

---

#### `toggle_task_status(task_id: int) -> bool`

**Purpose**: Switch task between pending and completed states

**Parameters**:
- `task_id` (int): Validated task ID

**Returns**:
- True if task found and status toggled
- False if task ID doesn't exist

**Side Effects**:
- Inverts `completed` field: False → True or True → False
- Does NOT modify: id, title, description, created_at

**Guarantees**:
- Bidirectional toggle (can go back and forth)
- Only `completed` field changes
- Returns False without error if task not found

**Example**:
```python
# Task starts as pending (completed=False)
manager.toggle_task_status(1)  # Now completed=True
manager.toggle_task_status(1)  # Now completed=False again
```

---

### Internal State

**Private Attributes**:
```python
_tasks: list[Task]      # Ordered collection of all tasks
_next_id: int           # Next ID to assign (starts at 1, never decrements)
```

**Invariants** (must always be true):
- `_next_id` >= 1
- `_next_id` > max(task.id for task in _tasks) if tasks exist
- All task IDs in `_tasks` are unique
- `_tasks` preserves insertion order (oldest first)

### Responsibilities

**This module MUST**:
- Manage task collection in memory (list)
- Generate unique sequential IDs (counter pattern)
- Implement all CRUD operations (add, get, update, delete)
- Maintain creation order in task list
- Never reuse IDs after deletion
- Return None/False for missing IDs (no exceptions)

**This module MUST NOT**:
- Validate user input (validation done in validators module)
- Display output to user (CLI handlers do that)
- Persist data to files/database (in-memory only per Phase I)
- Import external dependencies (stdlib only)

### Exports

```python
# services/__init__.py
from .task_manager import TaskManager

__all__ = ["TaskManager"]
```

### Constitutional Compliance

- ✅ Type hints on all methods and returns (Principle III)
- ✅ Docstrings on all public methods (Principle III)
- ✅ Single responsibility - manage task collection (Principle III)
- ✅ In-memory storage only - no file I/O (Principle VI)
- ✅ Standard library only (Principle IV)
- ✅ No exceptions for missing IDs - returns None/False (Principle V)
