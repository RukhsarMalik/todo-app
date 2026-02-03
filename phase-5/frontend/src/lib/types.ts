/**
 * TypeScript interfaces for the Todo frontend application.
 * Phase V: Extended with priority, due dates, tags, recurrence, notifications.
 */

// =============================================================================
// Core Entities
// =============================================================================

export type Priority = 'low' | 'medium' | 'high' | 'urgent';

export interface Tag {
  id: number;
  name: string;
  created_at: string;
}

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: Priority;
  due_date: string | null;
  reminder_offset: number;
  recurrence_rule: RecurrenceRule | null;
  next_occurrence: string | null;
  parent_task_id: number | null;
  tags: Tag[];
  created_at: string;
  updated_at: string;
}

export interface RecurrenceRule {
  type: 'daily' | 'weekly' | 'monthly';
  days?: string[];
  day_of_month?: number;
}

export interface Notification {
  id: number;
  task_id: number | null;
  message: string;
  read: boolean;
  created_at: string;
}

export interface User {
  userId: string;
  email: string;
  name?: string;
}

export interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// =============================================================================
// API Request Types
// =============================================================================

export interface SignupRequest {
  email: string;
  password: string;
  name?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
  priority?: Priority;
  due_date?: string;
  reminder_offset?: number;
  recurrence_rule?: RecurrenceRule;
  tag_ids?: number[];
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  priority?: Priority;
  due_date?: string | null;
  reminder_offset?: number;
  recurrence_rule?: RecurrenceRule | null;
  tag_ids?: number[];
}

export interface TaskToggleRequest {
  completed: boolean;
}

export interface TagCreateRequest {
  name: string;
}

export interface ProfileUpdateRequest {
  name?: string;
}

export interface PasswordChangeRequest {
  current_password: string;
  new_password: string;
}

export interface UserProfileResponse {
  id: string;
  email: string;
  name: string | null;
}

// =============================================================================
// API Response Types
// =============================================================================

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user_id: string;
  email: string;
}

export interface MessageResponse {
  message: string;
}

export interface ErrorResponse {
  detail: string;
}

// =============================================================================
// Error Classes
// =============================================================================

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

export type StatusFilter = 'all' | 'pending' | 'completed';
export type SortField = 'created' | 'created_at' | 'title' | 'due_date' | 'priority';
export type SortOrder = 'asc' | 'desc';

export interface TaskListParams {
  status?: StatusFilter;
  sort?: SortField;
  order?: SortOrder;
  search?: string;
  priority?: Priority;
  tags?: string;
  due_date_from?: string;
  due_date_to?: string;
}

// =============================================================================
// Form State Types
// =============================================================================

export interface FormErrors {
  [field: string]: string | undefined;
}
