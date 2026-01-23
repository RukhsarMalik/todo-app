# Data Model: Chat Database Extension

**Feature**: Phase III Module 1 - Chat Database
**Date**: 2026-01-22

## Entity Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Entity Relationship Diagram                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────┐         ┌──────────────┐         ┌─────────┐      │
│  │  User   │ 1    N  │ Conversation │ 1    N  │ Message │      │
│  │  (PII)  │────────►│              │────────►│         │      │
│  └─────────┘         └──────────────┘         └─────────┘      │
│                                                                 │
│  Existing            NEW                      NEW               │
│  (Phase II)          (Phase III)              (Phase III)       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Entities

### Conversation (NEW)

Represents a chat session between a user and the AI assistant.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID (str) | PK, auto-generated | Unique conversation identifier |
| user_id | str(36) | FK → users.id, CASCADE DELETE, NOT NULL, INDEX | Owner of the conversation |
| title | str(255) | NULL | Optional conversation title (auto-generated or user-set) |
| created_at | datetime | NOT NULL, default NOW | When conversation was started |
| updated_at | datetime | NOT NULL, default NOW | When conversation was last updated |

**Relationships**:
- Belongs to one User (many-to-one)
- Has many Messages (one-to-many)

**Business Rules**:
- A conversation MUST have a user_id
- When user is deleted, all their conversations are deleted (CASCADE)
- updated_at is refreshed when new messages are added

### Message (NEW)

Represents a single message within a conversation.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID (str) | PK, auto-generated | Unique message identifier |
| conversation_id | str(36) | FK → conversations.id, CASCADE DELETE, NOT NULL, INDEX | Parent conversation |
| role | str(50) | NOT NULL, CHECK(user/assistant/system) | Who sent the message |
| content | text | NOT NULL, non-empty, max 10,000 chars | Message text content |
| created_at | datetime | NOT NULL, default NOW, INDEX | When message was sent |

**Relationships**:
- Belongs to one Conversation (many-to-one)

**Business Rules**:
- A message MUST have a conversation_id
- A message MUST have a valid role (user, assistant, or system)
- A message MUST have non-empty content
- Content is limited to 10,000 characters
- When conversation is deleted, all its messages are deleted (CASCADE)
- Messages are ordered by created_at (ascending) for display

## SQLModel Implementation

### Conversation Model

```python
from datetime import datetime
from uuid import uuid4
from typing import Optional

from sqlalchemy import Column, ForeignKey, String
from sqlmodel import SQLModel, Field
from pydantic import field_validator


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
```

### Message Model

```python
class Message(SQLModel, table=True):
    """
    Message model representing a single chat message.

    Attributes:
        id: Unique identifier (UUID string, primary key).
        conversation_id: Reference to the parent conversation.
        role: Message sender role (user, assistant, or system).
        content: Message text content (max 10,000 chars).
        created_at: When the message was sent.

    Table:
        Name: messages
        Indexes: idx_messages_conversation_id, idx_messages_created_at
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
```

## Database Schema (SQL)

```sql
-- Conversation table
CREATE TABLE conversations (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- Message table
CREATE TABLE messages (
    id VARCHAR(36) PRIMARY KEY,
    conversation_id VARCHAR(36) NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

## Validation Rules Summary

| Entity | Field | Rule | Error Message |
|--------|-------|------|---------------|
| Message | role | Must be user/assistant/system | "role must be one of {user, assistant, system}" |
| Message | content | Cannot be empty/whitespace | "content cannot be empty" |
| Message | content | Max 10,000 characters | "content exceeds 10000 character limit" |

## State Transitions

Conversations and Messages are append-only with no state transitions. Once created:
- Conversations can be deleted (cascade deletes messages)
- Messages cannot be modified or deleted individually
- updated_at on Conversation is refreshed when messages are added
