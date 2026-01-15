"""Menu display functions for Todo Console App CLI."""


def display_menu() -> None:
    """Display main menu with 6 numbered options.

    Shows:
        - Menu title
        - 6 numbered operations
        - Blank line for readability
    """
    print("\n=== Todo Console App ===")
    print("1. View All Tasks")
    print("2. Add Task")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Toggle Task Status")
    print("6. Exit")
    print()
