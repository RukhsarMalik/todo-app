# Tasks: Backend API (RESTful Endpoints)

**Input**: Design documents from `/specs/003-backend-api/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/openapi.yaml

**Tests**: Not requested in specification - manual testing via curl/Postman as per plan.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md structure:
- **Backend**: `phase-2/backend/`
- **Routes**: `phase-2/backend/routes/`
- **Schemas**: `phase-2/backend/schemas.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and create project structure

- [x] T001 Install FastAPI and Uvicorn dependencies via `uv add fastapi uvicorn[standard]` in phase-2/backend/
- [x] T002 [P] Create routes package directory phase-2/backend/routes/
- [x] T003 [P] Create routes/__init__.py with router exports in phase-2/backend/routes/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core schemas and app structure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Pydantic schemas (TaskCreate, TaskUpdate, TaskToggle, TaskResponse) in phase-2/backend/schemas.py
- [x] T005 Create query parameter enums (StatusFilter, SortField, SortOrder) in phase-2/backend/schemas.py
- [x] T006 Create FastAPI app with CORS and lifecycle hooks in phase-2/backend/main.py
- [x] T007 Create database session dependency for FastAPI in phase-2/backend/main.py
- [x] T008 Create routes/tasks.py with router setup in phase-2/backend/routes/tasks.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Application Setup (Priority: P1)

**Goal**: Configure application server with health check and root endpoints

**Independent Test**: Start server, access /health and / endpoints via curl

### Implementation for User Story 1

- [x] T009 [US1] Implement GET / endpoint returning API info in phase-2/backend/main.py
- [x] T010 [US1] Implement GET /health endpoint returning status in phase-2/backend/main.py
- [x] T011 [US1] Configure CORS middleware for localhost:3000 in phase-2/backend/main.py
- [x] T012 [US1] Implement lifespan context manager with init_db/close_db in phase-2/backend/main.py

**Checkpoint**: Server starts, health check works, CORS configured

---

## Phase 4: User Story 2 - List All Tasks (Priority: P1)

**Goal**: Retrieve all tasks for a user with filtering and sorting

**Independent Test**: Create tasks via database, retrieve via GET /api/{user_id}/tasks

### Implementation for User Story 2

- [x] T013 [US2] Implement GET /api/{user_id}/tasks endpoint in phase-2/backend/routes/tasks.py
- [x] T014 [US2] Add status filter (all/pending/completed) query parameter handling in phase-2/backend/routes/tasks.py
- [x] T015 [US2] Add sort (created/title) and order (asc/desc) query parameter handling in phase-2/backend/routes/tasks.py
- [x] T016 [US2] Implement user isolation filtering by user_id in phase-2/backend/routes/tasks.py

**Checkpoint**: Can list tasks with filtering/sorting, user isolation works

---

## Phase 5: User Story 3 - Get Single Task (Priority: P1)

**Goal**: Retrieve a specific task by ID with ownership verification

**Independent Test**: Create task, retrieve by ID via GET /api/{user_id}/tasks/{id}

### Implementation for User Story 3

- [x] T017 [US3] Implement GET /api/{user_id}/tasks/{task_id} endpoint in phase-2/backend/routes/tasks.py
- [x] T018 [US3] Add task ownership verification (return 404 if not owned) in phase-2/backend/routes/tasks.py

**Checkpoint**: Can get single task, ownership enforced

---

## Phase 6: User Story 4 - Create New Task (Priority: P1)

**Goal**: Create new tasks with validation

**Independent Test**: POST /api/{user_id}/tasks with valid/invalid data

### Implementation for User Story 4

- [x] T019 [US4] Implement POST /api/{user_id}/tasks endpoint in phase-2/backend/routes/tasks.py
- [x] T020 [US4] Add request body validation using TaskCreate schema in phase-2/backend/routes/tasks.py
- [x] T021 [US4] Set auto timestamps and default completed=false in phase-2/backend/routes/tasks.py
- [x] T022 [US4] Return 201 status with created task in phase-2/backend/routes/tasks.py

**Checkpoint**: Can create tasks with validation, timestamps auto-set

---

## Phase 7: User Story 5 - Update Task (Priority: P1)

**Goal**: Update existing tasks with partial updates

**Independent Test**: Create task, update via PUT /api/{user_id}/tasks/{id}

### Implementation for User Story 5

- [x] T023 [US5] Implement PUT /api/{user_id}/tasks/{task_id} endpoint in phase-2/backend/routes/tasks.py
- [x] T024 [US5] Add request body validation using TaskUpdate schema in phase-2/backend/routes/tasks.py
- [x] T025 [US5] Update only provided fields and refresh updated_at in phase-2/backend/routes/tasks.py
- [x] T026 [US5] Add task existence and ownership verification in phase-2/backend/routes/tasks.py

**Checkpoint**: Can update tasks with partial updates, ownership enforced

---

## Phase 8: User Story 6 - Delete Task (Priority: P1)

**Goal**: Permanently delete tasks

**Independent Test**: Create task, delete via DELETE /api/{user_id}/tasks/{id}

### Implementation for User Story 6

- [x] T027 [US6] Implement DELETE /api/{user_id}/tasks/{task_id} endpoint in phase-2/backend/routes/tasks.py
- [x] T028 [US6] Add task existence and ownership verification in phase-2/backend/routes/tasks.py
- [x] T029 [US6] Return 204 No Content on successful deletion in phase-2/backend/routes/tasks.py

**Checkpoint**: Can delete tasks, ownership enforced, correct status code

---

## Phase 9: User Story 7 - Toggle Task Completion (Priority: P1)

**Goal**: Toggle task completion status

