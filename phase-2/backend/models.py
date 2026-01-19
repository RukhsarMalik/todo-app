"""
SQLModel data models for the Todo application.

This module defines the data models for the application:
- User: Represents an authenticated user (Module 3)
- Task: Represents a todo item in the database

Usage:
    from models import User, Task

    user = User(email="user@example.com", password_hash="...")
    task = Task(user_id=user.id, title="Buy groceries")
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    """
    Task model representing a todo item in the database.

    Attributes:
        id: Unique identifier (auto-increment primary key).
        user_id: Reference to the task owner (indexed for filtering).
        title: Brief task description (1-200 characters, required).
        description: Detailed task information (max 1000 characters, optional).
        completed: Task completion status (defaults to False).
        created_at: Timestamp when task was created (auto-set).
        updated_at: Timestamp of last modification (auto-set, updated on save).

    Table:
        Name: tasks
        Indexes: idx_tasks_user_id, idx_tasks_completed

    Example:
        task = Task(
            user_id="auth0|123456",
            title="Complete project documentation",
            description="Write comprehensive docs for the API endpoints"
        )
    """

    __tablename__ = "tasks"

    # Primary key - auto-increment integer
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign key reference to user (indexed for efficient filtering)
    # Note: FK constraint to users table created when Module 3 adds auth
    user_id: str = Field(
        max_length=255,
        index=True,
        nullable=False,
        description="Reference to the task owner"
    )

    # Task title - required, 1-200 characters
    title: str = Field(
        min_length=1,
        max_length=200,
        nullable=False,
        description="Brief description of the task"
    )

    # Task description - optional, max 1000 characters
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Detailed task information"
    )

    # Completion status - defaults to incomplete
    completed: bool = Field(
        default=False,
        index=True,
        description="Whether the task is completed"
    )

    # Timestamps - auto-set on creation (UTC, timezone-naive for PostgreSQL compatibility)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="When the task was created (UTC)"
    )

    # Updated timestamp - set on creation, updated manually on modifications
    # Note: Auto-update logic will be added in Module 2 API layer
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="When the task was last modified (UTC)"
    )


class User(SQLModel, table=True):
    """
    User model representing an authenticated user.

    Attributes:
        id: Unique identifier (UUID string, primary key).
        email: User's email address (unique, used for login).
        password_hash: bcrypt hashed password (never exposed in responses).
        name: Optional display name.
        created_at: Account creation timestamp.

    Table:
        Name: users
        Indexes: idx_users_email

    Security:
        - password_hash is NEVER returned in API responses
        - Use separate response schemas without password_hash

    Example:
        user = User(
            email="user@example.com",
            password_hash=hash_password("secret123"),
            name="John Doe"
        )
    """

    __tablename__ = "users"

    # Primary key - UUID as string for JWT compatibility
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        max_length=36,
        description="Unique user identifier (UUID)"
    )

    # Email - unique login identifier
    email: str = Field(
        max_length=255,
        unique=True,
        index=True,
        nullable=False,
        description="User's email address (login identifier)"
    )

    # Password hash - bcrypt hashed, never exposed
    password_hash: str = Field(
        max_length=255,
        nullable=False,
        description="bcrypt hashed password"
    )

    # Display name - optional
    name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional display name"
    )

    # Creation timestamp
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="When the account was created"
    )


# Public exports
__all__ = ["Task", "User"]
