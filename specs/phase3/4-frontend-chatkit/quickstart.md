# Quickstart Guide: Frontend ChatKit UI

## Overview
This guide provides instructions for setting up and running the ChatKit UI component in the frontend application.

## Prerequisites
- Node.js 18+ installed
- Yarn or npm package manager
- Access to the backend API with chat endpoint
- Valid JWT token for authentication
- OpenAI domain allowlist configured with your frontend URL

## Installation

### 1. Install Dependencies
```bash
# Navigate to the frontend directory
cd phase-2/frontend

# Install the OpenAI ChatKit package
npm install @openai/chatkit

# Or with yarn
yarn add @openai/chatkit
```

### 2. Environment Configuration
Add the following environment variables to your `.env.local` file:

```env
# OpenAI domain allowlist key
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-from-openai

# Backend API URL
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### 3. OpenAI Domain Allowlist
1. Go to https://platform.openai.com/settings/organization/security/domain-allowlist
2. Add your frontend domain (e.g., https://your-frontend.vercel.app)
3. Copy the domain key and add it to your environment variables

## Implementation

### 1. Create Chat Interface Component
Create the ChatInterface component at `components/ChatInterface.tsx`:

```typescript
'use client';

import { ChatKit } from '@openai/chatkit';
import { useSession } from 'next-auth/react';
import { useState } from 'react';

interface ChatInterfaceProps {
  userId: string;
}

export default function ChatInterface({ userId }: ChatInterfaceProps) {
  const { data: session } = useSession();
  const [isLoading, setIsLoading] = useState(false);

  async function sendMessage(message: string) {
    setIsLoading(true);

    try {
      const res = await fetch(`/api/${userId}/chat`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${session?.user?.accessToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message })
      });

      if (!res.ok) {
        throw new Error(`API call failed: ${res.status}`);
      }

      const data = await res.json();
      return data.response;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="chat-container">
      <ChatKit
        onSendMessage={sendMessage}
        placeholder="Ask me to manage your tasks..."
        isLoading={isLoading}
      />
    </div>
  );
}
```

### 2. Create Chat Page
Create the chat page at `app/chat/page.tsx`:

```typescript
'use client';

import { useSession } from 'next-auth/react';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ChatInterface from '@/components/ChatInterface';

export default function ChatPage() {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/auth/signin");
    }
  }, [status, router]);

  if (status === "loading") {
    return <div>Loading...</div>;
  }

  if (!session?.user?.id) {
    return null; // Redirect handled by useEffect
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Task Management Chat</h1>
      <ChatInterface userId={session.user.id} />
    </div>
  );
}
```

### 3. Update Navigation
Add a link to the chat page in your main navigation:

```tsx
// Example in your layout or navigation component
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export function Navigation() {
  const pathname = usePathname();

  return (
    <nav className="flex space-x-4">
      <Link
        href="/todos"
        className={pathname === '/todos' ? 'font-bold' : ''}
      >
        Tasks
      </Link>
      <Link
        href="/chat"
        className={pathname === '/chat' ? 'font-bold' : ''}
      >
        Chat
      </Link>
    </nav>
  );
}
```

## Running the Application

### 1. Development
```bash
# Start the frontend in development mode
cd phase-2/frontend
npm run dev
# or
yarn dev
```

### 2. Production Build
```bash
# Build the application
npm run build

# Start the production server
npm start
```

## Testing the Feature

1. Navigate to `/chat` route when logged in
2. Verify the ChatKit component is displayed
3. Test sending messages like:
   - "Add buy groceries to my list"
   - "Show me all my tasks"
   - "What's pending?"
   - "Mark task 1 as done"
4. Verify responses come back from the backend
5. Check that loading states are displayed properly
6. Test error handling when the backend is unavailable

## Troubleshooting

### Common Issues

1. **ChatKit not loading**: Ensure NEXT_PUBLIC_OPENAI_DOMAIN_KEY is set correctly
2. **Authentication errors**: Verify JWT token is being passed correctly in headers
3. **API connectivity**: Check that the backend chat endpoint is accessible
4. **CORS errors**: Ensure backend has proper CORS configuration for your frontend domain

### Debugging Steps

1. Check browser console for errors
2. Verify network requests are being made to the correct endpoints
3. Confirm authentication token is valid and not expired
4. Test the backend chat endpoint directly using a tool like Postman