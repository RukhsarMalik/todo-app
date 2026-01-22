# Feature Specification: Backend API (RESTful Endpoints)

**Feature Branch**: `003-backend-api`
**Created**: 2026-01-18
**Status**: Draft
**Module**: Phase II - Module 2 of 5
**Input**: User description: "Module 2: Backend API - FastAPI REST endpoints for task CRUD operations"

## 1. Module Overview

| Attribute | Value |
|-----------|-------|
| **Module Name** | Backend API (RESTful Endpoints) |
| **Purpose** | Create REST API for task CRUD operations |
| **Dependencies** | Module 1 (Database) completed - db.py, models.py available |
| **Phase** | Phase II - Module 2 of 5 |

---

## 2. Scope of This Module

### What's INCLUDED in this module

- Application setup and configuration
- RESTful API endpoints for tasks (GET, POST, PUT, DELETE, PATCH)
- Request/Response validation models
- CRUD operations using database queries
- Error handling (404, 400, 500)
- CORS configuration for frontend access
- **Mock user_id parameter** (no JWT verification yet - added in Module 3)

### What's NOT INCLUDED (handled in other modules)

| Excluded Item | Target Module |
|---------------|---------------|
| JWT token verification | Module 3: Authentication |
| Better Auth integration | Module 3: Authentication |
| User table creation | Module 3: Better Auth handles this |
| Frontend UI | Module 4: Frontend |
| Real user authentication | Module 3: Authentication |

### Important Note on Authentication

This module accepts `user_id` as a URL parameter without verification. Security will be added in Module 3. This allows:
- Building and testing API endpoints independently
- Using tools like Postman/curl with any user_id
- Adding security later without rewriting endpoints

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Application Setup (Priority: P1)

As a backend developer, I want a configured application server so that I can add and run API endpoints.

**Why this priority**: Foundation for all API functionality. Nothing works without a running server.

**Independent Test**: Can be fully tested by starting the server and accessing health check endpoint.

**Acceptance Scenarios**:

1. **Given** the application is started, **When** I access the root endpoint, **Then** I receive API information with version.
2. **Given** the application is started, **When** I access the health endpoint, **Then** I receive a success status.
3. **Given** the application starts, **When** database initialization occurs, **Then** tables are ready for operations.
4. **Given** the application shuts down, **When** cleanup runs, **Then** database connections are closed properly.
5. **Given** a frontend origin, **When** making cross-origin requests, **Then** CORS headers allow the request.

---

### User Story 2 - List All Tasks (Priority: P1)

As a frontend developer, I want to retrieve all tasks for a user so that I can display them in the UI.

**Why this priority**: Core read operation - users need to see their existing tasks.

**Independent Test**: Can be fully tested by creating tasks via database and retrieving via API endpoint.

**Acceptance Scenarios**:

1. **Given** a user has tasks, **When** I request their task list, **Then** I receive all tasks for that user.
2. **Given** a user has no tasks, **When** I request their task list, **Then** I receive an empty array.
3. **Given** tasks exist, **When** I filter by completion status, **Then** I receive only matching tasks.
4. **Given** tasks exist, **When** I specify sort order, **Then** tasks are returned in that order.
5. **Given** multiple users have tasks, **When** I request one user's tasks, **Then** I only see that user's tasks (isolation).

---

### User Story 3 - Get Single Task (Priority: P1)

As a frontend developer, I want to retrieve a specific task so that I can display its details.

**Why this priority**: Needed for task detail views and edit forms.

**Independent Test**: Can be fully tested by creating a task and retrieving by ID.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** I request it by ID, **Then** I receive the complete task details.
2. **Given** a task doesn't exist, **When** I request it, **Then** I receive a not found error.
3. **Given** a task belongs to another user, **When** I request it, **Then** I receive a not found error (no information leak).

---

### User Story 4 - Create New Task (Priority: P1)

As a frontend developer, I want to create a new task so that users can add todos.

**Why this priority**: Core write operation - users need to add new tasks.

**Independent Test**: Can be fully tested by sending create request and verifying in database.

**Acceptance Scenarios**:

1. **Given** valid task data, **When** I submit a create request, **Then** the task is created with a generated ID.
2. **Given** a title exceeding 200 characters, **When** I submit, **Then** I receive a validation error.
3. **Given** missing required title, **When** I submit, **Then** I receive a validation error with field name.
4. **Given** valid data, **When** task is created, **Then** timestamps are automatically set.
5. **Given** valid data, **When** task is created, **Then** completion status defaults to false.

---

### User Story 5 - Update Task (Priority: P1)

As a frontend developer, I want to update a task so that users can modify details.

**Why this priority**: Users need to correct mistakes and update task information.

