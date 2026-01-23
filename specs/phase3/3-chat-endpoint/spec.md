# Feature Specification: Chat Endpoint with OpenAI Agent

**Module**: Phase III Module 3
**Created**: 2026-01-23
**Status**: Draft
**Dependencies**: Phase III Module 1 (Chat Database), Phase III Module 2 (MCP Server), Phase II (Auth, Tasks API)

## Overview

This module creates a chat endpoint that integrates OpenAI's Agents SDK with the MCP server tools. Users can send natural language messages to an AI assistant that can manage their tasks through conversation. The endpoint stores conversation history using the Conversation and Message models from Module 1.

### Scope

**INCLUDED:**
- POST `/api/{user_id}/chat` endpoint for sending messages
- GET `/api/{user_id}/conversations` endpoint for listing conversations
- GET `/api/{user_id}/conversations/{conversation_id}` endpoint for retrieving messages
- OpenAI Agent with MCP tool integration
- Conversation and message persistence
- JWT authentication (reuse existing middleware)
- Stateless server design (conversation history loaded from database)

**NOT INCLUDED:**
- Streaming responses (future enhancement)
- WebSocket real-time chat (future enhancement)
- Frontend integration (Module 4)
- Multiple AI models/providers (only OpenAI)
- File attachments or image processing

## User Scenarios & Testing

### User Story 1 - Send Chat Message (Priority: P1)

A user wants to have a conversation with an AI assistant about their tasks.

**Why this priority**: Core functionality - this is the primary interaction point for the AI chatbot feature.

**Independent Test**: Can be tested by calling the chat endpoint with a message, verifying the AI responds and the message is stored.

**Acceptance Scenarios**:

1. **Given** a valid user with JWT token, **When** POST `/api/{user_id}/chat` is called with a message and no conversation_id, **Then** a new conversation is created, the message is stored, and the AI response is returned
2. **Given** an existing conversation_id, **When** POST `/api/{user_id}/chat` is called with a follow-up message, **Then** the message is added to the existing conversation
3. **Given** a message like "Add a task to buy groceries", **When** POST `/api/{user_id}/chat` is called, **Then** the AI uses the add_task MCP tool and responds confirming the task was created
4. **Given** a message like "What are my pending tasks?", **When** POST `/api/{user_id}/chat` is called, **Then** the AI uses the list_tasks MCP tool and responds with the user's tasks

---

### User Story 2 - List Conversations (Priority: P1)

A user wants to see their previous chat conversations.

**Why this priority**: Core functionality - users need to access their conversation history.

**Independent Test**: Can be tested by creating conversations, then calling the list endpoint and verifying all conversations are returned.

**Acceptance Scenarios**:

1. **Given** a user with existing conversations, **When** GET `/api/{user_id}/conversations` is called, **Then** all conversations for that user are returned sorted by updated_at descending
2. **Given** a user with no conversations, **When** GET `/api/{user_id}/conversations` is called, **Then** an empty array is returned
3. **Given** multiple users with conversations, **When** GET `/api/{user_id}/conversations` is called, **Then** only conversations belonging to that user are returned

---

### User Story 3 - Get Conversation History (Priority: P1)

A user wants to view all messages in a specific conversation.

**Why this priority**: Core functionality - users need to see the full context of a conversation.

**Independent Test**: Can be tested by creating a conversation with messages, then retrieving it and verifying all messages are returned in order.

**Acceptance Scenarios**:

1. **Given** an existing conversation with messages, **When** GET `/api/{user_id}/conversations/{conversation_id}` is called, **Then** all messages are returned in chronological order (oldest first)
2. **Given** a conversation_id that doesn't exist, **When** GET is called, **Then** 404 Not Found is returned
3. **Given** a conversation belonging to another user, **When** GET is called, **Then** 404 Not Found is returned (no information leakage)

---

### User Story 4 - AI Task Management (Priority: P1)

A user wants the AI to perform task operations through natural language.

**Why this priority**: This is the core value proposition - AI-powered task management.

**Independent Test**: Can be tested by sending task-related messages and verifying the correct MCP tools are invoked.

