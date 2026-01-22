# Phase 0 Research: JWT Authentication

**Feature**: 004-jwt-auth
**Date**: 2026-01-18
**Status**: Complete

## Research Questions

### 1. JWT Library Selection

**Question**: Which Python JWT library is best for FastAPI integration?

**Options Evaluated**:

| Library | Pros | Cons | Verdict |
|---------|------|------|---------|
| python-jose | FastAPI official recommendation, JWK support, active maintenance | Requires cryptography extras | ✅ SELECTED |
| PyJWT | Simple API, widely used | Less FastAPI integration docs | ❌ |
| authlib | Full OAuth2 support | Overkill for simple JWT | ❌ |

**Decision**: Use `python-jose[cryptography]`

**Rationale**: FastAPI's official security documentation recommends python-jose. It provides robust JWT encoding/decoding with proper algorithm support and integrates well with FastAPI's dependency injection pattern.

**Installation**:
```bash
uv add "python-jose[cryptography]"
```

**Usage Pattern**:
```python
from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
EXPIRE_DAYS = 7

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

---

### 2. Password Hashing Library

**Question**: Which bcrypt implementation for secure password hashing?

**Options Evaluated**:

| Library | Pros | Cons | Verdict |
|---------|------|------|---------|
| passlib[bcrypt] | FastAPI recommended, CryptContext abstraction, auto-upgrade | Additional dependency | ✅ SELECTED |
| bcrypt | Direct, minimal | Manual salt handling | ❌ |
| argon2-cffi | Modern algorithm | Not as widely tested | ❌ |

**Decision**: Use `passlib[bcrypt]`

**Rationale**: FastAPI security tutorial uses passlib's CryptContext for password hashing. It provides automatic bcrypt configuration with secure defaults and supports password hash upgrades.

**Installation**:
```bash
uv add "passlib[bcrypt]"
```

**Usage Pattern**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

---

### 3. Route Protection Pattern

**Question**: How to protect routes - middleware or dependency injection?

**Options Evaluated**:

| Pattern | Pros | Cons | Verdict |
|---------|------|------|---------|
| Dependency Injection | Per-route control, testable, type-safe | Repetitive on many routes | ✅ SELECTED |
| Middleware Class | Global, automatic | Less flexibility | ❌ |
| APIRouter dependencies | Applied to all routes in router | Still need extraction logic | Combined |

**Decision**: Dependency injection with `Depends()`

**Rationale**: FastAPI's dependency injection provides route-level control and is easily testable. We can combine with APIRouter's `dependencies` parameter to apply to all task routes at once.

**Usage Pattern**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """Extract and verify user_id from JWT token."""
    token = credentials.credentials
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Apply to router
router = APIRouter(dependencies=[Depends(get_current_user)])
```

---

### 4. User ID Format

**Question**: UUID vs string for user_id in the User model?

**Options Evaluated**:

| Format | Pros | Cons | Verdict |
|--------|------|------|---------|
| UUID string | Constitution suggests UUID, globally unique | Requires uuid generation | ✅ SELECTED |
| Integer | Simple, auto-increment | Predictable, not portable | ❌ |
| Pure UUID type | Type-safe | Mismatch with existing Task.user_id (str) | ❌ |

**Decision**: UUID stored as string

**Rationale**: The existing Task model uses `user_id: str`. For consistency and easy JWT integration (JWT claims are strings), we'll use UUID strings. The `uuid.uuid4()` function generates globally unique identifiers.

**Usage Pattern**:
```python
from uuid import uuid4

class User(SQLModel, table=True):
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True
    )
```

---

### 5. Token Storage Strategy

**Question**: Where should the frontend store JWT tokens?

**Options Evaluated**:

| Storage | Pros | Cons | Verdict |
|---------|------|------|---------|
| httpOnly Cookie | XSS-safe | Requires CORS config, CSRF risk | Future consideration |
| localStorage | Simple, persistent | XSS vulnerable | ✅ MVP |
| sessionStorage | Tab-scoped | Lost on close | ❌ |
| Memory only | Most secure | Lost on refresh | ❌ |

**Decision**: localStorage for MVP (frontend decision)

**Rationale**: For the MVP, localStorage is simplest. The backend returns the token in the response body, and the frontend (Module 4) decides storage. Token is sent via `Authorization: Bearer <token>` header.

---

## Dependencies Summary

```toml
# Add to pyproject.toml
[project.dependencies]
# ... existing deps ...
python-jose = { version = "^3.3.0", extras = ["cryptography"] }
passlib = { version = "^1.7.4", extras = ["bcrypt"] }
```

**UV Command**:
```bash
cd phase-2/backend
uv add "python-jose[cryptography]" "passlib[bcrypt]"
```

---

## Environment Variables

```env
# Add to .env
JWT_SECRET_KEY=your-super-secret-key-at-least-32-characters-long
```

**Requirements**:
- Minimum 32 characters for security
- Random, unpredictable string
- Different per environment (dev/staging/prod)
- Never committed to version control

---

## Security Considerations

1. **Token Expiry**: 7 days balances UX and security for MVP
2. **No Refresh Tokens**: Simplifies MVP; users re-login after expiry
3. **Client-Side Logout**: Backend stateless; client discards token
4. **Password Requirements**: Minimum 8 characters (can enhance later)
5. **Rate Limiting**: Not in MVP scope; recommended for production
6. **HTTPS**: Required in production; enforced by deployment platform

---

## References

- [FastAPI Security Tutorial](https://fastapi.tiangolo.com/tutorial/security/)
- [FastAPI OAuth2 with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [python-jose Documentation](https://python-jose.readthedocs.io/)
- [passlib Documentation](https://passlib.readthedocs.io/)
