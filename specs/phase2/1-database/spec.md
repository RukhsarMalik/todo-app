# Module Specification: Database Setup & Models

**Module**: Phase II - Module 1 of 5
**Created**: 2026-01-16
**Status**: Draft
**Constitution Reference**: `.specify/memory/constitution.md` (Phase II Section)

---

## 1. Module Overview

| Attribute | Value |
|-----------|-------|
| **Module Name** | Database Setup & Models |
| **Purpose** | Create PostgreSQL database schema and SQLModel classes for task storage |
| **Dependencies** | Neon DB account created, DATABASE_URL obtained |
| **Technology** | SQLModel, Neon Serverless PostgreSQL, asyncpg driver |
| **Phase** | Phase II - Module 1 of 5 |

---

## 2. Scope of This Module

### What's INCLUDED in this module

- Neon database connection setup
- SQLModel Task model class definition
- Database session management (async)
- Table creation script (tasks table)
- Database utility functions
- Connection testing

### What's NOT INCLUDED (handled in other modules)

| Excluded Item | Target Module |
|---------------|---------------|
| API endpoints | Module 2: Backend API |
| User authentication logic | Module 3: Authentication |
| Better Auth user table | Module 3: Authentication (auto-managed) |
| Frontend components | Module 4: Frontend |
| Deployment configuration | Module 5: Deployment |

---

## 3. User Stories (Database Developer Perspective)

### US-DB-1: Database Connection Setup (Priority: P1)

**As a** backend developer, **I want to** establish connection to Neon PostgreSQL **so that** I can perform database operations.

**Why this priority**: Foundation for all database operations. Nothing else works without a connection.

**Independent Test**: Can be fully tested by verifying connection to Neon database and executing a simple query.

**Acceptance Scenarios**:

1. **Given** a valid DATABASE_URL environment variable, **When** the application starts, **Then** an async database connection is established successfully.

2. **Given** an invalid or missing DATABASE_URL, **When** the application starts, **Then** a clear error message is displayed explaining the issue.

3. **Given** an established connection, **When** multiple requests arrive concurrently, **Then** the connection pool handles them without blocking.

4. **Given** a connection failure mid-operation, **When** the error occurs, **Then** the system logs the error and provides a user-friendly message.

**Acceptance Criteria**:
- DATABASE_URL loaded from environment variable
- AsyncEngine created using SQLModel
- Connection string format: `postgresql+asyncpg://user:pass@host/db?sslmode=require`
- Connection pool configured (min_size=1, max_size=10)
- SSL mode set to 'require' for security
- Connection tested successfully on startup
- Error handling for connection failures with clear messages
- Connection can be reused across requests

---

### US-DB-2: Task Model Definition (Priority: P1)

**As a** backend developer, **I want** a Task SQLModel class **so that** I have type-safe database operations.

**Why this priority**: Core data structure that all CRUD operations depend on.

**Independent Test**: Can be fully tested by creating Task instances and validating field constraints.

**Acceptance Scenarios**:

1. **Given** a Task model class, **When** I create an instance with valid data, **Then** all fields are properly initialized with correct types.

2. **Given** a Task model, **When** I attempt to create a task with a title exceeding 200 characters, **Then** validation fails with a clear error.

3. **Given** a Task model, **When** I create a task without specifying completed status, **Then** it defaults to False.

4. **Given** a Task model, **When** I create a task, **Then** created_at and updated_at timestamps are automatically set.

**Acceptance Criteria**:
- Task class inherits from SQLModel with `table=True`
- Fields defined:
  - id: Optional[int] - Primary key, auto-increment
  - user_id: str - Foreign key reference, indexed, max 255 chars
  - title: str - Required, 1-200 characters
  - description: Optional[str] - Max 1000 characters
  - completed: bool - Default False
  - created_at: datetime - Auto-set on creation
  - updated_at: datetime - Auto-update on modification
- Type hints present for all fields
- Field validation rules enforced (length constraints)
- Proper defaults set (completed=False, timestamps=now)
- Table name explicitly set to "tasks"

---

### US-DB-3: Async Session Management (Priority: P1)

**As a** backend developer, **I want** session factory functions **so that** I can safely perform database transactions.

**Why this priority**: Required for any database read/write operations in the API layer.

**Independent Test**: Can be fully tested by performing database operations within a session context.

**Acceptance Scenarios**:

1. **Given** a session factory, **When** I request a session, **Then** I receive an async session ready for database operations.

2. **Given** an active session with pending changes, **When** the operation completes successfully, **Then** changes are committed automatically.

3. **Given** an active session, **When** an exception occurs, **Then** changes are rolled back and the session is cleaned up.

4. **Given** the session factory, **When** used with FastAPI's Depends(), **Then** session lifecycle is managed automatically per request.

**Acceptance Criteria**:
- AsyncSession maker configured
- `get_session()` function that yields session (FastAPI dependency pattern)
- Automatic session commit on success
- Automatic rollback on exception
- Session cleanup guaranteed (finally block or context manager)
- Can be used with FastAPI's Depends()
- Support for multiple concurrent sessions

