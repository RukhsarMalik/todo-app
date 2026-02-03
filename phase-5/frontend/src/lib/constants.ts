/**
 * Validation constants matching backend Pydantic constraints.
 */

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
    messageRequired: 'Title is required',
    messageMaxLength: 'Title cannot exceed 200 characters',
  },
  taskDescription: {
    maxLength: 1000,
    message: 'Description cannot exceed 1000 characters',
  },
} as const;

/**
 * API configuration
 */
export const API_CONFIG = {
  baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
} as const;

/**
 * Auth storage keys
 */
export const AUTH_STORAGE_KEYS = {
  token: 'auth_token',
  userId: 'auth_user_id',
  email: 'auth_email',
} as const;
