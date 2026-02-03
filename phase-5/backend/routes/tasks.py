"""
Task CRUD endpoints with JWT authentication.

Phase V extensions:
- Priority, due_date, reminder_offset, recurrence_rule fields
- Search (keyword across title/description)
- Filter (status, priority, tags, due_date range)
- Sort (created_at, due_date, priority, title)
- Tag associations via tag_ids
- Event publishing via Dapr Pub/Sub
- Recurring task next occurrence on completion
"""

import logging
from datetime import datetime, timedelta
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from db import get_session
from models import Task, Tag, TaskTag, Notification
from schemas import (
    TaskCreate,
    TaskUpdate,
    TaskToggle,
    TaskResponse,
    TagResponse,
    StatusFilter,
    PriorityFilter,
    SortField,
    SortOrder,
)
from auth.middleware import get_current_user
from events import publish_task_event, publish_reminder_event

logger = logging.getLogger(__name__)

router = APIRouter(tags=["tasks"])

# Priority sort order mapping (urgent highest)
PRIORITY_ORDER = {"urgent": 0, "high": 1, "medium": 2, "low": 3}


# ============================================================================
# Helper Functions
# ============================================================================

def verify_user_access(current_user: dict, user_id: str) -> None:
    """Verify that the authenticated user can access the requested user's resources."""
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
    """Get a task by ID, verifying ownership. Returns 404 if not found/owned."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


async def get_tags_for_task(session: AsyncSession, task_id: int) -> List[Tag]:
    """Get all tags associated with a task."""
    statement = (
        select(Tag)
        .join(TaskTag, TaskTag.tag_id == Tag.id)
        .where(TaskTag.task_id == task_id)
        .order_by(Tag.name.asc())
    )
    result = await session.execute(statement)
    return list(result.scalars().all())


async def sync_task_tags(
    session: AsyncSession,
    task_id: int,
    user_id: str,
    tag_ids: List[int],
) -> None:
    """Replace all tag associations for a task with the given tag_ids."""
    # Remove existing associations
    existing = select(TaskTag).where(TaskTag.task_id == task_id)
    result = await session.execute(existing)
    for tt in result.scalars().all():
        await session.delete(tt)

    # Add new associations (validate tags belong to user)
    for tag_id in tag_ids:
        tag_check = select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
        tag_result = await session.execute(tag_check)
        if tag_result.scalar_one_or_none() is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tag {tag_id} not found or not owned by user"
            )
        session.add(TaskTag(task_id=task_id, tag_id=tag_id))


def task_to_response(task: Task, tags: List[Tag]) -> dict:
    """Convert Task model + tags to response dict."""
    return {
        "id": task.id,
        "user_id": task.user_id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "priority": task.priority,
        "due_date": task.due_date,
        "reminder_offset": task.reminder_offset,
        "recurrence_rule": task.recurrence_rule,
        "next_occurrence": task.next_occurrence,
        "parent_task_id": task.parent_task_id,
        "tags": [{"id": t.id, "name": t.name, "created_at": t.created_at} for t in tags],
        "created_at": task.created_at,
        "updated_at": task.updated_at,
    }


def compute_next_occurrence(due_date: datetime, recurrence_rule: dict[str, Any]) -> Optional[datetime]:
    """Compute the next occurrence date from a recurrence rule."""
    rule_type = recurrence_rule.get("type")
    today = datetime.utcnow()
    base = max(due_date, today)

    if rule_type == "daily":
        return base + timedelta(days=1)
    elif rule_type == "weekly":
        days = recurrence_rule.get("days", [])
        if not days:
            return base + timedelta(weeks=1)
        # Find next matching weekday
        day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
                   "Friday": 4, "Saturday": 5, "Sunday": 6}
        target_days = sorted([day_map.get(d, 0) for d in days])
        current_weekday = base.weekday()
        for d in target_days:
            if d > current_weekday:
                delta = d - current_weekday
                return base + timedelta(days=delta)
        # Wrap to next week
        delta = 7 - current_weekday + target_days[0]
        return base + timedelta(days=delta)
    elif rule_type == "monthly":
        day_of_month = recurrence_rule.get("day_of_month", base.day)
        # Next month
        if base.month == 12:
            next_month = base.replace(year=base.year + 1, month=1, day=min(day_of_month, 28))
        else:
            import calendar
            max_day = calendar.monthrange(base.year, base.month + 1)[1]
            next_month = base.replace(month=base.month + 1, day=min(day_of_month, max_day))
        return next_month
    return None


# ============================================================================
# List Tasks with Search/Filter/Sort
# ============================================================================

@router.get(
    "/{user_id}/tasks",
    response_model=List[TaskResponse],
    summary="List Tasks",
    description="List tasks with optional search, filter, and sort.",
)
async def list_tasks(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    status_filter: StatusFilter = StatusFilter.all,
    priority: Optional[PriorityFilter] = None,
    tags: Optional[str] = Query(default=None, description="Comma-separated tag names"),
    search: Optional[str] = Query(default=None, description="Search title and description"),
    due_date_from: Optional[datetime] = None,
    due_date_to: Optional[datetime] = None,
    sort: SortField = SortField.created,
    order: SortOrder = SortOrder.desc,
    session: AsyncSession = Depends(get_session),
) -> List[dict]:
    """List tasks with search, filter by status/priority/tags/date range, and sort."""
    verify_user_access(current_user, user_id)

    statement = select(Task).where(Task.user_id == user_id)

    # Status filter
    if status_filter == StatusFilter.pending:
        statement = statement.where(Task.completed == False)
    elif status_filter == StatusFilter.completed:
        statement = statement.where(Task.completed == True)

    # Priority filter
    if priority is not None:
        statement = statement.where(Task.priority == priority.value)

    # Search (case-insensitive partial match)
    if search:
        search_pattern = f"%{search}%"
        statement = statement.where(
            (Task.title.ilike(search_pattern)) | (Task.description.ilike(search_pattern))
        )

    # Due date range filter
    if due_date_from:
        statement = statement.where(Task.due_date >= due_date_from)
    if due_date_to:
        statement = statement.where(Task.due_date <= due_date_to)

    # Tag filter
    if tags:
        tag_names = [t.strip() for t in tags.split(",") if t.strip()]
        if tag_names:
            # Subquery: task IDs that have ALL specified tags
            for tag_name in tag_names:
                tag_subq = (
                    select(TaskTag.task_id)
                    .join(Tag, Tag.id == TaskTag.tag_id)
                    .where(Tag.user_id == user_id, Tag.name == tag_name)
                )
                statement = statement.where(Task.id.in_(tag_subq))

    # Sort
    if sort in (SortField.created, SortField.created_at):
        sort_column = Task.created_at
    elif sort == SortField.title:
        sort_column = Task.title
    elif sort == SortField.due_date:
        sort_column = Task.due_date
    elif sort == SortField.priority:
        # Use CASE expression for priority ordering
        from sqlalchemy import case
        sort_column = case(
            (Task.priority == "urgent", 0),
            (Task.priority == "high", 1),
            (Task.priority == "medium", 2),
            (Task.priority == "low", 3),
            else_=4,
        )
    else:
        sort_column = Task.created_at

    if order == SortOrder.desc:
        statement = statement.order_by(sort_column.desc())
    else:
        statement = statement.order_by(sort_column.asc())

    result = await session.execute(statement)
    tasks = result.scalars().all()

    # Build responses with tags
    responses = []
    for task in tasks:
        task_tags = await get_tags_for_task(session, task.id)
        responses.append(task_to_response(task, task_tags))
    return responses


# ============================================================================
# Get Single Task
# ============================================================================

@router.get(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get Task",
)
async def get_task(
    user_id: str,
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Get a specific task by ID."""
    verify_user_access(current_user, user_id)
    task = await get_task_or_404(session, task_id, user_id)
    task_tags = await get_tags_for_task(session, task.id)
    return task_to_response(task, task_tags)


