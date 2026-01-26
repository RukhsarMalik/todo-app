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
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator


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


# ============================================================================
# Chat Endpoint Schemas (Phase III)
# ============================================================================


class ChatRequest(BaseModel):
    """
    Schema for chat message requests.

    Used for POST /api/{user_id}/chat endpoint.

    Attributes:
        message: User's message content (1-10,000 characters, required).
        conversation_id: Optional existing conversation ID (UUID format).
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="User's message content (1-10,000 characters)"
    )
    conversation_id: Optional[str] = Field(
        default=None,
        description="Optional existing conversation ID (UUID format)"
    )

    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Message content cannot be empty')
        if len(v) > 10000:
            raise ValueError('Message exceeds 10,000 character limit')
        return v.strip()

    @field_validator('conversation_id')
    @classmethod
    def validate_conversation_id(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            try:
                UUID(v)  # Validate UUID format
            except ValueError:
                raise ValueError('conversation_id must be a valid UUID')
        return v


class ActionResult(BaseModel):
    """
    Schema for MCP tool action results.

    Part of ChatResponse to track what tools were called.

    Attributes:
        tool: Name of the MCP tool that was called.
        result: Result of the tool call.
        task_id: Optional task ID affected by the tool call.
    """
    tool: str = Field(
        ...,
        description="Name of the MCP tool that was called"
    )
    result: str = Field(
        ...,
        description="Result of the tool call"
    )
    task_id: Optional[str] = Field(
        default=None,
        description="Optional task ID affected by the tool call"
    )


class ChatResponse(BaseModel):
    """
    Schema for chat message responses.

    Used as response model for POST /api/{user_id}/chat endpoint.

    Attributes:
        response: AI-generated response message.
        conversation_id: ID of the conversation (new or existing).
        message_id: ID of the AI response message.
        actions_taken: List of MCP tool actions taken by the AI agent.
    """
    response: str = Field(
        ...,
        description="AI-generated response message"
    )
    conversation_id: str = Field(
        ...,
        description="ID of the conversation (new or existing)"
    )
    message_id: str = Field(
        ...,
        description="ID of the AI response message"
    )
    actions_taken: List[ActionResult] = Field(
        default=[],
        description="List of MCP tool actions taken by the AI agent"
    )


class ConversationSummary(BaseModel):
    """
    Schema for conversation summary in list responses.

    Part of ConversationListResponse for listing user's conversations.

    Attributes:
        id: Unique conversation identifier (UUID).
        title: Optional conversation title.
        created_at: When the conversation was created.
        updated_at: When the conversation was last updated.
        message_count: Number of messages in the conversation.
    """
    id: str = Field(
        ...,
        description="Unique conversation identifier (UUID)"
    )
    title: Optional[str] = Field(
        default=None,
        description="Optional conversation title"
    )
    created_at: datetime = Field(
        ...,
        description="When the conversation was created"
    )
    updated_at: datetime = Field(
        ...,
        description="When the conversation was last updated"
    )
    message_count: int = Field(
        ...,
        description="Number of messages in the conversation"
    )


class ConversationListResponse(BaseModel):
    """
    Schema for conversation list responses.

    Used as response model for GET /api/{user_id}/conversations endpoint.

    Attributes:
        conversations: Array of conversation summaries.
        count: Total number of conversations.
    """
    conversations: List[ConversationSummary] = Field(
        ...,
        description="Array of conversation summaries"
    )
    count: int = Field(
        ...,
        description="Total number of conversations"
    )


class MessageDetail(BaseModel):
    """
    Schema for individual message details.

    Part of ConversationDetailResponse for detailed conversation view.

    Attributes:
        id: Unique message identifier (UUID).
        role: Message sender role ('user', 'assistant', 'system').
        content: Message text content.
        created_at: When the message was sent.
    """
    id: str = Field(
        ...,
        description="Unique message identifier (UUID)"
    )
    role: str = Field(
        ...,
        description="Message sender role ('user', 'assistant', 'system')"
    )
    content: str = Field(
        ...,
        description="Message text content"
    )
    created_at: datetime = Field(
        ...,
        description="When the message was sent"
    )


class ConversationDetailResponse(BaseModel):
    """
    Schema for conversation detail responses.

    Used as response model for GET /api/{user_id}/conversations/{id} endpoint.

    Attributes:
        id: Conversation ID.
        title: Conversation title.
        created_at: When conversation was created.
        updated_at: When conversation was last updated.
        messages: Array of messages in chronological order.
    """
    id: str = Field(
        ...,
        description="Conversation ID"
    )
    title: Optional[str] = Field(
        default=None,
        description="Conversation title"
    )
    created_at: datetime = Field(
        ...,
        description="When conversation was created"
    )
    updated_at: datetime = Field(
        ...,
        description="When conversation was last updated"
    )
    messages: List[MessageDetail] = Field(
        ...,
        description="Array of messages in chronological order"
    )


class DeleteConversationResponse(BaseModel):
    """
    Schema for conversation deletion responses.

    Used as response model for DELETE /api/{user_id}/conversations/{id} endpoint.

    Attributes:
        status: Deletion status ('deleted').
        conversation_id: ID of the deleted conversation.
    """
    status: str = Field(
        ...,
        description="Deletion status ('deleted')"
    )
    conversation_id: str = Field(
        ...,
        description="ID of the deleted conversation"
    )


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
    "ChatRequest",
    "ChatResponse",
    "ActionResult",
    "ConversationSummary",
    "ConversationListResponse",
    "MessageDetail",
    "ConversationDetailResponse",
    "DeleteConversationResponse",
]
