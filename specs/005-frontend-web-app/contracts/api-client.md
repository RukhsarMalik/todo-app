# API Client Contract

**Feature**: 005-frontend-web-app
**Date**: 2026-01-19
**Phase**: 1 - Design

---

## Overview

This document defines the TypeScript API client interface that the frontend uses to communicate with the backend. The client wraps native fetch with authentication and error handling.

---

## Client Configuration

```typescript
// lib/api.ts

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface RequestConfig extends RequestInit {
  skipAuth?: boolean;
}
```

---

## Core Functions

### fetchWithAuth

Base function for all API calls. Handles JWT injection and error responses.

```typescript
/**
 * Make an authenticated fetch request.
 *
 * @param endpoint - API endpoint path (e.g., '/api/auth/login')
 * @param options - Fetch options with optional skipAuth flag
 * @returns Parsed JSON response
 * @throws ApiError on non-2xx response
 */
async function fetchWithAuth<T>(
  endpoint: string,
  options: RequestConfig = {}
): Promise<T>;
```

**Behavior**:
1. Prepends `API_URL` to endpoint
2. Adds `Content-Type: application/json` header
3. Adds `Authorization: Bearer {token}` if token exists and `skipAuth` is false
4. On 401 response: clears auth state, redirects to `/login`
5. On non-2xx response: throws `ApiError` with status and message
6. On 204 No Content: returns `undefined`
7. On success: returns parsed JSON

---

## Authentication API

### signup

```typescript
/**
 * Register a new user account.
 *
 * @param data - Signup credentials
 * @returns Token response with access_token and user info
 * @throws ApiError(400) if email already registered
 * @throws ApiError(422) if validation fails
 */
async function signup(data: SignupRequest): Promise<TokenResponse>;
```

**Endpoint**: `POST /api/auth/signup`

**Request**:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"  // optional
}
```

**Response (201)**:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user_id": "uuid-string",
  "email": "user@example.com"
}
```

**Errors**:
| Status | Detail |
|--------|--------|
| 400 | "Email already registered" |
| 422 | Validation error (email format, password length) |

---

### login

```typescript
/**
 * Authenticate a user and receive JWT token.
 *
 * @param data - Login credentials
 * @returns Token response with access_token and user info
 * @throws ApiError(401) if credentials invalid
 */
async function login(data: LoginRequest): Promise<TokenResponse>;
```

**Endpoint**: `POST /api/auth/login`

**Request**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200)**:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user_id": "uuid-string",
  "email": "user@example.com"
}
```

**Errors**:
| Status | Detail |
|--------|--------|
| 401 | "Invalid credentials" |

---

### logout

```typescript
/**
 * Log out the current user (client-side token discard).
 *
 * @returns Success message
 */
async function logout(): Promise<MessageResponse>;
```

**Endpoint**: `POST /api/auth/logout`

**Response (200)**:
```json
{
  "message": "Successfully logged out"
}
```

**Note**: This is a stateless logout. Client must discard stored token.

---

## Task API

All task endpoints require JWT authentication.

### getTasks

```typescript
/**
 * List all tasks for the authenticated user.
 *
 * @param userId - User ID from auth state
 * @param params - Optional filter/sort parameters
 * @returns Array of tasks
 * @throws ApiError(401) if not authenticated
 * @throws ApiError(403) if user_id mismatch
 */
async function getTasks(
  userId: string,
  params?: TaskListParams
): Promise<Task[]>;
```

**Endpoint**: `GET /api/{user_id}/tasks`

**Query Parameters**:
| Param | Type | Default | Values |
|-------|------|---------|--------|
| status | string | "all" | "all", "pending", "completed" |
| sort | string | "created" | "created", "title" |
| order | string | "desc" | "asc", "desc" |

**Response (200)**:
```json
[
  {
    "id": 1,
    "user_id": "uuid-string",
    "title": "Task title",
    "description": "Description",
    "completed": false,
    "created_at": "2026-01-19T12:00:00",
    "updated_at": "2026-01-19T12:00:00"
  }
]
```

---

### getTask

```typescript
/**
 * Get a single task by ID.
 *
 * @param userId - User ID from auth state
 * @param taskId - Task ID to retrieve
 * @returns Task object
 * @throws ApiError(401) if not authenticated
 * @throws ApiError(403) if user_id mismatch
 * @throws ApiError(404) if task not found or not owned
 */
async function getTask(userId: string, taskId: number): Promise<Task>;
```

**Endpoint**: `GET /api/{user_id}/tasks/{task_id}`

**Response (200)**:
```json
{
  "id": 1,
  "user_id": "uuid-string",
  "title": "Task title",
  "description": "Description",
  "completed": false,
  "created_at": "2026-01-19T12:00:00",
  "updated_at": "2026-01-19T12:00:00"
}
```

---

### createTask

```typescript
/**
 * Create a new task.
 *
 * @param userId - User ID from auth state
 * @param data - Task creation data
 * @returns Created task with generated ID and timestamps
 * @throws ApiError(401) if not authenticated
 * @throws ApiError(403) if user_id mismatch
 * @throws ApiError(422) if validation fails
 */
