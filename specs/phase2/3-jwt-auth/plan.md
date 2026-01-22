# Implementation Plan: JWT Authentication

**Branch**: `004-jwt-auth` | **Date**: 2026-01-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-jwt-auth/spec.md`

## Summary

Implement JWT-based authentication for the Todo API with user signup/login endpoints, password hashing with bcrypt, and middleware to protect all task endpoints. The authentication module integrates with existing Module 2 (Backend API) by adding authorization checks to verify that the JWT token's user_id matches the URL path user_id.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: FastAPI, SQLModel, python-jose (JWT), passlib[bcrypt] (password hashing)
**Storage**: Neon PostgreSQL (existing from Module 1) + User table
**Testing**: Manual testing via curl (per spec)
**Target Platform**: Linux server (via Railway/Render)
**Project Type**: Web application backend (monorepo)
**Performance Goals**: <50ms JWT verification overhead, <5s signup, <3s login
**Constraints**: 7-day token expiry, no refresh tokens, client-side logout only
**Scale/Scope**: MVP authentication - single auth method (email/password)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| VIII. Monorepo Structure | ✅ PASS | Auth code in `phase-2/backend/` following existing structure |
| IX. API-First Design | ✅ PASS | RESTful endpoints (POST /api/auth/signup, /login, /logout) |
| X. Database Persistence | ✅ PASS | User table in Neon PostgreSQL |
| XI. Multi-User Support | ✅ PASS | JWT enables user isolation via token.user_id |
| XII. Authentication Required | ✅ PASS | This module implements the JWT requirement |

**Phase II Security Requirements Check**:
- ✅ JWT tokens for authentication
- ✅ Token verification on every API request (middleware)
- ✅ User isolation via user_id validation
- ✅ Environment variable for JWT_SECRET_KEY
- ✅ No hardcoded credentials

## Project Structure

### Documentation (this feature)

```text
specs/004-jwt-auth/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── auth-openapi.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
phase-2/backend/
├── main.py              # FastAPI app (add auth router, update CORS)
├── schemas.py           # Add auth schemas (UserCreate, UserLogin, TokenResponse)
├── models.py            # Add User model
├── db.py                # Existing - no changes needed
├── auth/                # NEW: Authentication module
│   ├── __init__.py      # Auth exports
│   ├── jwt.py           # JWT creation and verification
│   ├── password.py      # Password hashing with bcrypt
│   └── middleware.py    # JWT verification middleware/dependency
└── routes/
    ├── __init__.py      # Update to include auth_router
    ├── tasks.py         # Update to require JWT verification dependency
    └── auth.py          # NEW: Auth endpoints (signup, login, logout)
```

**Structure Decision**: Modular structure within existing `phase-2/backend/` directory. Auth logic separated into `auth/` package for clean separation. Routes extended in `routes/` following Module 2 pattern.

## Phase 0: Technology Research

### Research Questions

1. **JWT Library Selection**: Which Python JWT library for FastAPI?
   - Options: python-jose, PyJWT, authlib
   - Recommendation: python-jose (FastAPI docs recommend it)

2. **Password Hashing**: Which bcrypt implementation?
   - Options: passlib[bcrypt], bcrypt
   - Recommendation: passlib[bcrypt] (FastAPI security docs recommend it)

3. **Middleware Pattern**: How to protect routes in FastAPI?
   - Options: Dependency injection, middleware class
   - Recommendation: Dependency injection via `Depends()` for route-level control

4. **User ID Format**: UUID vs string for user_id?
   - Options: UUID (constitution suggests), string (simpler, matches existing Task.user_id)
   - Recommendation: String for consistency with existing Task model

### Research Artifacts

See `research.md` for detailed research findings.

## Phase 1: Design

### Data Model

**User Entity** (new table):

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | str | PK, unique | User identifier (UUID string) |
| email | str | unique, indexed | User's email address |
| password_hash | str | not null | bcrypt hashed password |
| name | str | nullable | Optional display name |
| created_at | datetime | not null, default now | Account creation timestamp |

See `data-model.md` for SQLModel implementation.

### API Contracts

**Auth Endpoints**:

| Method | Endpoint | Request | Response | Status |
|--------|----------|---------|----------|--------|
| POST | /api/auth/signup | UserCreate | TokenResponse | 201 |
| POST | /api/auth/login | UserLogin | TokenResponse | 200 |
| POST | /api/auth/logout | - | {message} | 200 |

**Protected Endpoints** (existing, add JWT dependency):

All `/api/{user_id}/tasks/*` endpoints require:
- `Authorization: Bearer <token>` header
- token.user_id must match URL user_id

See `contracts/auth-openapi.yaml` for OpenAPI specification.

### JWT Token Structure

```json
{
  "sub": "user_id_string",
  "email": "user@example.com",
  "exp": 1234567890
}
```

- `sub`: User ID (maps to user_id in Task)
- `email`: User's email for display purposes
- `exp`: Expiration timestamp (7 days from issuance)

### Integration Points

**Module 2 Updates Required**:

1. `routes/tasks.py`: Add `Depends(get_current_user)` to all endpoints
2. `routes/tasks.py`: Validate token.user_id == URL user_id
3. `main.py`: Include auth_router
4. `routes/__init__.py`: Export auth_router

### Error Handling

| Condition | HTTP Status | Error Detail |
|-----------|-------------|--------------|
| Missing Authorization header | 401 | "Not authenticated" |
| Invalid/expired token | 401 | "Invalid token" or "Token expired" |
| Wrong auth format | 401 | "Invalid authorization format" |
| user_id mismatch | 403 | "Access denied" |
| Duplicate email | 400 | "Email already registered" |
| Invalid credentials | 401 | "Invalid credentials" |
| Password too short | 400 | "Password must be at least 8 characters" |

## Complexity Tracking

> No constitution violations identified. All design choices follow Phase II principles.

| Decision | Rationale | Alternative Considered |
|----------|-----------|------------------------|
| passlib[bcrypt] | FastAPI recommended, secure defaults | Raw bcrypt (less ergonomic) |
| python-jose | FastAPI recommended, good JWK support | PyJWT (fewer features) |
| Dependency injection | Per-route control, testable | Middleware class (less flexible) |
| String user_id | Matches existing Task.user_id type | UUID (type mismatch with Module 2) |

## Next Steps

1. **Phase 0**: Complete research.md with library comparisons
2. **Phase 1**: Create data-model.md, contracts/, quickstart.md
3. **Phase 2**: Generate tasks.md via `/sp.tasks`
4. **Implementation**: Execute via `/sp.implement`