**Independent Test**: Can be fully tested by creating a task, updating it, and verifying changes.

**Acceptance Scenarios**:

1. **Given** an existing task, **When** I update the title, **Then** the title changes and timestamp updates.
2. **Given** an existing task, **When** I update description only, **Then** only description and timestamp change.
3. **Given** a non-existent task, **When** I try to update, **Then** I receive a not found error.
4. **Given** another user's task, **When** I try to update, **Then** I receive a not found error.
5. **Given** invalid field values, **When** I submit, **Then** I receive validation errors.

---

### User Story 6 - Delete Task (Priority: P1)

As a frontend developer, I want to delete a task so that users can remove todos.

**Why this priority**: Users need to clean up completed or unwanted tasks.

**Independent Test**: Can be fully tested by creating a task, deleting it, and verifying removal.

**Acceptance Scenarios**:

1. **Given** an existing task, **When** I delete it, **Then** it's permanently removed.
2. **Given** a non-existent task, **When** I try to delete, **Then** I receive a not found error.
3. **Given** another user's task, **When** I try to delete, **Then** I receive a not found error.
4. **Given** successful deletion, **When** response returns, **Then** no content is returned (204 status).

---

### User Story 7 - Toggle Task Completion (Priority: P1)

As a frontend developer, I want to toggle task completion so that users can mark todos complete/incomplete.

**Why this priority**: Primary user interaction - marking tasks done is core functionality.

**Independent Test**: Can be fully tested by creating a task and toggling its status.

**Acceptance Scenarios**:

1. **Given** an incomplete task, **When** I mark it complete, **Then** status changes to complete.
2. **Given** a complete task, **When** I mark it incomplete, **Then** status changes to incomplete.
3. **Given** a status change, **When** saved, **Then** updated_at timestamp is refreshed.
4. **Given** a non-existent task, **When** I try to toggle, **Then** I receive a not found error.
5. **Given** missing completion value, **When** I submit, **Then** I receive a validation error.

---

### User Story 8 - Error Handling (Priority: P2)

As a frontend developer, I want consistent error responses so that I can handle errors properly.

**Why this priority**: Supports all other stories but not blocking for basic functionality.

**Independent Test**: Can be fully tested by triggering various error conditions.

**Acceptance Scenarios**:

1. **Given** invalid input data, **When** request fails validation, **Then** I receive 400 with error details.
2. **Given** a resource not found, **When** request fails, **Then** I receive 404 with message.
3. **Given** a server error, **When** exception occurs, **Then** I receive 500 without stack trace exposure.
4. **Given** any error, **When** response returns, **Then** format is consistent JSON with detail field.

---

### Edge Cases

- What happens when title is exactly 200 characters? (Should succeed)
- What happens when description is exactly 1000 characters? (Should succeed)
- What happens when title is empty string? (Should fail validation)
- What happens when user_id contains special characters? (Should be URL-encoded)
- What happens when database connection fails mid-request? (Should return 500, rollback)
- What happens with concurrent updates to same task? (Last write wins)

---

## Requirements *(mandatory)*

### Functional Requirements

#### API Endpoint Requirements

- **FR-001**: System MUST provide a health check endpoint returning status information
- **FR-002**: System MUST provide a root endpoint returning API name and version
- **FR-003**: System MUST provide endpoint to list all tasks for a specific user
- **FR-004**: System MUST provide endpoint to retrieve a single task by ID
- **FR-005**: System MUST provide endpoint to create a new task
- **FR-006**: System MUST provide endpoint to update an existing task
- **FR-007**: System MUST provide endpoint to delete a task
- **FR-008**: System MUST provide endpoint to toggle task completion status

#### Data Validation Requirements

- **FR-009**: System MUST validate task title is between 1-200 characters
- **FR-010**: System MUST validate task description is maximum 1000 characters when provided
- **FR-011**: System MUST validate completion status is a boolean value
- **FR-012**: System MUST return descriptive validation errors including field names

#### User Isolation Requirements

- **FR-013**: System MUST filter tasks by user_id for all list operations
- **FR-014**: System MUST verify task ownership before allowing read/update/delete
- **FR-015**: System MUST return 404 (not 403) when accessing another user's task (no information leak)

#### Data Management Requirements

- **FR-016**: System MUST auto-set created_at timestamp when creating tasks
- **FR-017**: System MUST auto-update updated_at timestamp when modifying tasks
- **FR-018**: System MUST default completion status to false for new tasks
- **FR-019**: System MUST permanently delete tasks (no soft delete)

#### Cross-Origin Requirements

- **FR-020**: System MUST allow cross-origin requests from configured frontend origins
- **FR-021**: System MUST support credentials in cross-origin requests

#### Lifecycle Requirements

