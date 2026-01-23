# Research: MCP Server with Task Tools

**Date**: 2026-01-23
**Feature**: Phase III Module 2 - MCP Server
**Spec**: [spec.md](./spec.md)

## Research Tasks

### 1. MCP Python SDK - Installation and Setup

**Decision**: Use official `mcp` package from Anthropic

**Installation**:
```bash
# Using uv (recommended)
uv add "mcp[cli]"

# Using pip
pip install "mcp[cli]"
```

**Current Version**: 1.25.0 (as of January 2026)
**Requirements**: Python 3.10+

**Rationale**: The official MCP SDK provides FastMCP, a high-level API for building MCP servers. It's maintained by Anthropic and is the recommended approach.

**Alternatives Considered**:
- `fastmcp` separate package - Now incorporated into official SDK
- Custom protocol implementation - Unnecessary, SDK handles all protocol details

---

### 2. MCP Server Creation Pattern

**Decision**: Use `FastMCP` class from `mcp.server.fastmcp`

**Pattern**:
```python
from mcp.server.fastmcp import FastMCP

# Initialize server with descriptive name
mcp = FastMCP("todo-task-tools")

# Define tools using decorator
@mcp.tool()
def add_task(user_id: str, title: str, description: str = None) -> str:
    """Create a new task for the user."""
    # Implementation
    return f"Task '{title}' created"

# Run server
def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
```

**Rationale**: FastMCP provides the simplest, most maintainable approach with decorator-based tool definitions and automatic schema generation from type hints.

---

### 3. Tool Definition Pattern

**Decision**: Use `@mcp.tool()` decorator with typed parameters and docstrings

**Requirements**:
- Function name becomes tool identifier
- Docstring becomes tool description (shown to LLM)
- Type hints generate JSON schema automatically
- Return type should be `str` for LLM consumption

**Pattern for Task Tools**:
```python
@mcp.tool()
async def add_task(user_id: str, title: str, description: str = "") -> str:
    """Create a new task for the user.

    Args:
        user_id: The user's unique identifier
        title: The task title (required)
        description: Optional task description
    """
    # Implementation using existing db.py
    return json.dumps({"task_id": task.id, "status": "created", "title": title})
```

**Rationale**: Docstrings with Args help the AI agent understand parameter purposes. JSON response format enables structured data handling.

---

### 4. Transport Selection

**Decision**: Use `stdio` transport for local development

**Options**:
| Transport | Use Case |
|-----------|----------|
| `stdio` | Local development, Claude Desktop integration |
| `streamable-http` | Production web deployments |
| `sse` | Web-based real-time deployments |

**Rationale**: stdio is the simplest for Phase III development and testing. Can upgrade to HTTP transport for production later.

**Critical Note**: Never use `print()` in stdio servers - it corrupts JSON-RPC protocol. Use `logging` module instead.

---

### 5. Async/Await for Database Operations

**Decision**: Use async tools for all database operations

**Pattern**:
```python
@mcp.tool()
async def list_tasks(user_id: str, status: str = "all") -> str:
    """List user's tasks filtered by status.

    Args:
        user_id: The user's unique identifier
        status: Filter - 'all', 'pending', or 'completed'
    """
    async with get_session() as session:
        # Query using existing SQLModel patterns
        statement = select(Task).where(Task.user_id == user_id)
        if status == "pending":
            statement = statement.where(Task.completed == False)
        elif status == "completed":
            statement = statement.where(Task.completed == True)

        result = await session.execute(statement)
        tasks = result.scalars().all()

        return json.dumps([
            {"id": str(t.id), "title": t.title, "completed": t.completed}
            for t in tasks
        ])
```

**Rationale**: Database operations benefit from non-blocking async execution. FastMCP supports both sync and async tools seamlessly.

---

### 6. Database Session Integration

**Decision**: Reuse existing `db.py` patterns from Phase II

**Pattern**:
```python
# In mcp_server.py
from db import get_session  # Reuse existing session factory
from models import Task     # Reuse existing Task model

@mcp.tool()
async def add_task(user_id: str, title: str, description: str = "") -> str:
    """Create a new task."""
    async with get_session() as session:
        task = Task(
            user_id=user_id,
            title=title,
            description=description if description else None
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return json.dumps({
            "task_id": str(task.id),
            "status": "created",
            "title": task.title
        })
```

**Rationale**: Reusing existing database infrastructure ensures consistency and avoids code duplication.

---

### 7. Error Handling Pattern

**Decision**: Return structured error responses, never raise exceptions to MCP client

**Pattern**:
```python
@mcp.tool()
async def complete_task(user_id: str, task_id: str) -> str:
    """Mark a task as completed."""
    try:
        async with get_session() as session:
            statement = select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id
            )
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                return json.dumps({
                    "error": True,
                    "message": "Task not found or access denied"
                })

            task.completed = True
            await session.commit()

            return json.dumps({
                "task_id": str(task.id),
                "status": "completed",
                "title": task.title
            })
    except Exception as e:
        logging.error(f"Error completing task: {e}")
        return json.dumps({
            "error": True,
            "message": "Failed to complete task"
        })
```

**Rationale**: Structured error responses allow the AI agent to handle errors gracefully and provide helpful feedback to users.

---

## Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Package | `mcp[cli]` | Official Anthropic SDK |
| Server API | `FastMCP` | High-level, decorator-based |
| Transport | `stdio` | Simple for development |
| Database | Reuse `db.py` | Consistency with Phase II |
| Async | Required for DB ops | Non-blocking I/O |
| Errors | JSON responses | Agent-friendly handling |
