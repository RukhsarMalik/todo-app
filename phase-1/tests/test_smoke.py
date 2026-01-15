"""Smoke test to verify application can start and basic functionality works.

This test verifies:
- All modules import correctly
- TaskManager can be instantiated
- Basic operations are callable
- No import errors or syntax errors
"""

import sys


def test_imports():
    """Test that all modules can be imported."""
    try:
        from models.task import Task
        from services.task_manager import TaskManager
        from validators.input_validators import (
            validate_title,
            validate_description,
            validate_task_id,
            validate_menu_choice,
            validate_confirmation,
        )
        from cli import (
            display_menu,
            handle_view_all,
            handle_add_task,
            handle_toggle_status,
            handle_update_task,
            handle_delete_task,
        )
        print("All imports successful")
        return True
    except Exception as e:
        print(f"Import failed: {e}")
        return False


def test_task_manager_instantiation():
    """Test that TaskManager can be created."""
    try:
        from services.task_manager import TaskManager
        manager = TaskManager()
        assert manager is not None
        assert len(manager.get_all_tasks()) == 0
        print("TaskManager instantiation successful")
        return True
    except Exception as e:
        print(f"TaskManager instantiation failed: {e}")
        return False


def test_basic_operations():
    """Test that basic operations work."""
    try:
        from services.task_manager import TaskManager

        manager = TaskManager()

        # Add
        task = manager.add_task("Test task", "Test description")
        assert task.id == 1

        # Get all
        tasks = manager.get_all_tasks()
        assert len(tasks) == 1

        # Get by ID
        found = manager.get_task_by_id(1)
        assert found is not None

        # Toggle
        success, _, _ = manager.toggle_task_status(1)
        assert success is True

        # Update
        success, _, _ = manager.update_task(1, "Updated", "Updated desc")
        assert success is True

        # Delete
        success, _ = manager.delete_task(1)
        assert success is True

        print("Basic operations successful")
        return True
    except Exception as e:
        print(f"Basic operations failed: {e}")
        return False


def test_validators():
    """Test that validators work."""
    try:
        from validators.input_validators import (
            validate_title,
            validate_description,
            validate_task_id,
            validate_menu_choice,
            validate_confirmation,
        )

        # Test title validator
        is_valid, _, _ = validate_title("Test")
        assert is_valid is True

        # Test description validator
        is_valid, _, _ = validate_description("Test description")
        assert is_valid is True

        # Test task ID validator
        is_valid, _, _ = validate_task_id("1")
        assert is_valid is True

        # Test menu choice validator
        is_valid, _, _ = validate_menu_choice("1")
        assert is_valid is True

        # Test confirmation validator
        is_valid, _, _ = validate_confirmation("y")
        assert is_valid is True

        print("Validators successful")
        return True
    except Exception as e:
        print(f"Validators failed: {e}")
        return False


def main():
    """Run all smoke tests."""
    print("=" * 60)
    print("Running Smoke Tests")
    print("=" * 60)
    print()

    tests = [
        ("Import Test", test_imports),
        ("TaskManager Instantiation", test_task_manager_instantiation),
        ("Basic Operations", test_basic_operations),
        ("Validators", test_validators),
    ]

    results = []
    for name, test_func in tests:
        print(f"Running {name}...", end=" ")
        success = test_func()
        results.append((name, success))
        if success:
            print()

    print()
    print("=" * 60)
    print("Smoke Test Results")
    print("=" * 60)
    print()

    passed = sum(1 for _, success in results if success)
    failed = sum(1 for _, success in results if not success)

    for name, success in results:
        status = "PASSED" if success else "FAILED"
        print(f"{name:.<40} {status}")

    print()
    print(f"Total: {len(results)} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()

    if failed > 0:
        print("Smoke tests FAILED!")
        sys.exit(1)
    else:
        print("All smoke tests PASSED!")
        sys.exit(0)


if __name__ == "__main__":
    main()
