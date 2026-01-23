"""
Chat endpoint routes for AI-powered task management.

This module implements the API endpoints for the chat feature that integrates
OpenAI's Chat Completions API with direct database operations for task management.

Endpoints:
- POST /api/{user_id}/chat: Send a message to the AI assistant
- GET /api/{user_id}/conversations: List user's conversations
- GET /api/{user_id}/conversations/{conversation_id}: Get conversation history
- DELETE /api/{user_id}/conversations/{conversation_id}: Delete conversation

Usage:
    from routes.chat import router
    app.include_router(router, prefix="/api")
"""

import json
import time
import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from openai import AsyncOpenAI
from sqlmodel import select

from auth.middleware import get_current_user
from db import get_session_context
from models import Conversation, Message, Task
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/{user_id}")

# Lazy initialization of OpenAI client
_openai_client = None

def get_openai_client() -> AsyncOpenAI:
    """Get or create OpenAI client with lazy initialization."""
    global _openai_client
    if _openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=503,
                detail="Chat service unavailable: OPENAI_API_KEY not configured"
            )
        _openai_client = AsyncOpenAI(api_key=api_key)
    return _openai_client

# Define the tools/functions that OpenAI can call
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to the user's todo list. Use this when the user wants to create, add, or remember something to do.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The task title or name (what needs to be done)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional additional details about the task"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List the user's tasks. Use this when the user wants to see their tasks, todo list, or asks what they need to do.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter tasks by status. 'all' shows everything, 'pending' shows incomplete, 'completed' shows done tasks."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed/done. Use this when the user says they finished or completed a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to mark as completed"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete/remove a task from the list. Use this when the user wants to remove or delete a task entirely.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update/edit a task's title or description. Use this when the user wants to change or modify an existing task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the task (optional)"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description for the task (optional)"
                    }
                },
                "required": ["task_id"]
            }
        }
    }
]

# System prompt for the AI assistant
SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their todo list by adding, listing, completing, updating, and deleting tasks.

When users ask you to do something with their tasks, use the appropriate tool:
- add_task: When they want to add/create a new task
- list_tasks: When they want to see their tasks or ask what they need to do
- complete_task: When they finished a task and want to mark it done
- delete_task: When they want to remove a task entirely
- update_task: When they want to change/edit an existing task

Always be helpful and confirm actions you've taken. If a user asks about tasks by name and you need the task ID, first list the tasks to find the correct ID.

