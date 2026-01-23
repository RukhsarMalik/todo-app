# Implementation Tasks: Chat Endpoint with OpenAI Agent

**Feature**: Phase III Module 3 - Chat Endpoint
**Date**: 2026-01-23
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Overview

This document defines the implementation tasks for the chat endpoint with OpenAI Agent integration. The implementation follows the SDD (Spec-Driven Development) approach with tasks organized by user story priority and dependencies.

## Implementation Strategy

**MVP Scope**: User Story 1 (Send Chat Message) - Implement the core chat functionality to enable AI-powered task management.

**Delivery Approach**: Incremental delivery with each user story as a complete, independently testable increment.

## Phase 1: Setup Tasks

### Project Initialization

- [X] T001 Install required dependencies (openai, mcp[cli]) in phase-3/backend/pyproject.toml
- [X] T002 Add OPENAI_API_KEY to .env.example file in phase-3/backend/
- [X] T003 Update README.md with chat endpoint setup instructions

## Phase 2: Foundational Tasks

### Prerequisites for All User Stories

- [X] T004 [P] Add chat request/response Pydantic schemas to schemas.py in phase-3/backend/schemas.py
- [X] T005 [P] Create agent.py with ChatAgent class and process_message method in phase-3/backend/agent.py
- [X] T006 [P] Update routes/__init__.py to import and export chat_router in phase-3/backend/routes/__init__.py
- [X] T007 [P] Update main.py to include chat routes in phase-3/backend/main.py

## Phase 3: User Story 1 - Send Chat Message (P1)

**Goal**: Implement the core functionality to send messages to the AI assistant and receive responses.

**Independent Test Criteria**: Can call the chat endpoint with a message, verify the AI responds and the message is stored.

### Tests (Manual Verification)
- [ ] T008 [P] [US1] Create manual test for new conversation creation via chat endpoint
- [ ] T009 [P] [US1] Create manual test for existing conversation continuation via chat endpoint
- [ ] T010 [P] [US1] Create manual test for AI task creation through natural language

### Implementation Tasks
- [X] T011 [P] [US1] Create POST /api/{user_id}/chat endpoint in phase-3/backend/routes/chat.py
- [X] T012 [P] [US1] Implement JWT authentication validation for chat endpoint in phase-3/backend/routes/chat.py
- [X] T013 [US1] Implement conversation creation/loading logic in agent.py
- [X] T014 [US1] Implement message persistence (store user and AI messages) in phase-3/backend/routes/chat.py
- [X] T015 [US1] Integrate OpenAI Assistant API with MCP tools in agent.py
- [X] T016 [US1] Implement error handling for OpenAI API unavailability in phase-3/backend/routes/chat.py
- [X] T017 [US1] Validate message content (length, emptiness) in phase-3/backend/routes/chat.py

## Phase 4: User Story 2 - List Conversations (P1)

**Goal**: Enable users to see their previous chat conversations.

**Independent Test Criteria**: Create conversations, call the list endpoint, verify all conversations are returned.

### Tests (Manual Verification)
- [ ] T018 [P] [US2] Create manual test for listing user's conversations
- [ ] T019 [P] [US2] Create manual test for empty conversations list
- [ ] T020 [P] [US2] Create manual test for cross-user data isolation

### Implementation Tasks
- [X] T021 [P] [US2] Create GET /api/{user_id}/conversations endpoint in phase-3/backend/routes/chat.py
- [X] T022 [US2] Implement conversation listing with proper sorting (updated_at desc) in phase-3/backend/routes/chat.py
- [X] T023 [US2] Add message counting for each conversation in phase-3/backend/routes/chat.py
- [X] T024 [US2] Implement user authorization validation in phase-3/backend/routes/chat.py

## Phase 5: User Story 3 - Get Conversation History (P1)

**Goal**: Allow users to view all messages in a specific conversation.

**Independent Test Criteria**: Create a conversation with messages, retrieve it, verify all messages are returned in order.

### Tests (Manual Verification)
- [ ] T025 [P] [US3] Create manual test for retrieving conversation with messages in chronological order
- [ ] T026 [P] [US3] Create manual test for non-existent conversation (404 response)
- [ ] T027 [P] [US3] Create manual test for cross-user conversation access (404 response)

### Implementation Tasks
- [X] T028 [P] [US3] Create GET /api/{user_id}/conversations/{conversation_id} endpoint in phase-3/backend/routes/chat.py
- [X] T029 [US3] Implement message retrieval in chronological order (oldest first) in phase-3/backend/routes/chat.py
- [X] T030 [US3] Add proper UUID validation for conversation_id in phase-3/backend/routes/chat.py
- [X] T031 [US3] Implement user authorization validation for conversation access in phase-3/backend/routes/chat.py

## Phase 6: User Story 4 - AI Task Management (P1)