- **FR-022**: System MUST initialize database tables on startup
- **FR-023**: System MUST close database connections on shutdown

### API Endpoint Specifications

| Method | Endpoint                             | Purpose       | Response Codes |
|--------|--------------------------------------|---------------|----------------|
| GET    | /health                              | Health check  | 200            |
| GET    | /                                    | API info      | 200            |
| GET    | /api/{user_id}/tasks                 | List tasks    | 200            |
| GET    | /api/{user_id}/tasks/{id}            | Get task      | 200, 404       |
| POST   | /api/{user_id}/tasks                 | Create task   | 201, 400       |
| PUT    | /api/{user_id}/tasks/{id}            | Update task   | 200, 400, 404  |
| DELETE | /api/{user_id}/tasks/{id}            | Delete task   | 204, 404       |
| PATCH  | /api/{user_id}/tasks/{id}/complete   | Toggle status | 200, 400, 404  |

### Query Parameters for List Endpoint

| Parameter | Values                   | Default | Description              |
|-----------|--------------------------|---------|--------------------------|
| status    | all, pending, completed  | all     | Filter by completion     |
| sort      | created, title           | created | Sort field               |
| order     | asc, desc                | desc    | Sort direction           |

### Key Entities

- **Task**: A todo item belonging to a user (id, user_id, title, description, completed, created_at, updated_at)
- **TaskCreate**: Input for creating a task (title required, description optional)
- **TaskUpdate**: Input for updating a task (title optional, description optional)
- **TaskToggle**: Input for toggling completion (completed boolean required)
- **TaskResponse**: Output format for task data (all fields)

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Server starts and responds to health check within 5 seconds
- **SC-002**: All 8 API endpoints are accessible and documented
- **SC-003**: CRUD operations complete successfully via API testing tools
- **SC-004**: Validation correctly rejects invalid input with descriptive errors
- **SC-005**: Error responses use consistent JSON format with detail field
- **SC-006**: API documentation is auto-generated and accessible
- **SC-007**: User isolation prevents access to other users' tasks
- **SC-008**: Cross-origin requests from frontend origin succeed
- **SC-009**: Database operations rollback on errors (no partial state)
- **SC-010**: Response times under 500ms for all endpoints under normal load

---

## Dependencies & Prerequisites

### Required (from Module 1)

- Database module completed (db.py, models.py)
- Neon database accessible
- Tasks table created

### Environment Variables

- DATABASE_URL (reuse from Module 1)

---

## Integration Points

### This Module Provides For

- **Module 3 (Authentication)**: Endpoints ready for JWT middleware injection
- **Module 4 (Frontend)**: REST API ready to consume

### This Module Depends On

- **Module 1 (Database)**: db.py, models.py, Task class

### This Module Prepares For

- **Module 3**: All endpoints have TODO markers for JWT verification
- **Module 4**: CORS configured, API docs available

---

## Known Limitations (To Address in Module 3)

- No authentication - any user_id accepted without verification
- No token verification
- No user validation (can use any user_id string)
- Foreign key to users table will fail until Better Auth creates it

These are intentional - security added in Module 3.

---

## Out of Scope (This Module)

- JWT token verification (Module 3)
- Better Auth integration (Module 3)
- User signup/signin endpoints (Module 3)
- Frontend UI (Module 4)
- Real-time updates
- Task search functionality
- Task categories/tags

---

## Testing Checklist

- [ ] Server starts without errors
- [ ] /docs shows all endpoints documented
- [ ] Can create task with valid data
- [ ] Validation rejects title > 200 chars
- [ ] Can list tasks filtered by user_id
- [ ] Can filter by completion status
- [ ] Can sort by different fields
- [ ] Can get single task by ID
- [ ] Returns 404 for non-existent task
- [ ] Can update task title/description
- [ ] Can toggle completion status
- [ ] Can delete task
- [ ] Returns 404 when accessing other user's task
- [ ] CORS headers present in responses
- [ ] Error responses have consistent format

---

## Assumptions

1. Frontend will run on localhost:3000 during development (CORS origin)
2. Server will run on port 8000 (standard development port)
3. All API endpoints are prefixed with /api/{user_id} for future auth integration
4. Task IDs are integers (auto-increment from database)
5. User IDs are strings (to support various auth provider formats)
6. Timestamps use UTC without timezone info for database compatibility
7. No pagination needed for MVP (assumption: <1000 tasks per user)
8. No rate limiting needed for MVP (added in production deployment)

---

## Next Steps After This Module

1. Complete specification.md (this file)
2. Create plan.md (HOW to architect the API)
3. Create tasks.md (atomic implementation tasks)
4. Implement via Claude Code
5. Test all endpoints manually
6. Move to Module 3: Authentication