Respond naturally and conversationally. Keep responses concise but informative."""


async def execute_tool(tool_name: str, arguments: dict, user_id: str) -> dict:
    """Execute a tool function and return the result."""

    async with get_session_context() as session:
        if tool_name == "add_task":
            title = arguments.get("title", "").strip()
            description = arguments.get("description", "").strip()

            if not title:
                return {"error": True, "message": "Title is required"}
            if len(title) > 200:
                return {"error": True, "message": "Title exceeds 200 character limit"}

            task = Task(
                user_id=user_id,
                title=title,
                description=description if description else None
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)

            logger.info(f"Created task {task.id} for user {user_id}")
            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "message": f"Task '{task.title}' has been added to your list."
            }

        elif tool_name == "list_tasks":
            status = arguments.get("status", "all")

            statement = select(Task).where(Task.user_id == user_id)
            if status == "pending":
                statement = statement.where(Task.completed == False)
            elif status == "completed":
                statement = statement.where(Task.completed == True)

            result = await session.execute(statement)
            tasks = result.scalars().all()

            logger.info(f"Listed {len(tasks)} tasks for user {user_id}")
            return {
                "success": True,
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description,
                        "completed": t.completed
                    }
                    for t in tasks
                ],
                "count": len(tasks)
            }

        elif tool_name == "complete_task":
            task_id = arguments.get("task_id")

            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                return {"error": True, "message": "Task not found"}

            task.completed = True
            task.updated_at = datetime.utcnow()
            await session.commit()

            logger.info(f"Completed task {task_id} for user {user_id}")
            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "message": f"Task '{task.title}' has been marked as completed."
            }

        elif tool_name == "delete_task":
            task_id = arguments.get("task_id")

            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                return {"error": True, "message": "Task not found"}

            title = task.title
            await session.delete(task)
            await session.commit()

            logger.info(f"Deleted task {task_id} for user {user_id}")
            return {
                "success": True,
                "task_id": task_id,
                "message": f"Task '{title}' has been deleted."
            }

        elif tool_name == "update_task":
            task_id = arguments.get("task_id")
            new_title = arguments.get("title", "").strip()
            new_description = arguments.get("description", "").strip()

            if not new_title and not new_description:
                return {"error": True, "message": "No updates provided"}

            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                return {"error": True, "message": "Task not found"}

            if new_title:
                task.title = new_title
            if new_description:
                task.description = new_description
            task.updated_at = datetime.utcnow()
            await session.commit()

            logger.info(f"Updated task {task_id} for user {user_id}")
            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "message": f"Task has been updated."
            }

        else:
            return {"error": True, "message": f"Unknown tool: {tool_name}"}


from schemas import (
    ChatRequest, ChatResponse, ActionResult,
    ConversationListResponse, ConversationSummary,
    ConversationDetailResponse, MessageDetail,
    DeleteConversationResponse
)


@router.post("/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Send a message to the AI assistant and receive a response.
    Creates a new conversation if no conversation_id is provided.
    """
    start_time = time.time()

    # Verify user_id matches JWT token
    if user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="User ID mismatch")

    # Validate message content
    if not request.message or len(request.message.strip()) == 0:
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    if len(request.message) > 10000:
        raise HTTPException(status_code=400, detail="Message exceeds 10,000 character limit")

    # Validate conversation_id format if provided
    if request.conversation_id:
        try:
            UUID(request.conversation_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid conversation_id format")

    try:
        async with get_session_context() as session:
            # Create or get conversation
            if request.conversation_id:
                # Verify conversation belongs to user
                stmt = select(Conversation).where(
                    Conversation.id == request.conversation_id,
                    Conversation.user_id == user_id
                )
                result = await session.execute(stmt)
                conversation = result.scalar_one_or_none()

                if not conversation:
                    raise HTTPException(status_code=404, detail="Conversation not found")

                conversation_id = conversation.id
            else:
                # Create new conversation
                new_conv = Conversation(
                    user_id=user_id,
                    title=f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                )
                session.add(new_conv)
                await session.commit()
                await session.refresh(new_conv)
                conversation_id = new_conv.id

            # Store user message
            user_message = Message(
                conversation_id=conversation_id,
                role="user",
                content=request.message
            )
            session.add(user_message)
            await session.commit()

            # Load conversation history for context
            msg_stmt = select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.created_at.asc())
            msg_result = await session.execute(msg_stmt)
            history_messages = msg_result.scalars().all()

            # Build messages for OpenAI
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            for msg in history_messages:
                messages.append({"role": msg.role, "content": msg.content})

        # Call OpenAI Chat Completions API with tools
        actions_taken = []
        max_iterations = 5  # Prevent infinite loops
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            response = await get_openai_client().chat.completions.create(
                model="gpt-4o-mini",  # Using a more cost-effective model
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )

            assistant_message = response.choices[0].message

            # Check if the model wants to call a tool
            if assistant_message.tool_calls:
                # Add assistant message with tool calls to history
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })

                # Execute each tool call
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    try:
                        arguments = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        arguments = {}

                    logger.info(f"Executing tool: {tool_name} with args: {arguments}")

                    # Execute the tool
                    tool_result = await execute_tool(tool_name, arguments, user_id)

                    # Record action taken
                    actions_taken.append(ActionResult(
                        tool=tool_name,
                        result="success" if tool_result.get("success") else "error",
                        task_id=str(tool_result.get("task_id")) if tool_result.get("task_id") else None
                    ))

                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result)
                    })
            else:
                # No more tool calls, we have the final response
                break

        # Get the final response text
        final_response = assistant_message.content or "I've completed the requested action."

        # Store AI response in database
        async with get_session_context() as session:
            ai_message = Message(
                conversation_id=conversation_id,
                role="assistant",
                content=final_response
            )
            session.add(ai_message)
            await session.commit()
            await session.refresh(ai_message)

        response_obj = ChatResponse(
            response=final_response,
            conversation_id=conversation_id,
            message_id=str(ai_message.id),
            actions_taken=actions_taken
        )

        # Performance monitoring
        elapsed_time = time.time() - start_time
        logger.info(f"Chat endpoint response time: {elapsed_time:.2f}s for user {user_id}")

        return response_obj

    except HTTPException:
        raise
    except Exception as e:
        # Performance monitoring for error case
        elapsed_time = time.time() - start_time
        logger.error(f"Internal error after {elapsed_time:.2f}s: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/conversations", response_model=ConversationListResponse)
async def list_conversations(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    List all conversations for the specified user.
    """
    # Verify user_id matches JWT token
    if user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="User ID mismatch")

    async with get_session_context() as session:
        stmt = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
        result = await session.execute(stmt)
        conversations = result.scalars().all()

        # Count messages for each conversation
        conversation_summaries = []
        for conv in conversations:
            # Count messages in this conversation
            msg_stmt = select(Message).where(Message.conversation_id == conv.id)
            msg_result = await session.execute(msg_stmt)
            message_count = len(msg_result.scalars().all())

            conversation_summaries.append(ConversationSummary(
                id=conv.id,
                title=conv.title,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                message_count=message_count
            ))

        return ConversationListResponse(
            conversations=conversation_summaries,
            count=len(conversation_summaries)
        )


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    user_id: str,
    conversation_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific conversation with all its messages.
    """
    # Verify user_id matches JWT token
    if user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="User ID mismatch")

    # Validate conversation_id format
    try:
        UUID(conversation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid conversation_id format")

    async with get_session_context() as session:
        # Verify conversation belongs to user
        stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await session.execute(stmt)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Get all messages in the conversation
        msg_stmt = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())
        msg_result = await session.execute(msg_stmt)
        messages = msg_result.scalars().all()

        message_details = [
            MessageDetail(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at
            )
            for msg in messages
        ]

        return ConversationDetailResponse(
            id=conversation.id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=message_details
        )


@router.delete("/conversations/{conversation_id}", response_model=DeleteConversationResponse)
async def delete_conversation(
    user_id: str,
    conversation_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a conversation and all its messages.
    """
    # Verify user_id matches JWT token
    if user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="User ID mismatch")

    # Validate conversation_id format
    try:
        UUID(conversation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid conversation_id format")

    async with get_session_context() as session:
        # Verify conversation belongs to user
        stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await session.execute(stmt)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Delete the conversation (messages will be deleted via CASCADE)
        await session.delete(conversation)
        await session.commit()

        return DeleteConversationResponse(
            status="deleted",
            conversation_id=conversation_id
        )
