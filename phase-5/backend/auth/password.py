"""
Password hashing utilities using bcrypt.

This module provides secure password hashing and verification
using bcrypt directly for maximum compatibility with modern versions.

Usage:
    from auth.password import hash_password, verify_password

    hashed = hash_password("my_password")
    is_valid = verify_password("my_password", hashed)
"""

import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.

    Args:
        password: The plaintext password to hash.

    Returns:
        str: The bcrypt hash of the password.

    Example:
        >>> hashed = hash_password("secret123")
        >>> hashed.startswith("$2b$")
        True
    """
    # Encode password to bytes, generate salt, and hash
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a bcrypt hash.

    Uses constant-time comparison to prevent timing attacks.

    Args:
        plain_password: The plaintext password to verify.
        hashed_password: The bcrypt hash to verify against.

    Returns:
        bool: True if password matches, False otherwise.

    Example:
        >>> hashed = hash_password("secret123")
        >>> verify_password("secret123", hashed)
        True
        >>> verify_password("wrong", hashed)
        False
    """
    try:
        password_bytes = plain_password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except (ValueError, TypeError):
        return False
