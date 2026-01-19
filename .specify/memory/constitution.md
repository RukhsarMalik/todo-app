<!--
Sync Impact Report:
- Version: None → 1.0.0 (Initial constitution for Evolution of Todo Hackathon Phase I)
- Principles added: 7 core principles established
- Sections added: Project Vision, Core Principles, Technical Standards, Development Workflow, Quality Gates, Governance
- Templates status:
  ✅ plan-template.md: Aligned with Python 3.13+, CLI architecture, in-memory constraints
  ✅ spec-template.md: Aligned with 5 basic features and user scenario requirements
  ✅ tasks-template.md: Aligned with spec-driven workflow and TDD approach
- Follow-up: None - all placeholders filled
-->

# Evolution of Todo - Phase I Constitution

## Project Vision & Purpose

**What**: A command-line todo application that stores tasks in memory, serving as the foundation
for mastering Spec-Driven Development (SDD) and AI-assisted coding workflows.

**Why**: To provide individual learners with hands-on experience in the Agentic Dev Stack
(Claude Code + Spec-Kit Plus) through a concrete, achievable project with clear success criteria.

**Who**: Individual learners participating in the "Evolution of Todo" hackathon, building
competency in AI-native development practices.

**Phase I Scope**: Basic in-memory CLI todo application with 5 core features, demonstrable
in a 90-second video, requiring zero external dependencies.

## Core Principles

### I. AI-Native Development (NON-NEGOTIABLE)

All code MUST be generated through Claude Code + Spec-Kit Plus workflow. Manual coding is
strictly prohibited. Every line of implementation code must trace back to an approved task in
the specification artifacts.

**Rationale**: Phase I is designed to teach disciplined AI-assisted development. Manual coding
bypasses the learning objective and breaks traceability between specifications and implementation.

**Enforcement**: Code reviews MUST verify that every function/class maps to a task ID. Commits
without task references will be rejected.

### II. Specification-First Development (NON-NEGOTIABLE)

No implementation work may begin without completed and approved specification artifacts following
the Spec-Driven Development loop: Specify → Plan → Tasks → Implement.

**Workflow Requirements**:
- All specifications stored in `/specs/<feature>/` directory
- Specifications MUST be approved before task generation
- Tasks MUST be approved before implementation begins
- No "code first, document later" permitted

**Rationale**: SDD ensures requirements are understood, architectures are validated, and tasks
are testable before any code is written. This prevents rework and maintains alignment with goals.

### III. Clean Code & Python Standards (NON-NEGOTIABLE)

All Python code MUST adhere to clean code principles with strict type safety and documentation.

**Mandatory Requirements**:
- Type hints on ALL functions, parameters, and return values (Python 3.13+ typing)
- Docstrings (Google or NumPy style) for ALL public functions and classes
- Single Responsibility Principle: one function = one clear purpose
- DRY: No duplicated logic; extract to functions when repeated
- Meaningful names: no single-letter variables except loop counters
- Maximum function length: 50 lines (refactor if exceeded)

**Rationale**: Clean code is maintainable code. Type hints catch errors early. Docstrings serve
as inline documentation. These practices are industry standards that AI-assisted development
must not compromise.

### IV. Zero External Dependencies (PHASE I CONSTRAINT)

Phase I implementation MUST use only Python 3.13+ standard library. No third-party packages,
frameworks, or external dependencies permitted except UV for package management.

**Allowed**: Standard library modules (sys, argparse, dataclasses, typing, uuid, datetime, etc.)
**Prohibited**: Any package requiring `pip install` or external downloads

**Rationale**: Simplicity for learning. External dependencies add complexity, version conflicts,
and installation friction. Phase I focuses on core concepts; future phases will add dependencies.

### V. Graceful Error Handling (NON-NEGOTIABLE)

All user inputs MUST be validated. All error conditions MUST produce clear, actionable error
messages. The application MUST NOT crash under any user input.

**Requirements**:
- Validate all user inputs before processing (type, range, format)
- Catch and handle ALL exceptions with user-friendly messages
- Error messages MUST explain what went wrong AND how to fix it
- No stack traces shown to end users (log them internally if needed)
- Invalid input returns to menu/prompt; never exits abruptly