---

### US-DB-4: Database Initialization (Priority: P1)

**As a** backend developer, **I want** an initialization script **so that** tables are created automatically.

**Why this priority**: Tables must exist before any data can be stored.

**Independent Test**: Can be fully tested by running init script and verifying table exists in Neon console.

**Acceptance Scenarios**:

1. **Given** no existing tasks table, **When** init_db() is called, **Then** the tasks table is created with correct schema.

2. **Given** an existing tasks table, **When** init_db() is called again, **Then** no errors occur (idempotent operation).

3. **Given** init_db() execution, **When** completed successfully, **Then** indexes on user_id and completed fields exist.

4. **Given** init_db() execution fails, **When** the error occurs, **Then** detailed error information is logged.

**Acceptance Criteria**:
- `init_db()` async function created
- Uses SQLModel.metadata.create_all()
- Creates 'tasks' table with correct schema
- Creates indexes on user_id and completed fields
- Idempotent (can run multiple times safely)
- Logs success/failure messages
- Can be called from main.py on startup
- Foreign key constraint defined (user_id reference, CASCADE delete)

---

### US-DB-5: Database Utilities (Priority: P2)

**As a** backend developer, **I want** helper functions **so that** I can manage database lifecycle.

**Why this priority**: Supports clean startup and shutdown, but not blocking for basic functionality.

**Independent Test**: Can be fully tested by verifying engine singleton and proper connection cleanup.

**Acceptance Scenarios**:

1. **Given** the application, **When** get_engine() is called multiple times, **Then** the same engine instance is returned (singleton).

2. **Given** an active database connection, **When** close_db() is called, **Then** all connections are properly closed.

3. **Given** application startup, **When** DATABASE_URL is not set, **Then** a clear error message indicates the missing configuration.

**Acceptance Criteria**:
- `get_engine()` function returns AsyncEngine singleton
- `close_db()` function properly closes all connections
- Engine created only once (singleton pattern)
- Proper cleanup on application shutdown
- Environment variable validation (DATABASE_URL must exist)

---

## 4. Functional Requirements

### FR-DB-1: Task Data Storage

System MUST store task data with the following attributes:
- Unique identifier (auto-generated)
- Owner reference (user identifier)
- Title (required, 1-200 characters)
- Description (optional, max 1000 characters)
- Completion status (boolean, default: incomplete)
- Creation timestamp (auto-set)
- Last modification timestamp (auto-updated)

### FR-DB-2: Data Persistence

System MUST persist all task data to database storage that survives:
- Application restarts
- Server restarts
- Network interruptions (via connection retry)

### FR-DB-3: Data Integrity

System MUST enforce data integrity through:
- Required fields validation (user_id, title)
- Field length constraints (title: 200 chars, description: 1000 chars)
- Foreign key reference for user ownership
- Cascade deletion when user is removed

### FR-DB-4: Connection Management

System MUST manage database connections with:
- Connection pooling (1-10 concurrent connections)
- Automatic connection recovery on transient failures
- Clean shutdown of all connections on application exit
- SSL/TLS encryption for all database traffic

### FR-DB-5: Query Performance

System MUST support efficient queries through:
- Index on user_id field (for user-specific task queries)
- Index on completed field (for status-based filtering)
- Async operations (non-blocking database calls)

### FR-DB-6: Error Handling

System MUST handle database errors gracefully:
- Connection failures: Clear message with retry suggestion
- Validation errors: Specific field and constraint information
- Query errors: Logged details without exposing internals to users
- Transaction failures: Automatic rollback with error reporting

---

## 5. Key Entities

### Task Entity

| Attribute | Description | Constraints |
|-----------|-------------|-------------|
| **id** | Unique identifier for the task | Auto-generated, immutable |
| **user_id** | Reference to task owner | Required, references user |
| **title** | Brief description of the task | Required, 1-200 characters |
| **description** | Detailed task information | Optional, max 1000 characters |
| **completed** | Task completion status | Boolean, default: false |
| **created_at** | When task was created | Auto-set, immutable |
| **updated_at** | When task was last modified | Auto-updated on changes |

### Entity Relationships

```
User (external) ──1:N──> Task
     │
     └── One user can have many tasks
         Tasks belong to exactly one user
         Deleting user cascades to delete all their tasks
```

---

## 6. Non-Functional Requirements

### NFR-DB-1: Performance

- Connection pooling: minimum 1, maximum 10 concurrent connections
- Async operations: All database calls use async/await (non-blocking)
- Indexes: Created on user_id (filtering) and completed (status queries)
- Query efficiency: Use ORM's efficient query building patterns

### NFR-DB-2: Security

- No hardcoded credentials (use environment variables only)
- SSL/TLS required for all database connections
- Parameterized queries only (SQL injection prevention)
- Foreign key constraints enforce referential integrity

