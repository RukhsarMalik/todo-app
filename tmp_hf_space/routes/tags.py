"""
Tag CRUD endpoints with JWT authentication.

Endpoints:
- GET /api/{user_id}/tags - List user's tags
- POST /api/{user_id}/tags - Create a new tag
- DELETE /api/{user_id}/tags/{tag_id} - Delete a tag (cascades to task_tags)
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from db import get_session
from models import Tag, TaskTag
from schemas import TagCreate, TagResponse, MessageResponse
from auth.middleware import get_current_user

router = APIRouter(tags=["tags"])


def verify_user_access(current_user: dict, user_id: str) -> None:
    """Verify authenticated user matches URL user_id."""
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )


@router.get(
    "/{user_id}/tags",
    response_model=List[TagResponse],
    summary="List Tags",
)
async def list_tags(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[Tag]:
    """List all tags for a user."""
    verify_user_access(current_user, user_id)
    statement = select(Tag).where(Tag.user_id == user_id).order_by(Tag.name.asc())
    result = await session.execute(statement)
    return result.scalars().all()


@router.post(
    "/{user_id}/tags",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Tag",
)
async def create_tag(
    user_id: str,
    tag_data: TagCreate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Tag:
    """Create a new tag. Returns 409 if tag name already exists for user."""
    verify_user_access(current_user, user_id)

    # Check for duplicate
    statement = select(Tag).where(Tag.user_id == user_id, Tag.name == tag_data.name)
    result = await session.execute(statement)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Tag '{tag_data.name}' already exists"
        )

    tag = Tag(user_id=user_id, name=tag_data.name)
    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return tag


@router.delete(
    "/{user_id}/tags/{tag_id}",
    response_model=MessageResponse,
    summary="Delete Tag",
)
async def delete_tag(
    user_id: str,
    tag_id: int,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Delete a tag. Cascades to task_tags junction table."""
    verify_user_access(current_user, user_id)

    statement = select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
    result = await session.execute(statement)
    tag = result.scalar_one_or_none()

    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )

    await session.delete(tag)
    await session.commit()
    return {"message": f"Tag '{tag.name}' deleted"}
