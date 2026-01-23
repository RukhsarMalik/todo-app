# Data Model: Chat Endpoint with OpenAI Agent

**Feature**: Phase III Module 3 - Chat Endpoint
**Date**: 2026-01-23
**Spec**: [spec.md](./spec.md)

## Overview

This document defines the data models for the chat endpoint feature. The implementation reuses existing `Conversation` and `Message` models from the database extension work, and adds new Pydantic schemas for API request/response handling.

## Existing Models (Reused)

### Conversation Model
**Location**: `phase-3/backend/models.py`
**Purpose**: Stores conversation metadata and links to associated messages

```python
class Conversation(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(sa_column=Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True))
    title: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

**Attributes**:
- `id`: Unique conversation identifier (UUID string)
- `user_id`: Reference to user who owns the conversation (foreign key to users table with CASCADE delete)
- `title`: Optional conversation title (auto-generated or user-set)
- `created_at`: Timestamp when conversation was started
- `updated_at`: Timestamp when conversation was last updated

### Message Model
**Location**: `phase-3/backend/models.py`
**Purpose**: Stores individual chat messages within conversations

```python
class Message(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    conversation_id: str = Field(sa_column=Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True))
    role: str = Field(max_length=50, nullable=False)  # 'user', 'assistant', 'system'
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        allowed = {"user", "assistant", "system"}
        if v not in allowed:
            raise ValueError(f"role must be one of {allowed}")
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("content cannot be empty")
        if len(v) > 10000:
            raise ValueError("content exceeds 10000 character limit")
        return v
```

**Attributes**:
- `id`: Unique message identifier (UUID string)
- `conversation_id`: Reference to parent conversation (foreign key with CASCADE delete)
- `role`: Message sender role ('user', 'assistant', 'system')
- `content`: Message text content (validated for length and non-empty)
- `created_at`: Timestamp when message was sent (indexed for ordering)

## New Schemas

### Chat Request Schema
**Purpose**: Validates incoming chat messages from clients

```python
from pydantic import BaseModel, field_validator
from typing import Optional
from uuid import UUID

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None  # UUID string format

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
```

**Attributes**:
- `message`: User's message content (required, 1-10,000 characters)
- `conversation_id`: Optional existing conversation ID (UUID string format)

### Chat Response Schema
**Purpose**: Structures the response from the chat endpoint

```python
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ActionResult(BaseModel):
    tool: str
    result: str
    task_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str  # UUID string
    message_id: str  # UUID string for the AI response message
    actions_taken: List[ActionResult] = []
```

**Attributes**:
- `response`: AI-generated response message
- `conversation_id`: ID of the conversation (new or existing)
- `message_id`: ID of the AI response message
- `actions_taken`: List of MCP tool actions taken by the AI agent

### Conversation List Response Schema
**Purpose**: Response for listing user's conversations

```python
from pydantic import BaseModel
from datetime import datetime
from typing import List
from uuid import UUID

class ConversationSummary(BaseModel):
    id: str  # UUID string
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    message_count: int

class ConversationListResponse(BaseModel):
    conversations: List[ConversationSummary]
    count: int
```

**Attributes**:
- `conversations`: Array of conversation summaries
- `count`: Total number of conversations

### Conversation Detail Response Schema
**Purpose**: Response for getting a specific conversation with messages

```python
from pydantic import BaseModel
from datetime import datetime
from typing import List
from uuid import UUID

class MessageDetail(BaseModel):
    id: str  # UUID string
    role: str  # 'user', 'assistant', 'system'
    content: str
    created_at: datetime

class ConversationDetailResponse(BaseModel):
    id: str  # UUID string
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    messages: List[MessageDetail]
```

**Attributes**:
- `id`: Conversation ID
- `title`: Conversation title
- `created_at`: When conversation was created
- `updated_at`: When conversation was last updated
- `messages`: Array of messages in chronological order

### Delete Conversation Response Schema
**Purpose**: Response for deleting a conversation

```python
from pydantic import BaseModel
from uuid import UUID

class DeleteConversationResponse(BaseModel):
    status: str  # "deleted"
    conversation_id: str  # UUID string
```

**Attributes**:
- `status`: Deletion status
- `conversation_id`: ID of the deleted conversation

## Database Relationships

### Conversation ↔ User
- One-to-many relationship (one user has many conversations)
- Foreign key: `conversations.user_id` → `users.id`
- Cascade delete: When user is deleted, all their conversations are deleted

### Conversation ↔ Message
- One-to-many relationship (one conversation has many messages)
- Foreign key: `messages.conversation_id` → `conversations.id`
- Cascade delete: When conversation is deleted, all its messages are deleted

### Indexes
- `idx_conversations_user_id`: Speeds up user conversation queries
- `idx_messages_conversation_id`: Speeds up conversation message queries
- `idx_messages_created_at`: Speeds up message ordering queries

## Validation Rules

### Message Content
- Minimum length: 1 character (after trimming)
- Maximum length: 10,000 characters
- Cannot be empty or whitespace-only

### Message Role
- Must be one of: 'user', 'assistant', 'system'
- Case-sensitive validation

### Conversation Title
- Maximum length: 255 characters
- Optional (can be None)

### UUID Format
- All ID fields must be valid UUID format
- Validation occurs at both database and API levels

## State Transitions

### Conversation States
- New: Created when first message is sent without conversation_id
- Active: When messages are added to existing conversation
- Updated: When conversation's updated_at timestamp changes
- Deleted: When conversation is removed (with all messages via cascade)

### Message States
- Created: When new message is added to conversation
- Stored: After successful database insertion
- Retrieved: When loaded as part of conversation history