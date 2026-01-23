# Chat API Contract

## Overview
API contract for the chat functionality that connects the frontend ChatKit component to the backend chat endpoint.

## Endpoints

### POST /api/{user_id}/chat
Send a message to the AI assistant and receive a response.

**Authentication**: JWT Bearer token required in Authorization header

**Path Parameters**:
- user_id (string, required): The authenticated user's ID

**Request Body**:
```json
{
  "message": "string, required: The user's message to the AI assistant",
  "conversation_id": "string, optional: The ID of the conversation to continue"
}
```

**Request Headers**:
- Authorization: "Bearer {jwt_token}"
- Content-Type: "application/json"

**Successful Response (200 OK)**:
```json
{
  "response": "string, required: The AI assistant's response",
  "conversation_id": "string, required: The conversation ID (new or existing)",
  "actions_taken": [
    {
      "tool": "string, required: Name of the tool called by the agent",
      "result": "string, required: Result of the tool call (success/error)",
      "task_id": "string, optional: ID of task affected by the tool call"
    }
  ]
}
```

**Error Responses**:
- 400 Bad Request: Invalid request body format
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: User ID in URL doesn't match JWT token
- 404 Not Found: User or conversation not found
- 500 Internal Server Error: Server error during processing

**Example Request**:
```http
POST /api/123e4567-e89b-12d3-a456-426614174000/chat
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "Add buy groceries to my list",
  "conversation_id": "abcde-fghij-klmno-pqrst"
}
```

**Example Response**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "response": "I've added 'buy groceries' to your task list!",
  "conversation_id": "abcde-fghij-klmno-pqrst",
  "actions_taken": [
    {
      "tool": "add_task",
      "result": "success",
      "task_id": "550e8400-e29b-41d4-a716-446655440000"
    }
  ]
}
```

## Frontend Component API

### ChatKit Component Props
The ChatKit component should accept the following props for integration:

**Props Interface**:
```typescript
interface ChatKitProps {
  userId: string;                    // Current user's ID
  onSendMessage?: (message: string) => Promise<any>;  // Handler for sending messages
  placeholder?: string;              // Placeholder text for input
  className?: string;                // Additional CSS classes
}
```

**onSendMessage Handler**:
- Receives the user's message as a string
- Returns a promise that resolves with the assistant's response
- Handles authentication token attachment
- Manages loading states