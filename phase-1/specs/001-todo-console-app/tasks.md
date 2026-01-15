---

description: "Task list for Todo Console App (Phase I) implementation"
---

# Tasks: Todo Console App (Phase I)

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/, research.md

**Tests**: No automated tests in Phase I (manual testing against acceptance criteria)

**Organization**: Tasks grouped by user story to enable independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below use single project structure as defined in plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure with src/, src/models/, src/services/, src/cli/, src/validators/ directories
- [x] T002 [P] Create pyproject.toml with UV configuration (Python 3.13+, no dependencies)
- [x] T003 [P] Create .gitignore with Python-specific ignores (__pycache__, *.pyc, .venv, *.egg-info)
- [x] T004 [P] Create README.md with project overview, setup instructions, and usage examples
- [x] T005 [P] Create empty __init__.py files in src/, src/models/, src/services/, src/cli/, src/validators/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 [P] Create Task dataclass in src/models/task.py with fields: id (int), title (str), description (str), completed (bool), created_at (datetime)
- [ ] T007 [P] Create TaskManager class skeleton in src/services/task_manager.py with __init__ method initializing _tasks list and _next_id counter
- [ ] T008 [P] Create validate_title function in src/validators/input_validators.py returning tuple[bool, str, str] for title validation (1-200 chars, non-empty after trim)
- [ ] T009 [P] Create validate_description function in src/validators/input_validators.py returning tuple[bool, str, str] for description validation (max 1000 chars after trim)
- [ ] T010 [P] Create validate_task_id function in src/validators/input_validators.py returning tuple[bool, str, int | None] for ID validation (numeric, positive)
- [ ] T011 [P] Create validate_menu_choice function in src/validators/input_validators.py returning tuple[bool, str, int | None] for menu validation (1-6)
- [ ] T012 [P] Create validate_confirmation function in src/validators/input_validators.py returning tuple[bool, str, bool] for yes/no validation
- [ ] T013 [P] Export all validators in src/validators/__init__.py
- [ ] T014 Export Task from src/models/__init__.py
- [ ] T015 Create display_menu function in src/cli/menu.py that prints main menu with 6 numbered options

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Display all tasks with status indicators, IDs, titles, descriptions in creation order

**Independent Test**: Launch app, add sample tasks via TaskManager (manual), select "View Tasks", verify display shows IDs, status indicators [✓]/[ ], titles, descriptions in correct format

### Implementation for User Story 1

- [ ] T016 [US1] Implement get_all_tasks method in src/services/task_manager.py that returns copy of _tasks list
- [ ] T017 [US1] Implement handle_view_tasks function in src/cli/handlers.py that calls TaskManager.get_all_tasks() and displays formatted task list with status indicators
- [ ] T018 [US1] Update handle_view_tasks in src/cli/handlers.py to show "No tasks found. Add your first task to get started!" when task list is empty
- [ ] T019 [US1] Format task display in handle_view_tasks to show: status [✓]/[ ], ID, title, indented description, creation timestamp
- [ ] T020 [US1] Export handle_view_tasks from src/cli/__init__.py

**Checkpoint**: At this point, User Story 1 (View Tasks) should be fully functional with proper display formatting

---

## Phase 4: User Story 2 - Add New Task (Priority: P2)

**Goal**: Create tasks with validated title and optional description, auto-generate IDs, confirm success

**Independent Test**: Select "Add Task", enter valid title + description, verify task appears in list with unique ID and pending status, verify validation errors for invalid inputs

### Implementation for User Story 2

- [ ] T021 [US2] Implement add_task method in src/services/task_manager.py that creates Task with auto-generated ID (_next_id), appends to _tasks, increments _next_id, returns Task
- [ ] T022 [US2] Implement handle_add_task function in src/cli/handlers.py that prompts for title, validates using validate_title, re-prompts on error
- [ ] T023 [US2] Update handle_add_task in src/cli/handlers.py to prompt for description (optional), validate using validate_description if provided
- [ ] T024 [US2] Update handle_add_task in src/cli/handlers.py to call TaskManager.add_task with validated title and description, display success message with task ID
- [ ] T025 [US2] Export handle_add_task from src/cli/__init__.py
- [ ] T026 [US2] Export TaskManager from src/services/__init__.py