**Rationale**: Professional software handles errors gracefully. Users should never see Python
tracebacks or cryptic messages. Every error is a teaching moment.

### VI. In-Memory Storage (PHASE I CONSTRAINT)

All task data MUST be stored in memory using Python data structures (lists, dicts, dataclasses).
No file I/O, databases, or persistence mechanisms permitted in Phase I.

**Requirements**:
- Tasks stored in memory (e.g., list of dataclass objects)
- Data resets on application restart (expected and acceptable)
- No pickles, JSON files, SQLite, or external storage

**Rationale**: Simplicity for Phase I. Persistence adds complexity (file locks, corruption,
serialization). In-memory focus teaches data structure design. Future phases add persistence.

### VII. User-Centric CLI Design

Command-line interface MUST be intuitive, with clear prompts, readable output, and helpful
guidance for users unfamiliar with the application.

**Requirements**:
- Main menu displays all available operations with numbered options
- Prompts clearly state expected input format and valid values
- Output formatted for readability (tables, numbered lists, clear sections)
- Confirmation messages for destructive operations (delete, update)
- Help text available for all commands

**Rationale**: CLI doesn't mean user-hostile. Clear interfaces reduce support burden and improve
the demo experience. Users should understand what to do without reading documentation.

## Technical Standards

### Runtime Environment

- **Python Version**: 3.13 or higher (REQUIRED)
- **Package Manager**: UV (for project setup and dependency management)
- **Platform**: Cross-platform (Linux, macOS, Windows via WSL)
- **Execution**: Single-command launch (e.g., `python src/main.py` or `uv run src/main.py`)

### Architecture

- **Type**: Single-file or modular structure (decide in planning phase)
- **Entry Point**: One main entry point that launches the CLI menu
- **Data Model**: Dataclasses for Task entity with typed fields
- **Storage**: In-memory list or dictionary holding Task objects
- **Interface**: Text-based menu with numbered options

### Required Features (Exactly 5 - No More, No Less)

Phase I MUST implement these features and ONLY these features:

1. **Add Task**: Create new task with title (required) and description (optional)
2. **Delete Task**: Remove task by ID with confirmation prompt
3. **Update Task**: Modify title and/or description of existing task by ID
4. **View Task List**: Display all tasks with ID, title, status, and description
5. **Toggle Status**: Mark task as complete/incomplete

**Success Criteria**: All 5 features working correctly, no crashes, demonstrable in 90 seconds.

### Code Quality Gates

Before any commit, code MUST pass:

- **Type Check**: All type hints valid (no `Any` types without justification)
- **Docstring Check**: All public functions documented
- **Validation Check**: All user inputs validated before use
- **Error Handling Check**: No unhandled exceptions possible from user input
- **Name Check**: All variables, functions, classes have descriptive names

## Development Workflow

### Spec-Driven Development Loop (MANDATORY)

```
1. SPECIFY  → Write specification in /specs/<feature>/spec.md
              Define user stories, acceptance criteria, requirements
              ↓
2. PLAN     → Create implementation plan in /specs/<feature>/plan.md
              Define architecture, data model, file structure
              ↓
3. TASKS    → Generate tasks in /specs/<feature>/tasks.md
              Break plan into concrete, testable implementation tasks
              ↓
4. IMPLEMENT → Execute tasks via Claude Code
              Generate code mapped to task IDs
              ↓
5. VERIFY   → Test all acceptance criteria
              Record results, iterate if needed
```

**Gate**: Each phase MUST complete and gain approval before proceeding to next phase.

### Version Control Discipline

- Git repository initialized from day 1
- Meaningful commit messages referencing task IDs (e.g., "T001: Create Task dataclass")
- Atomic commits: one logical unit of work per commit
- No commits with failing code or incomplete features
- Branch strategy: `main` for stable code, feature branches for development

### File Organization (REQUIRED)

