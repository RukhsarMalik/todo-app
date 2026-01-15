"""Tests for add task operations.

Test cases cover:
- Adding task with valid title and description
- Adding task with valid title only (empty description)
- ID auto-increment behavior
- Task properties (completed=False, timestamp)
"""

from datetime import datetime
from services.task_manager import TaskManager


def test_add_task_with_description():
    """Test adding task with title and description."""
    manager = TaskManager()

    task = manager.add_task("Buy groceries", "Milk, eggs, bread")

    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description == "Milk, eggs, bread"
    assert task.completed is False
    assert isinstance(task.created_at, datetime)

    # Verify task is in manager's list
    tasks = manager.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == 1


def test_add_task_without_description():
    """Test adding task with title only."""
    manager = TaskManager()

    task = manager.add_task("Review PR")

    assert task.id == 1
    assert task.title == "Review PR"
    assert task.description == ""
    assert task.completed is False


def test_add_multiple_tasks_id_increment():
    """Test ID auto-increment with multiple tasks."""
    manager = TaskManager()

    task1 = manager.add_task("Task 1", "First")
    task2 = manager.add_task("Task 2", "Second")
    task3 = manager.add_task("Task 3")

    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3

    tasks = manager.get_all_tasks()
    assert len(tasks) == 3


def test_add_task_timestamp_recent():
    """Test that created_at timestamp is recent."""
    manager = TaskManager()

    before = datetime.now()
    task = manager.add_task("Time test")
    after = datetime.now()

    assert before <= task.created_at <= after


def test_add_task_default_description():
    """Test that description defaults to empty string."""
    manager = TaskManager()

    task = manager.add_task("Task without description")

    assert task.description == ""
    assert isinstance(task.description, str)


if __name__ == "__main__":
    test_add_task_with_description()
    test_add_task_without_description()
    test_add_multiple_tasks_id_increment()
    test_add_task_timestamp_recent()
    test_add_task_default_description()
    print("All add operation tests passed!")
