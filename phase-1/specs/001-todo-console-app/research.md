# Research & Technology Decisions: Todo Console App (Phase I)

**Date**: 2025-12-25
**Context**: Phase I Evolution of Todo Hackathon - In-memory CLI todo application

## Overview

This document captures technology choices and design patterns for the Phase I implementation. All decisions align with constitutional constraints: Python 3.13+ stdlib only, zero external dependencies, clean code principles, graceful error handling, in-memory storage.

## Decision 1: Task Storage Data Structure

### Question
How should we store the in-memory task collection for efficient CRUD operations?

### Options Evaluated

| Option | Pros | Cons | Complexity |
|--------|------|------|------------|
| **List[Task]** | Simple iteration, natural ordering, minimal code | O(n) lookups, linear search for ID | Low |
| **Dict[int, Task]** | O(1) lookup by ID, fast access | Extra indexing logic, ordering not preserved | Medium |
| **OrderedDict** | Combines both benefits | More complex, overkill for <1000 tasks | Medium-High |

### Decision: **List[Task]**

**Rationale**:
- Performance acceptable: O(n) iteration fast enough for <1000 tasks (spec scope)
- Natural ordering: List preserves insertion order (matches "created_at" sort requirement)
- Simplicity: Fewer lines of code, easier to understand for learning project
- Constitutional alignment: Simplicity principle ("start simple, YAGNI")

**Implementation**:
```python
class TaskManager:
    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._next_id: int = 1
```

**Rejected Alternatives**:
- Dict[int, Task]: Over-engineering for small dataset, complicates ordering
- OrderedDict: Deprecated pattern in Python 3.7+ (dict preserves order), unnecessary

---

## Decision 2: ID Generation Strategy

### Question
How should unique task IDs be generated and managed?

### Options Evaluated

| Option | Pros | Cons | User Experience |
|--------|------|------|----------------|
| **Sequential Counter** | Predictable, short IDs (1, 2, 3...), never reused | Must track deletions | Excellent (easy to type) |
| **UUID** | Universally unique, no collision risk | Long strings, hard to type | Poor for CLI |
| **Timestamp-based** | Sortable, unique if ms precision | Potential collisions, long numbers | Medium |

### Decision: **Sequential Counter (never reused)**

**Rationale**:
- User-friendly: Short numeric IDs (1, 2, 3) easy to type and remember
- Spec compliance: "auto-generate unique, sequential task IDs starting from 1"
- Predictability: Users can guess next ID, understand ID history
- No reuse requirement: Spec explicitly states "IDs are not reused even after deletion"

**Implementation**:
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
    self._next_id += 1  # Increment even after delete
    return task
```

**Rejected Alternatives**:
- UUID: User-hostile for CLI (typing "550e8400-e29b-41d4-a716-446655440000" vs "5")
- Timestamp: Risk of collisions if tasks added in same millisecond, poor UX

---

## Decision 3: Input Validation Pattern

### Question
How should validation be structured to ensure type safety and clear error handling?

### Options Evaluated

| Option | Pros | Cons | Type Safety |
|--------|------|------|-------------|
| **Tuple Return Pattern** | Explicit, type-safe, no exceptions for control flow | Slightly verbose | Excellent |
| **Raise Exceptions** | Python-idiomatic, short code | Exceptions for non-exceptional cases, poor performance | Good |
| **Inline if-else** | Simple, direct | Scattered validation, hard to reuse, violates DRY | Poor |

### Decision: **Tuple Return Pattern (is_valid, error_msg, value)**

**Rationale**:
- Type safety: Return type `tuple[bool, str, T | None]` explicitly shows success/failure
- No exceptions for control flow: Validation failures are expected, not exceptional
- Reusability: Validators are pure functions, testable in isolation
- Constitutional alignment: Clean code (SRP), DRY (centralized validation)

**Implementation**:
```python
def validate_title(title: str) -> tuple[bool, str, str]:
    """Validate task title meets length and non-empty requirements.

    Returns:
        (True, "", trimmed_title) if valid
        (False, error_message, "") if invalid
    """
    trimmed = title.strip()
    if not trimmed:
        return (False, "Title cannot be empty. Please enter a task title (1-200 characters).", "")
    if len(trimmed) > 200:
        return (False, f"Title too long. Maximum 200 characters allowed. Current length: {len(trimmed)}", "")
    return (True, "", trimmed)
```

**Usage in Handlers**:
```python
def handle_add_task(manager: TaskManager) -> None:
    while True:
        title_input = input("Enter task title: ")
        is_valid, error_msg, title = validate_title(title_input)
        if is_valid:
            break
        print(f"❌ {error_msg}")