```
todo-app/
├── .specify/
│   ├── memory/
│   │   └── constitution.md          # This file
│   ├── templates/                   # Spec-Kit Plus templates
│   └── scripts/                     # Spec-Kit Plus scripts
├── specs/
│   └── <feature-name>/
│       ├── spec.md                  # Feature specification
│       ├── plan.md                  # Implementation plan
│       └── tasks.md                 # Task breakdown
├── src/
│   ├── main.py                      # Application entry point
│   ├── models/                      # Data models (Task dataclass)
│   ├── services/                    # Business logic (add, delete, update, etc.)
│   └── cli/                         # CLI interface and menu
├── tests/                           # Future: unit/integration tests
├── history/
│   ├── prompts/                     # Prompt History Records (PHRs)
│   └── adr/                         # Architecture Decision Records
├── CLAUDE.md                        # Claude Code configuration
├── README.md                        # Project documentation
└── pyproject.toml                   # UV project configuration
```

## Quality Gates

### Definition of Done (Per Feature)

A feature is complete when ALL criteria met:

- [ ] Specification approved and frozen
- [ ] Implementation plan reviewed and approved
- [ ] All tasks completed with code referencing task IDs
- [ ] All acceptance criteria pass manual testing
- [ ] No crashes on invalid input
- [ ] Error messages clear and actionable
- [ ] Code has type hints and docstrings
- [ ] Committed to Git with meaningful messages
- [ ] Demonstrable in isolation

### Phase I Success Criteria (Project Complete)

Phase I complete when:

- [ ] All 5 basic features implemented and working
- [ ] Clean console output with user-friendly prompts
- [ ] No application crashes under any user input scenario
- [ ] All code maps to approved specification tasks
- [ ] Git repository with meaningful commit history
- [ ] 90-second demonstration video recorded showing all features
- [ ] README documents how to run and use the application

## Governance

### Constitution Authority

This constitution supersedes all other guidance, conventions, or practices. In case of conflict
between this constitution and any other document (including templates, prior decisions, or
external guidelines), this constitution takes precedence.

### Amendment Process

Constitution amendments MUST:

1. Document the proposed change with rationale and impact analysis
2. Update version number following semantic versioning:
   - MAJOR: Breaking changes to principles or workflow
   - MINOR: New principles or sections added
   - PATCH: Clarifications or wording improvements
3. Propagate changes to dependent templates (spec, plan, tasks)
4. Gain explicit approval before taking effect
5. Record decision in Architecture Decision Record (ADR)

### Compliance Review

All specification artifacts (spec.md, plan.md, tasks.md) MUST include a "Constitution Check"
section verifying compliance with principles defined here.

Code reviews MUST verify:

- Traceability: Every implementation artifact maps to approved tasks
- Type Safety: All functions have type hints
- Documentation: All public APIs have docstrings
- Error Handling: All user inputs validated, all exceptions handled
- Simplicity: No external dependencies, no unnecessary complexity

### Complexity Justification

Any violation of constitutional principles (e.g., external dependency in Phase I, missing type
hints, manual code addition) MUST be explicitly justified in writing with:

- Why the violation is necessary
- What simpler alternative was considered and rejected
- What mitigation reduces the risk/impact
- Approval from project stakeholder (self-approval for solo learning)

Unjustified violations invalidate the Phase I completion criteria.

### Living Document

This constitution is a living document. As you progress through Phases II and III, you will
amend this constitution to reflect new requirements (persistence, authentication, collaboration).

Each amendment MUST:

- Maintain backward compatibility where possible
- Document what changed and why
- Update dependent artifacts (templates, existing specs)
- Increment version number appropriately

**Version**: 1.0.0 | **Ratified**: 2025-12-25 | **Last Amended**: 2025-12-25

---

# Evolution of Todo - Phase II Constitution

## Phase II: Full-Stack Web Application

### 1. Evolution from Phase I

- Phase I foundation: Console app with in-memory storage ✅
- Phase II evolution: Web app with database persistence
- Incremental enhancement: Same 5 basic features, new interface

### 2. Additional Core Principles (Phase II)

#### VIII. Monorepo Structure (PHASE II REQUIREMENT)

All project code MUST be organized in a monorepo structure with clearly separated frontend and backend
directories. This enables unified version control while maintaining separation of concerns.

**Rationale**: Monorepo simplifies dependency management, enables atomic commits across stack boundaries,
and provides a single source of truth for the entire application.

#### IX. API-First Design (NON-NEGOTIABLE)

