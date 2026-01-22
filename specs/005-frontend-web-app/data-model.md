# Data Model: Frontend Web Application

**Feature**: 005-frontend-web-app
**Date**: 2026-01-19
**Phase**: 1 - Design

---

## Overview

This document defines the TypeScript interfaces and types for the frontend application. These types mirror the backend Pydantic schemas and SQLModel models to ensure type-safe API communication.

---

## Core Entities

### Task

Represents a todo item. Matches backend `TaskResponse` schema.

```typescript
// lib/types.ts

/**
 * Task entity from backend API.
 * Represents a single todo item belonging to a user.
 */
export interface Task {
  /** Unique task identifier (auto-increment from backend) */
  id: number;

  /** Reference to the task owner (UUID string) */
  user_id: string;

  /** Task title (1-200 characters) */
  title: string;

  /** Optional task description (max 1000 characters) */
  description: string | null;

  /** Whether the task is completed */
  completed: boolean;

  /** ISO timestamp when task was created (UTC) */
  created_at: string;

  /** ISO timestamp when task was last modified (UTC) */
  updated_at: string;
}
```

### User (Auth Context)

Represents the authenticated user state stored in React Context.

```typescript
// lib/types.ts

/**
 * User authentication state.
 * Stored in AuthContext and localStorage.
 */
export interface User {
  /** User's unique identifier (UUID string) */
  userId: string;

  /** User's email address */
  email: string;

  /** Optional display name */
  name?: string;
}

/**
 * Complete authentication state.
 * Managed by AuthProvider context.
 */
export interface AuthState {
  /** JWT access token (null if not authenticated) */
  token: string | null;

  /** Current user info (null if not authenticated) */
  user: User | null;

  /** Convenience flag: true if token exists */
  isAuthenticated: boolean;

  /** True during initial auth state restoration */
  isLoading: boolean;
}
```

---

## API Request Types

### Authentication Requests

```typescript
// lib/types.ts

/**
 * Request body for POST /api/auth/signup
 */
export interface SignupRequest {
  /** User's email address */
  email: string;

  /** Password (minimum 8 characters) */
  password: string;

  /** Optional display name */
  name?: string;
}

/**
 * Request body for POST /api/auth/login
 */
export interface LoginRequest {
  /** Registered email address */
  email: string;

  /** Account password */
  password: string;
}
```

### Task Requests

```typescript
// lib/types.ts

/**
 * Request body for POST /api/{user_id}/tasks
 */
export interface TaskCreateRequest {
  /** Task title (1-200 characters, required) */
  title: string;

  /** Optional description (max 1000 characters) */
  description?: string;
}

/**
 * Request body for PUT /api/{user_id}/tasks/{id}
 */
export interface TaskUpdateRequest {
  /** New title (1-200 characters, optional) */
  title?: string;

  /** New description (max 1000 characters, optional) */
  description?: string;
}

/**
 * Request body for PATCH /api/{user_id}/tasks/{id}/complete
 */
export interface TaskToggleRequest {
  /** New completion status */
  completed: boolean;
}
```

---

## API Response Types

### Authentication Responses

```typescript
// lib/types.ts

/**
 * Response from POST /api/auth/signup and POST /api/auth/login
 */
export interface TokenResponse {
  /** JWT access token */
  access_token: string;

  /** Token type (always "bearer") */
  token_type: string;

  /** User's unique identifier */
  user_id: string;

  /** User's email address */
  email: string;
}

/**
 * Response from POST /api/auth/logout
 */
export interface MessageResponse {
  /** Success message */
  message: string;
}
```

### Error Responses

```typescript
// lib/types.ts

/**
 * Standard error response from FastAPI.
 * HTTPException responses follow this format.
 */
export interface ErrorResponse {
  /** Error message */
  detail: string;
}

/**
 * Custom API error for frontend error handling.
 */
export class ApiError extends Error {
  constructor(
    public status: number,
    public detail: string
  ) {
    super(detail);
    this.name = 'ApiError';
  }
}
```

---

## Query Parameters

```typescript
// lib/types.ts

/**
 * Filter options for task list (GET /api/{user_id}/tasks)
 */
export type StatusFilter = 'all' | 'pending' | 'completed';

/**
 * Sort field options
 */
export type SortField = 'created' | 'title';

/**
 * Sort order options
 */
export type SortOrder = 'asc' | 'desc';

/**
 * Query parameters for task list endpoint
 */
export interface TaskListParams {
  status?: StatusFilter;
  sort?: SortField;
  order?: SortOrder;
}
```

---

## Component Props Types

### Form Components

