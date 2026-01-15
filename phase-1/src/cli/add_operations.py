"""Add task operations for Todo Console App CLI."""

from services.task_manager import TaskManager
from validators.input_validators import validate_title, validate_description


def handle_add_task(manager: TaskManager) -> None:
    """Prompt user for task details and create new task.

    Args:
        manager: TaskManager instance to add task to

    Behavior:
        1. Prompt for title (required, 1-200 chars)
        2. Validate title, re-prompt on error
        3. Prompt for description (optional, max 1000 chars)
        4. Validate description, re-prompt on error
        5. Create task and display success message with ID

    Validation:
        - Title: trimmed, non-empty, max 200 chars
        - Description: trimmed, optional, max 1000 chars

    Example interaction:
        Enter task title: Buy groceries
        Enter task description (optional): Milk, eggs, bread
        Task added successfully! (ID: 1)
    """
    # Prompt and validate title (required)
    while True:
        title_input = input("Enter task title: ")
        is_valid, error_msg, title = validate_title(title_input)

        if is_valid:
            break
        print(f"Error: {error_msg}")

    # Prompt and validate description (optional)
    while True:
        description_input = input("Enter task description (optional): ")
        is_valid, error_msg, description = validate_description(description_input)

        if is_valid:
            break
        print(f"Error: {error_msg}")

    # Create task
    task = manager.add_task(title, description)

    print(f"Task added successfully! (ID: {task.id})")
