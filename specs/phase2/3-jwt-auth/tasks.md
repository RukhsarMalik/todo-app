# Tasks: JWT Authentication

**Input**: Design documents from `/specs/004-jwt-auth/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Manual testing via curl (per spec - no automated tests)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app backend**: `phase-2/backend/`
- All paths relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and create module structure

- [x] T001 Install python-jose[cryptography] and passlib[bcrypt] via UV in phase-2/backend/
- [x] T002 [P] Create auth/ package directory with __init__.py in phase-2/backend/auth/__init__.py
- [x] T003 [P] Add JWT_SECRET_KEY to .env.example in phase-2/backend/.env.example
- [x] T004 [P] Generate and add JWT_SECRET_KEY to .env in phase-2/backend/.env (gitignored)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core authentication infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [P] Create password hashing module with hash_password() and verify_password() in phase-2/backend/auth/password.py
- [x] T006 [P] Create JWT module with create_access_token() and decode_access_token() in phase-2/backend/auth/jwt.py
- [x] T007 [P] Add User model class to phase-2/backend/models.py
- [x] T008 [P] Add auth schemas (UserCreate, UserLogin, TokenResponse, MessageResponse) to phase-2/backend/schemas.py
- [x] T009 Create auth middleware get_current_user() dependency in phase-2/backend/auth/middleware.py
- [x] T010 Export auth module functions from phase-2/backend/auth/__init__.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Signup (Priority: P1) 🎯 MVP

**Goal**: New users can create an account and receive a JWT token

**Independent Test**: POST /api/auth/signup with valid credentials returns 201 with JWT token

### Implementation for User Story 1

- [x] T011 [US1] Create routes/auth.py with APIRouter setup in phase-2/backend/routes/auth.py
- [x] T012 [US1] Implement POST /api/auth/signup endpoint with email uniqueness check in phase-2/backend/routes/auth.py
- [x] T013 [US1] Add password length validation (min 8 chars) to signup endpoint in phase-2/backend/routes/auth.py
- [x] T014 [US1] Add email format validation via Pydantic EmailStr in phase-2/backend/schemas.py
- [x] T015 [US1] Return 400 error for duplicate email in signup endpoint in phase-2/backend/routes/auth.py
- [x] T016 [US1] Return 201 with TokenResponse on successful signup in phase-2/backend/routes/auth.py
- [x] T017 [US1] Export auth_router from phase-2/backend/routes/__init__.py
- [x] T018 [US1] Include auth_router in main app with /api prefix in phase-2/backend/main.py

**Checkpoint**: User Story 1 complete - can signup and receive JWT token

---

## Phase 4: User Story 2 - User Login (Priority: P1)

**Goal**: Returning users can authenticate and receive a JWT token

**Independent Test**: POST /api/auth/login with valid credentials returns 200 with JWT token

**Dependency**: Requires US1 (signup) to create test users

### Implementation for User Story 2

- [x] T019 [US2] Implement POST /api/auth/login endpoint in phase-2/backend/routes/auth.py
- [x] T020 [US2] Verify password against stored hash using verify_password() in phase-2/backend/routes/auth.py
- [x] T021 [US2] Return 401 for invalid credentials (no info leak about which field is wrong) in phase-2/backend/routes/auth.py
- [x] T022 [US2] Return 200 with TokenResponse on successful login in phase-2/backend/routes/auth.py
- [x] T023 [US2] Verify JWT token contains user_id, email, and 7-day expiration claims in phase-2/backend/auth/jwt.py

**Checkpoint**: User Story 2 complete - can login with existing account

---

## Phase 5: User Story 3 - JWT Verification Middleware (Priority: P1)

**Goal**: All task endpoints are protected and only allow authenticated users to access their own tasks

**Independent Test**:
- Request without token → 401
- Request with invalid token → 401
- Request with valid token but wrong user_id → 403
- Request with valid token and matching user_id → Success

### Implementation for User Story 3

- [x] T024 [US3] Add get_current_user dependency to list_tasks endpoint in phase-2/backend/routes/tasks.py
- [x] T025 [US3] Add user_id validation (token vs URL) to list_tasks endpoint in phase-2/backend/routes/tasks.py
- [x] T026 [P] [US3] Add get_current_user dependency to get_task endpoint in phase-2/backend/routes/tasks.py
- [x] T027 [P] [US3] Add get_current_user dependency to create_task endpoint in phase-2/backend/routes/tasks.py
- [x] T028 [P] [US3] Add get_current_user dependency to update_task endpoint in phase-2/backend/routes/tasks.py
- [x] T029 [P] [US3] Add get_current_user dependency to delete_task endpoint in phase-2/backend/routes/tasks.py
- [x] T030 [P] [US3] Add get_current_user dependency to toggle_task_complete endpoint in phase-2/backend/routes/tasks.py
- [x] T031 [US3] Add 403 response for user_id mismatch in all task endpoints in phase-2/backend/routes/tasks.py
- [x] T032 [US3] Remove TODO comments for JWT verification in phase-2/backend/routes/tasks.py
- [x] T033 [US3] Update API docs to show authentication requirements via OpenAPI in phase-2/backend/routes/tasks.py

**Checkpoint**: User Story 3 complete - all task endpoints are protected with JWT

---

## Phase 6: User Story 4 - User Logout (Priority: P2)

**Goal**: Users can log out (client-side token discard)

**Independent Test**: POST /api/auth/logout returns 200 with success message

### Implementation for User Story 4

- [x] T034 [US4] Implement POST /api/auth/logout endpoint in phase-2/backend/routes/auth.py
- [x] T035 [US4] Return 200 with MessageResponse on logout in phase-2/backend/routes/auth.py

**Checkpoint**: User Story 4 complete - logout endpoint functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T036 [P] Verify all error responses use consistent JSON format with detail field in phase-2/backend/routes/auth.py
- [x] T037 [P] Add logging for authentication events in phase-2/backend/routes/auth.py
- [x] T038 Update CLAUDE.md with Module 3 completion status in phase-2/backend/CLAUDE.md
- [x] T039 Run quickstart.md validation: test signup, login, protected endpoints via curl
- [x] T040 Verify OpenAPI docs at /docs show auth requirements for all protected endpoints

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 (Signup) and US2 (Login) can proceed in parallel after Foundational
  - US3 (Middleware) requires US1 to test protected endpoints
  - US4 (Logout) can proceed independently after Foundational
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1) - Signup**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1) - Login**: Can start after Foundational - Uses same auth infrastructure as US1
- **User Story 3 (P1) - Middleware**: Requires US1/US2 to test (need valid tokens)
- **User Story 4 (P2) - Logout**: Can start after Foundational - No dependencies on other stories

### Within Each User Story

- Models/schemas before services
- Services before endpoints
- Core implementation before validation
- Story complete before moving to next priority

### Parallel Opportunities

- T002, T003, T004 (Setup) can run in parallel
- T005, T006, T007, T008 (Foundational) can run in parallel
- T026, T027, T028, T029, T030 (US3 - adding dependency to endpoints) can run in parallel
- T036, T037 (Polish) can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# Launch all foundational tasks in parallel:
Task: "Create password hashing module in phase-2/backend/auth/password.py"
Task: "Create JWT module in phase-2/backend/auth/jwt.py"
Task: "Add User model to phase-2/backend/models.py"
Task: "Add auth schemas to phase-2/backend/schemas.py"
```

