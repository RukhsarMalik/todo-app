# Tasks: Chat Database Extension

**Input**: Design documents from `/specs/phase3/chat-database/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md, quickstart.md

**Tests**: Manual verification via test scripts (no automated tests requested)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `phase-2/backend/`
- **Models**: `phase-2/backend/models.py`
- **Tests**: `phase-2/backend/test_conversations.py`

---

## Phase 1: Setup

**Purpose**: Prepare models.py for new entity additions

- [x] T001 Add required imports (SQLAlchemy Column, ForeignKey, String, field_validator) to phase-3/backend/models.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create the Conversation model that Message depends on

**⚠️ CRITICAL**: Message model depends on Conversation model being defined first

- [x] T002 Create Conversation model class with id, user_id, title, created_at, updated_at in phase-3/backend/models.py
- [x] T003 Add user_id foreign key with CASCADE delete to Conversation in phase-3/backend/models.py
- [x] T004 Update __all__ exports to include Conversation in phase-3/backend/models.py

**Checkpoint**: Conversation model ready - Message model can now be created

---

## Phase 3: User Story 1 - Start New Conversation (Priority: P1) 🎯 MVP

**Goal**: Enable creating new chat conversations for users

**Independent Test**: Create a conversation for an existing user, verify it persists with correct user_id and timestamps

### Implementation for User Story 1

- [x] T005 [US1] Run init_db.py to create conversations table in database
- [x] T006 [US1] Create test_conversations.py with test for creating a conversation in phase-3/backend/test_conversations.py
- [x] T007 [US1] Verify conversation creation works with valid user_id in phase-3/backend/test_conversations.py
- [x] T008 [US1] Verify FK constraint rejects invalid user_id in phase-3/backend/test_conversations.py

**Checkpoint**: User Story 1 complete - conversations can be created and persisted

---

## Phase 4: User Story 2 - Store Chat Messages (Priority: P1)

**Goal**: Enable storing messages within conversations with role and content validation

**Independent Test**: Add messages to a conversation, verify they persist with correct role, content, and timestamps

### Implementation for User Story 2

- [x] T009 [US2] Create Message model class with id, conversation_id, role, content, created_at in phase-3/backend/models.py
- [x] T010 [US2] Add conversation_id foreign key with CASCADE delete to Message in phase-3/backend/models.py
- [x] T011 [US2] Add @field_validator for role (must be user/assistant/system) in phase-3/backend/models.py
- [x] T012 [US2] Add @field_validator for content (non-empty, max 10000 chars) in phase-3/backend/models.py
- [x] T013 [US2] Update __all__ exports to include Message in phase-3/backend/models.py
- [x] T014 [US2] Run init_db.py to create messages table in database
- [x] T015 [US2] Add test for creating messages with valid role in phase-3/backend/test_conversations.py
- [x] T016 [US2] Add test for role validation rejects invalid roles in phase-3/backend/test_conversations.py
- [x] T017 [US2] Add test for content validation rejects empty content in phase-3/backend/test_conversations.py
- [x] T018 [US2] Add test for content validation rejects >10000 char content in phase-3/backend/test_conversations.py
- [x] T019 [US2] Add test for FK constraint rejects invalid conversation_id in phase-3/backend/test_conversations.py

**Checkpoint**: User Story 2 complete - messages can be stored with validation

---

## Phase 5: User Story 3 - Retrieve Conversation History (Priority: P2)

**Goal**: Enable listing user's conversations and retrieving messages

**Independent Test**: Create multiple conversations with messages, verify retrieval returns correct data in correct order

### Implementation for User Story 3

- [x] T020 [US3] Add test for listing conversations by user_id (most recent first) in phase-3/backend/test_conversations.py
- [x] T021 [US3] Add test for retrieving messages by conversation_id (chronological order) in phase-3/backend/test_conversations.py
- [x] T022 [US3] Add test for empty list when user has no conversations in phase-3/backend/test_conversations.py

**Checkpoint**: User Story 3 complete - conversation history can be retrieved

---

## Phase 6: User Story 4 - Delete Conversation (Priority: P3)

**Goal**: Enable deleting conversations with cascade deletion of messages

**Independent Test**: Create conversation with messages, delete it, verify both conversation and messages are removed

### Implementation for User Story 4

- [x] T023 [US4] Add test for cascade delete removes conversation and all its messages in phase-3/backend/test_conversations.py
- [x] T024 [US4] Add test for user cascade delete removes all their conversations and messages in phase-3/backend/test_conversations.py

**Checkpoint**: User Story 4 complete - cascade deletion verified

---

## Phase 7: Polish & Verification

**Purpose**: Final validation and documentation

- [ ] T025 [P] Run all tests in test_conversations.py to verify complete functionality
- [ ] T026 [P] Verify existing users and tasks tables unaffected by migration
- [x] T027 Update phase-3/backend/CLAUDE.md with new Conversation and Message models documentation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - Creates Conversation model
- **User Story 1 (Phase 3)**: Depends on Foundational - Tests conversation creation
- **User Story 2 (Phase 4)**: Depends on User Story 1 - Message needs Conversation to exist
- **User Story 3 (Phase 5)**: Depends on User Story 2 - Retrieval needs messages to exist
- **User Story 4 (Phase 6)**: Depends on User Story 2 - Cascade delete needs both models
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

```
Phase 1: Setup
    │
    ▼