All backend functionality MUST be exposed through RESTful API endpoints with proper HTTP methods.
The frontend MUST consume these APIs exclusively—no direct database access from frontend.

**Requirements**:
- RESTful conventions (GET, POST, PUT, DELETE, PATCH)
- JSON request/response format
- Proper HTTP status codes (200, 201, 400, 401, 404, 500)
- Consistent error response format

**Rationale**: API-first design enables future extensibility (mobile apps, third-party integrations)
and enforces clean separation between presentation and business logic.

#### X. Database Persistence (PHASE II REQUIREMENT)

All task data MUST be persisted to a PostgreSQL database. Data MUST survive server restarts and
be recoverable across sessions.

**Requirements**:
- Neon Serverless PostgreSQL as database provider
- SQLModel ORM for database operations
- Proper schema design with constraints and indexes
- Migration support for schema changes

**Rationale**: Persistence is fundamental to a production-ready application. Users expect their
data to be available across sessions and devices.

#### XI. Multi-User Support (PHASE II REQUIREMENT)

The application MUST support multiple users, with complete data isolation between users.
Each user sees and manages only their own tasks.

**Requirements**:
- User-scoped data access (all queries filtered by user_id)
- No cross-user data leakage
- User-specific task counts and statistics

**Rationale**: Multi-user support is essential for a real-world application. Data isolation
protects user privacy and prevents unauthorized access.

#### XII. Authentication Required (NON-NEGOTIABLE)

All API endpoints (except auth endpoints) MUST require valid JWT authentication.
Better Auth provides the authentication framework.

**Requirements**:
- Better Auth for user registration and login
- JWT tokens for session management
- Token verification on every protected API request
- Secure token storage (httpOnly cookies or secure localStorage)

**Rationale**: Authentication protects user data and enables multi-user functionality.
JWT provides stateless, scalable authentication suitable for modern web applications.

### 3. Technical Stack (Phase II)

#### Frontend Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Framework | Next.js | 16+ | React framework with App Router |
| Language | TypeScript | 5.x | Type-safe JavaScript |
| Styling | Tailwind CSS | 3.x | Utility-first CSS framework |
| Auth UI | Better Auth | Latest | Authentication components |

#### Backend Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Framework | FastAPI | 0.100+ | Async Python web framework |
| ORM | SQLModel | 0.0.14+ | SQL database ORM |
| Database | Neon PostgreSQL | Serverless | Cloud PostgreSQL database |
| Auth | Better Auth + JWT | Latest | Token verification |

#### Development Tools

| Tool | Purpose |
|------|---------|
| Monorepo | /frontend and /backend folders |
| Spec-Kit Plus | Structured specifications |
| Claude Code | AI-assisted implementation |
| Git | Version control |
| UV | Python package management |
| npm/pnpm | Node.js package management |

### 4. Architecture Constraints (Phase II)

#### Monorepo Structure (REQUIRED)

```
hackathon-todo/
├── .specify/
│   ├── memory/
│   │   └── constitution.md          # This file (Phase I + II)
│   ├── templates/                   # Spec-Kit Plus templates
│   └── scripts/                     # Spec-Kit Plus scripts
├── specs/
│   ├── phase1/                      # Archived Phase I specs
│   └── phase2/
│       ├── overview.md              # Phase II overview
│       ├── architecture.md          # System architecture
│       ├── features/                # Feature specifications
│       ├── api/                     # API specifications
│       ├── database/                # Database schema specs
│       └── ui/                      # UI component specs
├── frontend/
│   ├── CLAUDE.md                    # Frontend-specific guidance
│   ├── src/
│   │   ├── app/                     # Next.js App Router pages
│   │   ├── components/              # React components
│   │   └── lib/                     # Utilities and API client
│   ├── package.json
│   └── tsconfig.json
├── backend/
│   ├── CLAUDE.md                    # Backend-specific guidance
│   ├── src/
│   │   ├── main.py                  # FastAPI entry point
│   │   ├── models/                  # SQLModel models
│   │   ├── routers/                 # API route handlers
│   │   ├── services/                # Business logic
│   │   └── auth/                    # JWT verification
│   └── pyproject.toml
├── history/
│   ├── prompts/                     # Prompt History Records
│   └── adr/                         # Architecture Decision Records
├── CLAUDE.md                        # Root monorepo guidance
├── README.md                        # Project documentation
└── .env.example                     # Environment variable template
```

