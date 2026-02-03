'use client';

/**
 * Authentication context provider.
 * Manages auth state and provides login/logout functionality.
 */

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { AuthState, User } from '@/lib/types';
import { getToken, getUserId, getEmail, setAuth, clearAuth } from '@/lib/auth';

// =============================================================================
// Context Definition
// =============================================================================

interface AuthContextValue {
  auth: AuthState;
  login: (token: string, userId: string, email: string) => void;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

// =============================================================================
// Provider Component
// =============================================================================

interface AuthProviderProps {
  children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const router = useRouter();
  const [auth, setAuthState] = useState<AuthState>({
    token: null,
    user: null,
    isAuthenticated: false,
    isLoading: true,
  });

  // Restore auth state from localStorage on mount
  useEffect(() => {
    const token = getToken();
    const userId = getUserId();
    const email = getEmail();

    if (token && userId && email) {
      setAuthState({
        token,
        user: { userId, email },
        isAuthenticated: true,
        isLoading: false,
      });
    } else {
      setAuthState(prev => ({ ...prev, isLoading: false }));
    }
  }, []);

  // Login: store credentials and update state
  const login = useCallback((token: string, userId: string, email: string) => {
    setAuth(token, userId, email);
    const user: User = { userId, email };
    setAuthState({
      token,
      user,
      isAuthenticated: true,
      isLoading: false,
    });
  }, []);

  // Logout: clear storage and state, redirect to login
  const logout = useCallback(() => {
    clearAuth();
    setAuthState({
      token: null,
      user: null,
      isAuthenticated: false,
      isLoading: false,
    });
    // Use replace to prevent back-button access
    router.replace('/login');
  }, [router]);

  // Update user info (e.g., after profile update)
  const updateUser = useCallback((userData: Partial<User>) => {
    setAuthState(prev => {
      if (!prev.user) return prev;
      return {
        ...prev,
        user: { ...prev.user, ...userData },
      };
    });
  }, []);

  return (
    <AuthContext.Provider value={{ auth, login, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
}

// =============================================================================
// Hook
// =============================================================================

/**
 * Hook to access auth context.
 * Must be used within an AuthProvider.
 */
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
