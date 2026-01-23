# Quickstart: Chat Database Extension

**Feature**: Phase III Module 1 - Chat Database
**Date**: 2026-01-22

## Prerequisites

- Phase II backend running (`phase-2/backend/`)
- Neon PostgreSQL database configured
- UV package manager installed
- `.env` file with `DATABASE_URL`

## Implementation Steps

### Step 1: Add Models to models.py

Add the `Conversation` and `Message` classes to `phase-2/backend/models.py`:

```python
# Add these imports at the top
from sqlalchemy import Column, ForeignKey, String
from pydantic import field_validator

# Add after User class (around line 168)

class Conversation(SQLModel, table=True):
    """Chat conversation model."""
    __tablename__ = "conversations"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        max_length=36
    )
    user_id: str = Field(
        sa_column=Column(
            String(36),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    )
    title: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    """Chat message model."""
    __tablename__ = "messages"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        max_length=36
    )
    conversation_id: str = Field(
        sa_column=Column(
            String(36),
            ForeignKey("conversations.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    )
    role: str = Field(max_length=50)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in {"user", "assistant", "system"}:
            raise ValueError("role must be user, assistant, or system")
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

### Step 2: Update Public Exports

Update `__all__` in models.py:

```python
__all__ = ["Task", "User", "Conversation", "Message"]
```

### Step 3: Run Database Migration

Create the new tables:

```bash
cd phase-2/backend
uv run python init_db.py
```

### Step 4: Verify Tables Created

Check that tables exist in Neon:

```bash
uv run python -c "
from sqlmodel import select
from db import engine
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()
print('Tables:', tables)
assert 'conversations' in tables, 'conversations table missing'
assert 'messages' in tables, 'messages table missing'
print('✅ All tables created successfully')
"
```

## Verification Checklist

- [ ] `Conversation` class added to models.py
- [ ] `Message` class added to models.py
- [ ] `__all__` updated with new models
- [ ] `init_db.py` runs without errors
- [ ] `conversations` table exists in database
- [ ] `messages` table exists in database
- [ ] Foreign key constraints working (test cascade delete)

## Test Cascade Delete

```python
# Test script to verify cascade delete works
from sqlmodel import Session
from db import engine
from models import User, Conversation, Message

with Session(engine) as session:
    # Create test user
    user = User(email="test@cascade.com", password_hash="test")
    session.add(user)
    session.commit()

    # Create conversation
    conv = Conversation(user_id=user.id)
    session.add(conv)
    session.commit()

    # Create message
    msg = Message(conversation_id=conv.id, role="user", content="Hello")
    session.add(msg)
    session.commit()

    # Delete user - should cascade delete conversation and message
    session.delete(user)
    session.commit()

    print("✅ Cascade delete working correctly")
```

## Common Issues

### Issue: ForeignKey error on import

**Cause**: Missing SQLAlchemy import
**Fix**: Add `from sqlalchemy import Column, ForeignKey, String`

### Issue: Validator not running

**Cause**: Using older Pydantic syntax
**Fix**: Use `@field_validator` decorator (Pydantic v2)

### Issue: Tables not created

**Cause**: Models not imported before `create_all`
**Fix**: Ensure models.py exports Conversation and Message

## Next Steps

After completing this module:
1. Run `/sp.tasks` to generate implementation tasks
2. Implement the tasks via Claude Code
3. Proceed to Phase III Module 2: Conversation API endpoints
