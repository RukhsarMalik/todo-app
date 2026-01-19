'use client';

/**
 * User login form component with modern design.
 * Features icon inputs and coral accent colors.
 */

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { useAuth } from '@/components/auth/AuthProvider';
import { login as apiLogin, ApiError } from '@/lib/api';
import { VALIDATION } from '@/lib/constants';

// Icons
const UserIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>
);

const LockIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
  </svg>
);

interface FormErrors {
  email?: string;
  password?: string;
}

export function LoginForm() {
  const router = useRouter();
  const { login } = useAuth();

  // Form state
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  // Validate individual field
  const validateField = (field: string, value: string): string | undefined => {
    switch (field) {
      case 'email':
        if (!value) return 'Email is required';
        if (!VALIDATION.email.pattern.test(value)) return VALIDATION.email.message;
        return undefined;
      case 'password':
        if (!value) return 'Password is required';
        if (value.length < VALIDATION.password.minLength) return VALIDATION.password.message;
        return undefined;
      default:
        return undefined;
    }
  };

  // Validate all fields
  const validate = (): boolean => {
    const newErrors: FormErrors = {
      email: validateField('email', email),
      password: validateField('password', password),
    };
    setErrors(newErrors);
    return !newErrors.email && !newErrors.password;
  };

  // Handle blur validation
  const handleBlur = (field: string, value: string) => {
    const error = validateField(field, value);
    setErrors(prev => ({ ...prev, [field]: error }));
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setApiError(null);

    if (!validate()) return;

    setIsSubmitting(true);

    try {
      const response = await apiLogin({ email, password });

      // Store auth data and update context
      login(response.access_token, response.user_id, response.email);

      // Redirect to tasks
      router.push('/tasks');
    } catch (err) {
      if (err instanceof ApiError) {
        setApiError('Invalid credentials');
      } else {
        setApiError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto animate-fade-in">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Header */}
        <div className="text-left">
          <h1 className="text-3xl font-bold text-gray-900">Sign In</h1>
        </div>

        {/* Error Message */}
        {apiError && (
          <ErrorMessage message={apiError} onDismiss={() => setApiError(null)} />
        )}

        {/* Email Input */}
        <Input
          type="email"
          name="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          onBlur={(e) => handleBlur('email', e.target.value)}
          error={errors.email}
          placeholder="Enter Username"
          autoComplete="email"
          icon={<UserIcon />}
          required
        />

        {/* Password Input */}
        <Input
          type="password"
          name="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onBlur={(e) => handleBlur('password', e.target.value)}
          error={errors.password}
          placeholder="Enter Password"
          autoComplete="current-password"
          icon={<LockIcon />}
          required
        />

        {/* Remember Me */}
        <div className="flex items-center">
          <input
            id="remember-me"
            name="remember-me"
            type="checkbox"
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
            className="h-4 w-4 text-red-500 focus:ring-red-500 border-gray-300 rounded cursor-pointer"
          />
          <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-700 cursor-pointer">
            Remember Me
          </label>
        </div>

        {/* Submit Button */}
        <Button
          type="submit"
          variant="primary"
          size="lg"
          isLoading={isSubmitting}
          className="w-full"
        >
          {isSubmitting ? 'Logging in...' : 'Login'}
        </Button>

        {/* Sign Up Link */}
        <p className="text-center text-sm text-gray-600">
          Don&apos;t have an account?{' '}
          <Link href="/signup" className="text-red-500 hover:text-red-600 font-medium">
            Create One
          </Link>
        </p>
      </form>
    </div>
  );
}
