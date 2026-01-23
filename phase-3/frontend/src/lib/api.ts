/**
 * API client for the Todo application.
 * Wraps fetch with JWT injection and error handling.
 */

import { API_CONFIG } from './constants';
import { getToken, clearAuth } from './auth';
import {
  Task,
  TokenResponse,
  MessageResponse,
  SignupRequest,
  LoginRequest,
  TaskCreateRequest,
  TaskUpdateRequest,
  TaskListParams,
  ApiError,
  ProfileUpdateRequest,
  PasswordChangeRequest,
  UserProfileResponse,
} from './types';

// =============================================================================
// Core Fetch Wrapper
// =============================================================================

interface RequestConfig extends RequestInit {
  skipAuth?: boolean;
}

/**
 * Make an authenticated fetch request.
 * Handles JWT injection, error responses, and 401 redirects.
 */
async function fetchWithAuth<T>(
  endpoint: string,
  options: RequestConfig = {}
): Promise<T> {
  const { skipAuth = false, ...fetchOptions } = options;
  const token = getToken();

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...fetchOptions.headers,
  };

  // Add Authorization header if token exists and not skipped
  if (!skipAuth && token) {
    (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_CONFIG.baseUrl}${endpoint}`, {
    ...fetchOptions,
    headers,
  });

  // Handle 401 Unauthorized
  if (response.status === 401) {
    clearAuth();
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
    throw new ApiError(401, 'Session expired. Please log in again.');
  }

  // Handle other errors
  if (!response.ok) {
    let detail = 'Request failed';
    try {
      const errorData = await response.json();
      detail = errorData.detail || detail;
    } catch {
      // Ignore JSON parse errors
    }
    throw new ApiError(response.status, detail);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

// =============================================================================
// Authentication API
// =============================================================================

/**
 * Register a new user account.
 */
export async function signup(data: SignupRequest): Promise<TokenResponse> {
  return fetchWithAuth<TokenResponse>('/api/auth/signup', {
    method: 'POST',
    body: JSON.stringify(data),
    skipAuth: true,
  });
}

/**
 * Authenticate a user and receive JWT token.
 */
export async function login(data: LoginRequest): Promise<TokenResponse> {
  return fetchWithAuth<TokenResponse>('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify(data),
    skipAuth: true,
  });
}

/**
 * Log out the current user (client-side token discard).
 */
export async function logout(): Promise<MessageResponse> {
  return fetchWithAuth<MessageResponse>('/api/auth/logout', {
    method: 'POST',
  });
}

// =============================================================================
// Task API
// =============================================================================

/**
 * List all tasks for the authenticated user.
 */
export async function getTasks(
  userId: string,
  params?: TaskListParams
): Promise<Task[]> {
  let endpoint = `/api/${userId}/tasks`;

  if (params) {
    const searchParams = new URLSearchParams();
    if (params.status) searchParams.append('status', params.status);
    if (params.sort) searchParams.append('sort', params.sort);
    if (params.order) searchParams.append('order', params.order);
    const queryString = searchParams.toString();
    if (queryString) {
      endpoint += `?${queryString}`;
    }
  }

  return fetchWithAuth<Task[]>(endpoint, {
    method: 'GET',
  });
}

/**
 * Get a single task by ID.
 */
export async function getTask(userId: string, taskId: number): Promise<Task> {
  return fetchWithAuth<Task>(`/api/${userId}/tasks/${taskId}`, {
    method: 'GET',
  });
}

/**
 * Create a new task.
 */
export async function createTask(
  userId: string,
  data: TaskCreateRequest
): Promise<Task> {
  return fetchWithAuth<Task>(`/api/${userId}/tasks`, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * Update an existing task.
 */
export async function updateTask(
  userId: string,
  taskId: number,
  data: TaskUpdateRequest
): Promise<Task> {
  return fetchWithAuth<Task>(`/api/${userId}/tasks/${taskId}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

/**
 * Delete a task permanently.
 */
export async function deleteTask(userId: string, taskId: number): Promise<void> {
  return fetchWithAuth<void>(`/api/${userId}/tasks/${taskId}`, {
    method: 'DELETE',
  });
}

/**
 * Toggle task completion status.
 */
export async function toggleTask(
  userId: string,
  taskId: number,
  completed: boolean
): Promise<Task> {
  return fetchWithAuth<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
    method: 'PATCH',
    body: JSON.stringify({ completed }),
  });
}

// =============================================================================
// Profile API
// =============================================================================

/**
 * Get the current user's profile.
 */
export async function getProfile(): Promise<UserProfileResponse> {
  return fetchWithAuth<UserProfileResponse>('/api/auth/profile', {
    method: 'GET',
  });
}

/**
 * Update the current user's profile (name).
 */
export async function updateProfile(data: ProfileUpdateRequest): Promise<UserProfileResponse> {
  return fetchWithAuth<UserProfileResponse>('/api/auth/profile', {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

/**
 * Change the current user's password.
 */
export async function changePassword(data: PasswordChangeRequest): Promise<MessageResponse> {
  return fetchWithAuth<MessageResponse>('/api/auth/password', {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

// Re-export ApiError for convenience
export { ApiError };
