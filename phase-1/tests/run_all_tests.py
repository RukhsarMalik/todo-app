"""Comprehensive test runner for Todo Console App.

Runs all test modules and reports results.
"""

import sys
import subprocess
import os


def run_test_file(filepath: str, name: str) -> tuple[bool, str]:
    """Run a single test file and capture result.

    Args:
        filepath: Path to test file
        name: Display name for test suite

    Returns:
        Tuple of (success, output)
    """
    try:
        # Get src directory path relative to this file
        test_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(os.path.dirname(test_dir), "src")

        result = subprocess.run(
            [sys.executable, filepath],
            capture_output=True,
            text=True,
            timeout=10,
            env={"PYTHONPATH": src_dir}
        )

        if result.returncode == 0:
            return (True, result.stdout.strip())
        else:
            return (False, result.stderr.strip())

    except subprocess.TimeoutExpired:
        return (False, "Test timed out after 10 seconds")
    except Exception as e:
        return (False, f"Error running test: {str(e)}")


def main():
    """Run all test suites and report results."""
    test_suites = [
        ("tests/test_validators.py", "Input Validators"),
        ("tests/test_view_operations.py", "View Operations"),
        ("tests/test_add_operations.py", "Add Operations"),
        ("tests/test_toggle_operations.py", "Toggle Operations"),
        ("tests/test_update_operations.py", "Update Operations"),
        ("tests/test_delete_operations.py", "Delete Operations"),
        ("tests/test_integration.py", "Integration Tests"),
    ]

    print("=" * 60)
    print("Running Todo Console App Test Suite")
    print("=" * 60)
    print()

    results = []

    for filepath, name in test_suites:
        print(f"Running {name}...", end=" ")
        success, output = run_test_file(filepath, name)

        if success:
            print("PASSED")
            results.append((name, True, output))
        else:
            print("FAILED")
            results.append((name, False, output))

    print()
    print("=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    print()

    passed = sum(1 for _, success, _ in results if success)
    failed = sum(1 for _, success, _ in results if not success)

    for name, success, output in results:
        status = "PASSED" if success else "FAILED"
        print(f"{name:.<40} {status}")

    print()
    print(f"Total: {len(results)} test suites")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()

    if failed > 0:
        print("Failed test details:")
        print("-" * 60)
        for name, success, output in results:
            if not success:
                print(f"\n{name}:")
                print(output)
        sys.exit(1)
    else:
        print("All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
