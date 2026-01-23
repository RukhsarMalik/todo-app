# Tasks: MCP Server with Task Tools

**Input**: Design documents from `/specs/phase3/2-mcp-server/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md, quickstart.md, contracts/

**Tests**: Manual verification via MCP inspector and stdio testing (no automated tests requested)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `phase-3/backend/`
- **MCP Server**: `phase-3/backend/mcp_server.py`
- **Models**: `phase-3/backend/models.py` (existing)
- **Database**: `phase-3/backend/db.py` (existing)

---

## Phase 1: Setup

**Purpose**: Add MCP SDK dependency to the project

- [x] T001 Add mcp[cli] dependency to phase-3/backend/pyproject.toml
- [ ] T002 Run uv sync to install MCP SDK in phase-3/backend/ (MANUAL: run `uv sync` in phase-3/backend/)

---

## Phase 2: Foundational (MCP Server Skeleton)

**Purpose**: Create the MCP server file with FastMCP initialization

**⚠️ CRITICAL**: All tool implementations depend on this phase

- [x] T003 Create mcp_server.py with imports and FastMCP initialization in phase-3/backend/mcp_server.py
- [x] T004 Add main() function with stdio transport runner in phase-3/backend/mcp_server.py
- [x] T005 Configure logging (never use print in stdio servers) in phase-3/backend/mcp_server.py

**Checkpoint**: MCP server skeleton ready - tool implementation can now begin

---

## Phase 3: User Story 1 - Add Task Tool (Priority: P1) 🎯 MVP

**Goal**: Enable AI agents to create new tasks for users

**Independent Test**: Call add_task with valid user_id and title, verify task created in database

### Implementation for User Story 1

- [x] T006 [US1] Implement add_task tool with @mcp.tool() decorator in phase-3/backend/mcp_server.py
- [x] T007 [US1] Add user_id validation (non-empty) to add_task in phase-3/backend/mcp_server.py
- [x] T008 [US1] Add title validation (non-empty, max 200 chars) to add_task in phase-3/backend/mcp_server.py
- [x] T009 [US1] Add description validation (max 1000 chars) to add_task in phase-3/backend/mcp_server.py
- [x] T010 [US1] Implement database INSERT using get_session() in add_task in phase-3/backend/mcp_server.py
- [x] T011 [US1] Return JSON response with task_id, status, title from add_task in phase-3/backend/mcp_server.py

**Checkpoint**: US1 complete - add_task tool functional and independently testable

---

## Phase 4: User Story 2 - List Tasks Tool (Priority: P1)

**Goal**: Enable AI agents to retrieve user's tasks with optional filtering

**Independent Test**: Create tasks, call list_tasks with different status filters, verify correct tasks returned

### Implementation for User Story 2

- [x] T012 [US2] Implement list_tasks tool with @mcp.tool() decorator in phase-3/backend/mcp_server.py
- [x] T013 [US2] Add user_id validation to list_tasks in phase-3/backend/mcp_server.py
- [x] T014 [US2] Add status parameter validation (all/pending/completed) to list_tasks in phase-3/backend/mcp_server.py
- [x] T015 [US2] Implement database SELECT with status filtering in list_tasks in phase-3/backend/mcp_server.py
- [x] T016 [US2] Return JSON response with tasks array and count from list_tasks in phase-3/backend/mcp_server.py

**Checkpoint**: US2 complete - list_tasks tool functional and independently testable

---

## Phase 5: User Story 3 - Complete Task Tool (Priority: P1)

**Goal**: Enable AI agents to mark tasks as completed

**Independent Test**: Create pending task, call complete_task, verify task.completed is True

### Implementation for User Story 3

- [x] T017 [US3] Implement complete_task tool with @mcp.tool() decorator in phase-3/backend/mcp_server.py
- [x] T018 [US3] Add user_id and task_id validation to complete_task in phase-3/backend/mcp_server.py
- [x] T019 [US3] Query task by id AND user_id (ownership check) in complete_task in phase-3/backend/mcp_server.py
- [x] T020 [US3] Return error if task not found (no info leakage) in complete_task in phase-3/backend/mcp_server.py
- [x] T021 [US3] Update task.completed=True and task.updated_at in complete_task in phase-3/backend/mcp_server.py
- [x] T022 [US3] Return JSON response with task_id, status, title from complete_task in phase-3/backend/mcp_server.py

**Checkpoint**: US3 complete - complete_task tool functional and independently testable

---

## Phase 6: User Story 4 - Delete Task Tool (Priority: P2)

**Goal**: Enable AI agents to remove tasks from user's list

**Independent Test**: Create task, call delete_task, verify task no longer exists in database

### Implementation for User Story 4

- [x] T023 [US4] Implement delete_task tool with @mcp.tool() decorator in phase-3/backend/mcp_server.py
- [x] T024 [US4] Add user_id and task_id validation to delete_task in phase-3/backend/mcp_server.py
- [x] T025 [US4] Query task by id AND user_id (ownership check) in delete_task in phase-3/backend/mcp_server.py
- [x] T026 [US4] Return error if task not found in delete_task in phase-3/backend/mcp_server.py
- [x] T027 [US4] Delete task from database in delete_task in phase-3/backend/mcp_server.py
- [x] T028 [US4] Return JSON response with task_id, status from delete_task in phase-3/backend/mcp_server.py

**Checkpoint**: US4 complete - delete_task tool functional and independently testable

---

## Phase 7: User Story 5 - Update Task Tool (Priority: P2)

**Goal**: Enable AI agents to modify task title and/or description

**Independent Test**: Create task, call update_task with new title, verify changes persisted

### Implementation for User Story 5

- [x] T029 [US5] Implement update_task tool with @mcp.tool() decorator in phase-3/backend/mcp_server.py
- [x] T030 [US5] Add user_id and task_id validation to update_task in phase-3/backend/mcp_server.py
- [x] T031 [US5] Validate at least one of title/description provided in update_task in phase-3/backend/mcp_server.py
- [x] T032 [US5] Add title validation (max 200 chars) if provided in update_task in phase-3/backend/mcp_server.py
- [x] T033 [US5] Add description validation (max 1000 chars) if provided in update_task in phase-3/backend/mcp_server.py
- [x] T034 [US5] Query task by id AND user_id (ownership check) in update_task in phase-3/backend/mcp_server.py
- [x] T035 [US5] Return error if task not found in update_task in phase-3/backend/mcp_server.py
- [x] T036 [US5] Update task fields and updated_at in update_task in phase-3/backend/mcp_server.py
- [x] T037 [US5] Return JSON response with task_id, status, title from update_task in phase-3/backend/mcp_server.py

**Checkpoint**: US5 complete - update_task tool functional and independently testable

---

## Phase 8: Polish & Verification

**Purpose**: Final validation and documentation

- [ ] T038 [P] Verify MCP server starts with: uv run python mcp_server.py (MANUAL)
- [ ] T039 [P] Verify all 5 tools discoverable via MCP tools/list method (MANUAL)
- [ ] T040 Test add_task with valid inputs via stdio (MANUAL)
- [ ] T041 Test list_tasks with all/pending/completed filters via stdio (MANUAL)
- [ ] T042 Test complete_task with valid task_id via stdio (MANUAL)
- [ ] T043 Test delete_task with valid task_id via stdio (MANUAL)
- [ ] T044 Test update_task with valid task_id via stdio (MANUAL)
- [ ] T045 Test error handling (invalid user_id, missing title, etc.) (MANUAL)
- [x] T046 Update phase-3/backend/CLAUDE.md with MCP server documentation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - Creates MCP server skeleton
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - Tools must be added sequentially to same file (mcp_server.py)
  - But can be tested independently after implementation
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

```
Phase 1: Setup
    │
    ▼
