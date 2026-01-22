# Implementation Plan: Database Setup & Models

**Branch**: `001-todo-console-app` | **Date**: 2026-01-16 | **Spec**: [specification.md](./specification.md)
**Module**: Phase II - Module 1 of 5
**Input**: Module specification from `specs/phase2/1-database/specification.md`

---

## Summary

This module establishes the database foundation for Phase II by implementing:
1. **Neon PostgreSQL connection** with async support via SQLModel + asyncpg
2. **Task SQLModel class** with type-safe field definitions and validation
3. **Async session management** using FastAPI dependency injection pattern
4. **Database initialization** script for table/index creation
5. **Utility functions** for engine lifecycle management

The implementation focuses solely on the data layer, providing a clean foundation for Module 2 (Backend API).

---

## Technical Context

| Aspect | Value |
|--------|-------|
| **Language/Version** | Python 3.13+ |
| **Primary Dependencies** | SQLModel 0.0.14+, asyncpg, python-dotenv |
| **Storage** | Neon Serverless PostgreSQL |
| **Testing** | Manual test script (test_db.py) |
| **Target Platform** | Linux server (WSL compatible) |
| **Project Type** | Backend module (part of monorepo) |
| **Performance Goals** | Connection pool 1-10, async non-blocking |
| **Constraints** | SSL required, env vars for secrets |
| **Scale/Scope** | Single database, multi-user support |

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase II Principles Compliance

| Principle | Status | Evidence |
|-----------|--------|----------|
| **VIII. Monorepo Structure** | ✅ PASS | Code in `/backend/` directory |
| **IX. API-First Design** | ⏭️ N/A | Module 2 responsibility |
| **X. Database Persistence** | ✅ PASS | Neon PostgreSQL + SQLModel |
| **XI. Multi-User Support** | ✅ PASS | user_id field with index |
| **XII. Authentication Required** | ⏭️ N/A | Module 3 responsibility |

### Core Principles Compliance

| Principle | Status | Evidence |
|-----------|--------|----------|
| **I. AI-Native Development** | ✅ PASS | All code via Claude Code |
| **II. Specification-First** | ✅ PASS | Spec complete before plan |
| **III. Clean Code & Python Standards** | ✅ PASS | Type hints, docstrings required |
| **V. Graceful Error Handling** | ✅ PASS | Error handling in requirements |

### Gate Result: **PASS** - Proceed to implementation planning

---

## Project Structure

### Documentation (this module)

```text
specs/phase2/1-database/
├── specification.md     # Module requirements (complete)
├── plan.md              # This file
├── research.md          # Phase 0 research findings
├── data-model.md        # Task entity definition
├── quickstart.md        # Setup and usage guide
├── contracts/           # Database contracts (schema)
│   └── task-schema.sql  # SQL schema definition
├── checklists/
│   └── requirements.md  # Quality checklist (complete)
└── tasks.md             # Implementation tasks (next step)
```

### Source Code (repository root)

```text
backend/
├── .env                 # Environment variables (DATABASE_URL)
├── .env.example         # Template for .env
├── pyproject.toml       # UV dependencies
├── CLAUDE.md            # Backend-specific AI guidance
├── db.py                # Database connection & session management
├── models.py            # Task SQLModel class
├── init_db.py           # Table creation script
└── test_db.py           # Validation test script
```

**Structure Decision**: Backend-only module following monorepo pattern. Files at root of `/backend/` for simplicity in Module 1. Module 2 will organize into `src/` subdirectories.

---

## Implementation Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     backend/ directory                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐ │
│  │  .env       │      │  models.py  │      │  init_db.py │ │
│  │             │      │             │      │             │ │
│  │ DATABASE_URL│─────▶│ Task class  │◀─────│ create_all  │ │
│  └─────────────┘      └──────┬──────┘      └─────────────┘ │
│                              │                              │
│                              │ imports                      │
│                              ▼                              │
│                       ┌─────────────┐                       │
│                       │   db.py     │                       │
│                       │             │                       │
│                       │ get_engine  │                       │
│                       │ get_session │                       │
│                       │ init_db     │                       │
│                       │ close_db    │                       │
│                       └──────┬──────┘                       │
│                              │                              │
│                              │ connects via asyncpg         │
│                              ▼                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Neon Serverless PostgreSQL               │  │
│  │                                                       │  │
│  │  ┌─────────────────────────────────────────────────┐ │  │
│  │  │                 tasks table                      │ │  │
│  │  │  id | user_id | title | description | completed │ │  │
│  │  │     | created_at | updated_at                   │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. Application starts
   │
   ▼
