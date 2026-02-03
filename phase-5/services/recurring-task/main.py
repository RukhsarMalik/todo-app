"""
Recurring Task Microservice - Dapr Pub/Sub consumer.

Subscribes to task-events topic. When a recurring task is completed,
creates the next occurrence automatically.

Note: The main backend already handles next-occurrence creation inline
in the toggle endpoint. This service acts as a backup/audit consumer
and can be extended for more complex scheduling logic (e.g., Dapr Jobs API).

Usage:
    uvicorn main:app --port 8002
"""

import logging
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel, Field, select, Column, JSON
import sqlalchemy as sa

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(max_length=200)
    description: str | None = None
    completed: bool = Field(default=False)
    priority: str = Field(default="medium")
    due_date: str | None = None
    reminder_offset: int = Field(default=30)
    recurrence_rule: dict | None = Field(default=None, sa_column=Column(JSON, nullable=True))
    next_occurrence: str | None = None
    parent_task_id: int | None = Field(
        default=None,
        sa_column=Column(sa.Integer, sa.ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True),
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


DATABASE_URL = os.getenv("DATABASE_URL", "")
engine = create_async_engine(DATABASE_URL, pool_size=5, max_overflow=5) if DATABASE_URL else None
SessionLocal = async_sessionmaker(engine, expire_on_commit=False) if engine else None

app = FastAPI(title="Recurring Task Service", version="1.0.0")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "recurring-task"}


@app.get("/dapr/subscribe")
async def subscribe():
    return [
        {
            "pubsubname": "pubsub",
            "topic": "task-events",
            "route": "/events/task",
        },
    ]


def compute_next_due(due_date: str, rule: dict) -> str | None:
    """Compute the next due date based on recurrence rule."""
    try:
        current = datetime.strptime(due_date, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None

    rtype = rule.get("type", "daily")
    if rtype == "daily":
        return (current + timedelta(days=1)).strftime("%Y-%m-%d")
    elif rtype == "weekly":
        return (current + timedelta(weeks=1)).strftime("%Y-%m-%d")
    elif rtype == "monthly":
        month = current.month + 1
        year = current.year
        if month > 12:
            month = 1
            year += 1
        day = min(current.day, 28)
        return datetime(year, month, day).strftime("%Y-%m-%d")
    return None


@app.post("/events/task")
async def handle_task_event(request: Request):
    """
    Listen for task.completed events on recurring tasks.
    Log the event for audit. The main backend handles inline creation,
    so this service only logs and could be extended for advanced scheduling.
    """
    try:
        event = await request.json()
        data = event.get("data", event)
        event_type = data.get("event_type", "")
        task_id = data.get("task_id")
        user_id = data.get("user_id")

        if event_type != "task.completed" or not task_id or not SessionLocal:
            return JSONResponse({"status": "DROP"})

        async with SessionLocal() as session:
            stmt = select(Task).where(Task.id == task_id)
            result = await session.execute(stmt)
            task = result.scalar_one_or_none()

            if not task or not task.recurrence_rule or not task.due_date:
                return JSONResponse({"status": "DROP"})

            # Log for audit
            logger.info(
                f"Recurring task completed: task_id={task_id}, user={user_id}, "
                f"rule={task.recurrence_rule}, next_due={compute_next_due(task.due_date, task.recurrence_rule)}"
            )

        return JSONResponse({"status": "SUCCESS"})
    except Exception as e:
        logger.error(f"Error handling task event: {e}")
        return JSONResponse({"status": "RETRY"})
