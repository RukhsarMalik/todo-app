"""Delete task operations for Todo Console App CLI."""

from services.task_manager import TaskManager
from validators.input_validators import validate_task_id, validate_confirmation


def handle_delete_task(manager: TaskManager) -> None:
    """Prompt user for task ID, confirm, then delete task.

    Args:
        manager: TaskManager instance containing tasks

    Behavior:
        1. Prompt for task ID
        2. Validate ID (numeric, positive)
        3. Check if task exists
        4. Display task details for confirmation
        5. Prompt for confirmation (y/n)
        6. If confirmed, delete task and display success
        7. If not confirmed, cancel operation

    Validation:
        - ID must be numeric and positive
        - Task must exist in system
        - Confirmation must be y/yes or n/no (case-insensitive)

    Example interaction (confirmed):
        Enter task ID to delete: 1
        Are you sure you want to delete this task?
        [1] Buy groceries - Milk, eggs
        Confirm deletion (y/n): y
        Task 1 deleted successfully.

    Example interaction (cancelled):
        Enter task ID to delete: 1
        Are you sure you want to delete this task?
        [1] Buy groceries - Milk, eggs
        Confirm deletion (y/n): n
        Deletion cancelled.

    Example interaction (not found):
        Enter task ID to delete: 999
        Error: Task with ID 999 not found. Use 'View All Tasks' to see available task IDs.
    """
    # Prompt and validate task ID
    while True:
        task_id_input = input("Enter task ID to delete: ")
        is_valid, error_msg, task_id = validate_task_id(task_id_input)

        if not is_valid:
            print(f"Error: {error_msg}")
            continue

        # Check if task exists
        existing_task = manager.get_task_by_id(task_id)
        if existing_task is None:
            print(f"Error: Task with ID {task_id} not found. Use 'View All Tasks' to see available task IDs.")
            continue

        # Show task details for confirmation
        print("Are you sure you want to delete this task?")
        if existing_task.description:
            print(f"[{existing_task.id}] {existing_task.title} - {existing_task.description}")
        else:
            print(f"[{existing_task.id}] {existing_task.title}")
        break

    # Prompt for confirmation
    while True:
        confirm_input = input("Confirm deletion (y/n): ")
        is_valid, error_msg, confirmed = validate_confirmation(confirm_input)

        if not is_valid:
            print(f"Error: {error_msg}")
            continue

        if not confirmed:
            print("Deletion cancelled.")
            return

        # Delete task
        success, message = manager.delete_task(task_id)

        if success:
            print(message)
        else:
            print(f"Error: {message}")
        break
