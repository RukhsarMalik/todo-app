# Research: Backend API

**Feature**: 003-backend-api
**Date**: 2026-01-18
**Status**: Complete

## Research Questions

No NEEDS CLARIFICATION items in technical context. All technology choices are well-defined by the constitution and Module 1.

## Technology Decisions

### FastAPI Pattern Selection

**Decision**: Use FastAPI with APIRouter for route organization

**Rationale**:
- FastAPI is mandated by Phase II constitution
- APIRouter provides clean separation of concerns
- Auto-generated OpenAPI docs at /docs
- Native async/await support matches SQLModel async

**Alternatives Considered**:
- Flask: Rejected - not async-native, manual OpenAPI
- Django REST: Rejected - heavier than needed for MVP
- Starlette: Rejected - FastAPI builds on it with better DX

### Pydantic Model Pattern

**Decision**: Separate request and response models

**Rationale**:
- TaskCreate: Only writable fields (title, description)
- TaskUpdate: Optional fields for partial updates
- TaskToggle: Only completion status
- TaskResponse: Full task with all fields for responses

**Alternatives Considered**:
- Single model with Optional fields: Rejected - unclear intent, validation issues
- SQLModel for both: Rejected - mixes ORM and API concerns

### Session Management Pattern

**Decision**: Reuse Module 1's `_get_session_maker()` with async context manager

**Rationale**:
- Module 1 already has working session factory
- Context manager ensures proper cleanup
- Matches FastAPI dependency injection pattern
- Avoids async generator break() issues from test_db.py learnings

**Note**: Based on Module 1 testing, use `async with session_maker() as session:` pattern, not `async for session in get_session():` with break.

### Error Handling Pattern

**Decision**: HTTPException with standard status codes

**Rationale**:
- 400: Validation errors (Pydantic handles automatically)
- 404: Task not found OR user isolation violation
- 500: Unexpected errors (logged, not exposed)

**Alternatives Considered**:
- Custom exception handlers: Rejected - HTTPException sufficient for MVP
- Error middleware: Rejected - adds complexity without benefit

### CORS Configuration

**Decision**: Allow localhost:3000 for development

**Rationale**:
- Frontend will run on port 3000 (Next.js default)
- Credentials allowed for future cookie-based auth
- All methods and headers allowed for flexibility

**Production Note**: Should be environment variable in Module 5 deployment.

## Best Practices Applied

### FastAPI Best Practices

1. **Lifespan Events**: Use `@asynccontextmanager` for startup/shutdown
2. **Dependency Injection**: Use `Depends()` for session management
3. **Response Models**: Specify `response_model` for auto-serialization
4. **Status Codes**: Explicit status codes (201 for create, 204 for delete)
5. **Path Parameters**: Type-annotated for auto-validation

### SQLModel Best Practices

1. **Select Statements**: Use `select(Model).where()` syntax
2. **Session Refresh**: Call `refresh()` after commit for updated data
3. **Async Operations**: All database calls use `await`
4. **Transaction Scope**: One session per request, auto-commit on success

### REST API Best Practices

1. **Resource Naming**: Plural nouns (/tasks, not /task)
2. **HTTP Methods**: Match action (GET=read, POST=create, PUT=update, DELETE=delete, PATCH=partial)
3. **Status Codes**: Semantic (201 Created, 204 No Content, 404 Not Found)
4. **Consistency**: Same error format across all endpoints

## Integration Patterns

### Module 1 Integration

```python
# Import from Module 1
from db import get_engine, init_db, close_db, _get_session_maker
from models import Task

# Session usage pattern
async def get_db_session():
    session_maker = _get_session_maker()
    async with session_maker() as session:
        yield session
```

### Module 3 Preparation

```python
# TODO markers for JWT verification
@router.get("/api/{user_id}/tasks")
async def get_tasks(user_id: str, session = Depends(get_db_session)):
    # TODO (Module 3): Add JWT verification here
    # Verify that token.user_id == user_id

    # Current implementation accepts any user_id
    ...
```

## Conclusion

All research complete. No blockers identified. Proceed to Phase 1 design artifacts.