**Acceptance Scenarios**:

1. **Given** user says "Create a task: Buy milk", **When** processed, **Then** AI calls add_task tool with title="Buy milk" and confirms creation
2. **Given** user says "Show me my tasks", **When** processed, **Then** AI calls list_tasks tool and formats the response conversationally
3. **Given** user says "Mark task 5 as done", **When** processed, **Then** AI calls complete_task tool with task_id=5 and confirms completion
4. **Given** user says "Delete task 3", **When** processed, **Then** AI calls delete_task tool with task_id=3 and confirms deletion
5. **Given** user says "Change task 2 title to 'Buy organic milk'", **When** processed, **Then** AI calls update_task tool and confirms the update

---

### User Story 5 - Delete Conversation (Priority: P2)

A user wants to delete a conversation they no longer need.

**Why this priority**: Secondary functionality - users should be able to clean up their conversation history.

**Independent Test**: Can be tested by creating a conversation, deleting it, and verifying it no longer exists.

**Acceptance Scenarios**:

1. **Given** an existing conversation, **When** DELETE `/api/{user_id}/conversations/{conversation_id}` is called, **Then** the conversation and all its messages are deleted
2. **Given** a conversation_id that doesn't exist, **When** DELETE is called, **Then** 404 Not Found is returned
3. **Given** a conversation belonging to another user, **When** DELETE is called, **Then** 404 Not Found is returned

---

### Edge Cases

- What happens when OpenAI API is unavailable? Return 503 Service Unavailable with appropriate message
- What happens when message content is empty? Return 400 Bad Request with validation error
- What happens when message exceeds 10,000 characters? Return 400 Bad Request with validation error
- What happens when conversation_id format is invalid? Return 400 Bad Request
- What happens when JWT token is missing? Return 401 Unauthorized
- What happens when user_id in URL doesn't match JWT? Return 403 Forbidden
- What happens when MCP tool execution fails? AI explains the error in its response

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a POST `/api/{user_id}/chat` endpoint that accepts message content and optional conversation_id
- **FR-002**: System MUST create a new Conversation when no conversation_id is provided
- **FR-003**: System MUST store user messages with role="user" in the messages table
- **FR-004**: System MUST store AI responses with role="assistant" in the messages table
- **FR-005**: System MUST integrate with OpenAI Agents SDK for AI responses
- **FR-006**: System MUST connect OpenAI Agent to MCP server tools (add_task, list_tasks, complete_task, delete_task, update_task)
- **FR-007**: System MUST load conversation history from database for each request (stateless design)
- **FR-008**: System MUST provide GET `/api/{user_id}/conversations` to list user's conversations
- **FR-009**: System MUST provide GET `/api/{user_id}/conversations/{conversation_id}` to get messages
- **FR-010**: System MUST provide DELETE `/api/{user_id}/conversations/{conversation_id}` to remove conversations
- **FR-011**: All endpoints MUST require JWT authentication
- **FR-012**: All endpoints MUST verify user_id in URL matches JWT token user_id
- **FR-013**: System MUST pass user_id to all MCP tool calls (ownership enforcement)

### Non-Functional Requirements

- **NFR-001**: Chat response time SHOULD be under 10 seconds for typical requests
- **NFR-002**: System MUST handle OpenAI API failures gracefully with appropriate error messages
- **NFR-003**: System MUST NOT expose internal error details to users
- **NFR-004**: System MUST log all MCP tool invocations for debugging

### Key Entities

- **Conversation**: Existing entity from Module 1 - id (UUID), user_id, title, created_at, updated_at
- **Message**: Existing entity from Module 1 - id (UUID), conversation_id, role, content, created_at
- **ChatRequest**: New Pydantic schema - message (str), conversation_id (optional UUID)
- **ChatResponse**: New Pydantic schema - response (str), conversation_id (UUID), message_id (UUID)

## API Contracts

### POST /api/{user_id}/chat

Send a message and receive AI response.