#### API Design Standards

**Base URL Pattern**: `/api/tasks`

**Authentication**: All endpoints require JWT in Authorization header (except auth routes)

**Endpoint Conventions**:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /api/tasks | List user's tasks |
| POST | /api/tasks | Create new task |
| GET | /api/tasks/{id} | Get specific task |
| PUT | /api/tasks/{id} | Update task |
| DELETE | /api/tasks/{id} | Delete task |
| PATCH | /api/tasks/{id}/toggle | Toggle task status |

**Response Format** (Success):
```json
{
  "success": true,
  "data": { ... }
}
```

**Response Format** (Error):
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message"
  }
}
```

#### Security Requirements (NON-NEGOTIABLE)

- JWT tokens for authentication (Better Auth issued)
- Token verification on every API request
- User isolation: Users can only access their own data
- Environment variables for ALL secrets:
  - `DATABASE_URL` - Neon PostgreSQL connection string
  - `BETTER_AUTH_SECRET` - JWT signing secret
  - `BETTER_AUTH_URL` - Auth service URL
- **NO hardcoded credentials** in source code
- HTTPS required in production
- CORS configured for frontend domain only

### 5. Database Requirements (Phase II)

#### Schema Design

**Users Table** (managed by Better Auth):
```sql
-- Better Auth manages this table
users (
  id            UUID PRIMARY KEY,
  email         VARCHAR(255) UNIQUE NOT NULL,
  name          VARCHAR(255),
  created_at    TIMESTAMP DEFAULT NOW(),
  updated_at    TIMESTAMP DEFAULT NOW()
)
```

**Tasks Table**:
```sql
tasks (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title         VARCHAR(255) NOT NULL,
  description   TEXT,
  is_completed  BOOLEAN DEFAULT FALSE,
  created_at    TIMESTAMP DEFAULT NOW(),
  updated_at    TIMESTAMP DEFAULT NOW()
)

-- Index for user queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

#### Data Integrity Rules

- **Foreign Key**: tasks.user_id MUST reference users.id
- **Cascade Delete**: When user deleted, all their tasks deleted
- **NOT NULL**: id, user_id, title, is_completed, created_at
- **Defaults**: is_completed = FALSE, timestamps = NOW()
- **Indexes**: user_id indexed for query performance

#### SQLModel Implementation

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255)
    description: str | None = None
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 6. Code Quality Standards (Phase II - Additional)

#### Frontend Standards

**Server vs Client Components**:
- Server Components by default (no directive needed)
- Client Components only when required (`'use client'` directive)
- Use Client Components for: interactivity, browser APIs, state, effects

**TypeScript Requirements**:
- Strict mode enabled
- No `any` types without explicit justification
- Interface definitions for all API responses
- Type-safe API client functions

**Styling Requirements**:
- Tailwind CSS utility classes exclusively
- No inline styles (`style={{ }}`)
- Responsive design (mobile-first)
- Consistent spacing and color tokens

**Component Patterns**:
- Reusable components in `/components`
- Page components in `/app` directory
- Loading and error states for async operations
- Proper form validation with user feedback

#### Backend Standards

**FastAPI Requirements**:
- Pydantic models for ALL request/response schemas
- Async/await for all I/O operations (database, external APIs)
- HTTPException for error responses
- Dependency injection for database sessions
- Router organization by feature

**SQLModel Requirements**:
- Models define table schema AND Pydantic validation
- Separate Create/Update/Response schemas when needed
- Async session management
- Proper transaction handling

**Error Handling**:
```python
from fastapi import HTTPException

# Example error handling pattern
if not task:
    raise HTTPException(status_code=404, detail="Task not found")

if task.user_id != current_user_id:
    raise HTTPException(status_code=403, detail="Access denied")
```

#### API Client Standards (Frontend)

**Centralized Client** (`/frontend/lib/api.ts`):
- Single source of truth for API calls
- JWT token attached to all requests
- Type-safe request/response handling
- Consistent error handling

