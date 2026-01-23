# Research: Chat Database Extension

**Feature**: Phase III Module 1 - Chat Database
**Date**: 2026-01-22

## Research Tasks

### 1. SQLModel Foreign Key Patterns

**Question**: How to implement foreign key relationships with cascade delete in SQLModel?

**Decision**: Use `Field(foreign_key="table.column")` with SQLAlchemy relationship for cascade.

**Rationale**:
- SQLModel inherits SQLAlchemy's FK support
- Existing Task model uses string-based user_id without FK constraint
- For chat tables, use proper FK with `ondelete="CASCADE"` via sa_column

**Alternatives Considered**:
- Manual FK via raw SQL - Rejected: Loses SQLModel benefits
- No FK, manual cleanup - Rejected: Risk of orphaned records

**Implementation Pattern**:
```python
from sqlalchemy import Column, ForeignKey, String

class Conversation(SQLModel, table=True):
    user_id: str = Field(
        sa_column=Column(
            String(36),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    )
```

### 2. Message Role Validation

**Question**: How to validate message role values (user/assistant/system)?

**Decision**: Use string field with Pydantic validator, plus CHECK constraint at DB level.

**Rationale**:
- Python Enum would require custom type handling
- String is simpler and matches OpenAI API message format
- Pydantic @field_validator provides application-level validation
- CHECK constraint provides database-level integrity

**Alternatives Considered**:
- Python Enum with sa_type - Rejected: Complex serialization
- No validation - Rejected: Data integrity risk

**Implementation Pattern**:
```python
from pydantic import field_validator

class Message(SQLModel, table=True):
    role: str = Field(max_length=50)

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        allowed = {"user", "assistant", "system"}
        if v not in allowed:
            raise ValueError(f"role must be one of {allowed}")
        return v
```

### 3. Content Length Validation

**Question**: How to enforce 10,000 character limit on message content?

**Decision**: Use Pydantic `max_length` validator with TEXT database column.

**Rationale**:
- TEXT type in PostgreSQL has no length limit, so validation must be at application level
- Pydantic validator runs before database insert
- 10,000 chars is sufficient for chat messages while preventing abuse

**Implementation Pattern**:
```python
from pydantic import field_validator

class Message(SQLModel, table=True):
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("content cannot be empty")
        if len(v) > 10000:
            raise ValueError("content exceeds 10000 character limit")
        return v
```

### 4. Existing User ID Type Compatibility

**Question**: What type does the existing User model use for ID?

**Decision**: Use `str` (UUID as string, max 36 chars) to match existing User.id type.

**Rationale**:
- Existing User model: `id: str = Field(default_factory=lambda: str(uuid4()), max_length=36)`
- Conversation.user_id must match this type for FK relationship
- String UUIDs are JWT-compatible (existing auth system)

**Source**: `phase-2/backend/models.py:129-134`

### 5. Index Strategy

**Question**: What indexes are needed for efficient queries?

**Decision**: Create indexes on:
1. `conversations.user_id` - List conversations by user
2. `messages.conversation_id` - Get messages for conversation
3. `messages.created_at` - Order messages chronologically

**Rationale**:
- User conversation listing is frequent (every chat page load)
- Message retrieval by conversation is the primary access pattern
- Chronological ordering requires timestamp index

**Query Patterns**:
```sql
-- List user's conversations (most recent first)
SELECT * FROM conversations WHERE user_id = ? ORDER BY updated_at DESC;

-- Get messages for conversation (chronological)
SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC;
```

## Summary of Decisions

| Topic | Decision | Key Reason |
|-------|----------|------------|
| FK Implementation | SQLAlchemy Column with ondelete CASCADE | Proper referential integrity |
| User ID Type | String (36 chars) | Match existing User.id |
| Role Validation | Pydantic validator + allowed set | Application-level safety |
| Content Validation | Pydantic validator (non-empty, max 10k) | Prevent empty/oversized messages |
| Indexes | user_id, conversation_id, created_at | Query performance |

## Unknowns Resolved

All NEEDS CLARIFICATION items from Technical Context have been resolved:
- ✅ FK cascade behavior confirmed
- ✅ Type compatibility with existing models verified
- ✅ Validation approach selected
- ✅ Index strategy defined
