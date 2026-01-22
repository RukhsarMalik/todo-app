<!--
Sync Impact Report:
- Version: 2.0.0 → 3.0.0 (MAJOR: Added Phase III AI Chatbot with 5 new principles)
- Principles added:
  - XIII. Natural Language Interface (PHASE III REQUIREMENT)
  - XIV. MCP Architecture (NON-NEGOTIABLE)
  - XV. Stateless Chat Design (PHASE III REQUIREMENT)
  - XVI. Conversation Persistence (PHASE III REQUIREMENT)
  - XVII. Agent Tool Safety (NON-NEGOTIABLE)
- Sections added:
  - Phase III: AI-Powered Todo Chatbot
  - Phase III Technical Stack
  - Phase III Architecture Constraints
  - Phase III MCP Tools Specification
  - Phase III Database Extensions
  - Phase III Success Criteria
- Sections removed: None (cumulative)
- Templates status:
  ✅ plan-template.md: No update required (SDD workflow unchanged)
  ✅ spec-template.md: No update required (feature spec pattern unchanged)
  ✅ tasks-template.md: No update required (task structure unchanged)
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
- [x] User can register new account (Better Auth)
- [x] User can sign in with credentials
- [x] User can sign out
- [x] User can add new task (title required, description optional)
- [x] User can view their task list (filtered by user_id)
- [x] User can update task title and description
- [x] User can delete task with confirmation
- [x] User can mark task complete/incomplete

#### Technical Requirements
- [x] Frontend deployed to Vercel with public URL
- [x] Backend deployed with public API URL
- [x] Database persists data across server restarts
- [x] JWT authentication working end-to-end
- [x] Multi-user isolation verified (users see only their tasks)
- [x] CORS configured correctly
- [x] All environment variables properly configured

#### Quality Requirements
- [x] No application crashes on invalid input
- [x] Error messages clear and actionable
- [x] Loading states shown during API calls
- [x] Responsive design (works on mobile and desktop)
- [x] All code maps to approved specification tasks
- [x] Git repository with meaningful commit history

#### Documentation Requirements
- [x] README.md with setup instructions
- [x] .env.example files for both frontend and backend
- [x] API documentation (endpoints, request/response formats)

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

---

# Evolution of Todo - Phase III Constitution

## Phase III: AI-Powered Todo Chatbot

### 1. Evolution from Phase II

- Phase I foundation: Console app with in-memory storage ✅
- Phase II evolution: Web app with database persistence ✅
- Phase III evolution: Add conversational AI interface for natural language task management

### 2. Additional Core Principles (Phase III)

#### XIII. Natural Language Interface (PHASE III REQUIREMENT)

Users MUST be able to manage tasks through conversational natural language commands.
The chatbot MUST understand intent and execute appropriate task operations.

**Requirements**:
- Understand commands like "Add buy groceries to my list"
- Understand queries like "Show me pending tasks"
- Understand actions like "Mark task 3 as complete"
- Provide friendly, conversational responses confirming actions
- Handle ambiguous requests with clarifying questions

**Rationale**: Natural language interfaces lower the barrier to entry and provide a more
intuitive user experience. Users can interact with tasks without learning specific commands.

#### XIV. MCP Architecture (NON-NEGOTIABLE)

All AI-task interactions MUST go through Model Context Protocol (MCP) tools.
The MCP server MUST be stateless and expose task operations as discrete tools.

**Requirements**:
- MCP server implemented using official MCP SDK (Python)
- Each task operation exposed as a separate MCP tool
- Tools MUST validate user_id before executing operations
- MCP server MUST NOT maintain conversation state (stateless)
- Agent orchestrates tool calls based on user intent

**Rationale**: MCP provides a standardized protocol for AI-tool interaction, enabling
interoperability with various AI agents. Stateless design ensures scalability and reliability.

#### XV. Stateless Chat Design (PHASE III REQUIREMENT)

The chat endpoint MUST be stateless. All conversation context MUST be loaded from the
database at the start of each request and NOT maintained in server memory.

**Requirements**:
- Chat endpoint: `POST /api/{user_id}/chat`
- Load conversation history from database on each request
- No server-side session storage for chat state
- Conversation context passed to AI agent on each request

**Rationale**: Stateless design enables horizontal scaling, fault tolerance, and
consistent behavior across server restarts or load-balanced instances.

#### XVI. Conversation Persistence (PHASE III REQUIREMENT)

All conversations and messages MUST be persisted to the database. Conversation history
MUST survive server restarts and be recoverable across sessions.

**Requirements**:
- `conversations` table: stores conversation metadata per user
- `messages` table: stores individual messages with role and content
- Messages linked to conversations via foreign key
- Conversation history loadable for context window management

**Rationale**: Persistence enables conversation continuity, user experience consistency,
and potential future features like conversation search or analytics.

#### XVII. Agent Tool Safety (NON-NEGOTIABLE)

MCP tools MUST validate user authorization before executing any task operation.
Tools MUST NOT allow cross-user data access under any circumstances.