```

**Rejected Alternatives**:
- Exceptions: `raise ValidationError("Title too long")` - creates exception overhead for expected failures
- Inline: Duplicates validation logic across handlers, violates DRY

---

## Decision 4: CLI Menu Pattern

### Question
How should the main menu loop be structured for clarity and maintainability?

### Options Evaluated

| Option | Pros | Cons | Complexity |
|--------|------|------|------------|
| **While True + Break** | Clear flow, standard pattern, no stack depth issues | Slightly imperative | Low |
| **Recursive Function** | Functional style, concise | Stack overflow risk, harder to debug | Medium |
| **State Machine** | Explicit states, extensible | Over-engineering for 6 menu items | High |

### Decision: **While True Loop with Break on Exit**

**Rationale**:
- Standard Python pattern: Widely recognized, easy for beginners
- Clear flow control: Loop continues until user chooses exit
- No stack depth issues: Recursive approach could overflow on long sessions
- Constitutional alignment: Simplicity, YAGNI (state machine overkill)

**Implementation**:
```python
def main() -> None:
    manager = TaskManager()

    while True:
        display_menu()
        choice_input = input("Enter your choice (1-6): ")
        is_valid, error_msg, choice = validate_menu_choice(choice_input)

        if not is_valid:
            print(f"❌ {error_msg}")
            continue

        if choice == 6:
            print("👋 Goodbye!")
            break

        handlers = {
            1: handle_view_tasks,
            2: handle_add_task,
            3: handle_update_task,
            4: handle_delete_task,
            5: handle_toggle_status
        }
        handlers[choice](manager)
```

**Rejected Alternatives**:
- Recursive: `def menu(manager): ...; menu(manager)` - risks stack overflow, harder to trace
- State Machine: Requires state enum, transition table - unnecessary complexity

---

## Decision 5: Error Message Formatting

### Question
How should error messages be formatted for clarity and actionability?

### Options Evaluated

| Option | Pros | Cons | User Experience |
|--------|------|------|----------------|
| **F-strings with Context** | Direct, readable, shows current state | Slightly verbose | Excellent |
| **Template Strings** | Reusable templates, consistent formatting | Extra indirection, overkill | Good |
| **Plain Strings** | Simple, short | No context, unhelpful | Poor |

### Decision: **F-strings with Inline Context**

**Rationale**:
- Constitutional requirement: "Error messages MUST explain what went wrong AND how to fix it"
- Context awareness: Can show current values (e.g., "Current length: 250")
- Readability: F-strings are Pythonic, easy to read and maintain
- No over-engineering: No template engine needed for simple messages

**Implementation**:
```python
# Title validation
if len(trimmed) > 200:
    return (False, f"Title too long. Maximum 200 characters allowed. Current length: {len(trimmed)}", "")

# ID validation
try:
    task_id = int(task_id_str.strip())
except ValueError:
    return (False, "Invalid task ID. Please enter a numeric ID.", None)

# Task not found
if task is None:
    print(f"❌ Task #{task_id} not found. Use 'View Tasks' to see valid task IDs.")
