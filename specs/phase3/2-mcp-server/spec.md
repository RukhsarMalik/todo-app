# Feature Specification: MCP Server with Task Tools

**Module**: Phase III Module 2
**Created**: 2026-01-23
**Status**: Draft
**Dependencies**: Phase III Module 1 (Chat Database), Phase II (Task model, db.py)

## Overview

This module creates an MCP (Model Context Protocol) server that exposes task management operations as tools for AI agents. The MCP server allows AI assistants to perform CRUD operations on user tasks through a standardized protocol.

### Scope

**INCLUDED:**
- MCP server setup using official Python SDK
- 5 MCP tools: add_task, list_tasks, complete_task, delete_task, update_task
- Tools reuse existing Task model and db.py from Phase II
- User ID validation for all tool operations

**NOT INCLUDED:**
- Chat endpoint (Module 3)
- OpenAI Agent integration (Module 3)
- Frontend changes (Module 4)

## User Scenarios & Testing

### User Story 1 - Add Task Tool (Priority: P1)

An AI agent needs to create a new task for a user in the todo system.

**Why this priority**: Core functionality - creating tasks is the primary write operation and foundational for the todo system.

**Independent Test**: Can be tested by calling the add_task tool with valid user_id and title, then verifying the task exists in the database.

**Acceptance Scenarios**:

1. **Given** a valid user_id and task title, **When** add_task is called, **Then** a new task is created in the database and the tool returns task_id, status="created", and title
2. **Given** a valid user_id, title, and optional description, **When** add_task is called, **Then** the task is created with both title and description stored
3. **Given** an empty title, **When** add_task is called, **Then** the tool returns an error indicating title is required

---

### User Story 2 - List Tasks Tool (Priority: P1)

An AI agent needs to retrieve a user's tasks to understand their current todo items.

**Why this priority**: Core functionality - listing tasks is essential for the AI to understand user context before making suggestions or modifications.

**Independent Test**: Can be tested by creating tasks for a user, then calling list_tasks and verifying the correct tasks are returned.

**Acceptance Scenarios**:

1. **Given** a user with existing tasks, **When** list_tasks is called with status="all", **Then** all tasks for that user are returned
2. **Given** a user with completed and pending tasks, **When** list_tasks is called with status="pending", **Then** only incomplete tasks are returned
3. **Given** a user with completed and pending tasks, **When** list_tasks is called with status="completed", **Then** only completed tasks are returned
4. **Given** a user with no tasks, **When** list_tasks is called, **Then** an empty array is returned

---

### User Story 3 - Complete Task Tool (Priority: P1)

An AI agent needs to mark a task as completed when a user indicates they've finished it.

**Why this priority**: Core functionality - completing tasks is the primary status change operation and essential for task workflow.

**Independent Test**: Can be tested by creating a pending task, calling complete_task, then verifying the task's completed field is true.

**Acceptance Scenarios**:

1. **Given** an existing pending task, **When** complete_task is called with valid user_id and task_id, **Then** the task is marked completed and returns task_id, status="completed", and title
2. **Given** a task that doesn't exist, **When** complete_task is called, **Then** the tool returns an error indicating task not found
3. **Given** a task belonging to a different user, **When** complete_task is called, **Then** the tool returns an error (task not found for this user)

---

### User Story 4 - Delete Task Tool (Priority: P2)

An AI agent needs to remove a task when a user no longer wants it in their list.

**Why this priority**: Secondary functionality - deletion is less common than creation/completion but still important for list management.

**Independent Test**: Can be tested by creating a task, calling delete_task, then verifying the task no longer exists in the database.

**Acceptance Scenarios**:

1. **Given** an existing task, **When** delete_task is called with valid user_id and task_id, **Then** the task is removed from the database and returns task_id and status="deleted"
2. **Given** a task that doesn't exist, **When** delete_task is called, **Then** the tool returns an error indicating task not found
3. **Given** a task belonging to a different user, **When** delete_task is called, **Then** the tool returns an error (task not found for this user)

---

### User Story 5 - Update Task Tool (Priority: P2)

An AI agent needs to modify a task's title or description when a user wants to change details.

**Why this priority**: Secondary functionality - updates are less common but needed for maintaining accurate task information.

**Independent Test**: Can be tested by creating a task, calling update_task with new title/description, then verifying the changes are persisted.

**Acceptance Scenarios**:

1. **Given** an existing task, **When** update_task is called with a new title, **Then** the task title is updated and returns task_id, status="updated", and new title
2. **Given** an existing task, **When** update_task is called with a new description, **Then** the task description is updated
3. **Given** an existing task, **When** update_task is called with both title and description, **Then** both fields are updated
4. **Given** a task that doesn't exist, **When** update_task is called, **Then** the tool returns an error indicating task not found
5. **Given** update_task called with no changes (empty title and description), **When** executed, **Then** the tool returns an error indicating no updates provided

---

### Edge Cases

- What happens when user_id is empty or invalid format? Tool returns validation error
- What happens when database connection fails? Tool returns error with appropriate message
- What happens when title exceeds maximum length (200 chars)? Tool returns validation error
- What happens when description exceeds maximum length (1000 chars)? Tool returns validation error
- What happens when task_id format is invalid? Tool returns validation error

## Requirements

### Functional Requirements

- **FR-001**: System MUST expose an MCP server that can be connected to by MCP-compatible clients
- **FR-002**: System MUST provide an `add_task` tool that creates tasks in the database
- **FR-003**: System MUST provide a `list_tasks` tool that retrieves tasks filtered by status
- **FR-004**: System MUST provide a `complete_task` tool that marks tasks as completed
- **FR-005**: System MUST provide a `delete_task` tool that removes tasks from the database
- **FR-006**: System MUST provide an `update_task` tool that modifies task title/description
- **FR-007**: All tools MUST validate that user_id is provided and non-empty
- **FR-008**: All tools MUST only operate on tasks belonging to the specified user_id
- **FR-009**: All tools MUST return structured responses with task_id and status fields
- **FR-010**: System MUST use the existing Task model from phase-3/backend/models.py
- **FR-011**: System MUST use the existing database session from phase-3/backend/db.py

### Key Entities

- **Task**: Existing entity from Phase II - id, user_id, title, description, completed, created_at, updated_at
- **MCP Tool**: Protocol-defined tool with name, description, and parameters schema
- **Tool Response**: Structured response containing task_id, status, and optional task data

## Success Criteria

### Measurable Outcomes

- **SC-001**: MCP server starts successfully and accepts connections
- **SC-002**: All 5 tools are discoverable via MCP tool listing
- **SC-003**: add_task creates tasks that persist in the database
- **SC-004**: list_tasks returns correct tasks based on filter criteria
- **SC-005**: complete_task successfully updates task completion status
- **SC-006**: delete_task removes tasks from database permanently
- **SC-007**: update_task modifies task fields correctly
- **SC-008**: All tools reject operations on tasks not owned by the specified user_id
- **SC-009**: All tools return appropriate error messages for invalid inputs

## Assumptions

- The MCP Python SDK is available and compatible with the project's Python version (3.12+)
- The existing Task model and database connection (db.py) work correctly
- User IDs are validated at a higher level (authentication) - tools trust the provided user_id
- MCP server runs as a separate process from the FastAPI server
- Standard MCP transport (stdio) is sufficient for this implementation

## File Structure

```
phase-3/backend/
├── mcp_server.py    (NEW - MCP server with task tools)
├── models.py        (EXISTING - reuse Task model)
└── db.py            (EXISTING - reuse database session)
```
