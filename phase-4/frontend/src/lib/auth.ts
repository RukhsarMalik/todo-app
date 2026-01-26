/**
 * Auth token storage utilities.
 * Manages JWT token persistence in localStorage.
 */

import { AUTH_STORAGE_KEYS } from './constants';

/**
 * Get the stored auth token.
 */
export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(AUTH_STORAGE_KEYS.token);
}

/**
 * Get the stored user ID.
 */
export function getUserId(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(AUTH_STORAGE_KEYS.userId);
}

/**
 * Get the stored user email.
 */
export function getEmail(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(AUTH_STORAGE_KEYS.email);
}

/**
 * Store auth data in localStorage.
 */
export function setAuth(token: string, userId: string, email: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(AUTH_STORAGE_KEYS.token, token);
  localStorage.setItem(AUTH_STORAGE_KEYS.userId, userId);
  localStorage.setItem(AUTH_STORAGE_KEYS.email, email);
}

/**
 * Clear all auth data from localStorage.
 */
export function clearAuth(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(AUTH_STORAGE_KEYS.token);
  localStorage.removeItem(AUTH_STORAGE_KEYS.userId);
  localStorage.removeItem(AUTH_STORAGE_KEYS.email);
}

/**
 * Check if user is authenticated (token exists).
 */
export function isAuthenticated(): boolean {
  return getToken() !== null;
}