Phase 2: Foundational (Conversation model)
    │
    ▼
Phase 3: US1 - Create Conversation (P1) ─── MVP COMPLETE
    │
    ▼
Phase 4: US2 - Store Messages (P1)
    │
    ├──────────────────┐
    ▼                  ▼
Phase 5: US3 (P2)    Phase 6: US4 (P3)
Retrieve History     Delete Conversation
    │                  │
    └──────────────────┘
              │
              ▼
        Phase 7: Polish
```

### Within Each User Story

- Model changes before database migration
- Database migration before tests
- Tests verify acceptance criteria

### Parallel Opportunities

- **Phase 5 and Phase 6** can run in parallel after Phase 4 completes
- **T025 and T026** in Polish phase can run in parallel

---

## Parallel Example: After Phase 4

```bash
# After US2 (Store Messages) is complete, these can run in parallel:

# Developer A - User Story 3:
Task: "Add test for listing conversations by user_id"
Task: "Add test for retrieving messages by conversation_id"

# Developer B - User Story 4:
Task: "Add test for cascade delete removes conversation and messages"
Task: "Add test for user cascade delete"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup (imports)
2. Complete Phase 2: Foundational (Conversation model)
3. Complete Phase 3: User Story 1 (create conversations)
4. Complete Phase 4: User Story 2 (store messages)
5. **STOP and VALIDATE**: Test conversation and message creation
6. Database ready for Phase III Module 2 (API endpoints)

### Incremental Delivery

1. Setup + Foundational → Conversation model ready
2. Add US1 → Test conversation creation → MVP foundation
3. Add US2 → Test message storage → Core functionality complete
4. Add US3 → Test history retrieval → Full read capability
5. Add US4 → Test cascade delete → Complete CRUD support

### Suggested MVP Scope

**MVP = Phase 1 + Phase 2 + Phase 3 + Phase 4**

This gives:
- Conversation model with user FK
- Message model with conversation FK
- Role and content validation
- Basic CRUD capability for chat persistence

---

## Summary

| Phase | Tasks | Parallel | Description |
|-------|-------|----------|-------------|
| 1: Setup | 1 | 0 | Add imports |
| 2: Foundational | 3 | 0 | Conversation model |
| 3: US1 (P1) | 4 | 0 | Create conversations |
| 4: US2 (P1) | 11 | 0 | Store messages |
| 5: US3 (P2) | 3 | 0 | Retrieve history |
| 6: US4 (P3) | 2 | 0 | Delete cascade |
| 7: Polish | 3 | 2 | Final verification |

**Total Tasks**: 27
**MVP Tasks**: 19 (Phases 1-4)
**Parallel Opportunities**: 2 tasks in Polish phase, Phases 5+6 can run in parallel

---

## Notes

- All model changes go in existing `phase-2/backend/models.py`
- Tests go in new `phase-2/backend/test_conversations.py`
- Run `uv run python init_db.py` after model changes to create tables
- Run tests with `uv run python test_conversations.py`
- Commit after each completed phase
