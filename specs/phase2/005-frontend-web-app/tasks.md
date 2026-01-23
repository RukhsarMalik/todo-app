# Tasks: Frontend Web Application

**Input**: Design documents from `/specs/005-frontend-web-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not requested for MVP. Manual testing via quickstart.md validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `phase-2/frontend/src/`
- All paths are relative to repository root

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create Next.js project with TypeScript, Tailwind CSS, and basic configuration

- [x] T001 Create Next.js 16+ project in phase-2/frontend/ with TypeScript, Tailwind, ESLint, App Router, src directory
- [x] T002 [P] Create .env.example with NEXT_PUBLIC_API_URL in phase-2/frontend/.env.example
- [x] T003 [P] Create .env.local with localhost API URL in phase-2/frontend/.env.local
- [x] T004 [P] Create CLAUDE.md for frontend module guidance in phase-2/frontend/CLAUDE.md
- [x] T005 [P] Update .gitignore to include .env.local in phase-2/frontend/.gitignore

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Library Layer

- [x] T006 Create TypeScript interfaces for all entities in phase-2/frontend/src/lib/types.ts
- [x] T007 [P] Create validation constants matching backend constraints in phase-2/frontend/src/lib/constants.ts
- [x] T008 Implement fetchWithAuth wrapper with JWT injection in phase-2/frontend/src/lib/api.ts
- [x] T009 Implement auth API functions (signup, login, logout) in phase-2/frontend/src/lib/api.ts
- [x] T010 Implement task API functions (getTasks, createTask, updateTask, deleteTask, toggleTask) in phase-2/frontend/src/lib/api.ts
- [x] T011 Create auth token storage utilities (getToken, setToken, clearToken) in phase-2/frontend/src/lib/auth.ts

### UI Components (Shared)

- [x] T012 [P] Create Button component with variants (primary, secondary, danger) in phase-2/frontend/src/components/ui/Button.tsx
- [x] T013 [P] Create Input component with label and error support in phase-2/frontend/src/components/ui/Input.tsx
- [x] T014 [P] Create LoadingSpinner component with size variants in phase-2/frontend/src/components/ui/LoadingSpinner.tsx
- [x] T015 [P] Create ErrorMessage component with dismiss option in phase-2/frontend/src/components/ui/ErrorMessage.tsx

### Auth Provider (Shared by all authenticated features)

- [x] T016 Implement AuthProvider context with login/logout in phase-2/frontend/src/components/auth/AuthProvider.tsx
- [x] T017 Implement useAuth hook for consuming auth state in phase-2/frontend/src/components/auth/AuthProvider.tsx
- [x] T018 Add AuthProvider to root layout in phase-2/frontend/src/app/layout.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal**: New visitors can create an account and be redirected to the task list

**Independent Test**: Visit /signup → Enter valid email, password (8+ chars), optional name → Verify redirect to /tasks

### Implementation for User Story 1

- [x] T019 [US1] Create SignupForm component with email, password, name fields in phase-2/frontend/src/components/auth/SignupForm.tsx
- [x] T020 [US1] Add client-side validation (email format, password 8+ chars) to SignupForm in phase-2/frontend/src/components/auth/SignupForm.tsx
- [x] T021 [US1] Add form submission with api.signup() and auth.login() to SignupForm in phase-2/frontend/src/components/auth/SignupForm.tsx
- [x] T022 [US1] Add error handling for "Email already registered" to SignupForm in phase-2/frontend/src/components/auth/SignupForm.tsx
- [x] T023 [US1] Create signup page with SignupForm and link to login in phase-2/frontend/src/app/signup/page.tsx

**Checkpoint**: User Story 1 (Registration) is independently testable

---

## Phase 4: User Story 2 - User Login (Priority: P1)

**Goal**: Returning users can log in with credentials and access their tasks

**Independent Test**: Visit /login → Enter valid credentials → Verify redirect to /tasks and session persistence

### Implementation for User Story 2

- [x] T024 [US2] Create LoginForm component with email, password fields in phase-2/frontend/src/components/auth/LoginForm.tsx
- [x] T025 [US2] Add client-side validation (email format, password 8+ chars) to LoginForm in phase-2/frontend/src/components/auth/LoginForm.tsx
- [x] T026 [US2] Add form submission with api.login() and auth.login() to LoginForm in phase-2/frontend/src/components/auth/LoginForm.tsx
- [x] T027 [US2] Add error handling for "Invalid credentials" (generic message) to LoginForm in phase-2/frontend/src/components/auth/LoginForm.tsx
- [x] T028 [US2] Create login page with LoginForm and link to signup in phase-2/frontend/src/app/login/page.tsx
- [x] T029 [US2] Add localStorage persistence check on app load in AuthProvider in phase-2/frontend/src/components/auth/AuthProvider.tsx

**Checkpoint**: User Stories 1-2 (Auth) are independently testable

---

## Phase 5: User Story 3 - View Task List (Priority: P1)

**Goal**: Logged-in users can see all their tasks with loading and empty states

**Independent Test**: Log in → View /tasks → Verify loading state, then task list or empty state

### Implementation for User Story 3

- [x] T030 [US3] Create TaskList component with data fetching in phase-2/frontend/src/components/tasks/TaskList.tsx
- [x] T031 [US3] Add loading state with LoadingSpinner to TaskList in phase-2/frontend/src/components/tasks/TaskList.tsx
- [x] T032 [US3] Add empty state message "Create your first task" to TaskList in phase-2/frontend/src/components/tasks/TaskList.tsx
- [x] T033 [US3] Add error state with ErrorMessage to TaskList in phase-2/frontend/src/components/tasks/TaskList.tsx
- [x] T034 [US3] Create TaskItem component for displaying single task in phase-2/frontend/src/components/tasks/TaskItem.tsx
- [x] T035 [US3] Add visual distinction for completed tasks (strikethrough, faded) in TaskItem in phase-2/frontend/src/components/tasks/TaskItem.tsx
- [x] T036 [US3] Create protected tasks page with redirect if not authenticated in phase-2/frontend/src/app/tasks/page.tsx
- [x] T037 [US3] Add header with user email display to tasks page in phase-2/frontend/src/app/tasks/page.tsx

**Checkpoint**: User Story 3 (View Tasks) is independently testable

---

## Phase 6: User Story 4 - Create Task (Priority: P1)

**Goal**: Logged-in users can add new tasks with title (required) and description (optional)

**Independent Test**: On /tasks → Enter title → Submit → Verify new task appears without page reload

### Implementation for User Story 4

- [x] T038 [US4] Create TaskForm component with title, description fields in phase-2/frontend/src/components/tasks/TaskForm.tsx
- [x] T039 [US4] Add client-side validation (title required, 1-200 chars) to TaskForm in phase-2/frontend/src/components/tasks/TaskForm.tsx
- [x] T040 [US4] Add form submission with api.createTask() to TaskForm in phase-2/frontend/src/components/tasks/TaskForm.tsx
- [x] T041 [US4] Add form clear on success and input preservation on error to TaskForm in phase-2/frontend/src/components/tasks/TaskForm.tsx
- [x] T042 [US4] Integrate TaskForm into TaskList with onTaskCreated callback in phase-2/frontend/src/components/tasks/TaskList.tsx

**Checkpoint**: User Story 4 (Create Task) is independently testable

---

## Phase 7: User Story 5 - Toggle Task Completion (Priority: P1)

**Goal**: Users can mark tasks complete/incomplete with immediate visual feedback and persistence

**Independent Test**: On /tasks → Click checkbox → Verify strikethrough immediately → Refresh → Verify state persisted

### Implementation for User Story 5

- [x] T043 [US5] Add checkbox for completion toggle to TaskItem in phase-2/frontend/src/components/tasks/TaskItem.tsx
- [x] T044 [US5] Implement optimistic update for toggle (immediate UI change) in TaskList in phase-2/frontend/src/components/tasks/TaskList.tsx
- [x] T045 [US5] Add api.toggleTask() call with rollback on error in TaskList in phase-2/frontend/src/components/tasks/TaskList.tsx
- [x] T046 [US5] Add error message display on toggle failure in TaskList in phase-2/frontend/src/components/tasks/TaskList.tsx

**Checkpoint**: User Stories 1-5 (Core MVP) are all independently testable

---

## Phase 8: User Story 6 - Update Task (Priority: P2)

**Goal**: Users can edit task title and description with inline editing

**Independent Test**: On /tasks → Click edit → Modify content → Save → Verify changes persist

### Implementation for User Story 6

- [x] T047 [US6] Create TaskEditForm component with pre-filled values in phase-2/frontend/src/components/tasks/TaskEditForm.tsx
- [x] T048 [US6] Add validation and api.updateTask() submission to TaskEditForm in phase-2/frontend/src/components/tasks/TaskEditForm.tsx
- [x] T049 [US6] Add cancel functionality that discards changes to TaskEditForm in phase-2/frontend/src/components/tasks/TaskEditForm.tsx
- [x] T050 [US6] Add edit button and editing state to TaskItem in phase-2/frontend/src/components/tasks/TaskItem.tsx
- [x] T051 [US6] Integrate TaskEditForm display when editing in TaskItem in phase-2/frontend/src/components/tasks/TaskItem.tsx
- [x] T052 [US6] Add editingTaskId state management to TaskList in phase-2/frontend/src/components/tasks/TaskList.tsx

**Checkpoint**: User Story 6 (Update Task) is independently testable

---

## Phase 9: User Story 7 - Delete Task (Priority: P2)

**Goal**: Users can remove tasks with confirmation dialog

**Independent Test**: On /tasks → Click delete → Confirm → Verify task removed

### Implementation for User Story 7

- [x] T053 [US7] Create ConfirmDialog component with modal overlay in phase-2/frontend/src/components/ui/ConfirmDialog.tsx
- [x] T054 [US7] Add keyboard (Escape) and click-outside dismiss to ConfirmDialog in phase-2/frontend/src/components/ui/ConfirmDialog.tsx
- [x] T055 [US7] Add delete button to TaskItem in phase-2/frontend/src/components/tasks/TaskItem.tsx
- [x] T056 [US7] Add delete confirmation dialog state to TaskList in phase-2/frontend/src/components/tasks/TaskList.tsx
- [x] T057 [US7] Add api.deleteTask() call with optimistic update in TaskList in phase-2/frontend/src/components/tasks/TaskList.tsx
- [x] T058 [US7] Add error handling with task restoration on delete failure in TaskList in phase-2/frontend/src/components/tasks/TaskList.tsx

**Checkpoint**: User Story 7 (Delete Task) is independently testable

---

## Phase 10: User Story 8 - User Logout (Priority: P2)

**Goal**: Users can log out and be redirected to login, with protected pages inaccessible

**Independent Test**: On /tasks → Click logout → Verify redirect to /login → Try accessing /tasks directly → Verify redirect

### Implementation for User Story 8

- [x] T059 [US8] Add logout button with api.logout() call to tasks page header in phase-2/frontend/src/app/tasks/page.tsx
- [x] T060 [US8] Implement auth.logout() with localStorage clear and redirect in AuthProvider in phase-2/frontend/src/components/auth/AuthProvider.tsx
- [x] T061 [US8] Add browser history replacement to prevent back-button access after logout in phase-2/frontend/src/components/auth/AuthProvider.tsx

**Checkpoint**: All 8 User Stories are independently testable

---

## Phase 11: Home Page & Polish

**Purpose**: Add home page redirect and final cross-cutting improvements

- [x] T062 Create home page with auth-based redirect (authenticated → /tasks, not → /login) in phase-2/frontend/src/app/page.tsx
- [x] T063 [P] Add responsive design classes for mobile (320px+) to all components
- [x] T064 [P] Add consistent error message styling across all forms
- [x] T065 [P] Verify all loading states have appropriate spinners
- [x] T066 Run manual quickstart.md validation for full flow test

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 - BLOCKS all user stories
- **Phases 3-10 (User Stories)**: All depend on Phase 2 completion
- **Phase 11 (Polish)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|-----------|-----------------|
| US1 (Registration) | Phase 2 | Phase 2 complete |
| US2 (Login) | Phase 2 | Phase 2 complete |
| US3 (View Tasks) | Phase 2 | Phase 2 complete |
| US4 (Create Task) | US3 | Phase 5 complete |
| US5 (Toggle) | US3 | Phase 5 complete |
| US6 (Update Task) | US3 | Phase 5 complete |
| US7 (Delete Task) | US3 | Phase 5 complete |
| US8 (Logout) | US2 | Phase 4 complete |

### Within Each User Story

1. Component creation first
2. Validation and error handling
3. API integration
4. Page integration

### Parallel Opportunities

**Phase 2 Parallel Tasks**:
```bash
# Can run in parallel:
T007, T012, T013, T014, T015  # UI components + constants
```

**After Phase 2**:
```bash
# US1, US2, US3 can start in parallel
Phase 3 (US1) | Phase 4 (US2) | Phase 5 (US3)

