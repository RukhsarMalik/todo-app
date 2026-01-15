# Module Contract: models/task.py

**Purpose**: Define the Task data structure with all required fields and type hints

**Dependencies**: Python standard library (dataclasses, datetime)

## Task Dataclass

### Class Signature

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    """A single todo item with title, description, and completion status."""
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
```

### Field Contracts

| Field | Type | Purpose | Constraints |
|-------|------|---------|-------------|
| `id` | int | Unique task identifier | Positive integer, auto-generated, never reused |
| `title` | str | Short task description | 1-200 characters (validated before creation) |
| `description` | str | Optional detailed information | 0-1000 characters (empty string if not provided) |
| `completed` | bool | Completion status | True (completed) or False (pending) |
| `created_at` | datetime | Creation timestamp | Valid datetime object, set on creation |

### Responsibilities

**This module MUST**:
- Define Task dataclass with exact fields above
- Use @dataclass decorator for auto-generated methods
- Provide type hints for all fields
- Include docstring explaining Task purpose

**This module MUST NOT**:
- Implement business logic (no methods beyond dataclass defaults)
- Perform validation (validation done before Task creation)
- Manage task collections (that's TaskManager's job)
- Import non-standard-library modules

### Exports

```python
# models/__init__.py
from .task import Task

__all__ = ["Task"]
```

### Usage Example

```python
from models import Task
from datetime import datetime

# TaskManager creates tasks with validated data
task = Task(
    id=1,
    title="Buy groceries",
    description="Milk, eggs, bread",
    completed=False,
    created_at=datetime.now()
)

# Access fields
print(task.id)          # 1
print(task.title)       # "Buy groceries"
print(task.completed)   # False

# Dataclass provides automatic __repr__
print(task)  # Task(id=1, title='Buy groceries', ...)
```

### Constitutional Compliance

- ✅ Type hints on all fields (Principle III)
- ✅ Docstring provided (Principle III)
- ✅ Standard library only - dataclasses, datetime (Principle IV)
- ✅ Single responsibility - represent task data (Principle III)
- ✅ No external dependencies (Principle IV)