**Checkpoint**: At this point, User Story 2 (Add Task) should be fully functional with input validation and success confirmation

---

## Phase 5: User Story 3 - Toggle Task Status (Priority: P3)

**Goal**: Toggle task between pending and completed states, display confirmation, update immediately visible

**Independent Test**: Add task, toggle to completed (verify [✓]), toggle back to pending (verify [ ]), verify error handling for invalid IDs

### Implementation for User Story 3

- [ ] T027 [P] [US3] Implement get_task_by_id method in src/services/task_manager.py that searches _tasks by ID, returns Task or None
- [ ] T028 [US3] Implement toggle_task_status method in src/services/task_manager.py that finds task by ID, inverts completed field, returns True if found else False
- [ ] T029 [US3] Implement handle_toggle_status function in src/cli/handlers.py that prompts for task ID, validates using validate_task_id
- [ ] T030 [US3] Update handle_toggle_status in src/cli/handlers.py to check task exists using get_task_by_id, show error if not found
- [ ] T031 [US3] Update handle_toggle_status in src/cli/handlers.py to call toggle_task_status, display confirmation "Task #X marked as completed/pending!"
- [ ] T032 [US3] Export handle_toggle_status from src/cli/__init__.py

**Checkpoint**: At this point, User Story 3 (Toggle Status) should be fully functional with bidirectional toggling

---

## Phase 6: User Story 4 - Update Task (Priority: P4)

**Goal**: Modify task title and/or description, validate inputs, confirm update, preserve other fields

**Independent Test**: Add task, update title only, verify change; update description only, verify change; update both, verify changes; test validation errors

### Implementation for User Story 4

- [ ] T033 [US4] Implement update_task method in src/services/task_manager.py that finds task by ID, updates title and/or description if provided, returns True if found else False
- [ ] T034 [US4] Implement handle_update_task function in src/cli/handlers.py that prompts for task ID, validates, checks existence
- [ ] T035 [US4] Update handle_update_task in src/cli/handlers.py to display current task title and description
- [ ] T036 [US4] Update handle_update_task in src/cli/handlers.py to prompt for new title (optional - press Enter to keep), validate if provided
- [ ] T037 [US4] Update handle_update_task in src/cli/handlers.py to prompt for new description (optional - press Enter to keep), validate if provided
- [ ] T038 [US4] Update handle_update_task in src/cli/handlers.py to call update_task with validated inputs, display success confirmation
- [ ] T039 [US4] Export handle_update_task from src/cli/__init__.py

**Checkpoint**: At this point, User Story 4 (Update Task) should be fully functional with partial update support

---

## Phase 7: User Story 5 - Delete Task (Priority: P5)

**Goal**: Remove tasks with confirmation prompt, prevent accidental deletion, confirm success

**Independent Test**: Add task, delete with confirmation (y), verify removed; add task, cancel deletion (n), verify preserved; test invalid ID handling

### Implementation for User Story 5

- [ ] T040 [US5] Implement delete_task method in src/services/task_manager.py that finds task by ID, removes from _tasks list, returns True if found else False (ID never reused - _next_id not decremented)
- [ ] T041 [US5] Implement handle_delete_task function in src/cli/handlers.py that prompts for task ID, validates, checks existence
- [ ] T042 [US5] Update handle_delete_task in src/cli/handlers.py to display confirmation prompt "Are you sure you want to delete task #X: [title]? (y/n)"
- [ ] T043 [US5] Update handle_delete_task in src/cli/handlers.py to validate confirmation using validate_confirmation
- [ ] T044 [US5] Update handle_delete_task in src/cli/handlers.py to call delete_task if confirmed, display success message; if cancelled, display "Deletion cancelled. Task #X preserved."
- [ ] T045 [US5] Export handle_delete_task from src/cli/__init__.py

**Checkpoint**: At this point, User Story 5 (Delete Task) should be fully functional with confirmation safety

---

## Phase 8: Integration & Main Loop

**Purpose**: Wire all components together into working application with main menu loop