# US4, US5, US6, US7 can start in parallel after US3
Phase 6 (US4) | Phase 7 (US5) | Phase 8 (US6) | Phase 9 (US7)
```

---


## Parallel Example: Foundational Phase

```bash
# Launch all UI components together:
Task: "Create Button component in phase-2/frontend/src/components/ui/Button.tsx"
Task: "Create Input component in phase-2/frontend/src/components/ui/Input.tsx"
Task: "Create LoadingSpinner component in phase-2/frontend/src/components/ui/LoadingSpinner.tsx"
Task: "Create ErrorMessage component in phase-2/frontend/src/components/ui/ErrorMessage.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1-5 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3-7: User Stories 1-5 (P1 priority)
4. **STOP and VALIDATE**: Test all core functionality
5. Deploy/demo if ready

**MVP Scope**: Registration, Login, View Tasks, Create Task, Toggle Completion

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 (Registration) → Can create accounts
3. US2 (Login) → Can log in
4. US3 (View Tasks) → Can see tasks
5. US4 (Create Task) → Can add tasks
6. US5 (Toggle) → Can complete tasks → **MVP Complete!**
7. US6 (Update) → Can edit tasks
8. US7 (Delete) → Can remove tasks
9. US8 (Logout) → Can log out securely

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: US1 (Registration) + US2 (Login)
   - Developer B: US3 (View Tasks) + US4 (Create Task)
   - Developer C: US5 (Toggle) → then US6, US7, US8
3. Stories integrate independently

---

## Summary

| Phase | Tasks | Parallel Opportunities |
|-------|-------|----------------------|
| Setup | 5 | 4 |
| Foundational | 13 | 4 |
| US1 Registration | 5 | 0 |
| US2 Login | 6 | 0 |
| US3 View Tasks | 8 | 0 |
| US4 Create Task | 5 | 0 |
| US5 Toggle | 4 | 0 |
| US6 Update | 6 | 0 |
| US7 Delete | 6 | 0 |
| US8 Logout | 3 | 0 |
| Polish | 5 | 3 |
| **TOTAL** | **66** | **11** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP = User Stories 1-5 (all P1 priority)
