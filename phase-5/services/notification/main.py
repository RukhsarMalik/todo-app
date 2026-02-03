"""
Notification Microservice - Dapr Pub/Sub consumer.

Subscribes to task-events and reminders topics via Dapr.
Creates notification records in the database when events are received.

Usage:
    uvicorn main:app --port 8001
"""

import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel, Field

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Inline model to avoid importing from backend
class Notification(SQLModel, table=True):
    __tablename__ = "notifications"
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    task_id: int | None = Field(default=None)
    message: str
    read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


DATABASE_URL = os.getenv("DATABASE_URL", "")
engine = create_async_engine(DATABASE_URL, pool_size=5, max_overflow=5) if DATABASE_URL else None
SessionLocal = async_sessionmaker(engine, expire_on_commit=False) if engine else None

app = FastAPI(title="Notification Service", version="1.0.0")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "notification"}


# Dapr subscription configuration
@app.get("/dapr/subscribe")
async def subscribe():
    """Tell Dapr which topics this service subscribes to."""
    return [
        {
            "pubsubname": "pubsub",
            "topic": "task-events",
            "route": "/events/task",
        },
        {
            "pubsubname": "pubsub",
            "topic": "reminders",
            "route": "/events/reminder",
        },
    ]


@app.post("/events/task")
async def handle_task_event(request: Request):
    """Handle task lifecycle events (created, updated, deleted, completed)."""
    try:
        event = await request.json()
        data = event.get("data", event)
        event_type = data.get("event_type", "unknown")
        user_id = data.get("user_id")
        task_id = data.get("task_id")
        title = data.get("title", "")

        if not user_id or not SessionLocal:
            return JSONResponse({"status": "DROP"})

        messages = {
            "task.created": f'New task created: "{title}"',
            "task.updated": f'Task updated: "{title}"',
            "task.deleted": f"Task #{task_id} deleted",
            "task.completed": f'Task completed: "{title}"',
        }
        message = messages.get(event_type)
        if not message:
            return JSONResponse({"status": "DROP"})

        async with SessionLocal() as session:
            notification = Notification(
                user_id=user_id,
                task_id=task_id,
                message=message,
            )
            session.add(notification)
            await session.commit()

        logger.info(f"Notification created: {event_type} for user {user_id}")
        return JSONResponse({"status": "SUCCESS"})
    except Exception as e:
        logger.error(f"Error handling task event: {e}")
        return JSONResponse({"status": "RETRY"})


@app.post("/events/reminder")
async def handle_reminder_event(request: Request):
    """Handle reminder events for tasks with due dates."""
    try:
        event = await request.json()
        data = event.get("data", event)
        user_id = data.get("user_id")
        task_id = data.get("task_id")
        title = data.get("title", "")
        due_date = data.get("due_date", "")

        if not user_id or not SessionLocal:
            return JSONResponse({"status": "DROP"})

        message = f'Reminder: "{title}" is due {due_date}'

        async with SessionLocal() as session:
            notification = Notification(
                user_id=user_id,
                task_id=task_id,
                message=message,
            )
            session.add(notification)
            await session.commit()

        logger.info(f"Reminder notification created for user {user_id}, task {task_id}")
        return JSONResponse({"status": "SUCCESS"})
    except Exception as e:
        logger.error(f"Error handling reminder event: {e}")
        return JSONResponse({"status": "RETRY"})
