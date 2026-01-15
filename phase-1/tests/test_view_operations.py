"""Tests for view operations module.

Test cases cover:
- Empty task list display
- Single task display (completed and incomplete)
- Multiple tasks display with mixed statuses
- Tasks with and without descriptions
"""

from datetime import datetime
from io import StringIO
import sys

from models.task import Task
from services.task_manager import TaskManager
from cli.view_operations import handle_view_all


def test_view_empty_list():
    """Test viewing when no tasks exist."""
    manager = TaskManager()

    # Capture output
    captured_output = StringIO()
    sys.stdout = captured_output

    handle_view_all(manager)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert "No tasks found. Add your first task to get started!" in output
    assert "=== All Tasks ===" not in output


def test_view_single_incomplete_task():
    """Test viewing a single incomplete task."""
    manager = TaskManager()
    # Directly add task to bypass add_task (not implemented yet)
    task = Task(
        id=1,
        title="Buy groceries",
        description="Milk, eggs, bread",
        completed=False,
        created_at=datetime(2025, 12, 25, 10, 30, 0)
    )
    manager._tasks.append(task)
    manager._next_id = 2

    captured_output = StringIO()
    sys.stdout = captured_output

    handle_view_all(manager)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert "=== All Tasks ===" in output
    assert "[1] [✗] Buy groceries - Milk, eggs, bread (Created: 2025-12-25 10:30:00)" in output


def test_view_single_completed_task():
    """Test viewing a single completed task."""
    manager = TaskManager()
    task = Task(
        id=1,
        title="Review PR",
        description="",
        completed=True,
        created_at=datetime(2025, 12, 25, 9, 15, 0)
    )
    manager._tasks.append(task)
    manager._next_id = 2

    captured_output = StringIO()
    sys.stdout = captured_output

    handle_view_all(manager)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert "=== All Tasks ===" in output
    assert "[1] [✓] Review PR (Created: 2025-12-25 09:15:00)" in output
    assert " - " not in output  # No description separator


def test_view_multiple_tasks_mixed_status():
    """Test viewing multiple tasks with mixed completion status."""
    manager = TaskManager()

    tasks = [
        Task(1, "Task 1", "First task", False, datetime(2025, 12, 25, 8, 0, 0)),
        Task(2, "Task 2", "", True, datetime(2025, 12, 25, 9, 0, 0)),
        Task(3, "Task 3", "Third task", True, datetime(2025, 12, 25, 10, 0, 0)),
    ]
    manager._tasks.extend(tasks)
    manager._next_id = 4

    captured_output = StringIO()
    sys.stdout = captured_output

    handle_view_all(manager)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert "=== All Tasks ===" in output
    assert "[1] [✗] Task 1 - First task" in output
    assert "[2] [✓] Task 2 (Created:" in output
    assert "[3] [✓] Task 3 - Third task" in output


if __name__ == "__main__":
    test_view_empty_list()
    test_view_single_incomplete_task()
    test_view_single_completed_task()
    test_view_multiple_tasks_mixed_status()
    print("All view operation tests passed!")