Phase 2: Foundational (MCP skeleton)
    │
    ▼
Phase 3: US1 - add_task (P1) ─── MVP COMPLETE
    │
    ▼
Phase 4: US2 - list_tasks (P1)
    │
    ▼
Phase 5: US3 - complete_task (P1)
    │
    ├──────────────────┐
    ▼                  ▼
Phase 6: US4 (P2)    Phase 7: US5 (P2)
delete_task          update_task
    │                  │
    └──────────────────┘
              │
              ▼
        Phase 8: Polish
```

### Within Each User Story

- Implement tool decorator first
- Add validations before database operations
- Database operations before response formatting
- All within same file (mcp_server.py)

### Parallel Opportunities

- **T038 and T039** in Polish phase can run in parallel
- **Phase 6 and Phase 7** (US4 and US5) can run in parallel after Phase 5
- Note: Since all tools are in one file, true parallel implementation is limited

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (add dependency)
2. Complete Phase 2: Foundational (MCP skeleton)
3. Complete Phase 3: User Story 1 (add_task)
4. **STOP and VALIDATE**: Test add_task independently
5. MCP server usable for creating tasks

### Incremental Delivery

1. Setup + Foundational → MCP server skeleton ready
2. Add US1 (add_task) → Test independently → Core write capability
3. Add US2 (list_tasks) → Test independently → Read capability
4. Add US3 (complete_task) → Test independently → Status updates
5. Add US4 + US5 → Test independently → Full CRUD complete

### Suggested MVP Scope

**MVP = Phase 1 + Phase 2 + Phase 3 + Phase 4 + Phase 5**

This gives:
- MCP server running
- add_task tool (create)
- list_tasks tool (read)
- complete_task tool (status update)
- Core functionality for AI agent task management

---

## Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| 1: Setup | 2 | Add MCP dependency |
| 2: Foundational | 3 | MCP server skeleton |
| 3: US1 (P1) | 6 | add_task tool |
| 4: US2 (P1) | 5 | list_tasks tool |
| 5: US3 (P1) | 6 | complete_task tool |
| 6: US4 (P2) | 6 | delete_task tool |
| 7: US5 (P2) | 9 | update_task tool |
| 8: Polish | 9 | Verification & docs |

**Total Tasks**: 46
**MVP Tasks**: 22 (Phases 1-5)
**P1 User Stories**: US1, US2, US3 (17 tasks)
**P2 User Stories**: US4, US5 (15 tasks)

---

## Notes

- All tool implementations go in single file: `phase-3/backend/mcp_server.py`
- Reuse existing `models.py` (Task) and `db.py` (get_session)
- Never use `print()` in MCP server - use `logging` module
- Run server with: `uv run python mcp_server.py`
- Test tools with stdio JSON-RPC messages
- Commit after each completed phase
