"""
MCP Server exposing task management tools for AI agents.

This module implements an MCP (Model Context Protocol) server that provides
5 tools for managing tasks: add_task, list_tasks, complete_task, delete_task,
and update_task. All tools validate user_id and operate on the existing
Task model from Phase II.

Usage:
    uv run python mcp_server.py

Transport:
    stdio (JSON-RPC over stdin/stdout)

Note:
    NEVER use print() in this module - it corrupts the JSON-RPC protocol.
    Use logging module for all debug output.
"""

import json
import logging
from datetime import datetime
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from mcp.server.fastmcp import FastMCP
from sqlmodel import select

from db import _get_session_maker
from models import Task

# Configure logging (writes to stderr, not stdout)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("todo-task-tools")


@asynccontextmanager
async def get_session() -> AsyncGenerator:
    """
    Async context manager for database sessions.

    Handles session lifecycle: create, commit on success, rollback on error, close.
    """
    session_maker = _get_session_maker()
    session = session_maker()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.error(f"Session error, rolled back: {e}")
        raise
    finally:
        await session.close()


# =============================================================================
# User Story 1: add_task Tool (P1)
# =============================================================================

@mcp.tool()
async def add_task(user_id: str, title: str, description: str = "") -> str:
    """Create a new task for the user.

    Use this tool when the user wants to add something to their todo list.

    Args:
        user_id: The user's unique identifier
        title: The task title (required, max 200 characters)
        description: Optional task description (max 1000 characters)

    Returns:
        JSON string with task_id, status, and title on success,
        or error message on failure.
    """
    # Validate user_id
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})

    # Validate title
    if not title or not title.strip():
        return json.dumps({"error": True, "message": "Title is required"})
    if len(title) > 200:
        return json.dumps({"error": True, "message": "Title exceeds 200 character limit"})

    # Validate description
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

            logger.info(f"Created task {task.id} for user {user_id}")

            return json.dumps({
                "task_id": task.id,
                "status": "created",
                "title": task.title
            })
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return json.dumps({"error": True, "message": "Failed to create task"})


# =============================================================================
# User Story 2: list_tasks Tool (P1)
# =============================================================================

@mcp.tool()
async def list_tasks(user_id: str, status: str = "all") -> str:
    """List user's tasks filtered by status.

    Use this tool when the user wants to see their tasks, todo list,
    or asks what they have to do.

    Args:
        user_id: The user's unique identifier
        status: Filter - 'all' (default), 'pending' (incomplete), or 'completed'

    Returns:
        JSON string with tasks array and count on success,
        or error message on failure.
    """
    # Validate user_id
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})

    # Validate status
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

            logger.info(f"Listed {len(tasks)} tasks for user {user_id} (status={status})")

            return json.dumps({
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description,
                        "completed": t.completed,
                        "created_at": t.created_at.isoformat() if t.created_at else None
                    }
                    for t in tasks
                ],
                "count": len(tasks)
            })
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        return json.dumps({"error": True, "message": "Failed to list tasks"})


# =============================================================================
# User Story 3: complete_task Tool (P1)
# =============================================================================

@mcp.tool()
async def complete_task(user_id: str, task_id: int) -> str:
    """Mark a task as completed.

    Use this tool when the user says they finished a task, completed something,
    or wants to mark it done.

    Args:
        user_id: The user's unique identifier
        task_id: The task ID to mark as completed

    Returns:
        JSON string with task_id, status, and title on success,
        or error message on failure.
    """
    # Validate user_id
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})

    try:
        async with get_session() as session:
            # Query task by id AND user_id (ownership check)
            statement = select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id.strip()
            )
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            # Return error if not found (no info leakage about other users' tasks)
            if not task:
                return json.dumps({"error": True, "message": "Task not found or access denied"})

            # Update task
            task.completed = True
            task.updated_at = datetime.utcnow()
            await session.commit()

            logger.info(f"Completed task {task_id} for user {user_id}")

            return json.dumps({
                "task_id": task.id,
                "status": "completed",
                "title": task.title
            })
    except Exception as e:
        logger.error(f"Error completing task: {e}")
        return json.dumps({"error": True, "message": "Failed to complete task"})


# =============================================================================
# User Story 4: delete_task Tool (P2)
# =============================================================================

@mcp.tool()
async def delete_task(user_id: str, task_id: int) -> str:
    """Delete a task from the user's list.

    Use this tool when the user wants to remove a task entirely.

    Args:
        user_id: The user's unique identifier
        task_id: The task ID to delete

    Returns:
        JSON string with task_id and status on success,
        or error message on failure.
    """
    # Validate user_id
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})

    try:
        async with get_session() as session:
            # Query task by id AND user_id (ownership check)
            statement = select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id.strip()
            )
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            # Return error if not found
            if not task:
                return json.dumps({"error": True, "message": "Task not found or access denied"})

            # Delete task
            await session.delete(task)
            await session.commit()

            logger.info(f"Deleted task {task_id} for user {user_id}")

            return json.dumps({
                "task_id": task_id,
                "status": "deleted"
            })
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        return json.dumps({"error": True, "message": "Failed to delete task"})


# =============================================================================
# User Story 5: update_task Tool (P2)
# =============================================================================

@mcp.tool()
async def update_task(user_id: str, task_id: int, title: str = "", description: str = "") -> str:
    """Update a task's title or description.

    Use this tool when the user wants to change, edit, or modify an existing task.

    Args:
        user_id: The user's unique identifier
        task_id: The task ID to update
        title: New task title (optional, max 200 characters)
        description: New task description (optional, max 1000 characters)

    Returns:
        JSON string with task_id, status, and title on success,
        or error message on failure.
    """
    # Validate user_id
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})

    # Validate at least one update provided
    if not title and not description:
        return json.dumps({"error": True, "message": "No updates provided (title or description required)"})

    # Validate title if provided
    if title and len(title) > 200:
        return json.dumps({"error": True, "message": "Title exceeds 200 character limit"})

    # Validate description if provided
    if description and len(description) > 1000:
        return json.dumps({"error": True, "message": "Description exceeds 1000 character limit"})

    try:
        async with get_session() as session:
            # Query task by id AND user_id (ownership check)
            statement = select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id.strip()
            )
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            # Return error if not found
            if not task:
                return json.dumps({"error": True, "message": "Task not found or access denied"})

            # Update fields
            if title:
                task.title = title.strip()
            if description:
                task.description = description.strip()
            task.updated_at = datetime.utcnow()

            await session.commit()

            logger.info(f"Updated task {task_id} for user {user_id}")

            return json.dumps({
                "task_id": task.id,
                "status": "updated",
                "title": task.title
            })
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        return json.dumps({"error": True, "message": "Failed to update task"})


# =============================================================================
# Main Entry Point
# =============================================================================

def main():
    """Run the MCP server with stdio transport."""
    logger.info("Starting MCP server: todo-task-tools")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
