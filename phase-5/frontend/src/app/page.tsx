'use client';

/**
 * Home page - Landing page for unauthenticated users
 * Authenticated users → /dashboard
 */

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/auth/AuthProvider';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { LandingPage } from '@/components/landing/LandingPage';

export default function Home() {
  const router = useRouter();
  const { auth } = useAuth();
  const [showLanding, setShowLanding] = useState(false);

  useEffect(() => {
    if (!auth.isLoading) {
      if (auth.isAuthenticated) {
        router.replace('/dashboard');
      } else {
        setShowLanding(true);
      }
    }
  }, [auth.isLoading, auth.isAuthenticated, router]);

  // Show loading spinner while checking auth
  if (auth.isLoading) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <LoadingSpinner size="lg" />
      </main>
    );
  }

  // Show landing page for unauthenticated users
  if (showLanding) {
    return <LandingPage />;
  }

  // Fallback loading state during redirect
  return (
    <main className="flex min-h-screen items-center justify-center">
      <LoadingSpinner size="lg" />
    </main>
  );
}
