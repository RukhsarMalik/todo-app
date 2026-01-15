"""Main entry point for Todo Console App.

This module implements the main application loop that:
1. Initializes TaskManager
2. Displays menu
3. Handles user choice
4. Routes to appropriate operation
5. Loops until user exits
"""

from services.task_manager import TaskManager
from cli import (
    display_menu,
    handle_view_all,
    handle_add_task,
    handle_toggle_status,
    handle_update_task,
    handle_delete_task,
)
from validators.input_validators import validate_menu_choice


def main() -> None:
    """Run the main application loop.

    Behavior:
        1. Create TaskManager instance
        2. Display menu
        3. Prompt for choice (1-6)
        4. Validate and execute choice
        5. Repeat until user selects Exit (6)

    Menu options:
        1. View All Tasks
        2. Add Task
        3. Update Task
        4. Delete Task
        5. Toggle Task Status
        6. Exit
    """
    manager = TaskManager()

    print("Welcome to Todo Console App!")

    while True:
        display_menu()

        # Get and validate user choice
        choice_input = input("Enter your choice (1-6): ")
        is_valid, error_msg, choice = validate_menu_choice(choice_input)

        if not is_valid:
            print(f"Error: {error_msg}")
            continue

        # Route to appropriate handler
        if choice == 1:
            handle_view_all(manager)
        elif choice == 2:
            handle_add_task(manager)
        elif choice == 3:
            handle_update_task(manager)
        elif choice == 4:
            handle_delete_task(manager)
        elif choice == 5:
            handle_toggle_status(manager)
        elif choice == 6:
            print("Thank you for using Todo Console App. Goodbye!")
            break


if __name__ == "__main__":
    main()
