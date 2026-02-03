"""
Notification endpoints with JWT authentication.

Endpoints:
- GET /api/{user_id}/notifications - List user's notifications
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from db import get_session
from models import Notification
from schemas import NotificationResponse
from auth.middleware import get_current_user

router = APIRouter(tags=["notifications"])


def verify_user_access(current_user: dict, user_id: str) -> None:
    """Verify authenticated user matches URL user_id."""
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )


@router.get(
    "/{user_id}/notifications",
    response_model=List[NotificationResponse],
    summary="List Notifications",
)
async def list_notifications(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[Notification]:
    """List all notifications for a user, newest first."""
    verify_user_access(current_user, user_id)
    statement = (
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
    )
    result = await session.execute(statement)
    return result.scalars().all()
