"""Tests for delete task operations.

Test cases cover:
- Delete existing task
- Delete nonexistent task (error handling)
- ID not reused after deletion
- Delete from multiple tasks
- Delete doesn't affect other tasks
"""

from services.task_manager import TaskManager


def test_delete_existing_task():
    """Test deleting a task that exists."""
    manager = TaskManager()
    manager.add_task("Task to delete", "Description")

    success, message = manager.delete_task(1)

    assert success is True
    assert "deleted successfully" in message.lower()
    assert len(manager.get_all_tasks()) == 0
    assert manager.get_task_by_id(1) is None


def test_delete_nonexistent_task():
    """Test deleting a task that doesn't exist."""
    manager = TaskManager()
    manager.add_task("Task 1")

    success, message = manager.delete_task(999)

    assert success is False
    assert "not found" in message.lower()
    assert len(manager.get_all_tasks()) == 1


def test_id_not_reused_after_deletion():
    """Test that IDs are never reused after task deletion."""
    manager = TaskManager()

    task1 = manager.add_task("Task 1")
    assert task1.id == 1

    manager.delete_task(1)

    task2 = manager.add_task("Task 2")
    assert task2.id == 2  # ID 2, not 1 (not reused)

    task3 = manager.add_task("Task 3")
    assert task3.id == 3


def test_delete_from_multiple_tasks():
    """Test deleting one task from multiple tasks."""
    manager = TaskManager()
    task1 = manager.add_task("Task 1")
    task2 = manager.add_task("Task 2")
    task3 = manager.add_task("Task 3")

    success, _ = manager.delete_task(2)

    assert success is True
    tasks = manager.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[1].id == 3


def test_delete_doesnt_affect_other_tasks():
    """Test that deleting one task doesn't affect others."""
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Desc 1")
    task2 = manager.add_task("Task 2", "Desc 2")
    task3 = manager.add_task("Task 3", "Desc 3")

    manager.delete_task(2)

    assert task1.title == "Task 1"
    assert task1.description == "Desc 1"
    assert task3.title == "Task 3"
    assert task3.description == "Desc 3"


def test_delete_all_tasks():
    """Test deleting all tasks one by one."""
    manager = TaskManager()
    manager.add_task("Task 1")
    manager.add_task("Task 2")
    manager.add_task("Task 3")

    manager.delete_task(1)
    manager.delete_task(2)
    manager.delete_task(3)

    assert len(manager.get_all_tasks()) == 0


def test_delete_then_add_new_task():
    """Test adding new task after deletion."""
    manager = TaskManager()

    task1 = manager.add_task("Task 1")
    manager.delete_task(1)

    task2 = manager.add_task("Task 2")

    assert len(manager.get_all_tasks()) == 1
    assert task2.id == 2
    assert task2.title == "Task 2"


if __name__ == "__main__":
    test_delete_existing_task()
    test_delete_nonexistent_task()
    test_id_not_reused_after_deletion()
    test_delete_from_multiple_tasks()
    test_delete_doesnt_affect_other_tasks()
    test_delete_all_tasks()
    test_delete_then_add_new_task()
    print("All delete operation tests passed!")
