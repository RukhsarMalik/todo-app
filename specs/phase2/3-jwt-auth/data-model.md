# Data Model: JWT Authentication

**Feature**: 004-jwt-auth
**Date**: 2026-01-18
**Status**: Design Complete

## Overview

This document defines the data model for user authentication in the Todo API. It introduces the `User` entity for storing user credentials and profile information.

## Entity: User

### Purpose

Store registered users with hashed passwords for authentication.

### Table Definition

```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,           -- UUID as string
    email VARCHAR(255) NOT NULL UNIQUE,   -- Login identifier
    password_hash VARCHAR(255) NOT NULL,  -- bcrypt hash
    name VARCHAR(255),                    -- Optional display name
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

### SQLModel Implementation

```python
"""
User model for authentication.

Location: phase-2/backend/models.py (add to existing file)
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlmodel import SQLModel, Field


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
```

### Field Specifications

| Field | Type | Constraints | Validation | Notes |
|-------|------|-------------|------------|-------|
| id | VARCHAR(36) | PK, NOT NULL | UUID format | Generated on signup |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email format | Case-insensitive |
| password_hash | VARCHAR(255) | NOT NULL | - | bcrypt output ~60 chars |
| name | VARCHAR(255) | NULL | Max 255 chars | Optional at signup |
| created_at | TIMESTAMP | NOT NULL | - | Auto-set |

---

## API Schemas

### Request Schemas

```python
"""
Auth request schemas.

Location: phase-2/backend/schemas.py (add to existing file)
"""

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Signup request body."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str | None = Field(default=None, max_length=255)


class UserLogin(BaseModel):
    """Login request body."""
    email: EmailStr
    password: str = Field(..., min_length=1)
```

### Response Schemas

```python
"""
Auth response schemas.

Location: phase-2/backend/schemas.py (add to existing file)
"""

from pydantic import BaseModel, EmailStr, ConfigDict


class TokenResponse(BaseModel):
    """JWT token response (signup/login success)."""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: EmailStr


class UserResponse(BaseModel):
    """User info without password (for future profile endpoints)."""
    id: str
    email: EmailStr
    name: str | None

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    """Generic message response (logout, errors)."""
    message: str
```

---

## JWT Token Structure

### Payload Claims

```json
{
    "sub": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "exp": 1737331200
}
```

| Claim | Type | Description |
|-------|------|-------------|
| sub | string | User ID (maps to User.id) |
| email | string | User's email (for display) |
| exp | integer | Expiration timestamp (Unix epoch) |

### Token Properties

- **Algorithm**: HS256 (HMAC with SHA-256)
- **Expiration**: 7 days from issuance
- **Issuer**: Not set (single-service MVP)
- **Audience**: Not set (single-service MVP)

---

## Relationships

### User → Task

```
users.id (PK) ←→ tasks.user_id (FK, indexed)
```

- One-to-Many: One user has many tasks
- Cascade Delete: When user deleted, all their tasks deleted
- Current State: tasks.user_id is string, matches User.id type

**Note**: Foreign key constraint will be added in implementation to enforce referential integrity.

### Updated Task Model

```python
# No changes needed - Task.user_id is already compatible
class Task(SQLModel, table=True):
    user_id: str = Field(
        max_length=255,
        index=True,
        nullable=False,
        # FK constraint added separately:
        # foreign_key="users.id"
    )
```

---

## Migration Considerations

### Initial Setup (Greenfield)

For MVP, User table is created fresh via `init_db.py`:

```python
# In db.py - already handles table creation
async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

### Data Integrity

1. **Email Uniqueness**: Enforced at database level
2. **Password Storage**: Only bcrypt hash stored, never plaintext
3. **User Deletion**: Consider soft delete for production (out of MVP scope)

---

## Security Considerations

1. **Password Never Exposed**: Use `UserResponse` (not `User`) in API responses
2. **Email Case**: Store lowercase, compare case-insensitively
3. **Token Claims**: Minimal - only sub, email, exp
4. **Timing Attacks**: Use constant-time comparison for passwords (passlib handles this)
