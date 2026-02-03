"""
SQLModel data models for the Todo application.

This module defines the data models for the application:
- User: Represents an authenticated user (Module 3)
- Task: Represents a todo item in the database (extended with Phase V fields)
- Tag: User-owned tag for task categorization
- TaskTag: Junction table linking tasks to tags (many-to-many)
- Notification: Reminder notification record
- Conversation: Chat session
- Message: Chat message

Usage:
    from models import User, Task, Tag, TaskTag, Notification
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, String, JSON
from sqlmodel import SQLModel, Field
from pydantic import field_validator


# ============================================================================
# Enums
# ============================================================================

class Priority(str, Enum):
    """Task priority levels."""
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


# ============================================================================
# Core Models
# ============================================================================

class Task(SQLModel, table=True):
    """
    Task model representing a todo item in the database.

    Attributes:
        id: Unique identifier (auto-increment primary key).
        user_id: Reference to the task owner (indexed for filtering).
        title: Brief task description (1-200 characters, required).
        description: Detailed task information (max 1000 characters, optional).
        completed: Task completion status (defaults to False).
        priority: Task priority level (low/medium/high/urgent, default: medium).
        due_date: Optional deadline timestamp.
        reminder_offset: Minutes before due_date to trigger reminder (default: 60).
        recurrence_rule: JSON recurrence config (e.g., {"type": "weekly", "days": ["Monday"]}).
        next_occurrence: Computed next due date for recurring tasks.
        parent_task_id: FK to tasks.id linking recurrence chain.
        created_at: Timestamp when task was created (auto-set).
        updated_at: Timestamp of last modification (auto-set, updated on save).
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: str = Field(
        max_length=255,
        index=True,
        nullable=False,
        description="Reference to the task owner"
    )

    title: str = Field(
        min_length=1,
        max_length=200,
        nullable=False,
        description="Brief description of the task"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Detailed task information"
    )

    completed: bool = Field(
        default=False,
        index=True,
        description="Whether the task is completed"
    )

    # Phase V: Advanced fields
    priority: str = Field(
        default="medium",
        max_length=10,
        index=True,
        description="Task priority: low, medium, high, urgent"
    )

    due_date: Optional[datetime] = Field(
        default=None,
        index=True,
        description="Task deadline (UTC)"
    )

    reminder_offset: int = Field(
        default=60,
        description="Minutes before due_date to trigger reminder"
    )

    recurrence_rule: Optional[dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
        description="Recurrence config: {type: daily|weekly|monthly, ...}"
    )

    next_occurrence: Optional[datetime] = Field(
        default=None,
        description="Computed next due date for recurring tasks"
    )

    parent_task_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True, index=True),
        description="FK to parent task in recurrence chain"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="When the task was created (UTC)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="When the task was last modified (UTC)"
    )


class Tag(SQLModel, table=True):
    """
    Tag model for task categorization.

    User-owned tags with unique constraint on (user_id, name).
    """

    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: str = Field(
        max_length=255,
        index=True,
        nullable=False,
        description="Reference to the tag owner"
    )

    name: str = Field(
        min_length=1,
        max_length=100,
        nullable=False,
        description="Tag name"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="When the tag was created (UTC)"
    )


class TaskTag(SQLModel, table=True):
    """
    Junction table linking tasks to tags (many-to-many).
    """

    __tablename__ = "task_tags"

    task_id: int = Field(
        sa_column=Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
        description="FK to tasks"
    )

    tag_id: int = Field(
        sa_column=Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
        description="FK to tags"
    )


class Notification(SQLModel, table=True):
    """
    Notification model for reminder records.
    """

    __tablename__ = "notifications"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: str = Field(
        max_length=255,
        index=True,
        nullable=False,
        description="Reference to the notification recipient"
    )

    task_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True),
        description="FK to the related task"
    )

    message: str = Field(
        nullable=False,
        description="Notification message"
    )

    read: bool = Field(
        default=False,
        description="Whether the notification has been read"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
        description="When the notification was created (UTC)"
    )


class User(SQLModel, table=True):
    """
    User model representing an authenticated user.
    """

    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        max_length=36,
        description="Unique user identifier (UUID)"
    )

    email: str = Field(
        max_length=255,
        unique=True,
        index=True,
        nullable=False,
        description="User's email address (login identifier)"
    )

    password_hash: str = Field(
        max_length=255,
        nullable=False,
        description="bcrypt hashed password"
    )

    name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional display name"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="When the account was created"
    )


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a chat session.
    """

    __tablename__ = "conversations"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        max_length=36,
        description="Unique conversation identifier (UUID)"
    )

    user_id: str = Field(
        sa_column=Column(
            String(36),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        ),
        description="Reference to the conversation owner"
    )

    title: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional conversation title"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="When the conversation was started"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="When the conversation was last updated"
    )


class Message(SQLModel, table=True):
    """
    Message model representing a single chat message.
    """

    __tablename__ = "messages"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        max_length=36,
        description="Unique message identifier (UUID)"
    )

    conversation_id: str = Field(
        sa_column=Column(
            String(36),
            ForeignKey("conversations.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        ),
        description="Reference to the parent conversation"
    )

    role: str = Field(
        max_length=50,
        nullable=False,
        description="Message sender role (user, assistant, system)"
    )

    content: str = Field(
        nullable=False,
        description="Message text content"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
        description="When the message was sent"
    )

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role is one of allowed values."""
        allowed = {"user", "assistant", "system"}
        if v not in allowed:
            raise ValueError(f"role must be one of {allowed}")
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate content is non-empty and within length limit."""
        if not v or not v.strip():
            raise ValueError("content cannot be empty")
        if len(v) > 10000:
            raise ValueError("content exceeds 10000 character limit")
        return v


# Public exports
__all__ = [
    "Priority", "Task", "Tag", "TaskTag", "Notification",
    "User", "Conversation", "Message",
]
