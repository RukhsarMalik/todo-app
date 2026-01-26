'use client';

/**
 * Protected chat page with dashboard layout.
 * Features dark sidebar with navigation and AI chat interface.
 */

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/auth/AuthProvider';
import ChatInterface from '@/components/ChatInterface';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { Sidebar } from '@/components/ui/Sidebar';

// Icons
const ChatBotIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
  </svg>
);

export default function ChatPage() {
  const router = useRouter();
  const { auth } = useAuth();

  // Get current date
  const currentDate = new Date();
  const dayName = currentDate.toLocaleDateString('en-US', { weekday: 'long' });
  const dateStr = currentDate.toLocaleDateString('en-US', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!auth.isLoading && !auth.isAuthenticated) {
      router.replace('/login');
    }
  }, [auth.isLoading, auth.isAuthenticated, router]);

  // Show loading while checking auth
  if (auth.isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // Don't render if not authenticated (will redirect)
  if (!auth.isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen flex bg-gray-50">
      {/* Sidebar */}
      <Sidebar activeItem="chat" />

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-h-screen overflow-hidden">
        {/* Header */}
        <header className="bg-white shadow-sm px-4 lg:px-6 py-4 flex-shrink-0">
          <div className="flex items-center justify-between gap-4">
            {/* Brand */}
            <h1 className="text-xl lg:text-2xl font-bold ml-12 lg:ml-0">
              <span className="text-red-500">AI</span>
              <span className="text-gray-800"> Assistant</span>
            </h1>

            {/* Status indicator */}
            <div className="flex items-center gap-2 lg:gap-4">
              <div className="flex items-center gap-2 px-3 py-1.5 bg-green-50 text-green-600 rounded-full text-sm">
                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                <span className="hidden sm:inline">Online</span>
              </div>
              <div className="hidden md:block text-right ml-2 border-l pl-4 border-gray-200">
                <p className="text-sm font-semibold text-gray-800">{dayName}</p>
                <p className="text-xs text-red-500">{dateStr}</p>
              </div>
            </div>
          </div>
        </header>

        {/* Main content area */}
        <main className="flex-1 p-4 lg:p-6 overflow-hidden bg-gray-50 flex flex-col">
          {/* Welcome message */}
          <div className="mb-4">
            <h2 className="text-xl lg:text-2xl font-bold text-gray-800 flex items-center gap-2">
              <span className="w-10 h-10 bg-red-100 rounded-xl flex items-center justify-center text-red-500">
                <ChatBotIcon />
              </span>
              Task Assistant
            </h2>
            <p className="text-gray-500 mt-1 text-sm lg:text-base ml-12">
              Ask me to add, complete, or manage your tasks using natural language
            </p>
          </div>

          {/* Chat interface */}
          <div className="flex-1 min-h-0">
            <ChatInterface userId={auth.user?.userId || ''} />
          </div>
        </main>
      </div>
    </div>
  );
}
