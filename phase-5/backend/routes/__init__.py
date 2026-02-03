"""
Routes package for the Todo API.

This package contains API route handlers organized by resource.
"""

from .tasks import router as tasks_router
from .auth import router as auth_router
from .chat import router as chat_router
from .tags import router as tags_router
from .notifications import router as notifications_router

__all__ = ["tasks_router", "auth_router", "chat_router", "tags_router", "notifications_router"]
