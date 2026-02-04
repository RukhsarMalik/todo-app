"""
Chat agent for integrating OpenAI's Assistant API with MCP tools.

This module implements a ChatAgent class that connects OpenAI's Assistant API
with the existing MCP server tools to enable AI-powered task management.
The agent follows a stateless design, loading conversation history from
the database for each request.

Usage:
    from agent import ChatAgent
    from openai import AsyncOpenAI

    openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # mcp_client = await initialize_mcp_client()  # Implementation depends on MCP SDK

    agent = ChatAgent(openai_client, mcp_client)
    response, conversation_id, actions = await agent.process_message(
        user_id="user123",
        message_content="Add buy groceries to my list",
        conversation_id="optional-existing-conversation-id"
    )
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID

import openai
from mcp import ClientSession
from sqlmodel import select

from models import Conversation, Message
from schemas import ActionResult

logger = logging.getLogger(__name__)


class ChatAgent:
    """
    Chat agent that integrates OpenAI's Assistant API with MCP tools.

    The agent handles user messages, loads conversation history from the database,
    processes the message through OpenAI's Assistant API with MCP tools,
    and returns the AI response along with any actions taken.
    """

    def __init__(self, openai_client: openai.AsyncOpenAI, mcp_client: ClientSession):
        """
        Initialize the chat agent.

        Args:
            openai_client: Initialized OpenAI async client
            mcp_client: Initialized MCP client for tool calls
        """
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
        args = json.loads(arguments)

        # Add user_id to arguments for authorization
        args['user_id'] = user_id

        # Call the appropriate MCP tool
        # Note: The exact method name may vary depending on the MCP SDK implementation
        # This is a placeholder that should be replaced with the correct method
        if tool_name == "add_task":
            # result = await self.mcp_client.call_tool("add_task", args)
            result = {"status": "mock", "message": "add_task called", "task_id": "mock_id"}  # Mock for now
        elif tool_name == "list_tasks":
            # result = await self.mcp_client.call_tool("list_tasks", args)
            result = {"status": "mock", "message": "list_tasks called", "tasks": []}  # Mock for now
        elif tool_name == "complete_task":
            # result = await self.mcp_client.call_tool("complete_task", args)
            result = {"status": "mock", "message": "complete_task called"}  # Mock for now
        elif tool_name == "delete_task":
            # result = await self.mcp_client.call_tool("delete_task", args)
            result = {"status": "mock", "message": "delete_task called"}  # Mock for now
        elif tool_name == "update_task":
            # result = await self.mcp_client.call_tool("update_task", args)
            result = {"status": "mock", "message": "update_task called"}  # Mock for now
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

        return json.dumps(result)

    def _extract_task_id_from_result(self, output: str) -> Optional[str]:
        """Extract task ID from tool call result."""
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