```typescript
// lib/types.ts

/**
 * Props for LoginForm component
 */
export interface LoginFormProps {
  /** Callback after successful login */
  onSuccess?: () => void;
}

/**
 * Props for SignupForm component
 */
export interface SignupFormProps {
  /** Callback after successful signup */
  onSuccess?: () => void;
}

/**
 * Props for TaskForm component (create new task)
 */
export interface TaskFormProps {
  /** Callback after successful creation */
  onTaskCreated: (task: Task) => void;
}

/**
 * Props for TaskEditForm component (edit existing task)
 */
export interface TaskEditFormProps {
  /** Task being edited */
  task: Task;

  /** Callback after successful update */
  onSave: (task: Task) => void;

  /** Callback to cancel editing */
  onCancel: () => void;
}
```

### Task Components

```typescript
// lib/types.ts

/**
 * Props for TaskList component
 */
export interface TaskListProps {
  /** Optional initial tasks (for SSR) */
  initialTasks?: Task[];
}

/**
 * Props for TaskItem component
 */
export interface TaskItemProps {
  /** Task to display */
  task: Task;

  /** Callback when task is toggled */
  onToggle: (task: Task) => void;

  /** Callback when task is updated */
  onUpdate: (task: Task) => void;

  /** Callback when task is deleted */
  onDelete: (taskId: number) => void;
}
```

---

## State Types

### Form State

```typescript
// lib/types.ts

/**
 * Form field error state
 */
export interface FormErrors {
  [field: string]: string | undefined;
}

/**
 * Generic form state for controlled inputs
 */
export interface FormState<T> {
  values: T;
  errors: FormErrors;
  isSubmitting: boolean;
}
```

### UI State

```typescript
// lib/types.ts

/**
 * Task list page state
 */
export interface TaskPageState {
  tasks: Task[];
  isLoading: boolean;
  error: string | null;
  editingTaskId: number | null;
}
```

---

## Validation Rules

Validation constants matching backend Pydantic constraints:

```typescript
// lib/constants.ts

export const VALIDATION = {
  email: {
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    message: 'Invalid email format',
  },
  password: {
    minLength: 8,
    message: 'Password must be at least 8 characters',
  },
  name: {
    maxLength: 255,
    message: 'Name cannot exceed 255 characters',
  },
  taskTitle: {
    minLength: 1,
    maxLength: 200,
    required: true,
    message: 'Title is required (1-200 characters)',
  },
  taskDescription: {
    maxLength: 1000,
    message: 'Description cannot exceed 1000 characters',
  },
} as const;
```

---

## Type Exports Summary

```typescript
// lib/types.ts - Export summary

// Core entities
export type { Task, User, AuthState };

// API requests
export type {
  SignupRequest,
  LoginRequest,
  TaskCreateRequest,
  TaskUpdateRequest,
  TaskToggleRequest,
};

// API responses
export type { TokenResponse, MessageResponse, ErrorResponse };
export { ApiError };

// Query params
export type { StatusFilter, SortField, SortOrder, TaskListParams };

// Component props
export type {
  LoginFormProps,
  SignupFormProps,
  TaskFormProps,
  TaskEditFormProps,
  TaskListProps,
  TaskItemProps,
};

// State types
export type { FormErrors, FormState, TaskPageState };
```

---

## Entity Relationships

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend State                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  AuthContext                                            │
│  ├── token: string (JWT)                               │
│  ├── user: User                                        │
│  │   ├── userId: string (UUID)                         │
│  │   └── email: string                                 │
│  └── isAuthenticated: boolean                          │
│                                                         │
│  TaskPageState                                          │
│  ├── tasks: Task[]                                     │
│  │   └── Task                                          │
│  │       ├── id: number                                │
│  │       ├── user_id: string (matches AuthContext.user)│
│  │       ├── title: string                             │
│  │       ├── description: string | null                │
│  │       ├── completed: boolean                        │
│  │       ├── created_at: string (ISO)                  │
│  │       └── updated_at: string (ISO)                  │
│  ├── isLoading: boolean                                │
│  └── error: string | null                              │
│                                                         │
└─────────────────────────────────────────────────────────┘

                           │
                           │ API Calls (fetchWithAuth)
                           ▼

┌─────────────────────────────────────────────────────────┐
│                    Backend API                           │
├─────────────────────────────────────────────────────────┤
│  POST /api/auth/signup → TokenResponse                  │
│  POST /api/auth/login  → TokenResponse                  │
│  POST /api/auth/logout → MessageResponse                │
│                                                         │
│  GET    /api/{user_id}/tasks          → Task[]          │
│  POST   /api/{user_id}/tasks          → Task            │
│  PUT    /api/{user_id}/tasks/{id}     → Task            │
│  DELETE /api/{user_id}/tasks/{id}     → 204 No Content  │
│  PATCH  /api/{user_id}/tasks/{id}/complete → Task       │
└─────────────────────────────────────────────────────────┘
```

---

**Phase 1 Data Model Complete**: TypeScript interfaces defined. Ready for API contracts.