- [ ] T046 Create main.py in src/ with main() function that creates TaskManager instance
- [ ] T047 Implement main menu loop in src/main.py using while True, displaying menu via display_menu()
- [ ] T048 Implement menu choice handling in src/main.py: get choice via get_menu_choice(), validate using validate_menu_choice
- [ ] T049 Implement handler routing in src/main.py: map choices 1-5 to respective handlers (view, add, update, delete, toggle), choice 6 exits
- [ ] T050 Add error handling in src/main.py: try-except around main loop to catch KeyboardInterrupt (Ctrl+C) and EOFError, display "Goodbye!" on exit
- [ ] T051 Create get_menu_choice function in src/cli/menu.py that prompts for choice, validates, re-prompts on error, returns valid int (1-6)
- [ ] T052 Export display_menu and get_menu_choice from src/cli/__init__.py
- [ ] T053 Add if __name__ == "__main__": main() block to src/main.py

**Checkpoint**: Full application integrated and runnable from command line

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final touches, documentation, validation against acceptance criteria

- [ ] T054 [P] Add module-level docstrings to all Python files (src/main.py, src/models/task.py, src/services/task_manager.py, src/cli/menu.py, src/cli/handlers.py, src/validators/input_validators.py)
- [ ] T055 [P] Add Google-style docstrings to all public functions and classes (Task, TaskManager, validators, handlers, menu functions)
- [ ] T056 [P] Add type hints to main() function and verify all functions have complete type hints
- [ ] T057 [P] Verify all error messages follow pattern "[What went wrong]. [How to fix it]. [Current state if relevant]"
- [ ] T058 Run manual acceptance test for User Story 1 (all 5 scenarios from spec.md)
- [ ] T059 Run manual acceptance test for User Story 2 (all 6 scenarios from spec.md)
- [ ] T060 Run manual acceptance test for User Story 3 (all 5 scenarios from spec.md)
- [ ] T061 Run manual acceptance test for User Story 4 (all 7 scenarios from spec.md)
- [ ] T062 Run manual acceptance test for User Story 5 (all 7 scenarios from spec.md)
- [ ] T063 Test all 9 edge cases from spec.md (empty list, boundary values, special chars, etc.)
- [ ] T064 Verify 90-second demo workflow: launch app → add task → view tasks → toggle status → update task → delete task → exit
- [ ] T065 Verify no crashes on 50+ consecutive operations (rapid add/delete/update/toggle cycles)
- [ ] T066 [P] Update README.md with quickstart instructions based on quickstart.md
- [ ] T067 Verify constitutional compliance: no external imports beyond stdlib (dataclasses, typing, datetime, sys)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - Can proceed in parallel if multiple developers
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Integration (Phase 8)**: Depends on all user stories being complete
- **Polish (Phase 9)**: Depends on Integration completion

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (T006-T015) → implements view functionality
- **User Story 2 (P2)**: Depends on Foundational (T006-T015) → implements add functionality
- **User Story 3 (P3)**: Depends on Foundational (T006-T015) → implements toggle functionality
- **User Story 4 (P4)**: Depends on Foundational (T006-T015) → implements update functionality
- **User Story 5 (P5)**: Depends on Foundational (T006-T015) → implements delete functionality

**Independence**: Each user story (P1-P5) can be implemented independently after Foundational phase. No cross-story dependencies.

### Within Each User Story

- User Story 1 (T016-T020): Sequential (each task builds on previous)
- User Story 2 (T021-T026): Sequential (handler depends on service method)
- User Story 3 (T027-T032): T027 can run in parallel with T028, rest sequential
- User Story 4 (T033-T039): Sequential (handler depends on service method)
- User Story 5 (T040-T045): Sequential (handler depends on service method)

### Parallel Opportunities

**Setup Phase** (can all run in parallel):
- T002, T003, T004, T005 (independent file creation)

**Foundational Phase** (can run in parallel):
- T006, T007, T008, T009, T010, T011, T012 (different modules)
- T013, T014 after respective modules complete

**User Story Implementation** (after Foundational complete):
- All 5 user stories (US1-US5) can be worked on in parallel by different developers
- Each story is independently testable

**Polish Phase** (can run in parallel):
- T054, T055, T056, T057, T066, T067 (different files/checks)
- T058-T065 must run sequentially (manual testing)

---

## Parallel Example: Foundational Phase

