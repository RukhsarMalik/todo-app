"""
Routes package for the Todo API.

This package contains API route handlers organized by resource.
"""

from .tasks import router as tasks_router
from .auth import router as auth_router

__all__ = ["tasks_router", "auth_router"]
