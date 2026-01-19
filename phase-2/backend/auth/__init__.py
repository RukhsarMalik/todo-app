"""
Authentication module for JWT-based user authentication.

This package provides:
- Password hashing with bcrypt
- JWT token creation and verification
- Auth middleware for FastAPI dependency injection

Usage:
    from auth import hash_password, verify_password
    from auth import create_access_token, decode_access_token
    from auth import get_current_user
"""

from auth.password import hash_password, verify_password
from auth.jwt import create_access_token, decode_access_token
from auth.middleware import get_current_user

__all__ = [
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_access_token",
    "get_current_user",
]