2. Load DATABASE_URL from .env
   │
   ▼
3. Create AsyncEngine (singleton)
   │
   ▼
4. Call init_db() to create tables
   │
   ▼
5. Tables ready for Module 2 API
```

---

## File Specifications

### 1. models.py - Task SQLModel Class

**Purpose**: Define the Task entity with SQLModel for type-safe ORM operations.

**Key Elements**:
- Class inherits from `SQLModel` with `table=True`
- All fields with type hints
- Field constraints (max_length, nullable, default)
- Indexes defined on user_id and completed
- Google-style docstrings

### 2. db.py - Database Connection Module

**Purpose**: Manage database connections, sessions, and lifecycle.

**Key Functions**:
| Function | Purpose | Returns |
|----------|---------|---------|
| `get_engine()` | Singleton AsyncEngine | AsyncEngine |
| `get_session()` | Yield async session | AsyncGenerator[AsyncSession] |
| `init_db()` | Create all tables | None |
| `close_db()` | Close connections | None |

**Connection Configuration**:
- Driver: `postgresql+asyncpg`
- Pool: min=1, max=10
- SSL: required
- Echo: False (production)

### 3. init_db.py - Standalone Initialization

**Purpose**: Script to initialize database tables, runnable standalone.

**Usage**:
```bash
cd backend
uv run python init_db.py
```

### 4. test_db.py - Validation Script

**Purpose**: Verify database setup works correctly.

**Test Cases**:
1. Connection established
2. Table created
3. Insert task succeeds
4. Query task succeeds
5. Session cleanup works

---

## Dependencies

### Python Packages (pyproject.toml)

```toml
[project]
name = "todo-backend"
version = "0.1.0"
requires-python = ">=3.13"

dependencies = [
    "sqlmodel>=0.0.14",
    "asyncpg>=0.29.0",
    "python-dotenv>=1.0.0",
]
```

### Installation Commands

```bash
cd backend
uv init
uv add sqlmodel asyncpg python-dotenv
```

---

## Environment Configuration

### .env.example

```env
# Neon PostgreSQL Connection
# Format: postgresql+asyncpg://user:password@host/database?sslmode=require
DATABASE_URL=postgresql+asyncpg://username:password@ep-example-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### Security Notes

- Never commit `.env` to git (add to `.gitignore`)
- Use Neon connection pooler for production
- SSL mode MUST be `require` for Neon

---

## Complexity Tracking

> No constitution violations - no complexity justification needed.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| No FK initially | Defer FK constraint | users table created in Module 3 |
| No migrations | Use create_all() | Simplicity for hackathon scope |
| Flat structure | Files at backend/ root | Module 2 will add src/ organization |

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Neon connection fails | Blocks all DB work | Test connection first, clear error messages |
| FK constraint fails | Warning only | Document in known limitations, handle gracefully |
| asyncpg version issues | Import errors | Pin version in pyproject.toml |
| SSL certificate issues | Connection refused | Ensure sslmode=require in URL |

---

## Success Metrics

| Metric | Target | Verification |
|--------|--------|--------------|
| Connection time | < 5 seconds | Startup log timestamp |
| Table created | tasks table exists | Neon console |
| Indexes created | 2 indexes | Neon console |
| Test script passes | All assertions | Script output |
| No connection leaks | Stable pool | Extended run test |

---

## Next Steps

1. ✅ **specification.md** - Complete
2. ✅ **plan.md** - This file
3. 📋 **research.md** - Technology research (minimal, tech stack defined)
4. 📋 **data-model.md** - Task entity definition
5. 📋 **quickstart.md** - Setup guide
6. 📋 **contracts/task-schema.sql** - SQL schema
7. ⏳ **tasks.md** - Run `/sp.tasks` after plan approval
8. ⏳ **Implementation** - Execute tasks via Claude Code
