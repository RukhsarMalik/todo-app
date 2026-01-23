"""
FastAPI application entry point.

This module creates and configures the FastAPI application with:
- CORS middleware for frontend access
- Database lifecycle management (init/close)
- Root and health check endpoints
- Task routes for CRUD operations

Usage:
    uv run uvicorn main:app --reload --port 8000
"""

import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from db import init_db, close_db
from routes import tasks_router, auth_router, chat_router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# Lifespan Management
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage application lifecycle events.

    Startup:
        - Initialize database tables

    Shutdown:
        - Close database connections
    """
    # Startup
    logger.info("Starting application...")
    await init_db()
    logger.info("Database initialized")

    yield

    # Shutdown
    logger.info("Shutting down application...")
    await close_db()
    logger.info("Database connections closed")


# ============================================================================
# Application Factory
# ============================================================================

app = FastAPI(
    title="Todo API",
    description="RESTful API for task management with JWT authentication (Phase II - Module 3)",
    version="1.1.0",
    lifespan=lifespan,
)


# ============================================================================
# CORS Configuration
# ============================================================================

# Build allowed origins list from environment
cors_origins = [
    "http://localhost:3000",  # Next.js frontend (development)
    "http://127.0.0.1:3000",
    "http://localhost:3003",
    "http://127.0.0.1:3003",
    "http://localhost:3004",
    "http://127.0.0.1:3004",
    "http://localhost:3005",
    "http://127.0.0.1:3005",
    "https://frontend-ten-opal-98.vercel.app",  # Production frontend
]

# Add production frontend URL if configured (backup)
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url and frontend_url not in cors_origins:
    cors_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Exception Handlers
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for unexpected errors.

    Returns a generic 500 error without exposing stack traces.
    Logs the full error for debugging.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# ============================================================================
# Root Endpoints
# ============================================================================

@app.get("/")
async def root() -> dict:
    """
    API information endpoint.

    Returns:
        dict: API name and version.
    """
    return {
        "name": "Todo API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.

    Returns:
        dict: Server health status.
    """
    return {"status": "ok"}


# ============================================================================
# Route Registration
# ============================================================================

app.include_router(auth_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
