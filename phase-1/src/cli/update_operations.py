"""Update task operations for Todo Console App CLI."""

from services.task_manager import TaskManager
from validators.input_validators import validate_task_id, validate_title, validate_description


def handle_update_task(manager: TaskManager) -> None:
    """Prompt user for task ID and new details, then update task.

    Args:
        manager: TaskManager instance containing tasks

    Behavior:
        1. Prompt for task ID
        2. Validate ID (numeric, positive)
        3. Check if task exists
        4. Display current task details
        5. Prompt for new title (required)
        6. Validate title, re-prompt on error
        7. Prompt for new description (optional)
        8. Validate description, re-prompt on error
        9. Update task and display success message

    Validation:
        - ID must be numeric and positive
        - Task must exist in system
        - New title: trimmed, non-empty, max 200 chars
        - New description: trimmed, optional, max 1000 chars

    Example interaction (success):
        Enter task ID to update: 1
        Current: [1] Buy groceries - Milk, eggs
        Enter new title: Buy groceries and household items
        Enter new description (optional): Milk, eggs, bread, cleaning supplies
        Task 1 updated successfully.

    Example interaction (not found):
        Enter task ID to update: 999
        Error: Task with ID 999 not found. Use 'View All Tasks' to see available task IDs.
    """
    # Prompt and validate task ID
    while True:
        task_id_input = input("Enter task ID to update: ")
        is_valid, error_msg, task_id = validate_task_id(task_id_input)

        if not is_valid:
            print(f"Error: {error_msg}")
            continue

        # Check if task exists
        existing_task = manager.get_task_by_id(task_id)
        if existing_task is None:
            print(f"Error: Task with ID {task_id} not found. Use 'View All Tasks' to see available task IDs.")
            continue

        # Show current task details
        print(f"Current: [{existing_task.id}] {existing_task.title} - {existing_task.description}")
        break

    # Prompt and validate new title
    while True:
        title_input = input("Enter new title: ")
        is_valid, error_msg, new_title = validate_title(title_input)

        if is_valid:
            break
        print(f"Error: {error_msg}")

    # Prompt and validate new description
    while True:
        description_input = input("Enter new description (optional): ")
        is_valid, error_msg, new_description = validate_description(description_input)

        if is_valid:
            break
        print(f"Error: {error_msg}")

    # Update task
    success, message, _ = manager.update_task(task_id, new_title, new_description)

    if success:
        print(message)
    else:
        print(f"Error: {message}")
