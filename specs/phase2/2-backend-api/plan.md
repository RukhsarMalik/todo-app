# Implementation Plan: Backend API (RESTful Endpoints)

**Branch**: `003-backend-api` | **Date**: 2026-01-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-backend-api/spec.md`

## Summary

Create a FastAPI REST API backend for task CRUD operations with 8 endpoints (health, root, 6 task operations). The API accepts user_id as a URL parameter (no JWT verification in this module - added in Module 3). Endpoints filter tasks by user_id for multi-user isolation. CORS configured for frontend access.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: FastAPI, Uvicorn, SQLModel (from Module 1), Pydantic
**Storage**: Neon PostgreSQL via SQLModel (from Module 1)
**Testing**: Manual testing via curl/Postman, OpenAPI docs
**Target Platform**: Linux server (Uvicorn ASGI server)
**Project Type**: Web backend (API server)
**Performance Goals**: <500ms response time for all endpoints
**Constraints**: Async operations, no authentication (added Module 3)
**Scale/Scope**: MVP - single backend serving REST API

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| VIII. Monorepo Structure | PASS | Backend in `/phase-2/backend/` folder |
| IX. API-First Design | PASS | RESTful endpoints with JSON responses |
| X. Database Persistence | PASS | Uses SQLModel + Neon PostgreSQL from Module 1 |
| XI. Multi-User Support | PASS | All queries filtered by user_id parameter |
| XII. Authentication | N/A | Deferred to Module 3 (documented with TODOs) |
| Clean Code | PASS | Type hints, docstrings, async/await required |
| Error Handling | PASS | Consistent JSON error responses, no stack traces |

**Gate Status**: PASSED - All applicable principles satisfied. Authentication intentionally deferred with TODO markers.

## Project Structure

### Documentation (this feature)

```text
specs/003-backend-api/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI spec)
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
phase-2/backend/
├── main.py              # FastAPI app, CORS, lifecycle hooks
├── routes/
│   ├── __init__.py
│   └── tasks.py         # Task CRUD endpoints
├── schemas.py           # Pydantic request/response models
├── db.py                # Database module (from Module 1)
├── models.py            # SQLModel Task class (from Module 1)
├── init_db.py           # Database init script (from Module 1)
├── test_db.py           # Database validation (from Module 1)
├── .env                 # Environment variables (gitignored)
├── .env.example         # Environment template
├── CLAUDE.md            # AI guidance
└── pyproject.toml       # UV project config
```

**Structure Decision**: Web backend structure with routes organized by resource. Main.py serves as entry point with CORS and lifecycle hooks. Routes folder contains endpoint handlers. Schemas module provides Pydantic validation models.

## Complexity Tracking

No constitution violations requiring justification. Design follows all applicable Phase II principles.

## Design Decisions

### DD-001: URL Structure with user_id

**Decision**: Include user_id in URL path: `/api/{user_id}/tasks`

**Rationale**:
- Prepares for Module 3 JWT integration (token.user_id must match URL user_id)
- Enables testing with any user_id via curl/Postman
- Clear ownership indication in URL
- Alternative rejected: Query parameter less RESTful, header-only harder to test

### DD-002: Async Session Management

**Decision**: Use FastAPI dependency injection with async context manager

**Rationale**:
- Matches Module 1's `get_session()` pattern
- Automatic cleanup on request completion
- Supports concurrent requests efficiently
- Transaction safety with commit/rollback

### DD-003: Error Response Format

**Decision**: Use FastAPI's HTTPException with detail field

**Rationale**:
- Consistent JSON format: `{"detail": "message"}`
- Automatic status code handling
- Follows REST conventions
- Enables frontend to parse errors consistently

### DD-004: Query Parameters for List Endpoint

**Decision**: Support status, sort, and order query parameters

**Rationale**:
- Reduces client-side filtering overhead
- Common REST API pattern
- Efficient database queries with SQLModel
- Defaults: status=all, sort=created, order=desc

## Integration with Module 1

This module reuses the following from Module 1 (Database):

| Component | File | Usage |
|-----------|------|-------|
| Database session | db.py | `get_session()` dependency |
| Task model | models.py | SQLModel for queries |
| Database init | db.py | `init_db()` on startup |
| Connection cleanup | db.py | `close_db()` on shutdown |

No modifications to Module 1 code required.

## API Design Summary

| Endpoint | Method | Purpose | Auth TODO |
|----------|--------|---------|-----------|
| /health | GET | Health check | No |
| / | GET | API info | No |
| /api/{user_id}/tasks | GET | List tasks | Yes |
| /api/{user_id}/tasks/{id} | GET | Get task | Yes |
| /api/{user_id}/tasks | POST | Create task | Yes |
| /api/{user_id}/tasks/{id} | PUT | Update task | Yes |
| /api/{user_id}/tasks/{id} | DELETE | Delete task | Yes |
| /api/{user_id}/tasks/{id}/complete | PATCH | Toggle status | Yes |

## Dependencies (New for Module 2)

```bash
uv add fastapi uvicorn[standard]
```

Already installed (Module 1): sqlmodel, asyncpg, python-dotenv
