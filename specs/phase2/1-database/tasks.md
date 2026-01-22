# Tasks: Database Setup & Models

**Module**: Phase II - Module 1 of 5
**Input**: Design documents from `specs/phase2/1-database/`
**Prerequisites**: plan.md (complete), specification.md (complete), data-model.md (complete)

**Tests**: Manual test script included (test_db.py) - not TDD, validation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Backend module**: `phase-2/backend/` (all Phase II work in phase-2 folder)
- Files at backend root (Module 2 will add src/ subdirectories)

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create backend directory structure and initialize UV project

- [x] T001 Create backend directory structure at `phase-2/backend/`
- [x] T002 Initialize UV project with `uv init` in `phase-2/backend/`
- [x] T003 Add dependencies: sqlmodel, asyncpg, python-dotenv via `uv add`
- [x] T004 [P] Create environment template at `phase-2/backend/.env.example`
- [x] T005 [P] Create backend CLAUDE.md guidance at `phase-2/backend/CLAUDE.md`
- [x] T006 [P] Update root `.gitignore` to exclude `phase-2/backend/.env` and `phase-2/backend/__pycache__/`

**Checkpoint**: ✅ Backend project initialized with all dependencies ready

---

## Phase 2: User Story 1 - Database Connection Setup (Priority: P1) 🎯 MVP

**Goal**: Establish async connection to Neon PostgreSQL with connection pooling

**Independent Test**: Verify connection to Neon and execute simple query

**Spec Reference**: US-DB-1 in specification.md

### Implementation for US-DB-1

- [x] T007 [US1] Create db.py module structure with imports at `phase-2/backend/db.py`
- [x] T008 [US1] Implement environment variable loading (DATABASE_URL) in `phase-2/backend/db.py`
- [x] T009 [US1] Implement `get_engine()` function with AsyncEngine creation in `phase-2/backend/db.py`
- [x] T010 [US1] Configure connection pool (min=1, max=10, SSL required) in `phase-2/backend/db.py`
- [x] T011 [US1] Add connection error handling with clear messages in `phase-2/backend/db.py`
- [x] T012 [US1] Add module docstring and function docstrings in `phase-2/backend/db.py`

**Checkpoint**: ✅ Database connection can be established to Neon PostgreSQL

---

## Phase 3: User Story 2 - Task Model Definition (Priority: P1)

**Goal**: Define Task SQLModel class with all fields, constraints, and type hints

**Independent Test**: Create Task instance and validate field constraints

**Spec Reference**: US-DB-2 in specification.md

### Implementation for US-DB-2

- [x] T013 [US2] Create models.py with imports and module docstring at `phase-2/backend/models.py`
- [x] T014 [US2] Define Task class inheriting from SQLModel with `table=True` in `phase-2/backend/models.py`
- [x] T015 [US2] Implement id field (primary key, auto-increment) in `phase-2/backend/models.py`
- [x] T016 [US2] Implement user_id field (str, indexed, max 255, FK reference) in `phase-2/backend/models.py`
- [x] T017 [US2] Implement title field (str, required, 1-200 chars) in `phase-2/backend/models.py`
- [x] T018 [US2] Implement description field (Optional[str], max 1000 chars) in `phase-2/backend/models.py`
- [x] T019 [US2] Implement completed field (bool, default False) in `phase-2/backend/models.py`
- [x] T020 [US2] Implement created_at and updated_at timestamp fields in `phase-2/backend/models.py`
- [x] T021 [US2] Add class docstring with attribute documentation in `phase-2/backend/models.py`
- [x] T022 [US2] Set explicit table name `__tablename__ = "tasks"` in `phase-2/backend/models.py`

**Checkpoint**: ✅ Task model can be instantiated with field validation working

---

## Phase 4: User Story 3 - Async Session Management (Priority: P1)

**Goal**: Implement session factory functions for FastAPI dependency injection pattern

