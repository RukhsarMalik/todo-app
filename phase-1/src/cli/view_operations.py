"""View operations for displaying tasks in Todo Console App CLI."""

from models.task import Task
from services.task_manager import TaskManager


def handle_view_all(manager: TaskManager) -> None:
    """Display all tasks or empty state message.

    Args:
        manager: TaskManager instance containing tasks

    Behavior:
        - If no tasks exist: prints friendly empty state message
        - If tasks exist: prints numbered list with status, title, description
        - Format: [ID] [✓/✗] Title - Description (Created: timestamp)

    Example output (empty):
        No tasks found. Add your first task to get started!

    Example output (with tasks):
        === All Tasks ===
        [1] [✗] Buy groceries - Milk, eggs, bread (Created: 2025-12-25 10:30:00)
        [2] [✓] Review PR - Check code quality (Created: 2025-12-25 09:15:00)
    """
    tasks = manager.get_all_tasks()

    if not tasks:
        print("No tasks found. Add your first task to get started!")
        return

    print("\n=== All Tasks ===")
    for task in tasks:
        status_icon = "✓" if task.completed else "✗"
        timestamp = task.created_at.strftime("%Y-%m-%d %H:%M:%S")

        # Format: [ID] [✓/✗] Title - Description (Created: timestamp)
        if task.description:
            print(f"[{task.id}] [{status_icon}] {task.title} - {task.description} (Created: {timestamp})")
        else:
            print(f"[{task.id}] [{status_icon}] {task.title} (Created: {timestamp})")

    print()
