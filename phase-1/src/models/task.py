"""Task data model for Todo Console App.

This module defines the Task dataclass representing a single todo item.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    """A single todo item with title, description, and completion status.

    Attributes:
        id: Unique sequential identifier (auto-generated, never reused)
        title: Short descriptive text (required, 1-200 characters)
        description: Optional detailed information (max 1000 characters)
        completed: Completion status (default False, toggleable)
        created_at: Timestamp when task was created (auto-generated)
    """

    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