**Independent Test**: Perform database operations within session context

**Spec Reference**: US-DB-3 in specification.md

### Implementation for US-DB-3

- [x] T023 [US3] Import AsyncSession and async_sessionmaker in `phase-2/backend/db.py`
- [x] T024 [US3] Create async_sessionmaker instance bound to engine in `phase-2/backend/db.py`
- [x] T025 [US3] Implement `get_session()` async generator function in `phase-2/backend/db.py`
- [x] T026 [US3] Add try/finally for session cleanup in `get_session()` in `phase-2/backend/db.py`
- [x] T027 [US3] Add commit on success, rollback on exception in `phase-2/backend/db.py`
- [x] T028 [US3] Add docstring with FastAPI Depends() usage example in `phase-2/backend/db.py`

**Checkpoint**: ✅ Sessions can be created, used, and cleaned up properly

---

## Phase 5: User Story 4 - Database Initialization (Priority: P1)

**Goal**: Create init_db script that creates tables and indexes automatically

**Independent Test**: Run init_db.py and verify tasks table exists in Neon console

**Spec Reference**: US-DB-4 in specification.md

### Implementation for US-DB-4

- [x] T029 [US4] Create init_db.py script structure at `phase-2/backend/init_db.py`
- [x] T030 [US4] Import Task model and db module in `phase-2/backend/init_db.py`
- [x] T031 [US4] Implement `init_db()` async function using metadata.create_all() in `phase-2/backend/db.py`
- [x] T032 [US4] Add init_db() call to `phase-2/backend/db.py` exports
- [x] T033 [US4] Implement standalone script runner in `phase-2/backend/init_db.py`
- [x] T034 [US4] Add logging for table creation success/failure in `phase-2/backend/init_db.py`
- [x] T035 [US4] Handle FK constraint warning gracefully (users table not yet exists) in `phase-2/backend/init_db.py`

**Checkpoint**: ✅ Running `uv run python init_db.py` creates tasks table in Neon

---

## Phase 6: User Story 5 - Database Utilities (Priority: P2)

**Goal**: Implement helper functions for engine lifecycle management

**Independent Test**: Verify engine singleton pattern and connection cleanup

**Spec Reference**: US-DB-5 in specification.md

### Implementation for US-DB-5

- [x] T036 [US5] Implement engine singleton pattern (module-level variable) in `phase-2/backend/db.py`
- [x] T037 [US5] Implement `close_db()` async function to dispose engine in `phase-2/backend/db.py`
- [x] T038 [US5] Add DATABASE_URL validation with helpful error message in `phase-2/backend/db.py`
- [x] T039 [US5] Export all public functions in `phase-2/backend/db.py` module

**Checkpoint**: ✅ Engine is singleton, connections can be cleanly closed

---

## Phase 7: Validation & Polish

**Purpose**: Verify all components work together, create validation script

### Validation Script

- [x] T040 Create test_db.py validation script structure at `phase-2/backend/test_db.py`
- [x] T041 Implement connection test in `phase-2/backend/test_db.py`
- [x] T042 Implement table creation verification in `phase-2/backend/test_db.py`
- [x] T043 Implement task insert test in `phase-2/backend/test_db.py`
- [x] T044 Implement task query test in `phase-2/backend/test_db.py`
- [x] T045 Implement cleanup (delete test data) in `phase-2/backend/test_db.py`
- [x] T046 Add main() runner with success/failure output in `phase-2/backend/test_db.py`

### Final Checks

- [x] T047 Verify all files have type hints and docstrings
- [x] T048 Test with invalid DATABASE_URL (error handling)
- [x] T049 Verify indexes in Neon console (idx_tasks_user_id, idx_tasks_completed)
- [x] T050 Run test_db.py validation - ALL 6 TESTS PASSED

**Checkpoint**: ✅ ALL TESTS PASSED! Module 1 complete and ready for Module 2 integration

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    │
    ▼
