"""Integration tests for complete workflows.

Test cases cover:
- Complete CRUD workflow (add, view, update, toggle, delete)
- Multi-task management scenario
- Error recovery scenarios
- Edge cases across operations
"""

from services.task_manager import TaskManager


def test_complete_crud_workflow():
    """Test complete workflow: add, view, update, toggle, delete."""
    manager = TaskManager()

    # Start with empty list
    tasks = manager.get_all_tasks()
    assert len(tasks) == 0

    # Add task
    task1 = manager.add_task("Buy groceries", "Milk, eggs, bread")
    assert task1.id == 1
    assert task1.completed is False

    # View all
    tasks = manager.get_all_tasks()
    assert len(tasks) == 1

    # Update task
    success, _, updated = manager.update_task(1, "Buy groceries and household items", "Milk, eggs, bread, soap")
    assert success is True
    assert updated.title == "Buy groceries and household items"

    # Toggle to complete
    success, _, toggled = manager.toggle_task_status(1)
    assert success is True
    assert toggled.completed is True

    # Toggle back to incomplete
    success, _, toggled = manager.toggle_task_status(1)
    assert success is True
    assert toggled.completed is False

    # Delete task
    success, _ = manager.delete_task(1)
    assert success is True
    assert len(manager.get_all_tasks()) == 0


def test_multi_task_management():
    """Test managing multiple tasks with various operations."""
    manager = TaskManager()

    # Add multiple tasks
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")
    task3 = manager.add_task("Task 3", "Description 3")
    task4 = manager.add_task("Task 4", "Description 4")

    assert len(manager.get_all_tasks()) == 4

    # Toggle some tasks
    manager.toggle_task_status(1)
    manager.toggle_task_status(3)

    # Verify status
    assert manager.get_task_by_id(1).completed is True
    assert manager.get_task_by_id(2).completed is False
    assert manager.get_task_by_id(3).completed is True
    assert manager.get_task_by_id(4).completed is False

    # Update middle task
    manager.update_task(2, "Updated Task 2", "Updated Description 2")
    assert manager.get_task_by_id(2).title == "Updated Task 2"

    # Delete one task
    manager.delete_task(3)
    tasks = manager.get_all_tasks()
    assert len(tasks) == 3
    assert manager.get_task_by_id(3) is None

    # Verify remaining tasks intact
    assert manager.get_task_by_id(1) is not None
    assert manager.get_task_by_id(2) is not None
    assert manager.get_task_by_id(4) is not None


def test_error_recovery_scenarios():
    """Test that operations handle errors gracefully."""
    manager = TaskManager()

    # Try to toggle nonexistent task
    success, msg, task = manager.toggle_task_status(999)
    assert success is False
    assert "not found" in msg.lower()

    # Try to update nonexistent task
    success, msg, task = manager.update_task(999, "Title", "Desc")
    assert success is False
    assert "not found" in msg.lower()

    # Try to delete nonexistent task
    success, msg = manager.delete_task(999)
    assert success is False
    assert "not found" in msg.lower()

    # Add a task
    manager.add_task("Task 1")

    # Try to operate on deleted task
    manager.delete_task(1)
    success, msg, task = manager.toggle_task_status(1)
    assert success is False


def test_id_sequence_after_operations():
    """Test that ID sequence remains correct after various operations."""
    manager = TaskManager()

    task1 = manager.add_task("Task 1")
    assert task1.id == 1

    task2 = manager.add_task("Task 2")
    assert task2.id == 2

    # Delete task 1
    manager.delete_task(1)

    # Next task should be ID 3, not 1
    task3 = manager.add_task("Task 3")
    assert task3.id == 3

    # Update task 2
    manager.update_task(2, "Updated Task 2", "")

    # Next task should be ID 4
    task4 = manager.add_task("Task 4")
    assert task4.id == 4


def test_empty_list_operations():
    """Test operations on empty task list."""
    manager = TaskManager()

    # View empty list
    tasks = manager.get_all_tasks()
    assert len(tasks) == 0
    assert tasks == []

    # Try to get task by ID from empty list
    task = manager.get_task_by_id(1)
    assert task is None

    # Try to delete from empty list
    success, msg = manager.delete_task(1)
    assert success is False


def test_description_optional_workflow():
    """Test workflow with and without descriptions."""
    manager = TaskManager()

    # Add task without description
    task1 = manager.add_task("Task without desc")
    assert task1.description == ""

    # Add task with description
    task2 = manager.add_task("Task with desc", "This has a description")
    assert task2.description == "This has a description"

    # Update task to remove description
    manager.update_task(2, "Task with desc", "")
    assert manager.get_task_by_id(2).description == ""

    # Update task to add description
    manager.update_task(1, "Task without desc", "Now has description")
    assert manager.get_task_by_id(1).description == "Now has description"


if __name__ == "__main__":
    test_complete_crud_workflow()
    test_multi_task_management()
    test_error_recovery_scenarios()
    test_id_sequence_after_operations()
    test_empty_list_operations()
    test_description_optional_workflow()
    print("All integration tests passed!")