### NFR-DB-3: Reliability

- Connection retry: 3 attempts with exponential backoff on transient failures
- Graceful error messages: User-friendly error descriptions
- Transaction support: Automatic rollback on failure
- Session lifecycle: Guaranteed cleanup via context managers

### NFR-DB-4: Maintainability

- Type hints: All functions and fields typed
- Docstrings: Module, class, and function documentation
- Clear separation: Connection logic separate from data models
- Logging: Info/error logs for debugging and monitoring

---

## 7. Success Criteria

### Measurable Outcomes

| Criterion | Metric | Verification |
|-----------|--------|--------------|
| **SC-DB-1** | Database connection established within 5 seconds | Startup log shows successful connection |
| **SC-DB-2** | Task table created with all required columns | Visible in Neon database console |
| **SC-DB-3** | Both indexes created (user_id, completed) | Visible in Neon database console |
| **SC-DB-4** | Task data persists across application restarts | Create task, restart app, task still exists |
| **SC-DB-5** | Connection pool handles 10 concurrent requests | Load test shows no connection exhaustion |
| **SC-DB-6** | Invalid DATABASE_URL produces clear error message | Startup with bad URL shows helpful message |
| **SC-DB-7** | Session cleanup works (no connection leaks) | Extended operation shows stable connection count |
| **SC-DB-8** | Test script creates and retrieves task successfully | Script output shows task creation and retrieval |

---

## 8. Dependencies & Prerequisites

### External Dependencies

| Dependency | Purpose | Status Required |
|------------|---------|-----------------|
| Neon account | Cloud PostgreSQL hosting | Account created |
| Neon database | Database instance | Database provisioned |
| DATABASE_URL | Connection credentials | Connection string obtained |

### Module Dependencies

| This Module Provides | For Module |
|---------------------|------------|
| Task model class | Module 2: Backend API |
| Database session factory | Module 2: Backend API |
| Database initialization | Module 2: Backend API |

| This Module Requires | From |
|---------------------|------|
| users table | Module 3: Authentication (Better Auth) |

---

## 9. Assumptions

1. **Neon Database**: User has created a Neon account and provisioned a PostgreSQL database before starting implementation.

2. **Foreign Key Timing**: The foreign key constraint to users table will initially fail until Module 3 (Authentication) creates the users table. Implementation should handle this gracefully.

3. **No Migration System**: For Phase II simplicity, using `create_all()` instead of a migration system like Alembic. Schema changes require manual intervention.

4. **updated_at Manual**: The `updated_at` field auto-update will be implemented via ORM hooks in Module 2, not database triggers.

5. **Connection String Format**: Using asyncpg driver format: `postgresql+asyncpg://...` with SSL required.

---

## 10. Known Limitations

| Limitation | Reason | Future Resolution |
|------------|--------|-------------------|
| FK constraint fails initially | users table doesn't exist yet | Module 3 creates users table |
| No migration system | Simplicity for hackathon | Add Alembic in Phase III |
| updated_at not auto-updating | Requires ORM hook | Module 2 adds update logic |
| No soft deletes | MVP simplicity | Add in Phase V if needed |

---

## 11. Out of Scope (This Module)

| Item | Target Module |
|------|---------------|
| API endpoints | Module 2: Backend API |
| CRUD operations/business logic | Module 2: Backend API |
| User authentication | Module 3: Authentication |
| JWT token handling | Module 3: Authentication |
| Better Auth setup | Module 3: Authentication |
| Frontend components | Module 4: Frontend |
| Deployment configuration | Module 5: Deployment |
| Database migrations | Future enhancement |
| Database seeding | Manual testing only |

---

## 12. Testing & Validation

### Manual Testing Checklist

- [ ] Connection succeeds with valid DATABASE_URL
- [ ] Connection fails gracefully with invalid URL
- [ ] Table 'tasks' created in Neon console
- [ ] Indexes visible: idx_tasks_user_id, idx_tasks_completed
- [ ] Can insert task programmatically
- [ ] Can query tasks by user_id
- [ ] Session cleanup works (no connection leaks)
- [ ] Application handles database unavailability gracefully

### Validation Script Requirements

A test script should be able to:
1. Initialize database tables
2. Create a test task with all required fields
3. Retrieve the created task
4. Verify field values match input
5. Clean up test data

---

## 13. Next Steps After This Module

1. **Complete specification.md** (this file)
2. **Create plan.md** - HOW to implement architecture
3. **Create tasks.md** - Breakdown into atomic tasks
4. **Implement via Claude Code** - db.py, models.py, init_db.py
5. **Test database setup** - Manual validation
6. **Move to Module 2** - Backend API

---

## Constitution Compliance

This specification aligns with Phase II constitution requirements:

- Database persistence with Neon PostgreSQL
- SQLModel ORM for type-safe operations
- Async operations for non-blocking I/O
- Environment variables for credentials (no hardcoding)
- Foreign key constraints for referential integrity
- Spec-Driven Development workflow followed
