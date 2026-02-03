"""
MCP Server exposing task management tools for AI agents.

Phase V: Extended with priority, due_date, tags support.

Usage:
    uv run python mcp_server.py

Transport:
    stdio (JSON-RPC over stdin/stdout)

Note:
    NEVER use print() in this module - it corrupts the JSON-RPC protocol.
"""

import json
import logging
from datetime import datetime
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from mcp.server.fastmcp import FastMCP
from sqlmodel import select

from db import _get_session_maker
from models import Task, Tag, TaskTag, Notification

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

mcp = FastMCP("todo-task-tools")


@asynccontextmanager
async def get_session() -> AsyncGenerator:
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


def _task_to_dict(task: Task, tags: list[Tag] | None = None) -> dict:
    """Convert a task to a dictionary for JSON serialization."""
    d = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "priority": task.priority or "medium",
        "due_date": task.due_date if task.due_date else None,
        "recurrence_rule": task.recurrence_rule,
        "created_at": task.created_at.isoformat() if task.created_at else None,
    }
    if tags is not None:
        d["tags"] = [{"id": t.id, "name": t.name} for t in tags]
    return d


async def _get_tags_for_task(session, task_id: int) -> list[Tag]:
    stmt = select(Tag).join(TaskTag, TaskTag.tag_id == Tag.id).where(TaskTag.task_id == task_id)
    result = await session.execute(stmt)
    return list(result.scalars().all())


@mcp.tool()
async def add_task(
    user_id: str,
    title: str,
    description: str = "",
    priority: str = "medium",
    due_date: str = "",
    tag_names: str = "",
) -> str:
    """Create a new task for the user.

    Args:
        user_id: The user's unique identifier
        title: The task title (required, max 200 characters)
        description: Optional task description (max 1000 characters)
        priority: Task priority: low, medium, high, or urgent (default: medium)
        due_date: Optional due date in YYYY-MM-DD format
        tag_names: Optional comma-separated tag names to assign

    Returns:
        JSON string with task details on success, or error message on failure.
    """
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})
    if not title or not title.strip():
        return json.dumps({"error": True, "message": "Title is required"})
    if len(title) > 200:
        return json.dumps({"error": True, "message": "Title exceeds 200 character limit"})
    if description and len(description) > 1000:
        return json.dumps({"error": True, "message": "Description exceeds 1000 character limit"})
    if priority not in ("low", "medium", "high", "urgent"):
        return json.dumps({"error": True, "message": "Priority must be low, medium, high, or urgent"})

    try:
        async with get_session() as session:
            task = Task(
                user_id=user_id.strip(),
                title=title.strip(),
                description=description.strip() if description else None,
                priority=priority,
                due_date=due_date.strip() if due_date else None,
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)

            # Handle tags
            tags = []
            if tag_names:
                for name in [n.strip() for n in tag_names.split(",") if n.strip()]:
                    stmt = select(Tag).where(Tag.user_id == user_id.strip(), Tag.name == name)
                    result = await session.execute(stmt)
                    tag = result.scalar_one_or_none()
                    if not tag:
                        tag = Tag(user_id=user_id.strip(), name=name)
                        session.add(tag)
                        await session.commit()
                        await session.refresh(tag)
                    task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
                    session.add(task_tag)
                    tags.append(tag)
                await session.commit()

            logger.info(f"Created task {task.id} for user {user_id}")
            return json.dumps({"status": "created", "task": _task_to_dict(task, tags)})
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return json.dumps({"error": True, "message": "Failed to create task"})


