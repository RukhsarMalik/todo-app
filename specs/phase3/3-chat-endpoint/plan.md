# Implementation Plan: Chat Endpoint with OpenAI Agent

**Branch**: `006-chat-database` | **Date**: 2026-01-23 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/phase3/3-chat-endpoint/spec.md`

## Summary

Implement a chat endpoint (`POST /api/{user_id}/chat`) that integrates OpenAI Agents SDK with MCP server tools for natural language task management. The endpoint stores conversation history using existing Conversation and Message models, enabling stateless server design with full conversation persistence.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: FastAPI, OpenAI Agents SDK (`openai-agents`), MCP SDK (`mcp[cli]`)
**Storage**: Neon PostgreSQL via SQLModel (existing Conversation/Message models from Module 1)
**Testing**: Manual verification (consistent with Module 2 approach)
**Target Platform**: Linux server (deployed backend)
**Project Type**: Web application (monorepo with frontend/backend)
**Performance Goals**: Chat response time < 10 seconds
**Constraints**: Stateless design (no server-side session storage), JWT authentication required
**Scale/Scope**: Single user conversations, up to 100 messages per conversation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| XIII. Natural Language Interface | ✅ PASS | Chat endpoint enables conversational task management |
| XIV. MCP Architecture | ✅ PASS | Integrates with MCP server tools from Module 2 |
| XV. Stateless Chat Design | ✅ PASS | Conversation history loaded from database each request |
| XVI. Conversation Persistence | ✅ PASS | Uses Conversation/Message models from Module 1 |
| XVII. Agent Tool Safety | ✅ PASS | user_id passed to all MCP tools for ownership validation |
| IX. API-First Design | ✅ PASS | RESTful endpoints with JSON request/response |
| XII. Authentication Required | ✅ PASS | JWT authentication reused from Phase II |

**All gates passed. Proceeding with Phase 0 research.**

## Project Structure

### Documentation (this feature)

```text
specs/phase3/3-chat-endpoint/
├── plan.md              # This file
├── research.md          # Phase 0 output - OpenAI Agents SDK research
├── data-model.md        # Phase 1 output - Chat schemas
├── quickstart.md        # Phase 1 output - Implementation example
├── contracts/           # Phase 1 output - API contracts
│   └── chat-api.json    # OpenAPI schema for chat endpoints
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
phase-3/backend/
├── routes/
│   ├── __init__.py      # MODIFY - add chat router
│   └── chat.py          # NEW - chat endpoints
├── schemas.py           # MODIFY - add chat request/response schemas
├── agent.py             # NEW - OpenAI Agent + MCP integration
├── mcp_server.py        # EXISTING - MCP tools from Module 2
├── models.py            # EXISTING - Conversation, Message from Module 1
├── db.py                # EXISTING - database session
└── auth/
    └── middleware.py    # EXISTING - JWT verification
```

**Structure Decision**: Extends existing backend structure with new `routes/chat.py` for chat endpoints and `agent.py` for OpenAI Agent orchestration. No new directories needed.

## Complexity Tracking

> **No violations detected. All implementation follows existing patterns.**

| Aspect | Approach | Rationale |
|--------|----------|-----------|
| OpenAI Agent | OpenAI Agents SDK | Official SDK, built-in tool calling |
| MCP Integration | Subprocess stdio | MCP server runs as separate process |
| Session Management | Load from DB | Stateless design per constitution |
| Authentication | Reuse Phase II | Consistency, no new auth code |