**Goal**: Enable the AI to perform task operations through natural language.

**Independent Test Criteria**: Send task-related messages, verify correct MCP tools are invoked.

### Tests (Manual Verification)
- [ ] T032 [P] [US4] Create manual test for add_task tool invocation via natural language
- [ ] T033 [P] [US4] Create manual test for list_tasks tool invocation via natural language
- [ ] T034 [P] [US4] Create manual test for complete_task tool invocation via natural language
- [ ] T035 [P] [US4] Create manual test for delete_task tool invocation via natural language
- [ ] T036 [P] [US4] Create manual test for update_task tool invocation via natural language

### Implementation Tasks
- [X] T037 [P] [US4] Implement MCP tool integration in ChatAgent class in phase-3/backend/agent.py
- [X] T038 [US4] Create proper tool definitions for OpenAI Assistant (add_task, list_tasks, etc.) in phase-3/backend/agent.py
- [X] T039 [US4] Implement user_id passing to MCP tools for authorization in phase-3/backend/agent.py
- [X] T040 [US4] Handle MCP tool execution failures gracefully in phase-3/backend/agent.py
- [X] T041 [US4] Track and return actions_taken in chat response in phase-3/backend/agent.py

## Phase 7: User Story 5 - Delete Conversation (P2)

**Goal**: Allow users to delete conversations they no longer need.

**Independent Test Criteria**: Create a conversation, delete it, verify it no longer exists.

### Tests (Manual Verification)
- [ ] T042 [P] [US5] Create manual test for deleting existing conversation
- [ ] T043 [P] [US5] Create manual test for non-existent conversation deletion (404 response)
- [ ] T044 [P] [US5] Create manual test for cross-user conversation deletion (404 response)

### Implementation Tasks
- [X] T045 [P] [US5] Create DELETE /api/{user_id}/conversations/{conversation_id} endpoint in phase-3/backend/routes/chat.py
- [X] T046 [US5] Implement conversation deletion with cascade (removes messages) in phase-3/backend/routes/chat.py
- [X] T047 [US5] Add proper UUID validation for conversation_id in phase-3/backend/routes/chat.py
- [X] T048 [US5] Implement user authorization validation for deletion in phase-3/backend/routes/chat.py

## Phase 8: Polish & Cross-Cutting Concerns

### Error Handling & Validation
- [X] T049 Add comprehensive input validation for all endpoints (message length, UUID format, etc.) in phase-3/backend/routes/chat.py
- [X] T050 Implement proper error responses (400, 401, 403, 404, 503) in phase-3/backend/routes/chat.py
- [X] T051 Add logging for MCP tool invocations in phase-3/backend/agent.py

### Performance & Monitoring
- [X] T052 Add performance monitoring for chat response times in phase-3/backend/routes/chat.py
- [X] T053 Implement rate limiting for chat endpoints (if needed) in phase-3/backend/routes/chat.py

### Documentation & Testing
- [X] T054 Update API documentation with chat endpoint details in phase-3/backend/docs/api.md
- [X] T055 Create integration tests for chat functionality in phase-3/backend/tests/test_chat.py

## Dependencies

- **User Story 1** (P1) - Core functionality, no dependencies on other stories
- **User Story 2** (P1) - Depends on foundational models and authentication (completed by T007)
- **User Story 3** (P1) - Depends on foundational models and authentication (completed by T007)
- **User Story 4** (P1) - Depends on User Story 1 (core chat functionality)
- **User Story 5** (P2) - Depends on foundational models and authentication (completed by T007)

## Parallel Execution Opportunities

- **Setup tasks** (T001-T003) can run in parallel with foundational tasks (T004-T007)
- **User Story 2, 3, and 5** can be developed in parallel after foundational tasks (T004-T007) are complete
- **Schema creation** (T004) can run in parallel with agent implementation (T005)
- **Route updates** (T006-T007) can run in parallel with endpoint implementations (T011, T021, T028, T045)

## Success Criteria Verification

Each user story includes tasks to verify the success criteria from the specification:

- SC-001: Chat endpoint responds with AI-generated content (verified in US1)
- SC-002: User and assistant messages are persisted in database (verified in US1)
- SC-003: AI can successfully invoke all 5 MCP tools through conversation (verified in US4)
- SC-004: Conversation history is loaded correctly for follow-up messages (verified in US1)
- SC-005: List conversations returns correct data for authenticated user (verified in US2)
- SC-006: Get conversation returns all messages in chronological order (verified in US3)
- SC-007: Delete conversation removes both conversation and messages (verified in US5)
- SC-008: JWT authentication is enforced on all endpoints (verified in US1, US2, US3, US5)
- SC-009: user_id/JWT mismatch returns 403 Forbidden (verified in US1, US2, US3, US5)