@mcp.tool()
async def list_tasks(
    user_id: str,
    status: str = "all",
    priority: str = "",
    search: str = "",
) -> str:
    """List user's tasks filtered by status, priority, or search term.

    Args:
        user_id: The user's unique identifier
        status: Filter - 'all' (default), 'pending', or 'completed'
        priority: Optional filter by priority: low, medium, high, urgent
        search: Optional search term to match in title or description

    Returns:
        JSON string with tasks array and count.
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
            if priority and priority in ("low", "medium", "high", "urgent"):
                statement = statement.where(Task.priority == priority)
            if search:
                statement = statement.where(Task.title.ilike(f"%{search}%"))

            result = await session.execute(statement)
            tasks = result.scalars().all()

            task_dicts = []
            for t in tasks:
                tags = await _get_tags_for_task(session, t.id)
                task_dicts.append(_task_to_dict(t, tags))

            logger.info(f"Listed {len(tasks)} tasks for user {user_id}")
            return json.dumps({"tasks": task_dicts, "count": len(tasks)})
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        return json.dumps({"error": True, "message": "Failed to list tasks"})


@mcp.tool()
async def complete_task(user_id: str, task_id: int) -> str:
    """Mark a task as completed.

    Args:
        user_id: The user's unique identifier
        task_id: The task ID to mark as completed

    Returns:
        JSON string with task details on success.
    """
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})

    try:
        async with get_session() as session:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id.strip())
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                return json.dumps({"error": True, "message": "Task not found or access denied"})

            task.completed = True
            task.updated_at = datetime.utcnow()
            await session.commit()

            tags = await _get_tags_for_task(session, task.id)
            logger.info(f"Completed task {task_id} for user {user_id}")
            return json.dumps({"status": "completed", "task": _task_to_dict(task, tags)})
    except Exception as e:
        logger.error(f"Error completing task: {e}")
        return json.dumps({"error": True, "message": "Failed to complete task"})


@mcp.tool()
async def delete_task(user_id: str, task_id: int) -> str:
    """Delete a task from the user's list.

    Args:
        user_id: The user's unique identifier
        task_id: The task ID to delete

    Returns:
        JSON string with task_id and status on success.
    """
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})

    try:
        async with get_session() as session:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id.strip())
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                return json.dumps({"error": True, "message": "Task not found or access denied"})

            await session.delete(task)
            await session.commit()

            logger.info(f"Deleted task {task_id} for user {user_id}")
            return json.dumps({"task_id": task_id, "status": "deleted"})
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        return json.dumps({"error": True, "message": "Failed to delete task"})


@mcp.tool()
async def update_task(
    user_id: str,
    task_id: int,
    title: str = "",
    description: str = "",
    priority: str = "",
    due_date: str = "",
) -> str:
    """Update a task's fields.

    Args:
        user_id: The user's unique identifier
        task_id: The task ID to update
        title: New task title (optional)
        description: New task description (optional)
        priority: New priority: low, medium, high, urgent (optional)
        due_date: New due date YYYY-MM-DD (optional)

    Returns:
        JSON string with updated task on success.
    """
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})
    if not title and not description and not priority and not due_date:
        return json.dumps({"error": True, "message": "No updates provided"})
    if title and len(title) > 200:
        return json.dumps({"error": True, "message": "Title exceeds 200 character limit"})
    if description and len(description) > 1000:
        return json.dumps({"error": True, "message": "Description exceeds 1000 character limit"})
    if priority and priority not in ("low", "medium", "high", "urgent"):
        return json.dumps({"error": True, "message": "Priority must be low, medium, high, or urgent"})

    try:
        async with get_session() as session:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id.strip())
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                return json.dumps({"error": True, "message": "Task not found or access denied"})

            if title:
                task.title = title.strip()
            if description:
                task.description = description.strip()
            if priority:
                task.priority = priority
            if due_date:
                task.due_date = due_date.strip()
            task.updated_at = datetime.utcnow()

            await session.commit()

            tags = await _get_tags_for_task(session, task.id)
            logger.info(f"Updated task {task_id} for user {user_id}")
            return json.dumps({"status": "updated", "task": _task_to_dict(task, tags)})
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        return json.dumps({"error": True, "message": "Failed to update task"})


@mcp.tool()
async def list_tags(user_id: str) -> str:
    """List all tags for the user.

    Args:
        user_id: The user's unique identifier

    Returns:
        JSON string with tags array.
    """
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})

    try:
        async with get_session() as session:
            stmt = select(Tag).where(Tag.user_id == user_id.strip())
            result = await session.execute(stmt)
            tags = result.scalars().all()
            return json.dumps({
                "tags": [{"id": t.id, "name": t.name} for t in tags],
                "count": len(tags),
            })
    except Exception as e:
        logger.error(f"Error listing tags: {e}")
        return json.dumps({"error": True, "message": "Failed to list tags"})


@mcp.tool()
async def list_notifications(user_id: str) -> str:
    """List recent notifications for the user.

    Args:
        user_id: The user's unique identifier

    Returns:
        JSON string with notifications array.
    """
    if not user_id or not user_id.strip():
        return json.dumps({"error": True, "message": "User ID is required"})

    try:
        async with get_session() as session:
            stmt = (
                select(Notification)
                .where(Notification.user_id == user_id.strip())
                .order_by(Notification.created_at.desc())
                .limit(20)
            )
            result = await session.execute(stmt)
            notifs = result.scalars().all()
            return json.dumps({
                "notifications": [
                    {
                        "id": n.id,
                        "task_id": n.task_id,
                        "message": n.message,
                        "read": n.read,
                        "created_at": n.created_at.isoformat() if n.created_at else None,
                    }
                    for n in notifs
                ],
                "count": len(notifs),
            })
    except Exception as e:
        logger.error(f"Error listing notifications: {e}")
        return json.dumps({"error": True, "message": "Failed to list notifications"})


def main():
    """Run the MCP server with stdio transport."""
    logger.info("Starting MCP server: todo-task-tools")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
