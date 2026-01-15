# Module Contracts: CLI (menu.py, handlers.py)

**Purpose**: Provide user interface for menu navigation and operation handling

**Dependencies**: services.TaskManager, validators

## cli/menu.py

### Function Signatures

```python
def display_menu() -> None:
    """Display main menu with 6 numbered options."""
    ...

def get_menu_choice() -> int:
    """Prompt for and validate menu choice (1-6). Re-prompts on invalid input."""
    ...
```

### display_menu() Contract

**Purpose**: Show menu options to user

**Output Format**:
```
=== Todo Console App ===
1. View All Tasks
2. Add Task
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit

```

**Side Effects**: Prints to stdout

**Guarantees**: Consistent formatting, clear option labels

---

### get_menu_choice() Contract

**Purpose**: Get and validate user's menu selection

**Returns**: int (1-6)

**Behavior**:
- Prompts: `"Enter your choice (1-6): "`
- Validates using `validate_menu_choice()`
- Re-prompts on invalid input with error message
- Only returns when valid choice (1-6) received

**Example**:
```python
choice = get_menu_choice()
# Guaranteed to be 1, 2, 3, 4, 5, or 6
```

---

## cli/handlers.py

### Function Signatures

```python
from services import TaskManager

def handle_view_tasks(manager: TaskManager) -> None:
    """Display all tasks or empty message."""
    ...

def handle_add_task(manager: TaskManager) -> None:
    """Prompt for title/description, validate, create task."""
    ...

def handle_update_task(manager: TaskManager) -> None:
    """Prompt for ID and new title/description, update task."""
    ...

def handle_delete_task(manager: TaskManager) -> None:
    """Prompt for ID, confirm, delete task."""
    ...

def handle_toggle_status(manager: TaskManager) -> None:
    """Prompt for ID, toggle task completion status."""
    ...
```

### Handler Contracts

All handlers follow common pattern:
1. Prompt for user input
2. Validate input using validators module
3. Re-prompt on validation failure with error message
4. Call TaskManager method with validated data
5. Display success/error result
6. Return to main menu

#### handle_view_tasks(manager: TaskManager) -> None

**Behavior**:
- Calls `manager.get_all_tasks()`
- If empty: prints `"No tasks found. Add your first task to get started!"`
- If tasks exist: prints formatted list with status indicators, IDs, titles, descriptions

**Output Format** (non-empty):
```
=== Your Tasks ===

[✓] 1. Buy groceries
    Milk, eggs, bread

[ ] 2. Call dentist
    Schedule checkup
```

---

#### handle_add_task(manager: TaskManager) -> None

**Steps**:
1. Prompt: `"Enter task title: "`
2. Validate title (re-prompt until valid)
3. Prompt: `"Enter task description (optional, press Enter to skip): "`
4. Validate description if provided (re-prompt until valid)
5. Call `manager.add_task(title, description)`
6. Print: `"Task added successfully! (ID: {task.id})"`

---

#### handle_update_task(manager: TaskManager) -> None

**Steps**:
1. Prompt: `"Enter task ID to update: "`
2. Validate ID, check task exists (re-prompt until valid)
3. Display current task details
4. Prompt: `"Enter new title (or press Enter to keep current): "`
5. If provided, validate new title
6. Prompt: `"Enter new description (or press Enter to keep current): "`
7. If provided, validate new description
8. Call `manager.update_task(id, title, description)`
9. Print: `"Task #{id} updated successfully!"`

---

#### handle_delete_task(manager: TaskManager) -> None

**Steps**:
1. Prompt: `"Enter task ID to delete: "`
2. Validate ID, check task exists (show error if not)
3. Prompt: `"Are you sure you want to delete task #{id}: {title}? (y/n): "`
4. Validate confirmation (y/yes/n/no, case-insensitive)
5. If confirmed: call `manager.delete_task(id)`, print success
6. If cancelled: print `"Deletion cancelled. Task #{id} preserved."`

---

#### handle_toggle_status(manager: TaskManager) -> None

**Steps**:
1. Prompt: `"Enter task ID to toggle status: "`
2. Validate ID, check task exists
3. Get task to determine current status
4. Call `manager.toggle_task_status(id)`
5. Print: `"Task #{id} marked as {completed/pending}!"`

---

### Responsibilities

**These modules MUST**:
- Handle all user interaction (input/output)
- Validate ALL user inputs before processing
- Display clear, actionable error messages
- Confirm destructive operations (delete)
- Show success messages after operations
- Use validators module for all validation

**These modules MUST NOT**:
- Implement business logic (TaskManager does that)
- Create tasks directly (call TaskManager)
- Modify TaskManager internal state
- Import external dependencies

### Exports

```python
# cli/__init__.py
from .menu import display_menu, get_menu_choice
from .handlers import (
    handle_view_tasks,
    handle_add_task,
    handle_update_task,
    handle_delete_task,
    handle_toggle_status
)

__all__ = [
    "display_menu",
    "get_menu_choice",
    "handle_view_tasks",
    "handle_add_task",
    "handle_update_task",
    "handle_delete_task",
    "handle_toggle_status"
]
```

### Constitutional Compliance

- ✅ Type hints on all functions (Principle III)
- ✅ Docstrings on all functions (Principle III)
- ✅ Validate all user inputs (Principle V)
- ✅ Clear error messages (Principle V)
- ✅ User-centric design - prompts explain expected input (Principle VII)
- ✅ No crashes on invalid input - re-prompt instead (Principle V)
