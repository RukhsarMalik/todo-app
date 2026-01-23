# Data Model: MCP Server with Task Tools

**Date**: 2026-01-23
**Feature**: Phase III Module 2 - MCP Server
**Spec**: [spec.md](./spec.md)

## Overview

This module reuses the existing Task model from Phase II. This document defines the MCP tool schemas and response structures.

## Existing Entity (Reused)

### Task (from Phase II)

**Location**: `phase-3/backend/models.py`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | int | PK, auto-increment | Unique task identifier |
| user_id | str(255) | NOT NULL, indexed | Owner reference |
| title | str(200) | NOT NULL, 1-200 chars | Task title |
| description | str(1000) | nullable | Task description |
| completed | bool | default=False | Completion status |
| created_at | datetime | NOT NULL | Creation timestamp |
| updated_at | datetime | NOT NULL | Last update timestamp |

## MCP Tool Schemas

### Tool: add_task

**Purpose**: Create a new task for a user

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "The user's unique identifier"
    },
    "title": {
      "type": "string",
      "description": "The task title (required, max 200 chars)",
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "description": "Optional task description (max 1000 chars)",
      "maxLength": 1000
    }
  },
  "required": ["user_id", "title"]
}
```

**Output Schema**:
```json
{
  "task_id": "integer",
  "status": "created",
  "title": "string"
}
```

---

### Tool: list_tasks

**Purpose**: Retrieve user's tasks with optional filtering

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "The user's unique identifier"
    },
    "status": {
      "type": "string",
      "enum": ["all", "pending", "completed"],
      "description": "Filter tasks by status",
      "default": "all"
    }
  },
  "required": ["user_id"]
}
```

**Output Schema**:
```json
{
  "tasks": [
    {
      "id": "integer",
      "title": "string",
      "description": "string | null",
      "completed": "boolean",
      "created_at": "datetime"
    }
  ],
  "count": "integer"
}
```

---

### Tool: complete_task

**Purpose**: Mark a task as completed

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "The user's unique identifier"
    },
    "task_id": {
      "type": "integer",
      "description": "The task ID to complete"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema**:
```json
{
  "task_id": "integer",
  "status": "completed",
  "title": "string"
}
```

---

### Tool: delete_task

**Purpose**: Remove a task from the database

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "The user's unique identifier"
    },
    "task_id": {
      "type": "integer",
      "description": "The task ID to delete"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema**:
```json
{
  "task_id": "integer",
  "status": "deleted"
}
```

---

### Tool: update_task

**Purpose**: Modify task title and/or description

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "The user's unique identifier"
    },
    "task_id": {
      "type": "integer",
      "description": "The task ID to update"
    },
    "title": {
      "type": "string",
      "description": "New task title (optional)",
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "description": "New task description (optional)",
      "maxLength": 1000
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema**:
```json
{
  "task_id": "integer",
  "status": "updated",
  "title": "string"
}
```

---

## Error Response Schema

All tools return errors in this format:

```json
{
  "error": true,
  "message": "Human-readable error description"
}
```

**Error Cases**:

| Error | Message |
|-------|---------|
| Task not found | "Task not found or access denied" |
| Empty title | "Title is required" |
| Title too long | "Title exceeds 200 character limit" |
| Description too long | "Description exceeds 1000 character limit" |
| Invalid user_id | "User ID is required" |
| No updates provided | "No updates provided (title or description required)" |
| Database error | "Failed to [operation] task" |

---

## Validation Rules

### user_id Validation
- MUST NOT be empty or whitespace-only
- MUST be validated on every tool call

### title Validation
- MUST NOT be empty or whitespace-only
- MUST NOT exceed 200 characters
- Leading/trailing whitespace stripped

### description Validation
- MAY be empty or null
- MUST NOT exceed 1000 characters if provided
- Leading/trailing whitespace stripped

### task_id Validation
- MUST be a valid integer
- MUST belong to the specified user_id
- Task not found = access denied (no information leakage)
