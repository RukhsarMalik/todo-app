# Todo Console App - Phase I

A command-line todo application built for the Evolution of Todo Hackathon using Spec-Driven Development with Claude Code + Spec-Kit Plus.

## Overview

**Phase I**: In-memory Python CLI application with 5 core operations
- View all tasks with status indicators
- Add tasks with title and optional description
- Toggle task completion status
- Update task title/description
- Delete tasks with confirmation

**Key Features**:
- ✅ Zero external dependencies (Python 3.13+ stdlib only)
- ✅ Type-safe with full type hints
- ✅ Graceful error handling (no crashes)
- ✅ In-memory storage (data lost on exit - by design)
- ✅ 90-second demo workflow

## Prerequisites

- **Python 3.13+** (required)
- **Terminal** with UTF-8 support

Check your Python version:
```bash
python --version  # Should show 3.13.x or higher
```

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd hackathon-2/phase-1

# Verify structure
ls src/
# Should see: main.py models/ services/ cli/ validators/
```

## Usage

### Run the Application

```bash
# From phase-1 directory
python src/main.py
```

### Main Menu

```
=== Todo Console App ===
1. View All Tasks
2. Add Task
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit

Enter your choice (1-6):
```

### Quick Start

**Add a task**:
```
Choose: 2
Title: Buy groceries
Description: Milk, eggs, bread
→ Task added successfully! (ID: 1)
```

**View tasks**:
```
Choose: 1
→ Displays all tasks with status [✓]/[ ], IDs, titles, descriptions
```

**Mark complete**:
```
Choose: 5
Task ID: 1
→ Task #1 marked as completed!
```

## Features

### 1. View All Tasks
- Displays ID, title, status, description
- Status indicators: `[✓]` completed, `[ ]` pending
- Empty list shows helpful guidance message

### 2. Add Task
- Title required (1-200 characters)
- Description optional (max 1000 characters)
- Auto-generated unique IDs
- Validation with clear error messages

### 3. Toggle Status
- Switch between pending ↔ completed
- Bidirectional (can toggle back and forth)
- Immediate visual feedback

### 4. Update Task
- Modify title and/or description
- Press Enter to keep current values
- Validates inputs before saving

### 5. Delete Task
- Confirmation prompt before deletion
- Shows task details for verification
- Can cancel with 'n'

## Technical Details

**Architecture**:
- `models/` - Task dataclass (data structure)
- `services/` - TaskManager (business logic)
- `cli/` - Menu and handlers (user interface)
- `validators/` - Input validation (reusable validators)

**Data Model**:
- Tasks stored in-memory (Python list)
- Sequential IDs starting at 1 (never reused)
- Fields: id, title, description, completed, created_at

**Error Handling**:
- All inputs validated before processing
- Clear error messages explaining what went wrong and how to fix it
- No crashes on invalid input - re-prompts instead

## Constitutional Principles

This project follows strict constitutional requirements:

1. **AI-Native Development**: All code generated via Claude Code + Spec-Kit Plus
2. **Specification-First**: Spec → Plan → Tasks → Implement workflow
3. **Clean Code**: Type hints, docstrings, SRP, DRY, max 50-line functions
4. **Zero Dependencies**: Python 3.13+ standard library only
5. **Graceful Errors**: Validate all inputs, clear messages, no crashes
6. **In-Memory Storage**: No file I/O or databases in Phase I
7. **User-Centric CLI**: Intuitive menus, helpful prompts, readable output

## Development

### Project Structure

```
hackathon-2/
├── src/
│   ├── main.py              # Entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py         # Task dataclass
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_manager.py # CRUD operations
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── menu.py         # Menu display
│   │   └── handlers.py     # Operation handlers
│   └── validators/
│       ├── __init__.py
│       └── input_validators.py
├── specs/001-todo-console-app/
│   ├── spec.md             # Feature specification
│   ├── plan.md             # Implementation plan
│   ├── tasks.md            # Task breakdown
│   └── ... (design docs)
├── pyproject.toml
└── README.md
```

### Documentation

- **Specification**: `specs/001-todo-console-app/spec.md`
- **Implementation Plan**: `specs/001-todo-console-app/plan.md`
- **Task Breakdown**: `specs/001-todo-console-app/tasks.md`
- **Data Model**: `specs/001-todo-console-app/data-model.md`
- **Quickstart Guide**: `specs/001-todo-console-app/quickstart.md`

## Testing

### Run All Tests

```bash
# Run comprehensive test suite
python tests/run_all_tests.py
```

This executes:
- **Input Validators**: 25+ test cases for all validation functions
- **View Operations**: Empty list, single/multiple tasks, status indicators
- **Add Operations**: ID increment, timestamps, validation
- **Toggle Operations**: Bidirectional toggle, error handling
- **Update Operations**: Title/description changes, preserves ID/status
- **Delete Operations**: Confirmation, ID non-reuse, multi-task scenarios
- **Integration Tests**: Complete CRUD workflows, error recovery, edge cases

### Run Individual Test Suites

```bash
# Set PYTHONPATH for module imports (adjust path as needed)
export PYTHONPATH=./src

# Run specific test suite
python tests/test_validators.py
python tests/test_integration.py
python tests/test_smoke.py
```

### Smoke Tests

Quick verification that app can start:

```bash
python tests/test_smoke.py
```

Verifies:
- All modules import correctly
- TaskManager instantiation
- Basic CRUD operations
- Validator functionality

### Manual Testing

Phase I also includes manual testing against acceptance criteria:
- 35 acceptance scenarios (from spec.md)
- 9 edge cases
- 90-second demo workflow
- 50+ consecutive operations stress test

## Limitations (Phase I)

- **No Persistence**: Tasks lost when app exits (in-memory only)
- **Single User**: No multi-user support
- **No Search**: Cannot filter or search tasks
- **No Categories**: No tags, priorities, or due dates
- **No Undo**: Operations are immediate (except delete confirmation)

## Future Phases

**Phase II** (Planned):
- File-based persistence (JSON storage)
- Task categories and tags
- Search and filter

**Phase III** (Planned):
- Database backend (SQLite)
- Multi-user support
- Task priorities and due dates

## License

Built for the Evolution of Todo Hackathon following Spec-Driven Development principles.

## Support

For issues or questions, refer to:
- Constitution: `.specify/memory/constitution.md`
- Specification: `specs/001-todo-console-app/spec.md`
- Implementation Plan: `specs/001-todo-console-app/plan.md`
