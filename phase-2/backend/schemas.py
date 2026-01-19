"""
Pydantic schemas for API request/response validation.

This module defines the data transfer objects (DTOs) used for
validating API input and serializing output. These schemas are
separate from the SQLModel models to maintain clean separation
between database and API concerns.

Usage:
    from schemas import TaskCreate, TaskResponse, StatusFilter
    from schemas import UserCreate, UserLogin, TokenResponse
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, EmailStr


# ============================================================================
# Query Parameter Enums
# ============================================================================

class StatusFilter(str, Enum):
    """Filter options for task completion status."""
    all = "all"
    pending = "pending"
    completed = "completed"


class SortField(str, Enum):
    """Available fields for sorting tasks."""
    created = "created"
    title = "title"


class SortOrder(str, Enum):
    """Sort order direction."""
    asc = "asc"
    desc = "desc"


# ============================================================================
# Request Schemas
# ============================================================================

class TaskCreate(BaseModel):
    """
    Schema for creating a new task.

    Used for POST /api/{user_id}/tasks endpoint.

    Attributes:
        title: Task title (1-200 characters, required).
        description: Task description (max 1000 characters, optional).
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional task description (max 1000 characters)"
    )


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    Used for PUT /api/{user_id}/tasks/{id} endpoint.
    Allows partial updates - only provided fields are updated.

    Attributes:
        title: New task title (1-200 characters, optional).
        description: New task description (max 1000 characters, optional).
    """
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="New task title (1-200 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="New task description (max 1000 characters)"
    )


class TaskToggle(BaseModel):
    """
    Schema for toggling task completion status.

    Used for PATCH /api/{user_id}/tasks/{id}/complete endpoint.

    Attributes:
        completed: New completion status (required).
    """
    completed: bool = Field(
        ...,
        description="New completion status"
    )


# ============================================================================
# Response Schemas
# ============================================================================

class TaskResponse(BaseModel):
    """
    Schema for task responses.

    Used as the response model for all task endpoints.
    Maps directly from the Task SQLModel.

    Attributes:
        id: Unique task identifier.
        user_id: Owner user identifier.
        title: Task title.
        description: Task description (nullable).
        completed: Completion status.
        created_at: Creation timestamp (UTC).
        updated_at: Last update timestamp (UTC).
    """
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Auth Request Schemas (Module 3)
# ============================================================================

class UserCreate(BaseModel):
    """
    Schema for user registration (signup).

    Used for POST /api/auth/signup endpoint.

    Attributes:
        email: User's email address (must be valid email format).
        password: User's password (minimum 8 characters).
        name: Optional display name.
    """
    email: EmailStr = Field(
        ...,
        description="User's email address"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Password (minimum 8 characters)"
    )
    name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional display name"
    )


class UserLogin(BaseModel):
    """
    Schema for user authentication (login).

    Used for POST /api/auth/login endpoint.

    Attributes:
        email: Registered email address.
        password: Account password.
    """
    email: EmailStr = Field(
        ...,
        description="Registered email address"
    )
    password: str = Field(
        ...,
        min_length=1,
        description="Account password"
    )


# ============================================================================
# Auth Response Schemas (Module 3)
# ============================================================================

class TokenResponse(BaseModel):
    """
    Schema for JWT token response (signup/login success).

    Used as response model for successful authentication.

    Attributes:
        access_token: JWT access token string.
        token_type: Token type (always "bearer").
        user_id: Authenticated user's ID.
        email: Authenticated user's email.
    """
    access_token: str = Field(
        ...,
        description="JWT access token"
    )
    token_type: str = Field(
        default="bearer",
        description="Token type (always 'bearer')"
    )
    user_id: str = Field(
        ...,
        description="Authenticated user's ID"
    )
    email: EmailStr = Field(
        ...,
        description="Authenticated user's email"
    )


class MessageResponse(BaseModel):
    """
    Schema for generic message responses.

    Used for logout and other simple success responses.

    Attributes:
        message: Response message.
    """
    message: str = Field(
        ...,
        description="Response message"
    )


# ============================================================================
# Profile Update Schemas (Settings)
# ============================================================================

class ProfileUpdate(BaseModel):
    """
    Schema for updating user profile (name).

    Used for PUT /api/auth/profile endpoint.

    Attributes:
        name: New display name.
    """
    name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="New display name"
    )


class PasswordChange(BaseModel):
    """
    Schema for changing user password.

    Used for PUT /api/auth/password endpoint.

    Attributes:
        current_password: Current password for verification.
        new_password: New password (minimum 8 characters).
    """
    current_password: str = Field(
        ...,
        min_length=1,
        description="Current password"
    )
    new_password: str = Field(
        ...,
        min_length=8,
        description="New password (minimum 8 characters)"
    )


class UserResponse(BaseModel):
    """
    Schema for user profile response.

    Used as response model for profile endpoints.

    Attributes:
        id: User's unique identifier.
        email: User's email address.
        name: User's display name.
    """
    id: str = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email")
    name: Optional[str] = Field(default=None, description="Display name")

    model_config = ConfigDict(from_attributes=True)


# Public exports
__all__ = [
    "StatusFilter",
    "SortField",
    "SortOrder",
    "TaskCreate",
    "TaskUpdate",
    "TaskToggle",
    "TaskResponse",
    "UserCreate",
    "UserLogin",
    "TokenResponse",
    "MessageResponse",
    "ProfileUpdate",
    "PasswordChange",
    "UserResponse",
]
