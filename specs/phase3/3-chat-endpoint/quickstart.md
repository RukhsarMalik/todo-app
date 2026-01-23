# Quickstart Guide: Chat Endpoint with OpenAI Agent

**Feature**: Phase III Module 3 - Chat Endpoint
**Date**: 2026-01-23
**Spec**: [spec.md](./spec.md)

## Overview

This guide provides a quick implementation example of the chat endpoint with OpenAI Agent integration. It demonstrates how to create the chat endpoint that connects OpenAI's Agent API with the existing MCP server tools.

## Prerequisites

- Python 3.12+
- FastAPI
- OpenAI Python SDK
- MCP SDK
- SQLModel
- Existing Phase III infrastructure (MCP server, database models)

## Implementation Steps

### 1. Create Chat Request/Response Schemas

Create the Pydantic schemas in `schemas.py`:

```python
from pydantic import BaseModel, field_validator
from typing import List, Optional
from uuid import UUID

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None  # UUID string format

    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Message content cannot be empty')
        if len(v) > 10000:
            raise ValueError('Message exceeds 10,000 character limit')
        return v.strip()

    @field_validator('conversation_id')
    @classmethod
    def validate_conversation_id(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            try:
                UUID(v)  # Validate UUID format
            except ValueError:
                raise ValueError('conversation_id must be a valid UUID')
        return v

class ActionResult(BaseModel):
    tool: str
    result: str
    task_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str  # UUID string
    message_id: str  # UUID string for the AI response message
    actions_taken: List[ActionResult] = []

class ConversationSummary(BaseModel):
    id: str  # UUID string
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    message_count: int

class ConversationListResponse(BaseModel):
    conversations: List[ConversationSummary]
    count: int

class MessageDetail(BaseModel):
    id: str  # UUID string
    role: str  # 'user', 'assistant', 'system'
    content: str
    created_at: datetime

class ConversationDetailResponse(BaseModel):
    id: str  # UUID string
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    messages: List[MessageDetail]

class DeleteConversationResponse(BaseModel):
    status: str  # "deleted"
    conversation_id: str  # UUID string
```

### 2. Create Chat Agent Integration

Create `agent.py` to handle OpenAI Agent integration:

```python
import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import UUID

import openai
from sqlmodel import select, Session
from mcp.client import Client

from models import Conversation, Message
from schemas import ActionResult

logger = logging.getLogger(__name__)

class ChatAgent:
    def __init__(self, openai_client: openai.AsyncOpenAI, mcp_client: Client):
        self.openai_client = openai_client
        self.mcp_client = mcp_client

    async def process_message(
        self,
        user_id: str,
        message_content: str,
        conversation_id: Optional[str] = None
    ) -> tuple[str, str, List[ActionResult]]:
        """
        Process a user message and return AI response with actions taken.

        Args:
            user_id: The user's unique identifier
            message_content: The user's message
            conversation_id: Optional existing conversation ID

        Returns:
            Tuple of (response_text, conversation_id, list_of_actions_taken)
        """
        # Load or create conversation
        conversation = await self._get_or_create_conversation(user_id, conversation_id)

        # Load conversation history
        conversation_history = await self._load_conversation_history(conversation.id)

        # Prepare messages for OpenAI API
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation_history
        ]

        # Add the new user message
        messages.append({"role": "user", "content": message_content})

        # Create OpenAI Assistant with MCP tools
        assistant = await self.openai_client.beta.assistants.create(
            name="Task Management Assistant",
            instructions="You are a helpful assistant that manages tasks for users. Use the provided tools to add, list, complete, delete, and update tasks. Always confirm actions with the user.",
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "add_task",
                        "description": "Add a new task for the user",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string", "description": "The task title"},
                                "description": {"type": "string", "description": "Optional task description"}
                            },
                            "required": ["title"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "list_tasks",
                        "description": "List the user's tasks",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "status": {"type": "string", "enum": ["all", "pending", "completed"], "default": "all"}
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "complete_task",
                        "description": "Mark a task as completed",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "integer", "description": "The ID of the task to complete"}
                            },
                            "required": ["task_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "delete_task",
                        "description": "Delete a task",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                            },
                            "required": ["task_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "update_task",
                        "description": "Update a task's title or description",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "integer", "description": "The ID of the task to update"},
                                "title": {"type": "string", "description": "New title (optional)"},
                                "description": {"type": "string", "description": "New description (optional)"}
                            },
                            "required": ["task_id"]
                        }
                    }
                }
            ],
            model="gpt-4-turbo-preview"
        )

        # Create a thread and run the assistant
        thread = await self.openai_client.beta.threads.create(messages=messages)

        run = await self.openai_client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # Poll for completion
        while run.status in ["queued", "in_progress", "requires_action"]:
            await asyncio.sleep(0.5)
            run = await self.openai_client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

            if run.status == "requires_action":
                # Handle tool calls
                tool_outputs = []
                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    try:
                        result = await self._execute_tool_call(
                            tool_call.function.name,
                            tool_call.function.arguments,
                            user_id
                        )
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": result
                        })
                    except Exception as e:
                        logger.error(f"Tool call failed: {e}")
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": f"Error: {str(e)}"
                        })

                # Submit tool outputs
                run = await self.openai_client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )

        # Get the assistant's response
        messages_response = await self.openai_client.beta.threads.messages.list(
            thread_id=thread.id,
            order="asc"
        )

        # Find the newest assistant message
        assistant_message = None
        for msg in reversed(messages_response.data):
            if msg.role == "assistant":
                assistant_message = msg
                break

        if not assistant_message:
            raise Exception("No assistant response received")

        response_text = ""
        for content_block in assistant_message.content:
            if content_block.type == "text":
                response_text += content_block.text.value

        # Clean up assistant and thread
        await self.openai_client.beta.assistants.delete(assistant.id)

        # Extract actions taken from tool calls
        actions_taken = []
        for run_step in (await self.openai_client.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id)).data:
            if run_step.type == "tool_calls":
                for tool_call in run_step.step_details.tool_calls:
                    if tool_call.type == "function":
                        actions_taken.append(ActionResult(
                            tool=tool_call.function.name,
                            result="completed",
                            task_id=self._extract_task_id_from_result(tool_call.function.output)
                        ))

        return response_text, str(conversation.id), actions_taken

    async def _execute_tool_call(self, tool_name: str, arguments: str, user_id: str) -> str:
        """Execute a tool call via the MCP server."""
        # Parse arguments
        import json
        args = json.loads(arguments)

        # Add user_id to arguments for authorization
        args['user_id'] = user_id

        # Call the appropriate MCP tool
        if tool_name == "add_task":
            result = await self.mcp_client.call_tool("add_task", args)
        elif tool_name == "list_tasks":
            result = await self.mcp_client.call_tool("list_tasks", args)
        elif tool_name == "complete_task":
            result = await self.mcp_client.call_tool("complete_task", args)
        elif tool_name == "delete_task":
            result = await self.mcp_client.call_tool("delete_task", args)
        elif tool_name == "update_task":
            result = await self.mcp_client.call_tool("update_task", args)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

        return json.dumps(result)

    def _extract_task_id_from_result(self, output: str) -> Optional[str]:
        """Extract task ID from tool call result."""
        import json
        try:
            result = json.loads(output)
            return result.get('task_id')
        except:
            return None

    async def _get_or_create_conversation(self, user_id: str, conversation_id: Optional[str]):
        """Get existing conversation or create new one."""
        from db import get_session

        async with get_session() as session:
            if conversation_id:
                # Get existing conversation
                stmt = select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
                result = await session.execute(stmt)
                conv = result.scalar_one_or_none()

                if not conv:
                    raise ValueError("Conversation not found or access denied")

                return conv
            else:
                # Create new conversation
                new_conv = Conversation(
                    user_id=user_id,
                    title=f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                )
                session.add(new_conv)
                await session.commit()
                await session.refresh(new_conv)

                return new_conv

    async def _load_conversation_history(self, conversation_id: str) -> List[Message]:
        """Load conversation history from database."""
        from db import get_session

        async with get_session() as session:
            stmt = select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.created_at.asc())

            result = await session.execute(stmt)
            return result.scalars().all()
```

### 3. Create Chat Routes

Create `routes/chat.py`:

