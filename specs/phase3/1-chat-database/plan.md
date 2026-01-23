# Implementation Plan: Chat Database Extension

**Branch**: `006-chat-database` | **Date**: 2026-01-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/phase3/chat-database/spec.md`

## Summary

Extend the existing Phase II database schema to support AI chatbot conversation history. Add two new SQLModel classes (Conversation, Message) with proper foreign key relationships, cascade delete behavior, and indexes for efficient querying. Follows existing patterns from Task and User models.

## Technical Context

**Language/Version**: Python 3.12+ (matching Phase II backend)
**Primary Dependencies**: SQLModel 0.0.14+, FastAPI 0.100+, asyncpg (existing stack)
**Storage**: Neon PostgreSQL (existing, extend schema)
**Testing**: Manual testing via init_db.py and test scripts
**Target Platform**: Linux server / Vercel Serverless (existing deployment)
**Project Type**: Web application - backend extension
**Performance Goals**: <100ms query response for up to 1000 conversations/messages per user
**Constraints**: Must not modify existing users/tasks tables, cascade delete required
**Scale/Scope**: Multi-user application, expected <10k messages per conversation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. AI-Native Development | ✅ PASS | All code via Claude Code + Spec-Kit Plus |
| II. Specification-First | ✅ PASS | spec.md completed before implementation |
| III. Clean Code & Python Standards | ✅ WILL VERIFY | Type hints, docstrings, SRP required |
| VIII. Monorepo Structure | ✅ PASS | Extends existing phase-2/backend/ |
| IX. API-First Design | ✅ PASS | Database layer supports future API |
| X. Database Persistence | ✅ PASS | PostgreSQL with SQLModel |
| XI. Multi-User Support | ✅ PASS | user_id FK on conversations |
| XII. Authentication Required | ✅ PASS | Reuses existing JWT auth |
| XVI. Conversation Persistence | ✅ PASS | This feature implements it |
| XVII. Agent Tool Safety | ✅ PASS | user_id validation built into model |

**Gate Result**: PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/phase3/chat-database/
├── spec.md              # Feature specification (completed)
├── checklist.md         # Spec validation checklist (completed)
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
phase-2/backend/
├── models.py            # MODIFY: Add Conversation and Message classes
├── db.py                # NO CHANGE: Existing connection management
├── init_db.py           # NO CHANGE: Uses SQLModel.metadata.create_all
├── test_db.py           # MODIFY: Add conversation/message tests
├── schemas.py           # FUTURE: Add request/response schemas (Module 2)
└── routes/
    └── conversations.py # FUTURE: Add conversation routes (Module 2)
```

**Structure Decision**: Minimal change approach - add only new model classes to existing models.py file. No new directories required for this module.

## Complexity Tracking

> No violations identified. Implementation follows existing patterns.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Model Location | Add to existing models.py | Keeps all SQLModel classes together |
| FK Type | String (UUID) for user_id | Matches existing User.id type |
| Message Role | String with validation | Flexible, matches OpenAI message format |
