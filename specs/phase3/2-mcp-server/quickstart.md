# Quickstart: MCP Server with Task Tools

**Date**: 2026-01-23
**Feature**: Phase III Module 2 - MCP Server

## Prerequisites

- Phase III Module 1 (Chat Database) completed
- Python 3.12+ with uv
- Existing `phase-3/backend/` with models.py and db.py

## Installation

```bash
cd phase-3/backend

# Add MCP SDK
uv add "mcp[cli]"
```

## Implementation

### 1. Create mcp_server.py

```python
"""
MCP Server exposing task management tools for AI agents.

Run with: uv run python mcp_server.py
"""

import json
import logging
from datetime import datetime

from mcp.server.fastmcp import FastMCP
from sqlmodel import select

from db import get_session
from models import Task

# Configure logging (NEVER use print in stdio servers)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("todo-task-tools")


@mcp.tool()
async def add_task(user_id: str, title: str, description: str = "") -> str:
    """Create a new task for the user.

    Args:
        user_id: The user's unique identifier
        title: The task title (required)
        description: Optional task description
    """
    # Validate inputs
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})
    if not title or not title.strip():
        return json.dumps({"error": True, "message": "Title is required"})
    if len(title) > 200:
        return json.dumps({"error": True, "message": "Title exceeds 200 character limit"})
    if description and len(description) > 1000:
        return json.dumps({"error": True, "message": "Description exceeds 1000 character limit"})

    try:
        async with get_session() as session:
            task = Task(
                user_id=user_id.strip(),
                title=title.strip(),
                description=description.strip() if description else None
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)

            return json.dumps({
                "task_id": task.id,
                "status": "created",
                "title": task.title
            })
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return json.dumps({"error": True, "message": "Failed to create task"})


@mcp.tool()
async def list_tasks(user_id: str, status: str = "all") -> str:
    """List user's tasks filtered by status.

    Args:
        user_id: The user's unique identifier
        status: Filter - 'all', 'pending', or 'completed'
    """
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})
    if status not in ("all", "pending", "completed"):
        return json.dumps({"error": True, "message": "Status must be 'all', 'pending', or 'completed'"})

    try:
        async with get_session() as session:
            statement = select(Task).where(Task.user_id == user_id.strip())

            if status == "pending":
                statement = statement.where(Task.completed == False)
            elif status == "completed":
                statement = statement.where(Task.completed == True)

            result = await session.execute(statement)
            tasks = result.scalars().all()

            return json.dumps({
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description,
                        "completed": t.completed,
                        "created_at": t.created_at.isoformat()
                    }
                    for t in tasks
                ],
                "count": len(tasks)
            })
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        return json.dumps({"error": True, "message": "Failed to list tasks"})


@mcp.tool()
async def complete_task(user_id: str, task_id: int) -> str:
    """Mark a task as completed.

    Args:
        user_id: The user's unique identifier
        task_id: The task ID to mark as completed
    """
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})

    try:
        async with get_session() as session:
            statement = select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id.strip()
            )
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                return json.dumps({"error": True, "message": "Task not found or access denied"})

            task.completed = True
            task.updated_at = datetime.utcnow()
            await session.commit()

            return json.dumps({
                "task_id": task.id,
                "status": "completed",
                "title": task.title
            })
    except Exception as e:
        logger.error(f"Error completing task: {e}")
        return json.dumps({"error": True, "message": "Failed to complete task"})


@mcp.tool()
async def delete_task(user_id: str, task_id: int) -> str:
    """Delete a task from the user's list.

    Args:
        user_id: The user's unique identifier
        task_id: The task ID to delete
    """
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})

    try:
        async with get_session() as session:
            statement = select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id.strip()
            )
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                return json.dumps({"error": True, "message": "Task not found or access denied"})

            await session.delete(task)
            await session.commit()

            return json.dumps({
                "task_id": task_id,
                "status": "deleted"
            })
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        return json.dumps({"error": True, "message": "Failed to delete task"})


@mcp.tool()
async def update_task(user_id: str, task_id: int, title: str = "", description: str = "") -> str:
    """Update a task's title or description.

    Args:
        user_id: The user's unique identifier
        task_id: The task ID to update
        title: New task title (optional)
        description: New task description (optional)
    """
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})
    if not title and not description:
        return json.dumps({"error": True, "message": "No updates provided (title or description required)"})
    if title and len(title) > 200:
        return json.dumps({"error": True, "message": "Title exceeds 200 character limit"})
    if description and len(description) > 1000:
        return json.dumps({"error": True, "message": "Description exceeds 1000 character limit"})

    try:
        async with get_session() as session:
            statement = select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id.strip()
            )
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                return json.dumps({"error": True, "message": "Task not found or access denied"})

            if title:
                task.title = title.strip()
            if description:
                task.description = description.strip()
            task.updated_at = datetime.utcnow()

            await session.commit()

            return json.dumps({
                "task_id": task.id,
                "status": "updated",
                "title": task.title
            })
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        return json.dumps({"error": True, "message": "Failed to update task"})


def main():
    """Run the MCP server with stdio transport."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
```

## Running the Server

```bash
# From phase-3/backend directory
uv run python mcp_server.py
```

## Testing

### Manual Test via stdio

```bash
# Start server and send JSON-RPC messages
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | uv run python mcp_server.py
```

### Test with MCP Inspector (Optional)

```bash
# Install MCP CLI tools
uv add "mcp[cli]"

# Use inspector
mcp inspect
```

## Claude Desktop Integration (Optional)

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "todo-tasks": {
      "command": "uv",
      "args": ["run", "python", "/path/to/phase-3/backend/mcp_server.py"]
    }
  }
}
```

## Next Steps

After MCP server is working:
1. Phase III Module 3: Chat endpoint that uses MCP tools
2. Frontend ChatKit integration
