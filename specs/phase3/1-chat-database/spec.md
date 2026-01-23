# Feature Specification: Chat Database Extension

**Feature Branch**: `006-chat-database`
**Created**: 2026-01-22
**Status**: Draft
**Input**: User description: "Phase III Module 1 - Database Extension for Chat: Add conversations and messages tables to support AI chatbot conversation history persistence"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start New Conversation (Priority: P1)

As a user, I want to start a new chat conversation so that I can interact with the AI chatbot to manage my tasks through natural language.

**Why this priority**: Core functionality - without the ability to create conversations, no chat features can work. This is the foundation for the entire Phase III chatbot system.

**Independent Test**: Can be fully tested by creating a conversation record for a user and verifying it persists to the database with correct user association.

**Acceptance Scenarios**:

1. **Given** an authenticated user with user_id "abc-123", **When** they initiate a new chat, **Then** a conversation record is created with the user's ID and a timestamp.
2. **Given** an authenticated user, **When** a conversation is created, **Then** the conversation ID is returned and can be used for subsequent messages.
3. **Given** a user_id that doesn't exist in the users table, **When** attempting to create a conversation, **Then** the operation fails with a foreign key violation.

---

### User Story 2 - Store Chat Messages (Priority: P1)

As a user, I want my chat messages and AI responses to be saved so that I can see my conversation history and the AI can maintain context.

**Why this priority**: Essential for conversation persistence - messages are the core data that needs to be stored for the chatbot to function properly.

**Independent Test**: Can be fully tested by adding messages to a conversation and retrieving them in order.

**Acceptance Scenarios**:

1. **Given** an existing conversation, **When** a user sends a message, **Then** a message record is created with role "user" and the message content.
2. **Given** an existing conversation, **When** the AI responds, **Then** a message record is created with role "assistant" and the response content.
3. **Given** an existing conversation with multiple messages, **When** messages are retrieved, **Then** they are returned in chronological order (oldest first).
4. **Given** a conversation_id that doesn't exist, **When** attempting to add a message, **Then** the operation fails with a foreign key violation.

---

### User Story 3 - Retrieve Conversation History (Priority: P2)

As a user, I want to view my past conversations so that I can continue where I left off or reference previous interactions.

**Why this priority**: Important for user experience and AI context loading, but the system can function minimally without history retrieval initially.

**Independent Test**: Can be fully tested by creating multiple conversations with messages and retrieving them for a specific user.

**Acceptance Scenarios**:

1. **Given** a user with multiple conversations, **When** they request their conversation list, **Then** all their conversations are returned sorted by most recent first.
2. **Given** a specific conversation ID, **When** the user requests that conversation, **Then** all messages in that conversation are returned in chronological order.
3. **Given** a user with no conversations, **When** they request their conversation list, **Then** an empty list is returned.

---

### User Story 4 - Delete Conversation (Priority: P3)

As a user, I want to delete a conversation so that I can remove unwanted chat history.

**Why this priority**: Nice-to-have feature for user control over their data; not essential for core chatbot functionality.

**Independent Test**: Can be fully tested by creating a conversation with messages, deleting it, and verifying cascade deletion.

**Acceptance Scenarios**:

1. **Given** an existing conversation owned by the user, **When** they delete it, **Then** the conversation and all its messages are removed.
2. **Given** a conversation owned by another user, **When** attempting to delete it, **Then** the operation fails with a 403 Forbidden error.

---

### Edge Cases

- What happens when a message content is empty? System MUST reject empty messages.
- What happens when message content exceeds maximum length? System MUST enforce a reasonable limit (e.g., 10,000 characters).
- How does the system handle concurrent message additions to the same conversation? Messages MUST be timestamped and ordered correctly.
- What happens when a user is deleted? Conversations and messages MUST be cascade deleted.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST create a `conversations` table with columns: id (UUID, PK), user_id (UUID, FK to users), created_at (timestamp with timezone), updated_at (timestamp with timezone).
- **FR-002**: System MUST create a `messages` table with columns: id (UUID, PK), conversation_id (UUID, FK to conversations), role (varchar - "user" or "assistant"), content (text), created_at (timestamp with timezone).
- **FR-003**: System MUST enforce foreign key constraint from conversations.user_id to users.id with CASCADE delete.
- **FR-004**: System MUST enforce foreign key constraint from messages.conversation_id to conversations.id with CASCADE delete.
- **FR-005**: System MUST index conversations by user_id for efficient user conversation listing.
- **FR-006**: System MUST index messages by conversation_id for efficient message retrieval.
- **FR-007**: System MUST validate message role is one of: "user", "assistant", "system".
- **FR-008**: System MUST reject messages with empty content.
- **FR-009**: System MUST limit message content to 10,000 characters maximum.
- **FR-010**: System MUST automatically set created_at timestamps on record creation.

### Key Entities

- **Conversation**: Represents a chat session between a user and the AI. Contains reference to the owning user and timestamp of creation. One user can have many conversations.
- **Message**: Represents a single message within a conversation. Contains the role (who sent it), content (the actual text), and timestamp. One conversation has many messages in chronological order.

### Entity Relationships

```
User (1) ----< (N) Conversation (1) ----< (N) Message
```

- A User can have zero or more Conversations
- A Conversation belongs to exactly one User
- A Conversation can have zero or more Messages
- A Message belongs to exactly one Conversation

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Database migration creates both tables successfully without errors.
- **SC-002**: SQLModel/Pydantic models pass type validation for all fields.
- **SC-003**: Foreign key constraints prevent orphaned records (verified by constraint violation tests).
- **SC-004**: Cascade delete removes all related messages when a conversation is deleted.
- **SC-005**: Query for user's conversations returns results in under 100ms for up to 1000 conversations.
- **SC-006**: Query for conversation messages returns results in under 100ms for up to 1000 messages.
- **SC-007**: All CRUD operations for conversations and messages work correctly via SQLModel async session.
- **SC-008**: Existing users table and tasks table remain unaffected by migration.

## Technical Notes

### Integration with Existing Schema

The new tables extend the existing Phase II database schema:

```sql
-- Existing tables (DO NOT MODIFY)
-- users: id, email, hashed_password, created_at
-- tasks: id, user_id, title, description, completed, created_at, updated_at

-- New tables for Phase III
-- conversations: id, user_id, created_at, updated_at
-- messages: id, conversation_id, role, content, created_at
```

### SQLModel Implementation

Models should follow the existing patterns in `phase-2/backend/models.py`:
- Inherit from `SQLModel` with `table=True`
- Use `Field(default_factory=uuid4)` for UUID primary keys
- Use `Field(default_factory=datetime.utcnow)` for timestamps
- Include explicit `__tablename__` for clarity

### Migration Strategy

1. Create new model classes in existing models.py
2. Run `init_db.py` to create tables (SQLModel.metadata.create_all)
3. Verify with test script

### API Endpoints (Preview - for future spec)

The following endpoints will be needed (to be specified in Module 2):
- `POST /api/{user_id}/conversations` - Create conversation
- `GET /api/{user_id}/conversations` - List conversations
- `GET /api/{user_id}/conversations/{id}` - Get conversation with messages
- `DELETE /api/{user_id}/conversations/{id}` - Delete conversation
- `POST /api/{user_id}/conversations/{id}/messages` - Add message (internal use by chat endpoint)