Phase 2: US1 - Connection ──────┐
    │                           │
    ▼                           │
Phase 3: US2 - Model ──────────►│ (Models import db)
    │                           │
    ▼                           │
Phase 4: US3 - Sessions ───────►│ (Sessions use engine)
    │                           │
    ▼                           │
Phase 5: US4 - Init ───────────►│ (Init uses model + db)
    │                           │
    ▼                           │
Phase 6: US5 - Utilities ──────►│ (Utilities extend db)
    │                           │
    ▼
Phase 7: Validation
```

### User Story Dependencies

| User Story | Depends On | Can Start After |
|------------|------------|-----------------|
| US1 (Connection) | Setup | Phase 1 complete |
| US2 (Model) | US1 | Phase 2 complete |
| US3 (Sessions) | US1 | Phase 2 complete |
| US4 (Init) | US1, US2 | Phase 3 complete |
| US5 (Utilities) | US1 | Phase 2 complete |

### Parallel Opportunities

**Within Phase 1 (Setup):**
```
T004 .env.example    ─┐
T005 CLAUDE.md       ─┼─ [P] Can run in parallel
T006 .gitignore      ─┘
```

**After Phase 2 (Connection complete):**
```
US2 (Model)     ─┐
US3 (Sessions)  ─┼─ Can start in parallel
US5 (Utilities) ─┘
```

---

## Parallel Example: Phase 1 Setup

```bash
# Launch these tasks together (different files, no dependencies):
Task: "Create environment template at backend/.env.example"
Task: "Create backend CLAUDE.md guidance at backend/CLAUDE.md"
Task: "Update root .gitignore to exclude backend/.env"
```

---

## Implementation Strategy

### MVP First (Minimum Viable Database)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: US1 Connection (T007-T012)
3. Complete Phase 3: US2 Model (T013-T022)
4. Complete Phase 4: US3 Sessions (T023-T028)
5. Complete Phase 5: US4 Init (T029-T035)
6. **STOP and VALIDATE**: Run init_db.py, verify table in Neon
7. Module 1 MVP complete!

### Full Module

1. Complete MVP (Phases 1-5)
2. Add Phase 6: US5 Utilities (T036-T039)
3. Add Phase 7: Validation (T040-T050)
4. Module 1 complete, ready for Module 2

---

## Task Summary

| Phase | User Story | Task Count | Priority |
|-------|------------|------------|----------|
| 1 | Setup | 6 | - |
| 2 | US1 - Connection | 6 | P1 |
| 3 | US2 - Model | 10 | P1 |
| 4 | US3 - Sessions | 6 | P1 |
| 5 | US4 - Init | 7 | P1 |
| 6 | US5 - Utilities | 4 | P2 |
| 7 | Validation | 11 | - |
| **Total** | | **50** | |

---

## Files Created by This Module

| File | Created In | Purpose |
|------|------------|---------|
| `phase-2/backend/` | T001 | Backend directory |
| `phase-2/backend/pyproject.toml` | T002 | UV project config |
| `phase-2/backend/.env.example` | T004 | Environment template |
| `phase-2/backend/CLAUDE.md` | T005 | AI guidance |
| `phase-2/backend/db.py` | T007-T012, T023-T028, T031-T032, T036-T039 | Database module |
| `phase-2/backend/models.py` | T013-T022 | Task model |
| `phase-2/backend/init_db.py` | T029-T035 | Init script |
| `phase-2/backend/test_db.py` | T040-T046 | Validation script |

---

## Notes

- [P] tasks = different files, no dependencies on each other
- [USn] label maps task to specific user story for traceability
- All P1 user stories (US1-US4) are required for MVP
- US5 (P2) adds lifecycle management but not blocking
- Commit after each user story phase completes
- Test manually after Phase 5 to validate MVP
- No automated tests in this module (manual validation via test_db.py)
