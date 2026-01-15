# Implementation Plan: Todo Console App (Phase I)

**Branch**: `001-todo-console-app` | **Date**: 2025-12-25 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-todo-console-app/spec.md`

**Note**: This plan follows the Spec-Driven Development workflow and constitutional requirements for Phase I.

## Summary

Build an in-memory Python CLI todo application with 5 core operations (view, add, update, delete, toggle status). The app stores tasks in memory using Python standard library data structures (dataclasses + list), requires zero external dependencies, and focuses on clean code principles with full type hints and docstrings. Designed for learning Spec-Driven Development and AI-assisted coding through Claude Code + Spec-Kit Plus workflow.

**Technical Approach**: Modular architecture with separation of concerns - data models (Task dataclass), business logic (TaskManager service), CLI interface (menu + input handlers), and validation utilities. All operations return to main menu, all inputs validated before processing, all errors handled gracefully with actionable messages.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (dataclasses, typing, datetime, sys, enum)
**Storage**: In-memory (list of Task objects managed by TaskManager)
**Testing**: Manual testing against acceptance criteria (no automated tests in Phase I)
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows via WSL)
**Project Type**: Single project (CLI application)
**Performance Goals**: Instantaneous response (<100ms) for all operations on up to 1000 tasks
**Constraints**: Zero external dependencies, in-memory only (no persistence), 90-second demo requirement
**Scale/Scope**: Single user, session-based (data lost on exit), 5 operations, ~500 lines of code

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: AI-Native Development ✅ PASS
- **Requirement**: All code generated via Claude Code + Spec-Kit Plus
- **Compliance**: This plan will generate tasks that map to approved specifications
- **Verification**: Task IDs will be referenced in all commits

### Principle II: Specification-First Development ✅ PASS
- **Requirement**: Spec → Plan → Tasks → Implement workflow
- **Compliance**: Spec completed and validated (12/12 quality gates passed), now creating plan
- **Next Step**: Tasks generation via /sp.tasks after plan approval

### Principle III: Clean Code & Python Standards ✅ PASS
- **Requirement**: Type hints, docstrings, SRP, DRY, meaningful names, max 50-line functions
- **Compliance**:
  - All functions will have full type hints (typing module)
  - All public functions/classes will have Google-style docstrings
  - Modular design enforces SRP (models, services, cli, validators)
  - Validation logic centralized in validators module (DRY)
  - Functions designed for <50 lines (single responsibility)

### Principle IV: Zero External Dependencies ✅ PASS
- **Requirement**: Python 3.13+ standard library only
- **Compliance**: Using only: dataclasses, typing, datetime, sys, enum
- **Prohibited**: No pip packages, no third-party libraries
- **Package Manager**: UV for project setup only (no runtime dependencies)

### Principle V: Graceful Error Handling ✅ PASS
- **Requirement**: Validate all inputs, clear error messages, no crashes
- **Compliance**:
  - Dedicated validation module with specific validators (title, description, ID, menu choice)
  - All validators return Result type (success with value OR error with message)
  - Error messages follow pattern: "What went wrong + How to fix it + Current value if applicable"
  - Try-except blocks around user input with re-prompting on errors
  - No stack traces shown to users

### Principle VI: In-Memory Storage ✅ PASS
- **Requirement**: No file I/O, databases, or persistence
- **Compliance**:
  - TaskManager stores tasks in `List[Task]` (in-memory)
  - No import of pathlib, json, pickle, sqlite3, or file-related modules
  - Data intentionally lost on program exit (acceptable per constitution)

### Principle VII: User-Centric CLI Design ✅ PASS
- **Requirement**: Intuitive menus, clear prompts, readable output, helpful guidance
- **Compliance**:
  - Main menu with numbered options (1-6) and clear labels
  - All prompts explain expected input (e.g., "Enter task ID (numeric):")
  - Task display formatted with visual separators and status indicators
  - Empty list shows guidance: "No tasks found. Add your first task to get started!"
  - Deletion prompts for confirmation with task details

### Constitutional Compliance Summary
**Result**: ✅ ALL GATES PASS - No violations, no justifications needed

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-console-app/
├── spec.md                  # Feature specification (completed)
├── plan.md                  # This file (implementation plan)
├── research.md              # Phase 0: Technology decisions and patterns
├── data-model.md            # Phase 1: Task entity and relationships
├── quickstart.md            # Phase 1: How to run and use the application
├── contracts/               # Phase 1: Module contracts (function signatures)
│   ├── models.md           # Task dataclass contract
│   ├── services.md         # TaskManager contract
│   ├── cli.md              # Menu and input handler contracts
│   └── validators.md       # Validation function contracts
└── tasks.md                 # Phase 2: Implementation tasks (via /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── __init__.py              # Empty (makes src a package)
├── main.py                  # Application entry point, main loop
├── models/
│   ├── __init__.py         # Exports Task dataclass
│   └── task.py             # Task dataclass definition
├── services/
│   ├── __init__.py         # Exports TaskManager
│   └── task_manager.py     # Business logic (CRUD operations)
├── cli/
│   ├── __init__.py         # Exports menu and handlers
│   ├── menu.py             # Main menu display and selection
│   └── handlers.py         # Input handlers for each operation
└── validators/
    ├── __init__.py         # Exports all validators
    └── input_validators.py # Validation functions (title, description, ID)

tests/                       # Reserved for future phases
├── unit/                    # Unit tests (Phase II)
├── integration/             # Integration tests (Phase II)
└── contract/                # Contract tests (Phase II)

pyproject.toml               # UV project configuration (Python 3.13+, no deps)
README.md                    # Project documentation and usage
.gitignore                   # Python-specific ignores
```

