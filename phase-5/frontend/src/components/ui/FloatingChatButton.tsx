'use client';

/**
 * Floating chat assistant widget that opens a mini chat window.
 * Shares the same chat history with the main chat page.
 */

import { useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuth } from '@/components/auth/AuthProvider';
import ChatInterface from '@/components/ChatInterface';

// Icons
const ChatBotIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
  </svg>
);

const SparkleIcon = () => (
  <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
    <path d="M12 0L14.59 8.41L23 11L14.59 13.59L12 22L9.41 13.59L1 11L9.41 8.41L12 0Z" />
  </svg>
);

const CloseIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
  </svg>
);

const ExpandIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
  </svg>
);

const MinimizeIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 12H4" />
  </svg>
);

export function FloatingChatButton() {
  const router = useRouter();
  const pathname = usePathname();
  const { auth } = useAuth();
  const [isOpen, setIsOpen] = useState(false);

  // Don't show on login, signup pages
  const hiddenPaths = ['/login', '/signup'];
  if (hiddenPaths.includes(pathname) || !auth.isAuthenticated) {
    return null;
  }

  // On chat page, just show the button but disable popup (already on chat)
  const isOnChatPage = pathname === '/chat';

  const handleButtonClick = () => {
    if (isOnChatPage) {
      // Already on chat page, do nothing
      return;
    }
    setIsOpen(!isOpen);
  };

  const handleExpandClick = () => {
    setIsOpen(false);
    router.push('/chat');
  };

  return (
    <>
      {/* Mini Chat Window */}
      {isOpen && !isOnChatPage && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 bg-black/20 z-40 lg:hidden"
            onClick={() => setIsOpen(false)}
          />

          {/* Chat Window */}
          <div className="fixed bottom-24 right-4 sm:right-6 z-50 w-[calc(100vw-2rem)] sm:w-96 h-[500px] max-h-[70vh] bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden flex flex-col animate-in slide-in-from-bottom-5 duration-300">
            {/* Header */}
            <div className="bg-gradient-to-r from-red-500 to-red-600 px-4 py-3 flex items-center justify-between flex-shrink-0">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-white text-sm">AI Assistant</h3>
                  <p className="text-xs text-red-100">Always here to help</p>
                </div>
              </div>
              <div className="flex items-center gap-1">
                <button
                  onClick={handleExpandClick}
                  className="p-2 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                  title="Open full chat"
                >
                  <ExpandIcon />
                </button>
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-2 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                  title="Minimize"
                >
                  <MinimizeIcon />
                </button>
              </div>
            </div>

            {/* Chat Interface */}
            <div className="flex-1 overflow-hidden">
              <ChatInterface userId={auth.user?.userId || ''} isCompact />
            </div>
          </div>
        </>
      )}

      {/* Floating Button */}
      <button
        onClick={handleButtonClick}
        className={`fixed bottom-6 right-4 sm:right-6 z-50 group ${isOnChatPage ? 'opacity-50 cursor-default' : ''}`}
        aria-label={isOpen ? "Close AI Assistant" : "Open AI Assistant"}
        disabled={isOnChatPage}
      >
        {/* Pulse animation ring - only when closed */}
        {!isOpen && !isOnChatPage && (
          <span className="absolute inset-0 rounded-full bg-red-400 animate-ping opacity-25"></span>
        )}

        {/* Main button */}
        <div className={`relative flex items-center justify-center w-14 h-14 rounded-full shadow-lg transform transition-all duration-300 ${
          isOpen
            ? 'bg-gray-700 hover:bg-gray-800 rotate-0'
            : 'bg-gradient-to-br from-red-500 to-red-600 hover:shadow-xl hover:scale-110'
        }`}>
          {isOpen ? <CloseIcon /> : <ChatBotIcon />}

          {/* AI sparkle badge - only when closed */}
          {!isOpen && !isOnChatPage && (
            <span className="absolute -top-1 -right-1 w-5 h-5 bg-yellow-400 rounded-full flex items-center justify-center text-yellow-800 shadow-sm">
              <SparkleIcon />
            </span>
          )}
        </div>

        {/* Tooltip - only when closed */}
        {!isOpen && !isOnChatPage && (
          <div className="absolute bottom-full right-0 mb-2 px-3 py-1.5 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap pointer-events-none">
            AI Assistant
            <div className="absolute top-full right-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
          </div>
        )}
      </button>
    </>
  );
}