async function createTask(
  userId: string,
  data: TaskCreateRequest
): Promise<Task>;
```

**Endpoint**: `POST /api/{user_id}/tasks`

**Request**:
```json
{
  "title": "New task",
  "description": "Optional description"
}
```

**Response (201)**:
```json
{
  "id": 2,
  "user_id": "uuid-string",
  "title": "New task",
  "description": "Optional description",
  "completed": false,
  "created_at": "2026-01-19T12:00:00",
  "updated_at": "2026-01-19T12:00:00"
}
```

---

### updateTask

```typescript
/**
 * Update an existing task.
 *
 * @param userId - User ID from auth state
 * @param taskId - Task ID to update
 * @param data - Fields to update (partial update)
 * @returns Updated task
 * @throws ApiError(401) if not authenticated
 * @throws ApiError(403) if user_id mismatch
 * @throws ApiError(404) if task not found or not owned
 * @throws ApiError(422) if validation fails
 */
async function updateTask(
  userId: string,
  taskId: number,
  data: TaskUpdateRequest
): Promise<Task>;
```

**Endpoint**: `PUT /api/{user_id}/tasks/{task_id}`

**Request**:
```json
{
  "title": "Updated title",
  "description": "Updated description"
}
```

**Response (200)**:
```json
{
  "id": 1,
  "user_id": "uuid-string",
  "title": "Updated title",
  "description": "Updated description",
  "completed": false,
  "created_at": "2026-01-19T12:00:00",
  "updated_at": "2026-01-19T12:05:00"
}
```

---

### deleteTask

```typescript
/**
 * Delete a task permanently.
 *
 * @param userId - User ID from auth state
 * @param taskId - Task ID to delete
 * @throws ApiError(401) if not authenticated
 * @throws ApiError(403) if user_id mismatch
 * @throws ApiError(404) if task not found or not owned
 */
async function deleteTask(userId: string, taskId: number): Promise<void>;
```

**Endpoint**: `DELETE /api/{user_id}/tasks/{task_id}`

**Response**: 204 No Content (empty body)

---

### toggleTask

```typescript
/**
 * Toggle task completion status.
 *
 * @param userId - User ID from auth state
 * @param taskId - Task ID to toggle
 * @param completed - New completion status
 * @returns Updated task
 * @throws ApiError(401) if not authenticated
 * @throws ApiError(403) if user_id mismatch
 * @throws ApiError(404) if task not found or not owned
 */
async function toggleTask(
  userId: string,
  taskId: number,
  completed: boolean
): Promise<Task>;
```

**Endpoint**: `PATCH /api/{user_id}/tasks/{task_id}/complete`

**Request**:
```json
{
  "completed": true
}
```

**Response (200)**:
```json
{
  "id": 1,
  "user_id": "uuid-string",
  "title": "Task title",
  "description": "Description",
  "completed": true,
  "created_at": "2026-01-19T12:00:00",
  "updated_at": "2026-01-19T12:10:00"
}
```

---

## Error Handling

### ApiError Class

```typescript
/**
 * Custom error class for API errors.
 * Contains HTTP status code and error message.
 */
class ApiError extends Error {
  constructor(
    public status: number,
    public detail: string
  ) {
    super(detail);
    this.name = 'ApiError';
  }
}
```

### Common Error Codes

| Status | Meaning | Frontend Action |
|--------|---------|-----------------|
| 400 | Bad Request | Display error message |
| 401 | Unauthorized | Clear auth, redirect to login |
| 403 | Forbidden | Display "Access denied" |
| 404 | Not Found | Display "Task not found" |
| 422 | Validation Error | Display validation message |
| 500 | Server Error | Display "Something went wrong" |

---

## Exports

```typescript
// lib/api.ts

export {
  // Auth
  signup,
  login,
  logout,

  // Tasks
  getTasks,
  getTask,
  createTask,
  updateTask,
  deleteTask,
  toggleTask,

  // Error class
  ApiError,
};
```

---

## Usage Example

```typescript
import * as api from '@/lib/api';
import { useAuth } from '@/components/auth/AuthProvider';

function TasksPage() {
  const { auth } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (auth.user) {
      loadTasks();
    }
  }, [auth.user]);

  async function loadTasks() {
    try {
      const data = await api.getTasks(auth.user!.userId);
      setTasks(data);
    } catch (err) {
      if (err instanceof api.ApiError) {
        setError(err.detail);
      }
    }
  }

  async function handleCreate(title: string) {
    try {
      const task = await api.createTask(auth.user!.userId, { title });
      setTasks([task, ...tasks]);
    } catch (err) {
      if (err instanceof api.ApiError) {
        setError(err.detail);
      }
    }
  }

  // ... rest of component
}
```

---

**API Client Contract Complete**: Ready for implementation.
