import type { Metadata } from 'next';
import { AuthProvider } from '@/components/auth/AuthProvider';
import { FloatingChatButton } from '@/components/ui/FloatingChatButton';
import './globals.css';

export const metadata: Metadata = {
  title: 'To-Do | Task Manager',
  description: 'Professional task management application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-100 font-sans antialiased">
        <AuthProvider>
          {children}
          <FloatingChatButton />
        </AuthProvider>
      </body>
    </html>
  );
}