```

**Error Message Pattern**:
```
"[What went wrong]. [How to fix it]. [Current state if relevant]"
```

**Examples Meeting Constitutional Standard**:
- ✅ "Title cannot be empty. Please enter a task title (1-200 characters)."
- ✅ "Title too long. Maximum 200 characters allowed. Current length: 250"
- ✅ "Task #99 not found. Use 'View Tasks' to see valid task IDs."
- ✅ "Invalid choice. Please select a valid option (1-6)."

**Rejected Alternatives**:
- Template engine: `ErrorTemplate("title_too_long", length=250)` - over-engineering
- Plain strings: `"Invalid title"` - doesn't meet constitutional requirement

---

## Supporting Technology Choices

### Python Standard Library Modules

**Used**:
- `dataclasses`: Task entity definition with auto-generated `__init__`, `__repr__`
- `datetime`: Timestamp for `created_at` field
- `typing`: Type hints (list, tuple, Optional/None union via `|`)
- `sys`: Graceful exit handling (sys.exit())

**Explicitly NOT Used** (constitutional prohibition):
- `json`, `pickle`: Persistence (violates in-memory constraint)
- `sqlite3`: Database (violates in-memory constraint)
- `pathlib`, `os.path`: File I/O (violates in-memory constraint)
- `argparse`: CLI parsing (not needed for menu-driven app)
- External packages: pytest, click, rich, etc. (violates zero-dependency constraint)

### Type Hints Strategy

**Python 3.13+ Modern Syntax**:
- Union types: `str | None` instead of `Optional[str]`
- Built-in generics: `list[Task]` instead of `List[Task]`
- Pipe notation: `int | None` instead of `Union[int, None]`

**Why**:
- Cleaner syntax: Less imports, more readable
- Constitutional requirement: "Type hints on ALL functions, parameters, and return values"
- Python 3.13+ guaranteed: Constitution specifies 3.13+ only

---

## Best Practices Applied

### Clean Code Principles

1. **Single Responsibility Principle (SRP)**:
   - models/task.py: Only defines Task dataclass
   - services/task_manager.py: Only manages task collection
   - cli/handlers.py: Only orchestrates single operations
   - validators/input_validators.py: Only validates input

2. **DRY (Don't Repeat Yourself)**:
   - Validation centralized in validators module
   - Error message pattern consistent across all validators
   - Handler functions follow common pattern: validate → call service → display result

3. **Meaningful Names**:
   - Functions: `validate_title`, `add_task`, `handle_delete_task` (verb-noun)
   - Variables: `trimmed_title`, `is_valid`, `error_msg` (descriptive, no abbreviations)
   - Classes: `Task`, `TaskManager` (nouns, clear purpose)

4. **Maximum Function Length: 50 lines**:
   - Validators: ~10-15 lines each
   - Handlers: ~20-30 lines each
   - TaskManager methods: ~5-15 lines each
   - If any function exceeds 50 lines during implementation → refactor to helper functions

### Error Handling Strategy

**Three-Tier Approach**:

1. **Validation Layer** (expected errors):
   - Return `(False, error_msg, None)` for invalid input
   - Never raise exceptions for validation failures
   - Re-prompt user until valid input received

2. **System Layer** (unexpected errors):
   - Try-except around `input()` for KeyboardInterrupt, EOFError
   - Try-except around `int()` conversions for ValueError
   - Graceful degradation: print error, return to menu

3. **Application Layer** (crash prevention):
   - Catch-all in main loop: `except Exception as e:` print friendly message
   - No stack traces shown to user (constitutional requirement)

---

## Performance Considerations

### Expected Performance

| Operation | Algorithm | Time Complexity | Expected Latency |
|-----------|-----------|----------------|------------------|
| Add Task | Append to list | O(1) | <1ms |
| View All | Iterate list | O(n) | <10ms for 1000 tasks |
| Find by ID | Linear search | O(n) | <1ms for 1000 tasks |
| Update Task | Find + modify | O(n) | <1ms for 1000 tasks |
| Delete Task | Find + remove | O(n) | <1ms for 1000 tasks |
| Toggle Status | Find + modify | O(n) | <1ms for 1000 tasks |

**Performance Goal**: <100ms for all operations on up to 1000 tasks (constitutional constraint)

**Why This is Acceptable**:
- Scope limited to <1000 tasks (per spec assumptions)
- Python list operations highly optimized in C
- No I/O blocking (in-memory only)
- User perception threshold: ~100ms feels instant

### Scalability Considerations (Future Phases)

If Phase II/III require handling >10,000 tasks:
- Switch to `Dict[int, Task]` for O(1) lookup
- Add indexing for search/filter operations
- Consider database for persistence and query optimization

---

## Testing Strategy (Phase I)

### Manual Testing Against Acceptance Criteria

No automated tests in Phase I (constitutional scope). Testing approach:

1. **Per User Story**: Manually execute each acceptance scenario from spec.md
2. **Edge Cases**: Test all 9 edge cases identified in spec
3. **Error Handling**: Verify all validation errors produce clear messages
4. **90-Second Demo**: Practice full workflow to ensure <90 seconds

**Test Checklist** (to be created in tasks phase):
- [ ] Empty list shows "No tasks found" message
- [ ] Add task with title only (no description)
- [ ] Add task with title + description
- [ ] Validate empty title rejected
- [ ] Validate 201-char title rejected
- [ ] Validate 1001-char description rejected
- [ ] View tasks displays all with correct status indicators
- [ ] Toggle pending → completed shows [✓]
- [ ] Toggle completed → pending shows [ ]
- [ ] Update task title only
- [ ] Update task description only
- [ ] Update both title and description
- [ ] Delete task with confirmation
- [ ] Delete task with cancellation (n)
- [ ] Invalid menu choice shows error
- [ ] Invalid task ID shows helpful error
- [ ] 50+ consecutive operations without crash

---

## Summary of Decisions

| # | Decision Area | Choice | Rationale |
|---|--------------|--------|-----------|
| 1 | Task Storage | List[Task] | Simplicity, natural ordering, acceptable performance |
| 2 | ID Generation | Sequential counter (never reused) | User-friendly, spec-compliant, predictable |
| 3 | Validation | Tuple return pattern | Type-safe, explicit, reusable, no exceptions |
| 4 | Menu Loop | While True + break | Standard pattern, clear flow, no stack issues |
| 5 | Error Messages | F-strings with context | Direct, readable, shows current state |

**Constitutional Compliance**: All decisions align with 7 core principles - AI-native development, spec-first, clean code, zero deps, graceful errors, in-memory storage, user-centric CLI.

**Ready for Phase 1**: Design (data model, contracts, quickstart) can now proceed.
