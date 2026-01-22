# Research: Database Setup & Models

**Module**: Phase II - Module 1 of 5
**Date**: 2026-01-16
**Status**: Complete

---

## Research Summary

This module's technology stack is well-defined by the Phase II constitution. Research focused on best practices and implementation patterns rather than technology selection.

---

## 1. SQLModel with Async PostgreSQL

### Decision
Use SQLModel with asyncpg driver for async database operations.

### Rationale
- SQLModel combines SQLAlchemy + Pydantic for type-safe ORM
- asyncpg is the fastest PostgreSQL adapter for Python
- Native async support aligns with FastAPI in Module 2
- Constitution mandates SQLModel

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| SQLAlchemy alone | No built-in Pydantic integration |
| psycopg3 | asyncpg is more mature for async |
| Prisma Python | Not as well integrated with FastAPI |

### Best Practices
- Use `create_async_engine` from sqlalchemy.ext.asyncio
- Configure connection pool (min=1, max=10) for serverless
- Always use context managers for sessions
- Import Task model before calling create_all()

---

## 2. Neon Serverless PostgreSQL

### Decision
Use Neon as the PostgreSQL provider with SSL required.

### Rationale
- Constitution mandates Neon Serverless PostgreSQL
- Free tier sufficient for hackathon
- Serverless scaling handles variable load
- Built-in connection pooling available

### Connection String Format
```
postgresql+asyncpg://user:password@ep-name-123456.region.aws.neon.tech/dbname?sslmode=require
```

### Best Practices
- Always use `sslmode=require` for security
- Use connection pooler endpoint for production
- Keep connection pool small (max 10) for serverless
- Handle connection timeouts gracefully

---

## 3. Async Session Management

### Decision
Use async generator pattern for FastAPI dependency injection.

### Rationale
- FastAPI's Depends() works naturally with generators
- Ensures proper cleanup via try/finally
- Supports multiple concurrent requests
- Transaction boundaries clear per-request

### Pattern
```python
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker(engine)() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Global session | Not thread-safe, no request isolation |
| Manual session creation | More boilerplate, error-prone cleanup |
| Scoped sessions | Complexity not needed for FastAPI |

---

## 4. Table Initialization Strategy

### Decision
Use SQLModel's metadata.create_all() for table creation.

### Rationale
- Simple and sufficient for hackathon scope
- Idempotent (safe to run multiple times)
- No migration complexity
- Direct mapping from model to schema

### Limitations Accepted
- No schema migrations (acceptable for hackathon)
- Schema changes require manual intervention
- Foreign key to users table deferred to Module 3

### Best Practices
- Call create_all() on application startup
- Log success/failure for debugging
- Handle missing users table gracefully (warning, not error)

---

## 5. Environment Variable Management

### Decision
Use python-dotenv to load .env file.

### Rationale
- Simple, widely used pattern
- Separates config from code
- Easy local development
- Constitution requires env vars for secrets

### Pattern
```python
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")
```

---

## 6. Foreign Key Constraint Handling

### Decision
Define FK constraint but handle creation failure gracefully.

### Rationale
- Users table won't exist until Module 3
- SQLModel create_all() will warn but not fail
- Constraint will be enforced once users table exists
- Data integrity maintained via application logic initially

### Implementation
```python
user_id: str = Field(
    index=True,
    foreign_key="user.id",  # Will warn until users table exists
    nullable=False
)
```

---

## Research Conclusions

| Topic | Decision | Confidence |
|-------|----------|------------|
| ORM | SQLModel + asyncpg | High (mandated) |
| Database | Neon PostgreSQL | High (mandated) |
| Session Pattern | Async generator | High (best practice) |
| Table Init | create_all() | High (sufficient for scope) |
| Config | python-dotenv | High (standard practice) |
| FK Handling | Graceful warning | Medium (workaround) |

---

## References

- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Neon Documentation](https://neon.tech/docs)
- [asyncpg Documentation](https://magicstack.github.io/asyncpg/)
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
