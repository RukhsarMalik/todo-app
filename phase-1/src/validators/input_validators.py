"""Input validation functions for Todo Console App.

This module provides pure validation functions that return (is_valid, error_msg, value) tuples.
All validators trim whitespace and provide actionable error messages.
"""


def validate_title(title: str) -> tuple[bool, str, str]:
    """Validate task title meets length and non-empty requirements.

    Args:
        title: User-provided title string

    Returns:
        Tuple of (is_valid, error_message, trimmed_title):
        - (True, "", trimmed_title) if valid
        - (False, error_message, "") if invalid

    Rules:
        - Trim leading/trailing whitespace
        - Must be non-empty after trim
        - Maximum 200 characters after trim
    """
    trimmed = title.strip()

    if not trimmed:
        return (
            False,
            "Title cannot be empty. Please enter a task title (1-200 characters).",
            ""
        )

    if len(trimmed) > 200:
        return (
            False,
            f"Title too long. Maximum 200 characters allowed. Current length: {len(trimmed)}",
            ""
        )

    return (True, "", trimmed)


def validate_description(description: str) -> tuple[bool, str, str]:
    """Validate task description meets length requirements.

    Args:
        description: User-provided description string (optional)

    Returns:
        Tuple of (is_valid, error_message, trimmed_description):
        - (True, "", trimmed_description) if valid (including empty string)
        - (False, error_message, "") if invalid

    Rules:
        - Trim leading/trailing whitespace
        - Empty string allowed (description is optional)
        - Maximum 1000 characters after trim
    """
    trimmed = description.strip()

    if len(trimmed) > 1000:
        return (
            False,
            f"Description too long. Maximum 1000 characters allowed. Current length: {len(trimmed)}",
            ""
        )

    return (True, "", trimmed)


def validate_task_id(task_id_str: str) -> tuple[bool, str, int | None]:
    """Validate task ID is numeric and positive.

    Args:
        task_id_str: User-provided ID string

    Returns:
        Tuple of (is_valid, error_message, task_id):
        - (True, "", task_id_int) if valid
        - (False, error_message, None) if invalid

    Rules:
        - Trim whitespace
        - Must parse to integer
        - Must be positive (> 0)

    Note:
        Existence check (does task exist?) is done by caller using TaskManager.
    """
    trimmed = task_id_str.strip()

    try:
        task_id = int(trimmed)
    except ValueError:
        return (
            False,
            "Invalid task ID. Please enter a numeric ID.",
            None
        )

    if task_id <= 0:
        return (
            False,
            "Invalid task ID. Please enter a numeric ID.",
            None
        )

    return (True, "", task_id)


def validate_menu_choice(choice_str: str) -> tuple[bool, str, int | None]:
    """Validate menu choice is 1-6.

    Args:
        choice_str: User-provided choice string

    Returns:
        Tuple of (is_valid, error_message, choice):
        - (True, "", choice_int) if valid
        - (False, error_message, None) if invalid

    Rules:
        - Trim whitespace
        - Must parse to integer
        - Must be 1-6 inclusive
    """
    trimmed = choice_str.strip()

    try:
        choice = int(trimmed)
    except ValueError:
        return (
            False,
            "Invalid choice. Please select a valid option (1-6).",
            None
        )

    if choice < 1 or choice > 6:
        return (
            False,
            "Invalid choice. Please select a valid option (1-6).",
            None
        )

    return (True, "", choice)


def validate_confirmation(input_str: str) -> tuple[bool, str, bool]:
    """Validate yes/no confirmation input.

    Args:
        input_str: User-provided confirmation string

    Returns:
        Tuple of (is_valid, error_message, confirmed):
        - (True, "", True) for yes
        - (True, "", False) for no
        - (False, error_message, None) for invalid input

    Rules:
        - Trim whitespace
        - Convert to lowercase
        - Accept: 'y', 'yes', 'n', 'no' (case-insensitive)
    """
    trimmed = input_str.strip().lower()

    if trimmed in ['y', 'yes']:
        return (True, "", True)

    if trimmed in ['n', 'no']:
        return (True, "", False)

    return (
        False,
        "Please enter 'y' for yes or 'n' for no.",
        None  # type: ignore
    )