# ============================================================================
# Create Task
# ============================================================================

@router.post(
    "/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Task",
)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Create a new task with optional priority, due_date, tags, recurrence."""
    verify_user_access(current_user, user_id)

    now = datetime.utcnow()
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False,
        priority=task_data.priority or "medium",
        due_date=task_data.due_date,
        reminder_offset=task_data.reminder_offset if task_data.reminder_offset is not None else 60,
        recurrence_rule=task_data.recurrence_rule,
        created_at=now,
        updated_at=now,
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    # Sync tags
    if task_data.tag_ids:
        await sync_task_tags(session, task.id, user_id, task_data.tag_ids)
        await session.commit()

    # Publish events (graceful degradation)
    await publish_task_event(
        "task.created", task.id, user_id,
        {"title": task.title, "priority": task.priority,
         "due_date": task.due_date.isoformat() if task.due_date else None,
         "completed": False},
    )
    if task.due_date:
        await publish_reminder_event(
            task.id, user_id, task.title, task.due_date, task.reminder_offset,
        )

    task_tags = await get_tags_for_task(session, task.id)
    return task_to_response(task, task_tags)


# ============================================================================
# Update Task
# ============================================================================

@router.put(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update Task",
)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Update an existing task. Only provided fields are updated."""
    verify_user_access(current_user, user_id)
    task = await get_task_or_404(session, task_id, user_id)

    # Use model_fields_set to check which fields were explicitly provided
    # This allows clearing fields by sending null
    provided_fields = task_data.model_fields_set

    if "title" in provided_fields and task_data.title is not None:
        task.title = task_data.title
    if "description" in provided_fields:
        task.description = task_data.description
    if "priority" in provided_fields and task_data.priority is not None:
        task.priority = task_data.priority
    if "due_date" in provided_fields:
        task.due_date = task_data.due_date  # Can be None to clear
    if "reminder_offset" in provided_fields and task_data.reminder_offset is not None:
        task.reminder_offset = task_data.reminder_offset
    if "recurrence_rule" in provided_fields:
        task.recurrence_rule = task_data.recurrence_rule  # Can be None to clear

    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    # Sync tags if provided
    if task_data.tag_ids is not None:
        await sync_task_tags(session, task.id, user_id, task_data.tag_ids)
        await session.commit()

    # Publish events
    await publish_task_event(
        "task.updated", task.id, user_id,
        {"title": task.title, "priority": task.priority,
         "due_date": task.due_date.isoformat() if task.due_date else None,
         "completed": task.completed},
    )
    if task.due_date:
        await publish_reminder_event(
            task.id, user_id, task.title, task.due_date, task.reminder_offset,
        )

    task_tags = await get_tags_for_task(session, task.id)
    return task_to_response(task, task_tags)


