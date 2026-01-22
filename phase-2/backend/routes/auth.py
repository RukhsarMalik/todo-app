"""
Authentication routes for user signup, login, and logout.

This module provides the RESTful endpoints for user authentication:
- POST /api/auth/signup - Create a new user account
- POST /api/auth/login - Authenticate and receive JWT token
- POST /api/auth/logout - Log out (client-side token discard)

All endpoints return JSON responses with appropriate HTTP status codes.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from db import get_session
from models import User
from schemas import UserCreate, UserLogin, TokenResponse, MessageResponse, ProfileUpdate, PasswordChange, UserResponse
from auth.middleware import get_current_user
from auth.password import hash_password, verify_password
from auth.jwt import create_access_token

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


# ============================================================================
# User Signup (US1)
# ============================================================================

@router.post(
    "/signup",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="User Signup",
    description="Register a new user account and receive a JWT token"
)
async def signup(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
) -> TokenResponse:
    """
    Register a new user account.

    Creates a new user with the provided email and password.
    Returns a JWT token on successful registration.

    Args:
        user_data: User registration data (email, password, optional name).
        session: Database session (injected).

    Returns:
        TokenResponse: JWT token and user information.

    Raises:
        HTTPException: 400 if email is already registered.
        HTTPException: 422 if validation fails (email format, password length).
    """
    # Check if email already exists
    statement = select(User).where(User.email == user_data.email.lower())
    result = await session.execute(statement)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        logger.warning(f"Signup attempt with existing email: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    user = User(
        email=user_data.email.lower(),
        password_hash=hash_password(user_data.password),
        name=user_data.name,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    logger.info(f"New user registered: {user.email} (id: {user.id})")

    # Generate JWT token
    token = create_access_token(user.id, user.email)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
    )


# ============================================================================
# User Login (US2)
# ============================================================================

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="User Login",
    description="Authenticate with email and password to receive a JWT token"
)
async def login(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_session)
) -> TokenResponse:
    """
    Authenticate a user and return a JWT token.

    Verifies the provided email and password against stored credentials.
    Returns a JWT token on successful authentication.

    Args:
        credentials: Login credentials (email, password).
        session: Database session (injected).

    Returns:
        TokenResponse: JWT token and user information.

    Raises:
        HTTPException: 401 if credentials are invalid.
            Note: Uses generic error message to avoid revealing
            whether the email exists or the password is wrong.
    """
    # Find user by email
    statement = select(User).where(User.email == credentials.email.lower())
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    # Verify password (constant-time comparison via passlib)
    if not user or not verify_password(credentials.password, user.password_hash):
        logger.warning(f"Failed login attempt for: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    logger.info(f"User logged in: {user.email} (id: {user.id})")

    # Generate JWT token
    token = create_access_token(user.id, user.email)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
    )


# ============================================================================
# User Logout (US4)
# ============================================================================

@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="User Logout",
    description="Log out the current user (client-side token discard)"
)
async def logout() -> MessageResponse:
    """
    Log out the current user.

    Note: This is a stateless logout. The server does not maintain
    a session or token blacklist. The client should discard the
    stored JWT token upon receiving this response.

    Returns:
        MessageResponse: Success message.
    """
    return MessageResponse(message="Successfully logged out")


# ============================================================================
# User Profile (Settings)
# ============================================================================

@router.get(
    "/profile",
    response_model=UserResponse,
    summary="Get User Profile",
    description="Get the current user's profile information"
)
async def get_profile(
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> UserResponse:
    """
    Get the current user's profile.

    Args:
        current_user: Decoded JWT token data (injected).
        session: Database session (injected).

    Returns:
        UserResponse: User profile information.
    """
    user_id = current_user["user_id"]
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(id=user.id, email=user.email, name=user.name)


@router.put(
    "/profile",
    response_model=UserResponse,
    summary="Update User Profile",
    description="Update the current user's profile (name)"
)
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> UserResponse:
    """
    Update the current user's profile.

    Args:
        profile_data: Profile update data (name).
        current_user: Decoded JWT token data (injected).
        session: Database session (injected).

    Returns:
        UserResponse: Updated user profile.
    """
    user_id = current_user["user_id"]
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update name
    if profile_data.name is not None:
        user.name = profile_data.name

    await session.commit()
    await session.refresh(user)

    logger.info(f"Profile updated for user: {user.email}")

    return UserResponse(id=user.id, email=user.email, name=user.name)


@router.put(
    "/password",
    response_model=MessageResponse,
    summary="Change Password",
    description="Change the current user's password"
)
async def change_password(
    password_data: PasswordChange,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> MessageResponse:
    """
    Change the current user's password.

    Args:
        password_data: Password change data (current and new passwords).
        current_user: Decoded JWT token data (injected).
        session: Database session (injected).

    Returns:
        MessageResponse: Success message.

    Raises:
        HTTPException: 400 if current password is incorrect.
        HTTPException: 400 if new password is same as current.
    """
    user_id = current_user["user_id"]
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Verify current password
    if not verify_password(password_data.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Check if new password is same as current
    if verify_password(password_data.new_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password"
        )

    # Update password
    user.password_hash = hash_password(password_data.new_password)

    await session.commit()

    logger.info(f"Password changed for user: {user.email}")

    return MessageResponse(message="Password changed successfully")
