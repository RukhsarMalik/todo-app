/**
 * TypeScript interfaces for the Todo frontend application.
 * These types mirror the backend Pydantic schemas for type-safe API communication.
 */

// =============================================================================
// Core Entities
// =============================================================================

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

/**
 * User information from auth response.
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

// =============================================================================
// API Request Types
// =============================================================================

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

/**
 * Request body for PUT /api/auth/profile
 */
export interface ProfileUpdateRequest {
  /** New display name */
  name?: string;
}

/**
 * Request body for PUT /api/auth/password
 */
export interface PasswordChangeRequest {
  /** Current password */
  current_password: string;
  /** New password (minimum 8 characters) */
  new_password: string;
}

/**
 * Response from GET/PUT /api/auth/profile
 */
export interface UserProfileResponse {
  /** User's unique identifier */
  id: string;
  /** User's email address */
  email: string;
  /** User's display name */
  name: string | null;
}

// =============================================================================
// API Response Types
// =============================================================================

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

/**
 * Standard error response from FastAPI.
 */
export interface ErrorResponse {
  /** Error message */
  detail: string;
}

// =============================================================================
// Error Classes
// =============================================================================

/**
 * Custom API error for frontend error handling.
 * Contains HTTP status code and error message.
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

// =============================================================================
// Query Parameters
// =============================================================================

/**
 * Filter options for task list
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

// =============================================================================
// Form State Types
// =============================================================================

/**
 * Form field error state
 */
export interface FormErrors {
  [field: string]: string | undefined;
}
