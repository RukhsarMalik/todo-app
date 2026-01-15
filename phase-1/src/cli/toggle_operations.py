"""Toggle task status operations for Todo Console App CLI."""

from services.task_manager import TaskManager
from validators.input_validators import validate_task_id


def handle_toggle_status(manager: TaskManager) -> None:
    """Prompt user for task ID and toggle its completion status.

    Args:
        manager: TaskManager instance containing tasks

    Behavior:
        1. Prompt for task ID
        2. Validate ID (numeric, positive)
        3. Toggle status via TaskManager
        4. Display success or error message

    Validation:
        - ID must be numeric and positive
        - Task must exist in system

    Example interaction (success):
        Enter task ID to toggle: 1
        Task 1 marked as complete.

    Example interaction (not found):
        Enter task ID to toggle: 999
        Error: Task with ID 999 not found. Use 'View All Tasks' to see available task IDs.

    Example interaction (invalid input):
        Enter task ID to toggle: abc
        Error: Invalid task ID. Please enter a numeric ID.
    """
    while True:
        task_id_input = input("Enter task ID to toggle: ")
        is_valid, error_msg, task_id = validate_task_id(task_id_input)

        if not is_valid:
            print(f"Error: {error_msg}")
            continue

        # Attempt to toggle
        success, message, _ = manager.toggle_task_status(task_id)

        if success:
            print(message)
            break
        else:
            print(f"Error: {message}")
            # Re-prompt on not found