```python
from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
import openai

from auth.middleware import get_current_user
from db import get_session
from models import Conversation, Message
from schemas import (
    ChatRequest, ChatResponse, ActionResult,
    ConversationListResponse, ConversationSummary,
    ConversationDetailResponse, MessageDetail,
    DeleteConversationResponse
)
from agent import ChatAgent
import os

router = APIRouter(prefix="/{user_id}")

# Initialize OpenAI client
openai_client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize MCP client (placeholder - actual implementation may vary)
# mcp_client = Client(...)  # Implementation depends on MCP SDK specifics

@router.post("/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user)
):
    """
    Send a message to the AI assistant and receive a response.
    Creates a new conversation if no conversation_id is provided.
    """
    # Verify user_id matches JWT token
    if user_id != current_user_id:
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
        # Initialize chat agent
        # Note: MCP client initialization would go here in real implementation
        agent = ChatAgent(openai_client, None)  # Placeholder for MCP client

        # Process the message
        response_text, conversation_id, actions_taken = await agent.process_message(
            user_id=user_id,
            message_content=request.message,
            conversation_id=request.conversation_id
        )

        # Store user message in database
        async with get_session() as session:
            user_message = Message(
                conversation_id=conversation_id,
                role="user",
                content=request.message
            )
            session.add(user_message)

            # Store AI response in database
            ai_message = Message(
                conversation_id=conversation_id,
                role="assistant",
                content=response_text
            )
            session.add(ai_message)

            await session.commit()
            await session.refresh(user_message)
            await session.refresh(ai_message)

        return ChatResponse(
            response=response_text,
            conversation_id=conversation_id,
            message_id=str(ai_message.id),
            actions_taken=actions_taken
        )
    except openai.APIError as e:
        raise HTTPException(status_code=503, detail=f"OpenAI service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/conversations", response_model=ConversationListResponse)
async def list_conversations(
    user_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """
    List all conversations for the specified user.
    """
    # Verify user_id matches JWT token
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="User ID mismatch")

    async with get_session() as session:
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
    current_user_id: str = Depends(get_current_user)
):
    """
    Get a specific conversation with all its messages.
    """
    # Verify user_id matches JWT token
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="User ID mismatch")

    # Validate conversation_id format
    try:
        UUID(conversation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid conversation_id format")

    async with get_session() as session:
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
    current_user_id: str = Depends(get_current_user)
):
    """
    Delete a conversation and all its messages.
    """
    # Verify user_id matches JWT token
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="User ID mismatch")

    # Validate conversation_id format
    try:
        UUID(conversation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid conversation_id format")

    async with get_session() as session:
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
```

### 4. Update Main Application

Modify `routes/__init__.py` to include the chat router:

```python
from .tasks import router as tasks_router
from .auth import router as auth_router
from .chat import router as chat_router  # NEW

__all__ = ["tasks_router", "auth_router", "chat_router"]  # UPDATED
```

Update `main.py` to include the chat routes:

```python
from db import init_db, close_db
from routes import tasks_router, auth_router, chat_router  # UPDATED import

# ...
# In the route registration section:
app.include_router(auth_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")
app.include_router(chat_router, prefix="/api")  # NEW
```

### 5. Update Environment Variables

Add to `.env`:

```env
OPENAI_API_KEY=your-openai-api-key-here
```

## Testing

### Unit Tests

```python
# test_chat_endpoint.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chat_endpoint():
    # Requires authentication
    response = client.post(
        "/api/user123/chat",
        json={"message": "Add a test task"},
        headers={"Authorization": "Bearer valid_jwt_token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "conversation_id" in data
    assert "message_id" in data

def test_list_conversations():
    response = client.get(
        "/api/user123/conversations",
        headers={"Authorization": "Bearer valid_jwt_token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "conversations" in data
    assert "count" in data

def test_get_conversation():
    response = client.get(
        "/api/user123/conversations/conversation-id",
        headers={"Authorization": "Bearer valid_jwt_token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data

def test_delete_conversation():
    response = client.delete(
        "/api/user123/conversations/conversation-id",
        headers={"Authorization": "Bearer valid_jwt_token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "deleted"
```

## Deployment

1. Ensure MCP server is running
2. Set `OPENAI_API_KEY` in environment
3. Run migrations to ensure Conversation and Message tables exist
4. Start the FastAPI server: `uvicorn main:app --reload --port 8000`

## Error Handling

The implementation includes comprehensive error handling:

- **400 Bad Request**: Invalid input (empty message, invalid UUID format)
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: User ID mismatch between URL and JWT token
- **404 Not Found**: Conversation doesn't exist or user doesn't have access
- **503 Service Unavailable**: OpenAI API unavailable
- **500 Internal Server Error**: Unexpected server error

## Security Considerations

- JWT authentication required for all endpoints
- User ID validation to prevent cross-user data access
- Input validation for message content and conversation IDs
- MCP tools validate user authorization before operations
- MCP tools enforce user ownership of tasks