'use client';

/**
 * Signup page with split layout design.
 * Renders form on left, illustration on right.
 */

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { SignupForm } from '@/components/auth/SignupForm';
import { useAuth } from '@/components/auth/AuthProvider';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { AuthIllustration } from '@/components/ui/AuthIllustration';

export default function SignupPage() {
  const router = useRouter();
  const { auth } = useAuth();

  // Redirect to tasks if already authenticated
  useEffect(() => {
    if (!auth.isLoading && auth.isAuthenticated) {
      router.push('/tasks');
    }
  }, [auth.isLoading, auth.isAuthenticated, router]);

  // Show loading while checking auth
  if (auth.isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // Show signup form if not authenticated
  if (!auth.isAuthenticated) {
    return (
      <main className="min-h-screen flex auth-bg-pattern">
        {/* Left side - Illustration */}
        <div className="hidden lg:flex lg:w-1/2 items-center justify-center relative z-10">
          <AuthIllustration type="signup" />
        </div>

        {/* Right side - Form */}
        <div className="w-full lg:w-1/2 flex items-center justify-center px-6 py-12 relative z-10">
          <SignupForm />
        </div>
      </main>
    );
  }

  // Show loading while redirecting
  return (
    <div className="min-h-screen flex items-center justify-center bg-white">
      <LoadingSpinner size="lg" />
    </div>
  );
}
