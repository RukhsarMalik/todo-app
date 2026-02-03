"""
JWT token creation and verification.

This module provides functions for creating and decoding JWT tokens
using the HS256 algorithm with a secret key from environment variables.

Usage:
    from auth.jwt import create_access_token, decode_access_token

    token = create_access_token("user_id_123", "user@example.com")
    payload = decode_access_token(token)
"""

import os
from datetime import datetime, timedelta
from typing import Any

from jose import jwt, JWTError

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7


def create_access_token(user_id: str, email: str) -> str:
    """
    Create a JWT access token with user claims.

    The token includes:
    - sub: User ID (subject claim)
    - email: User's email address
    - exp: Expiration timestamp (7 days from now)

    Args:
        user_id: The unique identifier for the user.
        email: The user's email address.

    Returns:
        str: The encoded JWT token.

    Raises:
        ValueError: If JWT_SECRET_KEY is not configured.

    Example:
        >>> token = create_access_token("abc-123", "user@example.com")
        >>> token.count(".") == 2  # JWT has 3 parts
        True
    """
    if not SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY environment variable not set")

    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode: dict[str, Any] = {
        "sub": user_id,
        "email": email,
        "exp": expire,
    }

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and verify a JWT access token.

    Args:
        token: The JWT token string to decode.

    Returns:
        dict: The decoded payload containing sub, email, and exp claims.

    Raises:
        JWTError: If the token is invalid, expired, or tampered with.
        ValueError: If JWT_SECRET_KEY is not configured.

    Example:
        >>> token = create_access_token("abc-123", "user@example.com")
        >>> payload = decode_access_token(token)
        >>> payload["sub"]
        'abc-123'
    """
    if not SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY environment variable not set")

    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


# Re-export JWTError for convenience
__all__ = ["create_access_token", "decode_access_token", "JWTError"]
