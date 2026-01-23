# Implementation Plan: MCP Server with Task Tools

**Branch**: `006-chat-database` | **Date**: 2026-01-23 | **Spec**: [spec.md](./spec.md)
**Module**: Phase III Module 2

## Summary

Create an MCP (Model Context Protocol) server that exposes task CRUD operations as tools for AI agents. The server reuses existing Task model and database infrastructure from Phase II, implementing 5 tools: add_task, list_tasks, complete_task, delete_task, and update_task.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: `mcp[cli]` (official Anthropic MCP SDK), FastMCP
**Storage**: Neon PostgreSQL via existing db.py (reuse Phase II infrastructure)
**Testing**: Manual verification via MCP inspector and stdio testing
**Target Platform**: Linux server (WSL compatible)
**Project Type**: Backend module (single new file)
**Performance Goals**: Tool responses under 1 second
**Constraints**: Must reuse existing Task model, user_id validation required
**Scale/Scope**: 5 MCP tools, single mcp_server.py file

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| XIV. MCP Architecture (NON-NEGOTIABLE) | ✅ PASS | Using official MCP SDK, tools are stateless |
| XVII. Agent Tool Safety (NON-NEGOTIABLE) | ✅ PASS | All tools validate user_id, ownership check before operations |
| IX. API-First Design | ✅ PASS | MCP tools provide API-like interface |
| X. Database Persistence | ✅ PASS | Reusing existing Neon PostgreSQL |
| XI. Multi-User Support | ✅ PASS | All operations scoped by user_id |
| III. Clean Code & Python Standards | ✅ PASS | Type hints, docstrings, async/await |
| V. Graceful Error Handling | ✅ PASS | Structured JSON error responses |

**All gates pass. Proceeding to implementation.**

## Project Structure

### Documentation (this feature)

```text
specs/phase3/2-mcp-server/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # MCP SDK research findings
├── data-model.md        # Tool schemas and validation rules
├── quickstart.md        # Implementation guide
├── contracts/
│   └── mcp-tools.json   # MCP tool definitions
└── checklists/
    └── requirements.md  # Spec quality checklist
```

### Source Code (repository root)

```text
phase-3/backend/
├── mcp_server.py        # NEW - MCP server with 5 task tools
├── models.py            # EXISTING - Task model (reused)
├── db.py                # EXISTING - Database session (reused)
└── pyproject.toml       # UPDATE - Add mcp[cli] dependency
```

**Structure Decision**: Single new file (`mcp_server.py`) in existing backend directory. No new directories needed. Reuses existing database infrastructure.

## Implementation Overview

### File: mcp_server.py

**Purpose**: MCP server exposing task management tools

**Key Components**:
1. FastMCP server initialization
2. 5 async tool functions with `@mcp.tool()` decorator
3. Database session integration via existing `get_session()`
4. JSON response formatting for all outputs
5. Comprehensive input validation

### Tool Implementation Summary

| Tool | Function | DB Operation |
|------|----------|--------------|
| add_task | Create task | INSERT |
| list_tasks | Query tasks | SELECT with filters |
| complete_task | Mark done | UPDATE completed=True |
| delete_task | Remove task | DELETE |
| update_task | Modify fields | UPDATE title/description |

### Security Implementation

All tools follow this pattern:
1. Validate user_id is provided and non-empty
2. Query task with both task_id AND user_id
3. Return "not found" for missing OR unauthorized (no info leakage)
4. Log errors server-side, return generic messages to client

## Dependencies

### New Dependency

```toml
# Add to pyproject.toml
[project.dependencies]
mcp = { version = ">=1.0.0", extras = ["cli"] }
```

### Existing Dependencies (Reused)

- SQLModel (database ORM)
- asyncpg (async PostgreSQL driver)
- Existing Task model from models.py
- Existing get_session() from db.py

## Testing Strategy

### Manual Testing

1. **Tool Discovery**: Verify all 5 tools appear in MCP tool listing
2. **Happy Path**: Test each tool with valid inputs
3. **Validation**: Test each tool with invalid inputs
4. **Authorization**: Test cross-user access attempts

### Test Commands

```bash
# List tools
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | uv run python mcp_server.py

# Call add_task
echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"add_task","arguments":{"user_id":"test-user","title":"Buy groceries"}},"id":2}' | uv run python mcp_server.py
```

## Complexity Tracking

> No violations identified. Implementation is minimal and follows existing patterns.

| Aspect | Approach | Justification |
|--------|----------|---------------|
| Single file | mcp_server.py | Simple module, all tools related |
| Reuse db.py | Import get_session | Avoid duplication |
| JSON responses | String returns | MCP convention for tool outputs |

## Related Documents

- [spec.md](./spec.md) - Feature specification
- [research.md](./research.md) - MCP SDK research
- [data-model.md](./data-model.md) - Tool schemas
- [quickstart.md](./quickstart.md) - Implementation guide
- [contracts/mcp-tools.json](./contracts/mcp-tools.json) - Tool definitions

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement mcp_server.py
3. Test with MCP inspector
4. Proceed to Phase III Module 3 (Chat Endpoint)
