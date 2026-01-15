"""Tests for update task operations.

Test cases cover:
- Update task title and description
- Update task title only (empty description)
- Update nonexistent task (error handling)
- Update doesn't affect other tasks
- Update preserves ID, completed status, and timestamp
"""

from services.task_manager import TaskManager


def test_update_title_and_description():
    """Test updating both title and description."""
    manager = TaskManager()
    task = manager.add_task("Old title", "Old description")

    success, message, updated_task = manager.update_task(1, "New title", "New description")

    assert success is True
    assert "updated successfully" in message.lower()
    assert task.title == "New title"
    assert task.description == "New description"
    assert updated_task.title == "New title"


def test_update_title_only():
    """Test updating title while clearing description."""
    manager = TaskManager()
    task = manager.add_task("Old title", "Old description")

    success, message, updated_task = manager.update_task(1, "Updated title", "")

    assert success is True
    assert task.title == "Updated title"
    assert task.description == ""


def test_update_nonexistent_task():
    """Test updating a task that doesn't exist."""
    manager = TaskManager()
    manager.add_task("Task 1")

    success, message, task = manager.update_task(999, "New title", "New desc")

    assert success is False
    assert "not found" in message.lower()
    assert task is None


def test_update_preserves_id_and_status():
    """Test that update preserves ID, completion status, and timestamp."""
    manager = TaskManager()
    task = manager.add_task("Original", "Description")
    original_id = task.id
    original_timestamp = task.created_at

    # Toggle to complete
    manager.toggle_task_status(1)

    # Update task
    manager.update_task(1, "Updated", "New desc")

    assert task.id == original_id
    assert task.completed is True  # Status preserved
    assert task.created_at == original_timestamp  # Timestamp preserved


def test_update_doesnt_affect_other_tasks():
    """Test that updating one task doesn't affect others."""
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Desc 1")
    task2 = manager.add_task("Task 2", "Desc 2")
    task3 = manager.add_task("Task 3", "Desc 3")

    manager.update_task(2, "Updated Task 2", "Updated Desc 2")

    assert task1.title == "Task 1"
    assert task1.description == "Desc 1"
    assert task2.title == "Updated Task 2"
    assert task2.description == "Updated Desc 2"
    assert task3.title == "Task 3"
    assert task3.description == "Desc 3"


def test_update_from_empty_to_filled_description():
    """Test updating task from empty to filled description."""
    manager = TaskManager()
    task = manager.add_task("Task", "")

    success, _, _ = manager.update_task(1, "Task", "Now with description")

    assert success is True
    assert task.description == "Now with description"


def test_update_from_filled_to_empty_description():
    """Test updating task from filled to empty description."""
    manager = TaskManager()
    task = manager.add_task("Task", "Has description")

    success, _, _ = manager.update_task(1, "Task", "")

    assert success is True
    assert task.description == ""


if __name__ == "__main__":
    test_update_title_and_description()
    test_update_title_only()
    test_update_nonexistent_task()
    test_update_preserves_id_and_status()
    test_update_doesnt_affect_other_tasks()
    test_update_from_empty_to_filled_description()
    test_update_from_filled_to_empty_description()
    print("All update operation tests passed!")
