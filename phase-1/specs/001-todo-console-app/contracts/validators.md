# Module Contract: validators/input_validators.py

**Purpose**: Centralized input validation with consistent error messages

**Dependencies**: None (pure functions, stdlib only)

## Validator Function Signatures

```python
def validate_title(title: str) -> tuple[bool, str, str]:
    """Validate task title (1-200 chars, non-empty after trim)."""
    ...

def validate_description(description: str) -> tuple[bool, str, str]:
    """Validate task description (max 1000 chars after trim)."""
    ...

def validate_task_id(task_id_str: str) -> tuple[bool, str, int | None]:
    """Validate task ID is numeric and positive."""
    ...

def validate_menu_choice(choice_str: str) -> tuple[bool, str, int | None]:
    """Validate menu choice is 1-6."""
    ...

def validate_confirmation(input_str: str) -> tuple[bool, str, bool]:
    """Validate yes/no confirmation input."""
    ...
```

## Return Pattern

All validators return 3-tuple:
```python
(is_valid: bool, error_message: str, parsed_value: T | None)
```

**If valid**: `(True, "", parsed_value)`
**If invalid**: `(False, "Error message with guidance", None)`

---

## Function Contracts

### validate_title(title: str) -> tuple[bool, str, str]

**Validation Rules**:
1. Trim leading/trailing whitespace
2. Check non-empty after trim
3. Check length ≤ 200 characters after trim

**Returns**:
- Valid: `(True, "", trimmed_title)`
- Empty: `(False, "Title cannot be empty. Please enter a task title (1-200 characters).", "")`
- Too long: `(False, f"Title too long. Maximum 200 characters allowed. Current length: {len}", "")`

**Example**:
```python
is_valid, error, title = validate_title("  Buy groceries  ")
# (True, "", "Buy groceries")

is_valid, error, title = validate_title("")
# (False, "Title cannot be empty...", "")
```

---

### validate_description(description: str) -> tuple[bool, str, str]

**Validation Rules**:
1. Trim leading/trailing whitespace
2. Empty string allowed (description optional)
3. Check length ≤ 1000 characters after trim

**Returns**:
- Valid (empty): `(True, "", "")`
- Valid (with text): `(True, "", trimmed_description)`
- Too long: `(False, f"Description too long. Maximum 1000 characters allowed. Current length: {len}", "")`

---

### validate_task_id(task_id_str: str) -> tuple[bool, str, int | None]

**Validation Rules**:
1. Trim whitespace
2. Parse to integer
3. Check > 0 (positive)

**Returns**:
- Valid: `(True, "", task_id_int)`
- Non-numeric: `(False, "Invalid task ID. Please enter a numeric ID.", None)`
- Zero/negative: `(False, "Invalid task ID. Please enter a numeric ID.", None)`

**Note**: Existence check (does task exist in collection?) done by caller using TaskManager.get_task_by_id()

---

### validate_menu_choice(choice_str: str) -> tuple[bool, str, int | None]

**Validation Rules**:
1. Trim whitespace
2. Parse to integer
3. Check 1 ≤ choice ≤ 6

**Returns**:
- Valid: `(True, "", choice_int)`
- Invalid: `(False, "Invalid choice. Please select a valid option (1-6).", None)`

---

### validate_confirmation(input_str: str) -> tuple[bool, str, bool]

**Validation Rules**:
1. Trim whitespace
2. Convert to lowercase
3. Check if in ["y", "yes", "n", "no"]

**Returns**:
- Yes: `(True, "", True)`
- No: `(True, "", False)`
- Invalid: `(False, "Please enter 'y' for yes or 'n' for no.", None)`

**Example**:
```python
is_valid, error, confirmed = validate_confirmation("Y")
# (True, "", True)

is_valid, error, confirmed = validate_confirmation("no")
# (True, "", False)
```

---

## Design Principles

**Pure Functions**:
- No side effects (no prints, no file I/O, no state modification)
- Deterministic (same input always produces same output)
- Testable in isolation

**Consistent Error Messages**:
- Pattern: "[What went wrong]. [How to fix it]. [Current state if relevant]"
- Always actionable (tells user what to do)
- Includes context (e.g., current length for too-long inputs)

**Type Safety**:
- Explicit return types using tuples
- Generic pattern works for different value types (str, int, bool)
- Callers can destructure: `is_valid, error, value = validate_X(...)`

---

## Responsibilities

**This module MUST**:
- Validate all user inputs before processing
- Return consistent 3-tuple format
- Provide clear, actionable error messages
- Trim whitespace before validation
- Be pure functions (no side effects)

**This module MUST NOT**:
- Display output to user (callers do that)
- Check task existence (TaskManager does that)
- Raise exceptions for validation failures
- Import external dependencies

## Exports

```python
# validators/__init__.py
from .input_validators import (
    validate_title,
    validate_description,
    validate_task_id,
    validate_menu_choice,
    validate_confirmation
)

__all__ = [
    "validate_title",
    "validate_description",
    "validate_task_id",
    "validate_menu_choice",
    "validate_confirmation"
]
```

## Constitutional Compliance

- ✅ Type hints on all functions (Principle III)
- ✅ Docstrings on all functions (Principle III)
- ✅ Single responsibility - validate one input type (Principle III)
- ✅ DRY - centralized validation, no duplication (Principle III)
- ✅ Clear error messages with guidance (Principle V)
- ✅ Pure functions, no side effects (clean code)
- ✅ Standard library only (Principle IV)
