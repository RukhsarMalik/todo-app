'use client';

/**
 * Home page with auth-based redirect.
 * Authenticated users → /dashboard
 * Non-authenticated users → /login
 */

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/auth/AuthProvider';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';

export default function Home() {
  const router = useRouter();
  const { auth } = useAuth();

  useEffect(() => {
    if (!auth.isLoading) {
      if (auth.isAuthenticated) {
        router.replace('/dashboard');
      } else {
        router.replace('/login');
      }
    }
  }, [auth.isLoading, auth.isAuthenticated, router]);

  // Show loading spinner while checking auth
  return (
    <main className="flex min-h-screen items-center justify-center">
      <LoadingSpinner size="lg" />
    </main>
  );
}
