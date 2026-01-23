"""
Task CRUD endpoints with JWT authentication.

This module provides RESTful endpoints for task management:
- GET /api/{user_id}/tasks - List all tasks for a user
- GET /api/{user_id}/tasks/{task_id} - Get a specific task
- POST /api/{user_id}/tasks - Create a new task
- PUT /api/{user_id}/tasks/{task_id} - Update a task
- DELETE /api/{user_id}/tasks/{task_id} - Delete a task
- PATCH /api/{user_id}/tasks/{task_id}/complete - Toggle completion

All endpoints require JWT authentication and validate that the
token's user_id matches the URL user_id parameter.
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from db import get_session
from models import Task
from schemas import (
    TaskCreate,
    TaskUpdate,
    TaskToggle,
    TaskResponse,
    StatusFilter,
    SortField,
    SortOrder,
)
from auth.middleware import get_current_user

router = APIRouter(tags=["tasks"])


# ============================================================================
# Helper Functions
# ============================================================================

def verify_user_access(current_user: dict, user_id: str) -> None:
    """
    Verify that the authenticated user can access the requested user's resources.

    Args:
        current_user: The authenticated user from JWT token.
        user_id: The user_id from the URL path.

    Raises:
        HTTPException: 403 if user_id doesn't match the authenticated user.
    """
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )


async def get_task_or_404(
    session: AsyncSession,
    task_id: int,
    user_id: str
) -> Task:
    """
    Get a task by ID, verifying ownership.

    Returns 404 if task doesn't exist OR belongs to another user
    (no information leak about task existence).

    Args:
        session: Database session.
        task_id: Task ID to retrieve.
        user_id: Expected owner user ID.

    Returns:
        Task: The task if found and owned by user.

    Raises:
        HTTPException: 404 if task not found or not owned.
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


# ============================================================================
# List Tasks (US2)
# ============================================================================

@router.get(
    "/{user_id}/tasks",
    response_model=List[TaskResponse],
    summary="List Tasks",
    description="Get all tasks for a specific user with optional filtering and sorting. Requires JWT authentication."
)
async def list_tasks(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    status_filter: StatusFilter = StatusFilter.all,
    sort: SortField = SortField.created,
    order: SortOrder = SortOrder.desc,
    session: AsyncSession = Depends(get_session)
) -> List[Task]:
    """
    List all tasks for a user with filtering and sorting.

    Requires JWT authentication. The token's user_id must match
    the URL user_id parameter.

    Args:
        user_id: User identifier from URL path.
        current_user: Authenticated user from JWT token.
        status_filter: Filter by completion status (all/pending/completed).
        sort: Sort field (created/title).
        order: Sort order (asc/desc).
        session: Database session (injected).

    Returns:
        List[Task]: List of tasks matching the criteria.

    Raises:
        HTTPException: 401 if not authenticated.
        HTTPException: 403 if user_id doesn't match token.
    """
    # Verify user can access this resource
    verify_user_access(current_user, user_id)

    # Build base query filtered by user_id
    statement = select(Task).where(Task.user_id == user_id)

    # Apply status filter
    if status_filter == StatusFilter.pending:
        statement = statement.where(Task.completed == False)
    elif status_filter == StatusFilter.completed:
        statement = statement.where(Task.completed == True)

    # Apply sorting
    if sort == SortField.created:
        sort_column = Task.created_at
    else:
        sort_column = Task.title

    if order == SortOrder.desc:
        statement = statement.order_by(sort_column.desc())
    else:
        statement = statement.order_by(sort_column.asc())

    result = await session.execute(statement)
    return result.scalars().all()


# ============================================================================
# Get Single Task (US3)
# ============================================================================

