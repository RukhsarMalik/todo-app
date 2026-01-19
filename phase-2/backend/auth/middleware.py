"""
JWT verification middleware for FastAPI.

This module provides the authentication dependency for protecting
routes with JWT token verification.

Usage:
    from auth.middleware import get_current_user

    @router.get("/protected")
    async def protected_route(current_user: dict = Depends(get_current_user)):
        return {"user_id": current_user["user_id"]}
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from auth.jwt import decode_access_token

# HTTP Bearer token extractor
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Extract and verify the current user from JWT token.

    This dependency:
    1. Extracts the token from the Authorization header
    2. Decodes and verifies the JWT signature
    3. Extracts user_id and email from the token claims

    Args:
        credentials: The HTTP Authorization credentials containing the bearer token.

    Returns:
        dict: User information containing:
            - user_id: The user's unique identifier
            - email: The user's email address

    Raises:
        HTTPException: 401 if token is missing, invalid, or expired.

    Example:
        @router.get("/profile")
        async def get_profile(current_user: dict = Depends(get_current_user)):
            return {"user_id": current_user["user_id"]}
    """
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "user_id": user_id,
            "email": payload.get("email"),
        }

    except JWTError as e:
        # Handle specific JWT errors
        error_message = str(e)
        if "expired" in error_message.lower():
            detail = "Token expired"
        else:
            detail = "Invalid token"

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    except ValueError as e:
        # Handle missing secret key
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication configuration error",
        )
