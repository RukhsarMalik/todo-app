# Data Model: Frontend ChatKit UI

## Entities

### Conversation
Represents a series of exchanges between user and AI assistant, associated with a specific user session.

**Fields**:
- id: string (unique identifier for the conversation)
- createdAt: Date (timestamp when conversation started)
- updatedAt: Date (timestamp of last activity)
- title: string (optional, auto-generated or user-defined)

**Relationships**:
- Contains multiple Messages
- Associated with one User (via user session)

**Validation Rules**:
- id must be unique
- createdAt must be in the past
- updatedAt must be >= createdAt

### Message
Individual text communication in the conversation, either from user or assistant.

**Fields**:
- id: string (unique identifier for the message)
- role: 'user' | 'assistant' (indicates sender)
- content: string (the actual message text)
- timestamp: Date (when the message was sent/received)

**Relationships**:
- Belongs to one Conversation
- Part of ordered sequence within Conversation

**State Transitions**:
- When sent: role='user', content=filled, timestamp=now
- When received: role='assistant', content=filled, timestamp=now

**Validation Rules**:
- role must be either 'user' or 'assistant'
- content must not be empty
- timestamp must be in the past

### User Session
Authentication token that validates user identity and authorizes access to chat functionality.

**Fields**:
- userId: string (unique identifier from authentication system)
- token: string (JWT token for API authentication)
- isValid: boolean (whether the token is currently valid)
- expiresAt: Date (token expiration timestamp)

**Validation Rules**:
- userId must exist in the system
- token must be valid JWT
- token must not be expired
- token must have chat access permissions