```typescript
// Example API client pattern
export async function getTasks(): Promise<Task[]> {
  const response = await fetch('/api/tasks', {
    headers: {
      'Authorization': `Bearer ${getToken()}`,
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    throw new ApiError(response.status, await response.json());
  }

  return response.json();
}
```

### 7. Feature Parity (Phase II)

Phase II MUST implement the same 5 basic features from Phase I, adapted for web:

| # | Feature | Phase I (CLI) | Phase II (Web) |
|---|---------|---------------|----------------|
| 1 | Add Task | Console input | Web form + API POST |
| 2 | View Tasks | Console list | React component + API GET |
| 3 | Update Task | Console prompts | Edit form + API PUT |
| 4 | Delete Task | Console confirm | Delete button + API DELETE |
| 5 | Toggle Status | Console toggle | Checkbox + API PATCH |

**NEW in Phase II** (beyond 5 basic features):
- User signup (Better Auth registration)
- User signin (Better Auth login)
- User signout (Better Auth logout)
- Web UI (React/Next.js interface)
- Database persistence (PostgreSQL)
- Multi-user isolation (user_id filtering)

### 8. Authentication Flow (Phase II)

#### Better Auth + FastAPI Integration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        Authentication Flow                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. User visits app → Redirected to login if no session        │
│                              ↓                                  │
│  2. User enters credentials → Better Auth validates            │
│                              ↓                                  │
│  3. Better Auth issues JWT → Stored in secure cookie/storage   │
│                              ↓                                  │
│  4. Frontend API call → JWT in Authorization header            │
│                              ↓                                  │
│  5. FastAPI middleware → Verifies JWT signature                │
│                              ↓                                  │
│  6. Extract user_id → Inject into request context              │
│                              ↓                                  │
│  7. API handler → Filter data by user_id                       │
│                              ↓                                  │
│  8. Return user's data only                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Shared Secret Configuration

**CRITICAL**: Both frontend and backend MUST use the same `BETTER_AUTH_SECRET`:

```env
# Frontend .env.local
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# Backend .env
BETTER_AUTH_SECRET=your-secret-key-min-32-chars  # SAME SECRET
DATABASE_URL=postgresql://...
```

#### JWT Verification (Backend)

```python
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)) -> UUID:
    try:
        payload = jwt.decode(
            token.credentials,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return UUID(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### 9. Deployment Requirements (Phase II)

#### Frontend Deployment (Vercel)

**Requirements**:
- Deploy to Vercel (free tier acceptable)
- Environment variables configured in Vercel dashboard
- Production build optimizations enabled
- Public URL accessible for submission

**Environment Variables**:
```
BETTER_AUTH_SECRET=...
BETTER_AUTH_URL=https://your-app.vercel.app
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

#### Backend Deployment (Railway/Render/Vercel)

**Requirements**:
- Deploy to Railway, Render, or Vercel Serverless
- Neon PostgreSQL connection configured
- CORS enabled for frontend domain
- Health check endpoint (`GET /health`)
- Public API URL accessible

**Environment Variables**:
```
DATABASE_URL=postgresql://...@neon.tech/...
BETTER_AUTH_SECRET=...  # Same as frontend
FRONTEND_URL=https://your-app.vercel.app  # For CORS
```

#### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 10. Workflow Constraints (Phase II)

#### Spec-Driven Development Loop (CONTINUES)

Phase II follows the same SDD loop as Phase I:

```
1. SPECIFY  → Write specification in /specs/phase2/<area>/
              Define requirements, acceptance criteria
              ↓
2. PLAN     → Create implementation plan
              Define architecture, data flow, interfaces
              ↓
3. TASKS    → Generate tasks
              Break into concrete, testable implementation tasks
              ↓
4. IMPLEMENT → Execute tasks via Claude Code
              Generate code mapped to task IDs
              ↓
5. VERIFY   → Test all acceptance criteria
              Manual testing + automated tests where applicable
```

#### Specification Organization

```
specs/phase2/
├── overview.md           # Phase II goals and scope
├── architecture.md       # System architecture decisions
├── features/
│   ├── auth.md          # Authentication feature spec
│   ├── add-task.md      # Add task feature spec
│   ├── view-tasks.md    # View tasks feature spec
│   ├── update-task.md   # Update task feature spec
│   ├── delete-task.md   # Delete task feature spec
│   └── toggle-status.md # Toggle status feature spec
├── api/
│   └── tasks-api.md     # Tasks API specification
├── database/
│   └── schema.md        # Database schema specification
└── ui/
    ├── layout.md        # UI layout specification
    └── components.md    # Component specifications
```