**Requirements**:
- Every tool call MUST include and validate user_id
- Tools MUST verify task ownership before modification/deletion
- Failed authorization MUST return clear error (not silent failure)
- Tools MUST NOT expose internal errors to the AI agent

**Rationale**: Security is paramount. Even with AI intermediation, user data isolation
MUST be maintained. The agent MUST NOT be able to bypass authorization checks.

### 3. Technical Stack (Phase III)

#### AI & Agent Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| AI SDK | OpenAI Agents SDK | Latest | Agent orchestration and tool calling |
| MCP Server | Official MCP SDK (Python) | Latest | Tool exposure via MCP protocol |
| Chat UI | OpenAI ChatKit | Latest | Conversational interface component |

#### Extended Backend Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Framework | FastAPI | 0.100+ | Existing + new chat endpoint |
| AI Client | OpenAI Python SDK | Latest | Agent API calls |
| MCP | MCP Python SDK | Latest | Tool server implementation |

#### Database Extensions

| Table | Purpose |
|-------|---------|
| conversations | Store conversation metadata |
| messages | Store individual chat messages |

### 4. Architecture Constraints (Phase III)

#### Chat Endpoint Design

**Endpoint**: `POST /api/{user_id}/chat`

**Request**:
```json
{
  "message": "Add buy groceries to my list",
  "conversation_id": "uuid-optional"
}
```

**Response**:
```json
{
  "response": "I've added 'buy groceries' to your task list!",
  "conversation_id": "uuid",
  "actions_taken": [
    {
      "tool": "add_task",
      "result": "success",
      "task_id": "uuid"
    }
  ]
}
```

#### MCP Server Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Phase III Architecture                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User → ChatKit UI → POST /api/{user_id}/chat                  │
│                              ↓                                  │
│  FastAPI Chat Endpoint (JWT verified)                          │
│                              ↓                                  │
│  Load conversation history from DB                              │
│                              ↓                                  │
│  OpenAI Agent (with context + available tools)                 │
│                              ↓                                  │
│  Agent decides tool calls based on user intent                 │
│                              ↓                                  │
│  MCP Server executes tools (add_task, list_tasks, etc.)        │
│                              ↓                                  │
│  Tools interact with existing Task API/Database                │
│                              ↓                                  │
│  Agent formulates response                                     │
│                              ↓                                  │
│  Save message to DB, return response to user                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### MCP Tools Specification

The MCP server MUST expose these tools:

| Tool Name | Purpose | Parameters |
|-----------|---------|------------|
| `add_task` | Create new task | `title: str`, `description: str?` |
| `list_tasks` | Get user's tasks | `filter: "all" \| "pending" \| "completed"` |
| `complete_task` | Mark task done | `task_id: str` |
| `uncomplete_task` | Mark task pending | `task_id: str` |
| `delete_task` | Remove task | `task_id: str` |
| `update_task` | Modify task | `task_id: str`, `title: str?`, `description: str?` |
| `get_task` | Get single task | `task_id: str` |

**Tool Implementation Pattern**:
```python
@mcp_server.tool()
async def add_task(
    title: str,
    description: str | None = None,
    context: MCPContext
) -> dict:
    """Add a new task to the user's list."""
    user_id = context.user_id  # Injected by MCP server

    # Reuse existing task creation logic
    task = await task_service.create_task(
        user_id=user_id,
        title=title,
        description=description
    )

    return {
        "success": True,
        "task_id": str(task.id),
        "message": f"Task '{title}' created successfully"
    }
```

### 5. Database Extensions (Phase III)

#### New Tables

**Conversations Table**:
```sql
conversations (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title         VARCHAR(255),  -- Optional: auto-generated or user-set
  created_at    TIMESTAMP DEFAULT NOW(),
  updated_at    TIMESTAMP DEFAULT NOW()
)

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
```