```bash
# Launch all foundation tasks together (different files, no dependencies):
Task T006: Create Task dataclass in src/models/task.py
Task T007: Create TaskManager class skeleton in src/services/task_manager.py
Task T008: Create validate_title function in src/validators/input_validators.py
Task T009: Create validate_description function in src/validators/input_validators.py
Task T010: Create validate_task_id function in src/validators/input_validators.py
Task T011: Create validate_menu_choice function in src/validators/input_validators.py
Task T012: Create validate_confirmation function in src/validators/input_validators.py

# Then run exports after modules complete:
Task T013: Export all validators in src/validators/__init__.py
Task T014: Export Task from src/models/__init__.py
```

---

## Parallel Example: User Stories (after Foundational)

```bash
# Different developers can work on different stories simultaneously:
Developer A: User Story 1 (T016-T020) - View functionality
Developer B: User Story 2 (T021-T026) - Add functionality
Developer C: User Story 3 (T027-T032) - Toggle functionality
Developer D: User Story 4 (T033-T039) - Update functionality
Developer E: User Story 5 (T040-T045) - Delete functionality

# Each story is independently testable and deliverable
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T015) - CRITICAL BLOCKING PHASE
3. Complete Phase 3: User Story 1 (T016-T020)
4. **STOP and VALIDATE**: Manually test User Story 1 against all 5 acceptance scenarios
5. If ready, can demo basic "view tasks" functionality

**MVP Scope**: After T020, you have a working app that can display tasks (if you manually create them in code for testing)

### Incremental Delivery (Recommended)

1. **Iteration 1**: Setup + Foundational + US1 (View) → Test independently
   - Deliverable: App that displays task list (empty or hardcoded)
   - Value: Validates data model and display formatting

2. **Iteration 2**: Add US2 (Add Task) → Test independently
   - Deliverable: App that can add and view tasks
   - Value: Basic workflow (create → view)

3. **Iteration 3**: Add US3 (Toggle Status) → Test independently
   - Deliverable: App with progress tracking
   - Value: Complete basic workflow (create → view → mark done)

4. **Iteration 4**: Add US4 (Update Task) → Test independently
   - Deliverable: App with edit capability
   - Value: Fix typos without recreating tasks

5. **Iteration 5**: Add US5 (Delete Task) → Test independently
   - Deliverable: Full CRUD application
   - Value: Complete task management

6. **Iteration 6**: Integration + Polish (T046-T067)
   - Deliverable: Production-ready Phase I application
   - Value: 90-second demo ready, all acceptance criteria met

### Parallel Team Strategy (5 Developers)

1. **All developers**: Complete Setup + Foundational together (T001-T015)
2. **Once Foundational done**, split into parallel tracks:
   - **Dev A**: User Story 1 (T016-T020) - View
   - **Dev B**: User Story 2 (T021-T026) - Add
   - **Dev C**: User Story 3 (T027-T032) - Toggle
   - **Dev D**: User Story 4 (T033-T039) - Update
   - **Dev E**: User Story 5 (T040-T045) - Delete
3. **All developers**: Integration (T046-T053) - wire together
4. **All developers**: Polish & Testing (T054-T067) - final validation

**Timeline**: With 5 developers, could complete in 1-2 sessions after Foundational phase done.

---

## Task Execution Checklist

Before starting implementation:
- [ ] All design documents reviewed (spec.md, plan.md, data-model.md, contracts/)
- [ ] Python 3.13+ installed and verified
- [ ] Git repository initialized
- [ ] Constitutional requirements understood (zero deps, type hints, docstrings, etc.)

During implementation:
- [ ] Execute tasks in dependency order (Setup → Foundational → User Stories → Integration → Polish)
- [ ] Reference task IDs in commit messages (e.g., "T006: Create Task dataclass")
- [ ] Verify each module has type hints and docstrings before marking task complete
- [ ] Test each user story independently after completing its phase
- [ ] Validate error messages follow "[What]. [How]. [Current state]" pattern

After implementation:
- [ ] Run all 30 acceptance scenarios (5+6+5+7+7) from spec.md
- [ ] Test all 9 edge cases
- [ ] Verify 90-second demo workflow
- [ ] Check 50+ operations without crash
- [ ] Verify no external dependencies (import check)
- [ ] Ensure all task IDs traceable in git log

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- No automated tests in Phase I - all validation is manual against acceptance criteria
- Foundational phase (T006-T015) is CRITICAL - nothing else can start until complete
- Parallel execution possible for user stories after foundation ready