#### CLAUDE.md Organization

- **Root CLAUDE.md**: References monorepo structure, links to frontend/backend
- **Frontend CLAUDE.md**: Next.js patterns, TypeScript standards, component guidelines
- **Backend CLAUDE.md**: FastAPI patterns, SQLModel usage, auth implementation

### 11. Success Criteria (Phase II)

Phase II is complete when ALL criteria are met:

#### Functional Requirements
- [ ] User can register new account (Better Auth)
- [ ] User can sign in with credentials
- [ ] User can sign out
- [ ] User can add new task (title required, description optional)
- [ ] User can view their task list (filtered by user_id)
- [ ] User can update task title and description
- [ ] User can delete task with confirmation
- [ ] User can mark task complete/incomplete

#### Technical Requirements
- [ ] Frontend deployed to Vercel with public URL
- [ ] Backend deployed with public API URL
- [ ] Database persists data across server restarts
- [ ] JWT authentication working end-to-end
- [ ] Multi-user isolation verified (users see only their tasks)
- [ ] CORS configured correctly
- [ ] All environment variables properly configured

#### Quality Requirements
- [ ] No application crashes on invalid input
- [ ] Error messages clear and actionable
- [ ] Loading states shown during API calls
- [ ] Responsive design (works on mobile and desktop)
- [ ] All code maps to approved specification tasks
- [ ] Git repository with meaningful commit history

#### Documentation Requirements
- [ ] README.md with setup instructions
- [ ] .env.example files for both frontend and backend
- [ ] API documentation (endpoints, request/response formats)

#### Demonstration
- [ ] 90-second video demonstrating all features
- [ ] Video shows: signup, signin, all 5 CRUD operations, signout
- [ ] Video shows data persistence (refresh page, data still there)

### 12. Phase II Documentation Requirements

#### README.md Updates

Root README must include:
- Project overview (Phase I → Phase II evolution)
- Prerequisites (Node.js, Python, PostgreSQL account)
- Setup instructions for both frontend and backend
- Environment variable configuration guide
- Local development instructions
- Deployment instructions
- API endpoint documentation

#### Environment Templates

**Frontend** (`/frontend/.env.example`):
```env
# Better Auth
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend** (`/backend/.env.example`):
```env
# Database
DATABASE_URL=postgresql://user:pass@host/db

# Auth
BETTER_AUTH_SECRET=your-secret-key-min-32-chars

# CORS
FRONTEND_URL=http://localhost:3000
```

#### API Documentation

Document each endpoint:
- HTTP method and path
- Request headers (Authorization)
- Request body schema (JSON)
- Response body schema (JSON)
- Possible error codes and messages
- Example request/response

### 13. Phase Transition Notes

#### What Carries Forward from Phase I

- ✅ Core Principles I-VII (AI-Native, Spec-First, Clean Code, Error Handling, etc.)
- ✅ Spec-Driven Development workflow
- ✅ Git version control discipline
- ✅ Code quality gates (type hints, docstrings, validation)
- ✅ Definition of Done criteria pattern
- ✅ Constitution governance model

#### What Changes in Phase II

- 📝 Storage: In-memory → PostgreSQL database
- 📝 Interface: CLI → Web UI (Next.js)
- 📝 Architecture: Single-file → Monorepo (frontend + backend)
- 📝 Users: Single-user → Multi-user with authentication
- 📝 Deployment: Local only → Cloud deployment (Vercel + Railway/Render)

#### Phase I Artifacts

Phase I specifications archived in `/specs/phase1/` for reference.
Phase I code may be archived or serve as reference for business logic.

---

**IMPORTANT**: This constitution is cumulative. Phase II builds upon Phase I.
All Phase I principles remain in effect unless explicitly superseded.
Both phases follow Spec-Driven Development with Claude Code + Spec-Kit Plus.

**Version**: 2.0.0 | **Ratified**: 2025-12-25 | **Phase II Added**: 2026-01-16
