"""Tests for toggle task status operations.

Test cases cover:
- Toggle incomplete task to complete
- Toggle complete task to incomplete
- Toggle nonexistent task (error handling)
- Multiple toggles on same task
- get_task_by_id helper method
"""

from services.task_manager import TaskManager


def test_toggle_incomplete_to_complete():
    """Test toggling an incomplete task to complete."""
    manager = TaskManager()
    task = manager.add_task("Test task", "Description")

    assert task.completed is False

    success, message, updated_task = manager.toggle_task_status(1)

    assert success is True
    assert "marked as complete" in message
    assert updated_task.completed is True
    assert updated_task.id == 1


def test_toggle_complete_to_incomplete():
    """Test toggling a complete task to incomplete."""
    manager = TaskManager()
    task = manager.add_task("Test task")

    # Toggle to complete first
    manager.toggle_task_status(1)
    assert task.completed is True

    # Toggle back to incomplete
    success, message, updated_task = manager.toggle_task_status(1)

    assert success is True
    assert "marked as incomplete" in message
    assert updated_task.completed is False


def test_toggle_nonexistent_task():
    """Test toggling a task that doesn't exist."""
    manager = TaskManager()
    manager.add_task("Task 1")

    success, message, task = manager.toggle_task_status(999)

    assert success is False
    assert "not found" in message.lower()
    assert task is None


def test_toggle_multiple_times():
    """Test toggling the same task multiple times."""
    manager = TaskManager()
    task = manager.add_task("Toggle test")

    # First toggle: incomplete → complete
    success1, _, _ = manager.toggle_task_status(1)
    assert success1 is True
    assert task.completed is True

    # Second toggle: complete → incomplete
    success2, _, _ = manager.toggle_task_status(1)
    assert success2 is True
    assert task.completed is False

    # Third toggle: incomplete → complete
    success3, _, _ = manager.toggle_task_status(1)
    assert success3 is True
    assert task.completed is True


def test_get_task_by_id_found():
    """Test get_task_by_id when task exists."""
    manager = TaskManager()
    task1 = manager.add_task("Task 1")
    task2 = manager.add_task("Task 2")

    found = manager.get_task_by_id(2)

    assert found is not None
    assert found.id == 2
    assert found.title == "Task 2"


def test_get_task_by_id_not_found():
    """Test get_task_by_id when task doesn't exist."""
    manager = TaskManager()
    manager.add_task("Task 1")

    found = manager.get_task_by_id(999)

    assert found is None


def test_toggle_affects_correct_task():
    """Test that toggle only affects the specified task."""
    manager = TaskManager()
    task1 = manager.add_task("Task 1")
    task2 = manager.add_task("Task 2")
    task3 = manager.add_task("Task 3")

    manager.toggle_task_status(2)

    assert task1.completed is False
    assert task2.completed is True
    assert task3.completed is False


if __name__ == "__main__":
    test_toggle_incomplete_to_complete()
    test_toggle_complete_to_incomplete()
    test_toggle_nonexistent_task()
    test_toggle_multiple_times()
    test_get_task_by_id_found()
    test_get_task_by_id_not_found()
    test_toggle_affects_correct_task()
    print("All toggle operation tests passed!")
