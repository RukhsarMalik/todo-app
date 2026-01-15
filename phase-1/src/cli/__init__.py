"""CLI operations for Todo Console App."""

from .menu import display_menu
from .view_operations import handle_view_all
from .add_operations import handle_add_task
from .toggle_operations import handle_toggle_status
from .update_operations import handle_update_task
from .delete_operations import handle_delete_task

__all__ = [
    "display_menu",
    "handle_view_all",
    "handle_add_task",
    "handle_toggle_status",
    "handle_update_task",
    "handle_delete_task",
]