**Independent Test**: Create task, toggle via PATCH /api/{user_id}/tasks/{id}/complete

### Implementation for User Story 7

- [x] T030 [US7] Implement PATCH /api/{user_id}/tasks/{task_id}/complete endpoint in phase-2/backend/routes/tasks.py
- [x] T031 [US7] Add request body validation using TaskToggle schema in phase-2/backend/routes/tasks.py
- [x] T032 [US7] Update completed field and refresh updated_at in phase-2/backend/routes/tasks.py
- [x] T033 [US7] Add task existence and ownership verification in phase-2/backend/routes/tasks.py

**Checkpoint**: Can toggle completion, timestamp updates

---

## Phase 10: User Story 8 - Error Handling (Priority: P2)

**Goal**: Consistent error responses across all endpoints

**Independent Test**: Trigger various error conditions, verify consistent JSON format

### Implementation for User Story 8

- [x] T034 [US8] Verify 404 responses use HTTPException with detail field in phase-2/backend/routes/tasks.py
- [x] T035 [US8] Verify 422 validation errors include field information (handled by Pydantic) in phase-2/backend/routes/tasks.py
- [x] T036 [US8] Add global exception handler for 500 errors (no stack trace) in phase-2/backend/main.py

**Checkpoint**: All errors use consistent JSON format

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation

- [x] T037 [P] Include tasks router in main app in phase-2/backend/main.py
- [x] T038 [P] Add TODO markers for Module 3 JWT verification in phase-2/backend/routes/tasks.py
- [x] T039 Run quickstart.md validation - test all endpoints via curl
- [x] T040 Verify OpenAPI docs accessible at /docs and /redoc

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - app setup required first
- **User Stories 2-7 (Phase 4-9)**: Depend on Foundational, can be done in parallel after US1
- **User Story 8 (Phase 10)**: Can be done anytime after Foundational
- **Polish (Phase 11)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Requires router setup from Phase 2 - Independent of other CRUD operations
- **User Story 3 (P1)**: Independent - can be done in parallel with US2
- **User Story 4 (P1)**: Independent - can be done in parallel with US2/US3
- **User Story 5 (P1)**: Independent - can be done in parallel
- **User Story 6 (P1)**: Independent - can be done in parallel
- **User Story 7 (P1)**: Independent - can be done in parallel
- **User Story 8 (P2)**: Cross-cutting - affects all endpoints but can be verified anytime

### Parallel Opportunities

**Within Foundational Phase:**
- T004 and T005 (schemas) can be done together
- T006, T007, T008 must be sequential (app before dependency before router)

**After Foundational:**
- All user story phases (3-10) can theoretically run in parallel
- Recommend sequential by priority for single developer
- US1 first (server must start), then US2-7 in any order, US8 last

---

## Parallel Example: Foundational Phase

```bash
# These can be done in parallel:
Task: T004 "Create Pydantic schemas in phase-2/backend/schemas.py"
Task: T005 "Create query parameter enums in phase-2/backend/schemas.py"

# Then sequentially:
Task: T006 "Create FastAPI app in phase-2/backend/main.py"
Task: T007 "Create database session dependency in phase-2/backend/main.py"
Task: T008 "Create routes/tasks.py with router setup"
```

---

## Implementation Strategy

### MVP First (User Stories 1-4)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T008)
3. Complete Phase 3: US1 - Application Setup (T009-T012)
4. Complete Phase 4: US2 - List Tasks (T013-T016)
5. Complete Phase 6: US4 - Create Task (T019-T022)
6. **STOP and VALIDATE**: Test create + list workflow
7. Can deploy basic create/list functionality

### Full CRUD Delivery

1. Complete MVP (US1, US2, US4)
2. Add US3 - Get Single Task (T017-T018)
3. Add US5 - Update Task (T023-T026)
4. Add US6 - Delete Task (T027-T029)
5. Add US7 - Toggle Completion (T030-T033)
6. Add US8 - Error Handling (T034-T036)
7. Complete Polish (T037-T040)

### Suggested Order (Single Developer)

1. T001-T003 (Setup)
2. T004-T008 (Foundational)
3. T009-T012 (US1: Server)
4. T013-T016 (US2: List)
5. T019-T022 (US4: Create)
6. T017-T018 (US3: Get)
7. T023-T026 (US5: Update)
8. T027-T029 (US6: Delete)
9. T030-T033 (US7: Toggle)
10. T034-T036 (US8: Errors)
11. T037-T040 (Polish)

---

## Summary

| Category | Count |
|----------|-------|
| Total Tasks | 40 |
| Setup Phase | 3 |
| Foundational Phase | 5 |
| User Story Tasks | 28 |
| Polish Tasks | 4 |
| Parallel Opportunities | 8 tasks marked [P] |

### Tasks per User Story

| Story | Priority | Tasks | IDs |
|-------|----------|-------|-----|
| US1 - Application Setup | P1 | 4 | T009-T012 |
| US2 - List Tasks | P1 | 4 | T013-T016 |
| US3 - Get Single Task | P1 | 2 | T017-T018 |
| US4 - Create Task | P1 | 4 | T019-T022 |
| US5 - Update Task | P1 | 4 | T023-T026 |
| US6 - Delete Task | P1 | 3 | T027-T029 |
| US7 - Toggle Completion | P1 | 4 | T030-T033 |
| US8 - Error Handling | P2 | 3 | T034-T036 |

---

## Notes

- All CRUD endpoints go in routes/tasks.py for maintainability
- Schemas in dedicated schemas.py file per plan.md structure
- Task model already exists from Module 1 (models.py)
- Database session management reuses Module 1 patterns
- No automated tests - manual testing via curl as specified
- TODO markers prepared for Module 3 JWT integration