@router.get(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get Task",
    description="Get a specific task by ID. Requires JWT authentication."
)
async def get_task(
    user_id: str,
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Task:
    """
    Get a specific task by ID.

    Requires JWT authentication. The token's user_id must match
    the URL user_id parameter.

    Args:
        user_id: User identifier from URL path.
        task_id: Task ID to retrieve.
        current_user: Authenticated user from JWT token.
        session: Database session (injected).

    Returns:
        Task: The requested task.

    Raises:
        HTTPException: 401 if not authenticated.
        HTTPException: 403 if user_id doesn't match token.
        HTTPException: 404 if task not found or not owned by user.
    """
    verify_user_access(current_user, user_id)
    return await get_task_or_404(session, task_id, user_id)


# ============================================================================
# Create Task (US4)
# ============================================================================

@router.post(
    "/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Task",
    description="Create a new task for the specified user. Requires JWT authentication."
)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Task:
    """
    Create a new task for a user.

    Requires JWT authentication. The token's user_id must match
    the URL user_id parameter.

    Args:
        user_id: User identifier from URL path.
        task_data: Task creation data (validated by Pydantic).
        current_user: Authenticated user from JWT token.
        session: Database session (injected).

    Returns:
        Task: The created task with generated ID and timestamps.

    Raises:
        HTTPException: 401 if not authenticated.
        HTTPException: 403 if user_id doesn't match token.
    """
    verify_user_access(current_user, user_id)

    # Create task with user_id from URL and auto timestamps
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


# ============================================================================
# Update Task (US5)
# ============================================================================

@router.put(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update Task",
    description="Update a task's title and/or description. Requires JWT authentication."
)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Task:
    """
    Update an existing task.

    Requires JWT authentication. The token's user_id must match
    the URL user_id parameter.

    Only updates fields that are provided (partial update).
    Always refreshes updated_at timestamp.

    Args:
        user_id: User identifier from URL path.
        task_id: Task ID to update.
        task_data: Update data (validated by Pydantic).
        current_user: Authenticated user from JWT token.
        session: Database session (injected).

    Returns:
        Task: The updated task.

    Raises:
        HTTPException: 401 if not authenticated.
        HTTPException: 403 if user_id doesn't match token.
        HTTPException: 404 if task not found or not owned by user.
    """
    verify_user_access(current_user, user_id)
    task = await get_task_or_404(session, task_id, user_id)

    # Update only provided fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description

    # Always update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


# ============================================================================
# Delete Task (US6)
# ============================================================================

@router.delete(
    "/{user_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Task",
    description="Permanently delete a task. Requires JWT authentication."
)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> None:
    """
    Delete a task permanently.

    Requires JWT authentication. The token's user_id must match
    the URL user_id parameter.

    Args:
        user_id: User identifier from URL path.
        task_id: Task ID to delete.
        current_user: Authenticated user from JWT token.
        session: Database session (injected).

    Raises:
        HTTPException: 401 if not authenticated.
        HTTPException: 403 if user_id doesn't match token.
        HTTPException: 404 if task not found or not owned by user.
    """
    verify_user_access(current_user, user_id)
    task = await get_task_or_404(session, task_id, user_id)

    await session.delete(task)
    await session.commit()


# ============================================================================
# Toggle Completion (US7)
# ============================================================================

@router.patch(
    "/{user_id}/tasks/{task_id}/complete",
    response_model=TaskResponse,
    summary="Toggle Task Completion",
    description="Update task completion status. Requires JWT authentication."
)
async def toggle_task_complete(
    user_id: str,
    task_id: int,
    toggle_data: TaskToggle,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Task:
    """
    Toggle task completion status.

    Requires JWT authentication. The token's user_id must match
    the URL user_id parameter.

    Args:
        user_id: User identifier from URL path.
        task_id: Task ID to toggle.
        toggle_data: New completion status (validated by Pydantic).
        current_user: Authenticated user from JWT token.
        session: Database session (injected).

    Returns:
        Task: The updated task.

    Raises:
        HTTPException: 401 if not authenticated.
        HTTPException: 403 if user_id doesn't match token.
        HTTPException: 404 if task not found or not owned by user.
    """
    verify_user_access(current_user, user_id)
    task = await get_task_or_404(session, task_id, user_id)

    task.completed = toggle_data.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task
