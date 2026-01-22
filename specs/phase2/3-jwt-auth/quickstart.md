# Quickstart: JWT Authentication

**Feature**: 004-jwt-auth
**Date**: 2026-01-18

## Prerequisites

- Module 1 (Database) complete: Neon PostgreSQL connected
- Module 2 (Backend API) complete: FastAPI server running
- Python 3.12+ with UV package manager

## Step 1: Install Dependencies

```bash
cd phase-2/backend
uv add "python-jose[cryptography]" "passlib[bcrypt]"
```

This installs:
- `python-jose[cryptography]` - JWT encoding/decoding
- `passlib[bcrypt]` - Secure password hashing

## Step 2: Configure Environment

Add to `.env`:

```env
# Existing
DATABASE_URL=postgresql+asyncpg://...

# NEW: JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-minimum-32-characters-long
```

**Generate a secure secret**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Update `.env.example`:
```env
DATABASE_URL=postgresql+asyncpg://user:password@host/database?ssl=require
JWT_SECRET_KEY=your-super-secret-key-minimum-32-characters-long
```

## Step 3: Create Auth Module

Create the `auth/` package:

```bash
mkdir -p phase-2/backend/auth
touch phase-2/backend/auth/__init__.py
touch phase-2/backend/auth/password.py
touch phase-2/backend/auth/jwt.py
touch phase-2/backend/auth/middleware.py
```

## Step 4: Implement Password Hashing

`auth/password.py`:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

## Step 5: Implement JWT Handling

`auth/jwt.py`:
```python
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

def create_access_token(user_id: str, email: str) -> str:
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode = {"sub": user_id, "email": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

## Step 6: Implement Auth Middleware

`auth/middleware.py`:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from .jwt import decode_access_token

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id, "email": payload.get("email")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Step 7: Add User Model

Add to `models.py`:
```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Step 8: Add Auth Schemas

Add to `schemas.py`:
```python
from pydantic import EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: EmailStr
```

## Step 9: Create Auth Routes

Create `routes/auth.py`:
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from db import get_session
from models import User
from schemas import UserCreate, UserLogin, TokenResponse
from auth.password import hash_password, verify_password
from auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=TokenResponse, status_code=201)
async def signup(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    # Check email exists
    existing = await session.execute(select(User).where(User.email == user_data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        name=user_data.name
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Generate token
    token = create_access_token(user.id, user.email)
    return TokenResponse(access_token=token, user_id=user.id, email=user.email)

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, session: AsyncSession = Depends(get_session)):
    # Find user
    result = await session.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.id, user.email)
    return TokenResponse(access_token=token, user_id=user.id, email=user.email)

@router.post("/logout")
async def logout():
    return {"message": "Successfully logged out"}
```

## Step 10: Update Task Routes

In `routes/tasks.py`, add JWT dependency:
```python
from auth.middleware import get_current_user

# Add to each endpoint function signature:
async def list_tasks(
    user_id: str,
    current_user: dict = Depends(get_current_user),  # NEW
    ...
):
    # Verify user_id matches token
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    # ... rest of function
```

## Step 11: Register Auth Router

In `main.py`:
```python
from routes.auth import router as auth_router

app.include_router(auth_router, prefix="/api")
```

## Step 12: Test the Flow

```bash
# Start server
uv run uvicorn main:app --reload --port 8000

# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Use token for protected endpoints
TOKEN="<token from login>"
curl http://localhost:8000/api/<user_id>/tasks \
  -H "Authorization: Bearer $TOKEN"
```

## Verification Checklist

- [ ] Dependencies installed (`python-jose`, `passlib`)
- [ ] JWT_SECRET_KEY in .env (32+ characters)
- [ ] User table created on startup
- [ ] Signup returns 201 with token
- [ ] Login returns 200 with token
- [ ] Task endpoints return 401 without token
- [ ] Task endpoints return 403 for wrong user_id
- [ ] Task endpoints work with valid token + matching user_id