**Messages Table**:
```sql
messages (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role            VARCHAR(50) NOT NULL,  -- 'user', 'assistant', 'system'
  content         TEXT NOT NULL,
  tool_calls      JSONB,  -- Optional: store tool calls made
  created_at      TIMESTAMP DEFAULT NOW()
)

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

#### SQLModel Implementation

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Any

class Conversation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str | None = Field(max_length=255, default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=50)  # 'user', 'assistant', 'system'
    content: str
    tool_calls: dict[str, Any] | None = Field(default=None, sa_type=JSONB)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 6. Agent Behavior Requirements

#### Intent Understanding

The agent MUST understand these natural language patterns:

| User Says | Intent | Tool Called |
|-----------|--------|-------------|
| "Add buy groceries" | Create task | `add_task` |
| "Create a task to call mom" | Create task | `add_task` |
| "Show my tasks" | List tasks | `list_tasks` |
| "What's on my list?" | List tasks | `list_tasks` |
| "Show pending tasks" | List filtered | `list_tasks(filter="pending")` |
| "Mark task 3 as done" | Complete task | `complete_task` |
| "I finished buying groceries" | Complete task | `complete_task` |
| "Delete task 2" | Delete task | `delete_task` |
| "Remove the groceries task" | Delete task | `delete_task` |
| "Change task 1 title to..." | Update task | `update_task` |

#### Response Style

The agent MUST:
- Confirm actions with friendly, natural language
- Include relevant details (task title, ID) in confirmations
- Handle errors gracefully with helpful messages
- Ask for clarification when intent is ambiguous
- Never expose technical errors to users

**Example Responses**:
- "I've added 'buy groceries' to your list!"
- "You have 3 pending tasks: 1. Buy groceries, 2. Call mom, 3. Finish report"
- "Done! I've marked 'buy groceries' as complete."
- "I couldn't find a task matching 'groceries'. Did you mean task #2: 'Buy groceries'?"

### 7. Security Requirements (Phase III - Additional)

#### Chat Endpoint Security

- Chat endpoint MUST require valid JWT (reuse Phase II auth)
- user_id from URL MUST match JWT user_id (403 on mismatch)
- Rate limiting RECOMMENDED to prevent abuse
- Input sanitization for all user messages

#### MCP Tool Security

- Every tool MUST receive user_id from authenticated context
- Tools MUST NOT accept user_id as a parameter (prevent spoofing)
- Tools MUST validate task ownership before any operation
- Tools MUST NOT return other users' data under any circumstances

### 8. Frontend Integration (Phase III)

#### ChatKit Component

Add ChatKit UI component to the frontend:

```typescript
// /frontend/components/chat/ChatInterface.tsx
'use client';

import { ChatKit } from '@openai/chatkit';

export function ChatInterface({ userId }: { userId: string }) {
  const handleSendMessage = async (message: string) => {
    const response = await fetch(`/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${getToken()}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message })
    });

    return response.json();
  };

  return (
    <ChatKit
      onSendMessage={handleSendMessage}
      placeholder="Ask me to manage your tasks..."
    />
  );
}
```

#### UI Integration

- Chat interface accessible from main task view
- Toggle between list view and chat view
- Chat history persisted and visible
- Both interfaces manage the same tasks

### 9. Environment Variables (Phase III - Additional)

**Backend** (`/backend/.env`):
```env
# Existing Phase II variables...

# Phase III: AI Integration
OPENAI_API_KEY=sk-...
MCP_SERVER_URL=http://localhost:8001  # If separate process
```

### 10. Success Criteria (Phase III)

Phase III is complete when ALL criteria are met:

#### Functional Requirements
- [ ] User can chat with AI to add tasks ("Add buy groceries")
- [ ] User can ask AI to show tasks ("Show my pending tasks")
- [ ] User can ask AI to complete tasks ("Mark task 3 as done")
- [ ] User can ask AI to delete tasks ("Remove task 2")
- [ ] User can ask AI to update tasks ("Change task 1 title to...")
- [ ] Conversation history persists across sessions
- [ ] Chat works alongside existing task UI (both functional)

#### Technical Requirements
- [ ] MCP server exposes all required tools
- [ ] Chat endpoint is stateless (loads context from DB)
- [ ] Conversation and messages stored in database
- [ ] Agent correctly interprets natural language intents
- [ ] All tools validate user_id authorization

#### Quality Requirements
- [ ] Agent responses are friendly and helpful
- [ ] Errors handled gracefully with user-friendly messages
- [ ] Ambiguous requests prompt clarification
- [ ] No cross-user data leakage via chat
- [ ] Chat performance acceptable (< 5s response time)

#### Integration Requirements
- [ ] All Phase II features still work
- [ ] Same authentication for chat and REST API
- [ ] Tasks created via chat visible in task list UI
- [ ] Tasks created via UI manageable via chat

### 11. Phase Transition Notes

#### What Carries Forward from Phase II

- ✅ Core Principles I-XII (all previous principles)
- ✅ Full-stack web application (Next.js + FastAPI)
- ✅ Database persistence (Neon PostgreSQL)
- ✅ JWT authentication
- ✅ Multi-user isolation
- ✅ REST API for task CRUD
- ✅ Deployment infrastructure (Vercel)

#### What's NEW in Phase III

- 🆕 Conversational AI interface (ChatKit)
- 🆕 OpenAI Agent for intent understanding
- 🆕 MCP server for tool execution
- 🆕 Conversation persistence (new tables)
- 🆕 Natural language task management

#### Backward Compatibility

Phase III MUST NOT break Phase II functionality:
- REST API endpoints continue to work
- Task list UI continues to work
- Authentication unchanged
- Database schema extended (not modified)

---

**IMPORTANT**: This constitution is cumulative. Phase III builds upon Phase I and II.
All previous principles remain in effect unless explicitly superseded.
All phases follow Spec-Driven Development with Claude Code + Spec-Kit Plus.

**Version**: 3.0.0 | **Ratified**: 2025-12-25 | **Phase III Added**: 2026-01-22
