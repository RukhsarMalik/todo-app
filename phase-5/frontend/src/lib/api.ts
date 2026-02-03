/**
 * API client for the Todo application.
 * Phase V: Extended with tags, notifications, search/filter/sort params.
 */

import { API_CONFIG } from './constants';
import { getToken, clearAuth } from './auth';
import {
  Task,
  Tag,
  Notification,
  TokenResponse,
  MessageResponse,
  SignupRequest,
  LoginRequest,
  TaskCreateRequest,
  TaskUpdateRequest,
  TaskListParams,
  TagCreateRequest,
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

  if (!skipAuth && token) {
    (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_CONFIG.baseUrl}${endpoint}`, {
    ...fetchOptions,
    headers,
  });

  if (response.status === 401) {
    clearAuth();
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
    throw new ApiError(401, 'Session expired. Please log in again.');
  }

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

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

// =============================================================================
// Authentication API
// =============================================================================

export async function signup(data: SignupRequest): Promise<TokenResponse> {
  return fetchWithAuth<TokenResponse>('/api/auth/signup', {
    method: 'POST',
    body: JSON.stringify(data),
    skipAuth: true,
  });
}

export async function login(data: LoginRequest): Promise<TokenResponse> {
  return fetchWithAuth<TokenResponse>('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify(data),
    skipAuth: true,
  });
}

export async function logout(): Promise<MessageResponse> {
  return fetchWithAuth<MessageResponse>('/api/auth/logout', {
    method: 'POST',
  });
}

// =============================================================================
// Task API
// =============================================================================

export async function getTasks(
  userId: string,
  params?: TaskListParams
): Promise<Task[]> {
  let endpoint = `/api/${userId}/tasks`;

  if (params) {
    const searchParams = new URLSearchParams();
    if (params.status) searchParams.append('status_filter', params.status);
    if (params.sort) searchParams.append('sort', params.sort);
    if (params.order) searchParams.append('order', params.order);
    if (params.search) searchParams.append('search', params.search);
    if (params.priority) searchParams.append('priority', params.priority);
    if (params.tags) searchParams.append('tags', params.tags);
    if (params.due_date_from) searchParams.append('due_date_from', params.due_date_from);
    if (params.due_date_to) searchParams.append('due_date_to', params.due_date_to);
    const queryString = searchParams.toString();
    if (queryString) {
      endpoint += `?${queryString}`;
    }
  }

  return fetchWithAuth<Task[]>(endpoint, {
    method: 'GET',
  });
}

export async function getTask(userId: string, taskId: number): Promise<Task> {
  return fetchWithAuth<Task>(`/api/${userId}/tasks/${taskId}`, {
    method: 'GET',
  });
}

export async function createTask(
  userId: string,
  data: TaskCreateRequest
): Promise<Task> {
  return fetchWithAuth<Task>(`/api/${userId}/tasks`, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

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

export async function deleteTask(userId: string, taskId: number): Promise<void> {
  return fetchWithAuth<void>(`/api/${userId}/tasks/${taskId}`, {
    method: 'DELETE',
  });
}

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
// Tag API
// =============================================================================

export async function getTags(userId: string): Promise<Tag[]> {
  return fetchWithAuth<Tag[]>(`/api/${userId}/tags`, {
    method: 'GET',
  });
}

export async function createTag(userId: string, data: TagCreateRequest): Promise<Tag> {
  return fetchWithAuth<Tag>(`/api/${userId}/tags`, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function deleteTag(userId: string, tagId: number): Promise<MessageResponse> {
  return fetchWithAuth<MessageResponse>(`/api/${userId}/tags/${tagId}`, {
    method: 'DELETE',
  });
}

// =============================================================================
// Notification API
// =============================================================================

export async function getNotifications(userId: string): Promise<Notification[]> {
  return fetchWithAuth<Notification[]>(`/api/${userId}/notifications`, {
    method: 'GET',
  });
}

// =============================================================================
// Profile API
// =============================================================================

export async function getProfile(): Promise<UserProfileResponse> {
  return fetchWithAuth<UserProfileResponse>('/api/auth/profile', {
    method: 'GET',
  });
}

export async function updateProfile(data: ProfileUpdateRequest): Promise<UserProfileResponse> {
  return fetchWithAuth<UserProfileResponse>('/api/auth/profile', {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function changePassword(data: PasswordChangeRequest): Promise<MessageResponse> {
  return fetchWithAuth<MessageResponse>('/api/auth/password', {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export { ApiError };