**Structure Decision**: Selected "Single project" structure with modular organization. Rationale:
- **models/**: Data definitions (Task dataclass) - represents WHAT data looks like
- **services/**: Business logic (TaskManager) - represents HOW operations work
- **cli/**: User interface (menu, handlers) - represents HOW users interact
- **validators/**: Input validation (reusable validators) - represents WHAT inputs are valid
- **main.py**: Entry point orchestrating the above - represents application lifecycle

This separation enforces SRP, makes testing easier in future phases, and aligns with clean architecture principles while remaining simple enough for a learning project.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. This section intentionally left empty.

## Phase 0: Research & Technology Decisions

### Research Areas

No significant research needed - all technical decisions are straightforward:

1. **Data Structure for Task Storage**: `List[Task]` vs `Dict[int, Task]`
2. **ID Generation Strategy**: Counter vs UUID vs timestamp-based
3. **Input Validation Pattern**: Exceptions vs Result type vs inline checks
4. **CLI Menu Pattern**: While loop vs recursive calls vs state machine
5. **Error Message Formatting**: Template strings vs f-strings vs dedicated formatter

### Research Outcomes

See [research.md](research.md) for detailed analysis. Key decisions:

**Decision 1: Task Storage → List[Task]**
- **Rationale**: Simpler iteration, natural ordering, smaller codebase
- **Alternative**: Dict[int, Task] for O(1) lookup - rejected because list iteration is O(n) acceptable for <1000 tasks

**Decision 2: ID Generation → Counter (int starting at 1)**
- **Rationale**: Sequential IDs match user expectations, never reused (increment even after delete)
- **Alternative**: UUID - rejected due to poor UX (long strings hard to type)

**Decision 3: Validation → Result Type Pattern**
- **Rationale**: Explicit error handling, type-safe, no exceptions for control flow
- **Alternative**: Try-except - rejected because validation isn't exceptional, it's expected

**Decision 4: Menu → While loop with break on exit**
- **Rationale**: Clear flow control, standard pattern, easy to understand
- **Alternative**: Recursive - rejected due to stack depth concerns and complexity

**Decision 5: Errors → F-strings with inline context**
- **Rationale**: Direct, easy to read, no template overhead
- **Alternative**: Template engine - over-engineering for simple messages

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](data-model.md) for complete entity definitions.

**Task Entity**:
```python
@dataclass
class Task:
    id: int                      # Auto-generated, unique, sequential
    title: str                   # Required, 1-200 chars (trimmed)
    description: str             # Optional, max 1000 chars (trimmed)
    completed: bool              # Default False
    created_at: datetime         # Auto-generated on creation
```

**Validation Rules** (enforced in validators module):
- Title: non-empty after trim, length 1-200
- Description: if provided, length ≤ 1000 after trim
- ID: positive integer, must exist in task list for operations
- Menu choice: integer 1-6

**State Transitions**:
- Task created → completed = False
- Toggle operation → completed = not completed
- Update operation → title/description change, completed unchanged
- Delete operation → task removed from list (ID not reused)

### API Contracts

See [contracts/](contracts/) directory for complete function signatures.

**TaskManager Service Contract** (services/task_manager.py):
```python
class TaskManager:
    def __init__(self) -> None: ...
    def add_task(self, title: str, description: str = "") -> Task: ...
    def get_all_tasks(self) -> list[Task]: ...
    def get_task_by_id(self, task_id: int) -> Task | None: ...
    def update_task(self, task_id: int, title: str | None = None,
                    description: str | None = None) -> bool: ...
    def delete_task(self, task_id: int) -> bool: ...
    def toggle_task_status(self, task_id: int) -> bool: ...
```

**CLI Handlers Contract** (cli/handlers.py):
```python
def handle_view_tasks(manager: TaskManager) -> None: ...
def handle_add_task(manager: TaskManager) -> None: ...
def handle_update_task(manager: TaskManager) -> None: ...
def handle_delete_task(manager: TaskManager) -> None: ...
def handle_toggle_status(manager: TaskManager) -> None: ...
```

**Validator Contract** (validators/input_validators.py):
```python
def validate_title(title: str) -> tuple[bool, str, str]: ...
    # Returns: (is_valid, error_message, trimmed_value)
def validate_description(description: str) -> tuple[bool, str, str]: ...
def validate_task_id(task_id_str: str) -> tuple[bool, str, int | None]: ...
def validate_menu_choice(choice_str: str) -> tuple[bool, str, int | None]: ...
def validate_confirmation(input_str: str) -> tuple[bool, str, bool]: ...
```

### Module Responsibilities

**models/task.py**:
- Define Task dataclass with type hints
- No business logic, just data structure
- Single responsibility: represent task data

**services/task_manager.py**:
- Maintain in-memory task list
- Implement CRUD operations (add, get, update, delete, toggle)
- Generate unique sequential IDs
- Single responsibility: manage task collection

**cli/menu.py**:
- Display main menu with 6 options
- Get user's menu choice
- Route choice to appropriate handler
- Single responsibility: menu navigation

**cli/handlers.py**:
- One handler function per operation
- Collect user input, call validators, call TaskManager
- Display results and errors
- Single responsibility: orchestrate single operation

**validators/input_validators.py**:
- Validate title, description, ID, menu choice, confirmation
- Return (is_valid, error_message, parsed_value) tuple
- No side effects, pure functions
- Single responsibility: validate one type of input

**main.py**:
- Create TaskManager instance
- Run main loop: display menu → get choice → execute handler → repeat
- Handle exit gracefully
- Single responsibility: application lifecycle

### Error Handling Strategy

**Validation Errors** (expected, frequent):
- Validators return (False, error_msg, None) for invalid input
- Handlers check validation result, print error, re-prompt user
- Never raise exceptions for validation failures

**System Errors** (unexpected, rare):
- Try-except around input() calls (handles Ctrl+C, EOF)
- Try-except around int() conversions (handles non-numeric input)
- Catch-all in main loop to prevent crashes
- All exceptions print user-friendly message, return to menu

**Error Message Format**:
```
"[What went wrong]. [How to fix it]. [Current state if relevant]"

Examples:
- "Title cannot be empty. Please enter a task title (1-200 characters)."
- "Title too long. Maximum 200 characters allowed. Current length: 250"
- "Task #99 not found. Use 'View Tasks' to see valid task IDs."
- "Invalid choice. Please select a valid option (1-6)."
```

### User Flow Diagrams

**Main Loop Flow**:
```
START → Display Menu → Get Choice → Validate Choice
   ↑                                      ↓
   ↑                                   Valid?
   ↑                                   ↙    ↘
   ↑                                Yes      No
   ↑                                 ↓        ↓
   ↑                          Execute Handler  Show Error
   ↑                                 ↓        ↓
   ←─────────────────── Choice == 6? ───────┘
                        Yes ↓  No ↑
                           EXIT

Handler Flow (generic):
Get Input → Validate → Valid? → Yes → Call Service → Show Result → Return
                         ↓
                        No → Show Error → Re-prompt → (loop back)
```

**Add Task Flow** (detailed example):
```
1. Prompt for title
2. Validate title (1-200 chars, non-empty after trim)
   - Invalid? Show error, go to step 1
3. Prompt for description (optional)
4. Validate description (≤1000 chars if provided)
   - Invalid? Show error, go to step 3
5. Call manager.add_task(title, description)
6. Display "Task added successfully! (ID: X)"
7. Return to main menu
```

### Quickstart

See [quickstart.md](quickstart.md) for complete setup and usage instructions.

**Quick Setup**:
```bash
# Clone or navigate to project
cd /path/to/hackathon-2

# Ensure Python 3.13+ is installed
python --version  # Should show 3.13+

# Run the application
python src/main.py
```

**Usage Example**:
```
=== Todo Console App ===
1. View All Tasks
2. Add Task
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit

Enter your choice (1-6): 2

Enter task title: Buy groceries
Enter task description (optional, press Enter to skip): Milk, eggs, bread

Task added successfully! (ID: 1)

[Returns to main menu]
```

## Phase 2: Task Breakdown (Deferred)

Task generation will be handled by `/sp.tasks` command after this plan is approved.

Expected task structure:
- **Setup Tasks**: Initialize project structure, pyproject.toml, README
- **Foundation Tasks**: Create models, validators, base services
- **User Story 1 (P1)**: Implement view tasks functionality
- **User Story 2 (P2)**: Implement add task functionality
- **User Story 3 (P3)**: Implement toggle status functionality
- **User Story 4 (P4)**: Implement update task functionality
- **User Story 5 (P5)**: Implement delete task functionality
- **Integration Tasks**: Wire up main.py, test full workflow

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| Input validation complexity causes bugs | Medium | Medium | Centralize validation in dedicated module, use consistent return pattern |
| ID management errors (duplicates, reuse) | High | Low | Simple counter incremented on add (never decremented), tested thoroughly |
| Long descriptions break display | Low | Low | Accept as known limitation (per spec: display without truncation) |
| Unicode handling issues | Low | Low | Python 3.13 handles unicode natively, test with emojis and special chars |
| Function length exceeds 50 lines | Medium | Medium | Monitor during implementation, refactor if needed (extract to helper functions) |

## Success Validation

This implementation will be considered successful when:

1. ✅ All 5 user stories have acceptance scenarios passing
2. ✅ 90-second demo workflow completable (add → view → toggle → update → delete)
3. ✅ 100% of invalid inputs produce clear error messages (no crashes)
4. ✅ 50+ consecutive operations without errors
5. ✅ All code has type hints and docstrings (constitutional requirement)
6. ✅ No external dependencies (import check passes)
7. ✅ All task IDs traceable to specification (git log verification)

## Next Steps

1. **Approve this plan** - Review for alignment with spec and constitution
2. **Generate Phase 0 artifacts** - Create research.md with decision details
3. **Generate Phase 1 artifacts** - Create data-model.md, contracts/, quickstart.md
4. **Update agent context** - Run update-agent-context.sh to record technology stack
5. **Generate tasks** - Run `/sp.tasks` to create implementation task breakdown
6. **Begin implementation** - Execute tasks via `/sp.implement`

---

**Plan Status**: ✅ READY FOR REVIEW
**Constitutional Compliance**: ✅ ALL GATES PASS (7/7)
**Estimated Implementation Effort**: ~8-12 tasks, 500 lines of code, 2-3 hours hands-off time
