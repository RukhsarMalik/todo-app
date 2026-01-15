"""TaskManager service for managing in-memory task collection.

This module implements CRUD operations for tasks with auto-generated IDs.
"""

from datetime import datetime
from models.task import Task


class TaskManager:
    """Manages in-memory collection of tasks with CRUD operations.

    Maintains tasks in a list and generates sequential unique IDs.
    IDs are never reused, even after task deletion.
    """

    def __init__(self) -> None:
        """Initialize empty task list and ID counter.

        Attributes:
            _tasks: Ordered list of tasks (private)
            _next_id: Next ID to assign (starts at 1, never decremented)
        """
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def get_all_tasks(self) -> list[Task]:
        """Return copy of all tasks in creation order.

        Returns:
            List of all tasks (empty list if no tasks exist).
            Returns a copy to prevent external modification.

        Example:
            >>> manager = TaskManager()
            >>> tasks = manager.get_all_tasks()
            >>> len(tasks)
            0
        """
        return self._tasks.copy()

    def add_task(self, title: str, description: str = "") -> Task:
        """Create and add new task with auto-generated ID.

        Args:
            title: Task title (pre-validated, 1-200 chars)
            description: Optional task description (pre-validated, max 1000 chars)

        Returns:
            The newly created Task object with assigned ID and timestamp

        Side effects:
            - Increments _next_id counter
            - Appends task to _tasks list

        Example:
            >>> manager = TaskManager()
            >>> task = manager.add_task("Buy milk", "2% organic")
            >>> task.id
            1
            >>> task.title
            'Buy milk'
            >>> task.completed
            False
        """
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.now()
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_task_by_id(self, task_id: int) -> Task | None:
        """Find and return task by ID.

        Args:
            task_id: ID to search for

        Returns:
            Task object if found, None if not found

        Example:
            >>> manager = TaskManager()
            >>> task = manager.add_task("Test")
            >>> found = manager.get_task_by_id(1)
            >>> found.title
            'Test'
            >>> manager.get_task_by_id(999)
            None
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def toggle_task_status(self, task_id: int) -> tuple[bool, str, Task | None]:
        """Toggle completion status of task.

        Args:
            task_id: ID of task to toggle (pre-validated as positive integer)

        Returns:
            Tuple of (success, message, task):
            - (True, success_message, Task) if task found and toggled
            - (False, error_message, None) if task not found

        Side effects:
            - Modifies task.completed field if task exists

        Example:
            >>> manager = TaskManager()
            >>> task = manager.add_task("Test")
            >>> success, msg, updated = manager.toggle_task_status(1)
            >>> success
            True
            >>> updated.completed
            True
        """
        task = self.get_task_by_id(task_id)

        if task is None:
            return (
                False,
                f"Task with ID {task_id} not found. Use 'View All Tasks' to see available task IDs.",
                None
            )

        # Toggle the status
        task.completed = not task.completed
        new_status = "complete" if task.completed else "incomplete"

        return (
            True,
            f"Task {task_id} marked as {new_status}.",
            task
        )

    def update_task(self, task_id: int, new_title: str, new_description: str) -> tuple[bool, str, Task | None]:
        """Update title and description of existing task.

        Args:
            task_id: ID of task to update (pre-validated as positive integer)
            new_title: New title (pre-validated, 1-200 chars)
            new_description: New description (pre-validated, max 1000 chars)

        Returns:
            Tuple of (success, message, task):
            - (True, success_message, Task) if task found and updated
            - (False, error_message, None) if task not found

        Side effects:
            - Modifies task.title and task.description if task exists

        Example:
            >>> manager = TaskManager()
            >>> task = manager.add_task("Old title", "Old desc")
            >>> success, msg, updated = manager.update_task(1, "New title", "New desc")
            >>> success
            True
            >>> updated.title
            'New title'
        """
        task = self.get_task_by_id(task_id)

        if task is None:
            return (
                False,
                f"Task with ID {task_id} not found. Use 'View All Tasks' to see available task IDs.",
                None
            )

        # Update the task
        task.title = new_title
        task.description = new_description

        return (
            True,
            f"Task {task_id} updated successfully.",
            task
        )

    def delete_task(self, task_id: int) -> tuple[bool, str]:
        """Delete task by ID (ID is never reused).

        Args:
            task_id: ID of task to delete (pre-validated as positive integer)

        Returns:
            Tuple of (success, message):
            - (True, success_message) if task found and deleted
            - (False, error_message) if task not found

        Side effects:
            - Removes task from _tasks list if found
            - Does NOT decrement _next_id (IDs are never reused)

        Example:
            >>> manager = TaskManager()
            >>> task = manager.add_task("To delete")
            >>> success, msg = manager.delete_task(1)
            >>> success
            True
            >>> len(manager.get_all_tasks())
            0
        """
        task = self.get_task_by_id(task_id)

        if task is None:
            return (
                False,
                f"Task with ID {task_id} not found. Use 'View All Tasks' to see available task IDs."
            )

        # Remove task from list
        self._tasks.remove(task)

        return (
            True,
            f"Task {task_id} deleted successfully."
        )
