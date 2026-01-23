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

from sqlalchemy import Column, ForeignKey, String
from sqlmodel import SQLModel, Field
from pydantic import field_validator


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


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a chat session.

    Attributes:
        id: Unique identifier (UUID string, primary key).
        user_id: Reference to the conversation owner (FK to users).
        title: Optional conversation title.
        created_at: When the conversation was started.
        updated_at: When the conversation was last updated.

    Table:
        Name: conversations
        Indexes: idx_conversations_user_id
    """

    __tablename__ = "conversations"

    # Primary key - UUID as string
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        max_length=36,
        description="Unique conversation identifier (UUID)"
    )

    # Foreign key to users with CASCADE delete
    user_id: str = Field(
        sa_column=Column(
            String(36),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        ),
        description="Reference to the conversation owner"
    )

    # Optional title
    title: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional conversation title"
    )

    # Timestamps
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

    Attributes:
        id: Unique identifier (UUID string, primary key).
        conversation_id: Reference to the parent conversation (FK).
        role: Message sender role (user, assistant, or system).
        content: Message text content (max 10,000 chars).
        created_at: When the message was sent.

    Table:
        Name: messages
        Indexes: idx_messages_conversation_id, idx_messages_created_at
    """

    __tablename__ = "messages"

    # Primary key - UUID as string
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        max_length=36,
        description="Unique message identifier (UUID)"
    )

    # Foreign key to conversations with CASCADE delete
    conversation_id: str = Field(
        sa_column=Column(
            String(36),
            ForeignKey("conversations.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        ),
        description="Reference to the parent conversation"
    )

    # Message role - must be user, assistant, or system
    role: str = Field(
        max_length=50,
        nullable=False,
        description="Message sender role (user, assistant, system)"
    )

    # Message content - required, max 10000 characters
    content: str = Field(
        nullable=False,
        description="Message text content"
    )

    # Timestamp with index for ordering
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
__all__ = ["Task", "User", "Conversation", "Message"]