## Parallel Example: User Story 3

```bash
# After T024 and T025 complete, launch remaining endpoint updates in parallel:
Task: "Add get_current_user to get_task in phase-2/backend/routes/tasks.py"
Task: "Add get_current_user to create_task in phase-2/backend/routes/tasks.py"
Task: "Add get_current_user to update_task in phase-2/backend/routes/tasks.py"
Task: "Add get_current_user to delete_task in phase-2/backend/routes/tasks.py"
Task: "Add get_current_user to toggle_task_complete in phase-2/backend/routes/tasks.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 + 3)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Signup)
4. Complete Phase 4: User Story 2 (Login)
5. Complete Phase 5: User Story 3 (Middleware)
6. **STOP and VALIDATE**: Test signup, login, and protected endpoints via curl

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 (Signup) → Test independently → Users can create accounts
3. Add US2 (Login) → Test independently → Users can authenticate
4. Add US3 (Middleware) → Test independently → Task endpoints protected
5. Add US4 (Logout) → Test independently → Complete auth flow
6. Polish phase → Production ready

### Full Completion Order

```text
T001 → T002,T003,T004 (parallel) → T005,T006,T007,T008 (parallel) → T009 → T010
→ T011 → T012 → T013 → T014 → T015 → T016 → T017 → T018
→ T019 → T020 → T021 → T022 → T023
→ T024 → T025 → T026,T027,T028,T029,T030 (parallel) → T031 → T032 → T033
→ T034 → T035
→ T036,T037 (parallel) → T038 → T039 → T040
```

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Manual testing via curl (no automated tests per spec)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- US1+US2+US3 together form the MVP - all P1 priority
