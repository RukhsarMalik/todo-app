"""
Dapr event publisher for task events.

Publishes task lifecycle events and reminder events via Dapr Pub/Sub HTTP API.
Implements graceful degradation: CRUD operations succeed even if event publishing fails.

Usage:
    from events import publish_task_event, publish_reminder_event
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Optional

import httpx

logger = logging.getLogger(__name__)

# Dapr sidecar HTTP API base URL
DAPR_HTTP_PORT = 3500
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"
PUBSUB_NAME = "pubsub"


async def publish_task_event(
    event_type: str,
    task_id: int,
    user_id: str,
    task_data: dict[str, Any],
) -> bool:
    """
    Publish a task event to the task-events topic via Dapr Pub/Sub.

    Args:
        event_type: One of task.created, task.updated, task.completed, task.deleted.
        task_id: The task ID.
        user_id: The task owner's user ID.
        task_data: Dictionary of task fields to include in the event.

    Returns:
        True if published successfully, False on failure.
    """
    event = {
        "event_type": event_type,
        "task_id": task_id,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        **task_data,
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{DAPR_BASE_URL}/v1.0/publish/{PUBSUB_NAME}/task-events",
                json=event,
                timeout=5.0,
            )
            if resp.status_code in (200, 204):
                logger.info(f"Published {event_type} event for task {task_id}")
                return True
            else:
                logger.warning(
                    f"Failed to publish {event_type} event: status {resp.status_code}"
                )
                return False
    except Exception as e:
        logger.warning(f"Failed to publish {event_type} event for task {task_id}: {e}")
        return False


async def publish_reminder_event(
    task_id: int,
    user_id: str,
    title: str,
    due_date: datetime,
    reminder_offset: int,
) -> bool:
    """
    Publish a reminder event to the reminders topic via Dapr Pub/Sub.

    Args:
        task_id: The task ID.
        user_id: The task owner's user ID.
        title: The task title.
        due_date: The task due date.
        reminder_offset: Minutes before due_date to trigger reminder.

    Returns:
        True if published successfully, False on failure.
    """
    reminder_time = due_date - timedelta(minutes=reminder_offset)

    event = {
        "event_type": "reminder.schedule",
        "task_id": task_id,
        "user_id": user_id,
        "title": title,
        "due_date": due_date.isoformat(),
        "reminder_time": reminder_time.isoformat(),
        "timestamp": datetime.utcnow().isoformat(),
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{DAPR_BASE_URL}/v1.0/publish/{PUBSUB_NAME}/reminders",
                json=event,
                timeout=5.0,
            )
            if resp.status_code in (200, 204):
                logger.info(f"Published reminder event for task {task_id}")
                return True
            else:
                logger.warning(
                    f"Failed to publish reminder event: status {resp.status_code}"
                )
                return False
    except Exception as e:
        logger.warning(f"Failed to publish reminder event for task {task_id}: {e}")
        return False