# ============================================================================
# Delete Task
# ============================================================================

@router.delete(
    "/{user_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Task",
)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """Delete a task permanently."""
    verify_user_access(current_user, user_id)
    task = await get_task_or_404(session, task_id, user_id)

    await publish_task_event(
        "task.deleted", task.id, user_id,
        {"title": task.title},
    )

    await session.delete(task)
    await session.commit()


# ============================================================================
# Toggle Completion (with recurring task support)
# ============================================================================

@router.patch(
    "/{user_id}/tasks/{task_id}/complete",
    response_model=TaskResponse,
    summary="Toggle Task Completion",
)
async def toggle_task_complete(
    user_id: str,
    task_id: int,
    toggle_data: TaskToggle,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Toggle task completion. For recurring tasks, creates next occurrence."""
    verify_user_access(current_user, user_id)
    task = await get_task_or_404(session, task_id, user_id)

    task.completed = toggle_data.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    # Publish completion event
    await publish_task_event(
        "task.completed" if task.completed else "task.updated",
        task.id, user_id,
        {"title": task.title, "priority": task.priority,
         "due_date": task.due_date.isoformat() if task.due_date else None,
         "completed": task.completed,
         "recurrence_rule": task.recurrence_rule},
    )

    # Create next occurrence for recurring tasks (inline for now)
    if task.completed and task.recurrence_rule and task.due_date:
        next_due = compute_next_occurrence(task.due_date, task.recurrence_rule)
        if next_due:
            now = datetime.utcnow()
            new_task = Task(
                user_id=user_id,
                title=task.title,
                description=task.description,
                completed=False,
                priority=task.priority,
                due_date=next_due,
                reminder_offset=task.reminder_offset,
                recurrence_rule=task.recurrence_rule,
                parent_task_id=task.id,
                created_at=now,
                updated_at=now,
            )
            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)

            # Copy tags to new occurrence
            old_tags = await get_tags_for_task(session, task.id)
            for t in old_tags:
                session.add(TaskTag(task_id=new_task.id, tag_id=t.id))
            if old_tags:
                await session.commit()

            # Publish events for new task
            await publish_task_event(
                "task.created", new_task.id, user_id,
                {"title": new_task.title, "priority": new_task.priority,
                 "due_date": new_task.due_date.isoformat() if new_task.due_date else None,
                 "completed": False},
            )
            if new_task.due_date:
                await publish_reminder_event(
                    new_task.id, user_id, new_task.title,
                    new_task.due_date, new_task.reminder_offset,
                )

            logger.info(f"Created next occurrence task {new_task.id} for recurring task {task.id}")

    task_tags = await get_tags_for_task(session, task.id)
    return task_to_response(task, task_tags)