**Request:**
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": "optional-uuid-string"
}
```

**Response (200):**
```json
{
  "response": "I've created a new task 'Buy groceries' for you. Is there anything else you'd like to add?",
  "conversation_id": "uuid-string",
  "message_id": "uuid-string"
}
```

**Error Responses:**
- 400: Invalid request (empty message, invalid conversation_id)
- 401: Missing or invalid JWT token
- 403: user_id mismatch with JWT
- 404: conversation_id not found
- 503: OpenAI service unavailable

### GET /api/{user_id}/conversations

List user's conversations.

**Response (200):**
```json
{
  "conversations": [
    {
      "id": "uuid-string",
      "title": "Task management conversation",
      "created_at": "2026-01-23T10:00:00Z",
      "updated_at": "2026-01-23T11:30:00Z",
      "message_count": 5
    }
  ],
  "count": 1
}
```

### GET /api/{user_id}/conversations/{conversation_id}

Get conversation with all messages.

**Response (200):**
```json
{
  "id": "uuid-string",
  "title": "Task management conversation",
  "created_at": "2026-01-23T10:00:00Z",
  "updated_at": "2026-01-23T11:30:00Z",
  "messages": [
    {
      "id": "uuid-string",
      "role": "user",
      "content": "Add a task to buy groceries",
      "created_at": "2026-01-23T10:00:00Z"
    },
    {
      "id": "uuid-string",
      "role": "assistant",
      "content": "I've created a new task 'Buy groceries' for you.",
      "created_at": "2026-01-23T10:00:01Z"
    }
  ]
}
```

### DELETE /api/{user_id}/conversations/{conversation_id}

Delete a conversation and all its messages.

**Response (200):**
```json
{
  "status": "deleted",
  "conversation_id": "uuid-string"
}
```

## Success Criteria

### Measurable Outcomes

- **SC-001**: Chat endpoint responds with AI-generated content
- **SC-002**: User and assistant messages are persisted in database
- **SC-003**: AI can successfully invoke all 5 MCP tools through conversation
- **SC-004**: Conversation history is loaded correctly for follow-up messages
- **SC-005**: List conversations returns correct data for authenticated user
- **SC-006**: Get conversation returns all messages in chronological order
- **SC-007**: Delete conversation removes both conversation and messages
- **SC-008**: JWT authentication is enforced on all endpoints
- **SC-009**: user_id/JWT mismatch returns 403 Forbidden

## Assumptions

- OpenAI API key is available via environment variable (OPENAI_API_KEY)
- OpenAI Agents SDK (`openai-agents`) is compatible with Python 3.12+
- MCP server from Module 2 is running and accessible
- The MCP server's stdio transport can be connected programmatically
- Existing JWT middleware from Phase II can be reused
- Database connection pooling handles concurrent chat requests

## Technical Approach

### OpenAI Agent + MCP Integration

The OpenAI Agents SDK provides a way to create agents that can use tools. The MCP SDK provides a way to connect to MCP servers. The integration approach:

1. Create an OpenAI Agent with instructions for task management
2. Connect to MCP server tools using MCP client
3. Register MCP tools as OpenAI Agent tools
4. Run the agent with user message and conversation history
5. Return the agent's response

### Stateless Design

Each request:
1. Loads conversation history from database
2. Formats history as OpenAI messages
3. Adds new user message
4. Runs OpenAI Agent
5. Stores both user message and AI response
6. Returns response to client

This ensures horizontal scalability and no server-side session state.

## File Structure

```
phase-3/backend/
├── routes/
│   ├── __init__.py      (MODIFY - add chat router)
│   └── chat.py          (NEW - chat endpoints)
├── schemas.py           (MODIFY - add chat schemas)
├── agent.py             (NEW - OpenAI Agent + MCP integration)
├── mcp_server.py        (EXISTING - MCP tools from Module 2)
├── models.py            (EXISTING - Conversation, Message from Module 1)
└── db.py                (EXISTING - database session)
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| OPENAI_API_KEY | Yes | OpenAI API key for Agents SDK |
| DATABASE_URL | Yes | Neon PostgreSQL connection string |
| JWT_SECRET_KEY | Yes | JWT signing secret |
