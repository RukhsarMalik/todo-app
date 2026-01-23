# Research: Frontend Web Application

**Feature**: 005-frontend-web-app
**Date**: 2026-01-19
**Phase**: 0 - Research

---

## Research Tasks

This document resolves all technical questions identified during planning to inform Phase 1 design decisions.

---

## R1: Next.js 16+ App Router Patterns

### Decision
Use Next.js 16+ with App Router, Server Components by default, and Client Components only where interactivity is required.

### Rationale
- App Router is the stable routing paradigm in Next.js 16+
- Server Components reduce client bundle size
- Client Components (`'use client'`) needed for: forms, event handlers, React Context, browser APIs
- Streaming/Suspense for loading states

### Patterns Applied

**Route Structure**:
```
app/
├── layout.tsx         # Server Component - root layout
├── page.tsx           # Server Component - home redirect
├── login/page.tsx     # Client Component - login form
├── signup/page.tsx    # Client Component - signup form
└── tasks/page.tsx     # Client Component - task management
```

**Server vs Client Decision Matrix**:

| Component | Type | Reason |
|-----------|------|--------|
| RootLayout | Server | Static shell, no interactivity |
| HomePage | Server | Simple redirect logic |
| LoginPage | Client | Form state, event handlers |
| SignupPage | Client | Form state, event handlers |
| TasksPage | Client | Full interactivity, API calls |
| TaskItem | Client | Checkbox, edit, delete buttons |
| TaskForm | Client | Input state, form submission |
| AuthProvider | Client | React Context for auth state |

### Alternatives Considered
1. **Pages Router**: Legacy, not recommended for new Next.js 16+ projects
2. **Full Client-Side**: Would lose SSR benefits and increase bundle size

---

## R2: Authentication State Management

### Decision
Use React Context with localStorage for token persistence. AuthProvider wraps the app and exposes login/logout/user state.

### Rationale
- Simple, no external state library needed
- localStorage provides persistence across page refreshes
- Context allows access to auth state throughout component tree
- MVP-appropriate; can upgrade to httpOnly cookies for production security

### Implementation Pattern

```typescript
// lib/auth.ts
export interface AuthState {
  token: string | null;
  userId: string | null;
  email: string | null;
  isAuthenticated: boolean;
}

// components/auth/AuthProvider.tsx
const AuthContext = createContext<{
  auth: AuthState;
  login: (token: string, userId: string, email: string) => void;
  logout: () => void;
} | null>(null);
```

### Token Storage Strategy
1. On login/signup success: Store in localStorage + React state
2. On page load: Check localStorage, restore to state
3. On logout: Clear localStorage + state
4. On 401 response: Clear auth and redirect to login

### Alternatives Considered
1. **httpOnly Cookies**: More secure but requires backend changes for cookie-based auth
2. **Zustand/Redux**: Overkill for simple auth state
3. **Session storage**: Doesn't persist across tabs/browser close

---

## R3: API Client Architecture

### Decision
Create a centralized API client (`lib/api.ts`) that wraps fetch with JWT injection and error handling.

### Rationale
- Single source of truth for API calls
- Automatic token attachment to all requests
- Consistent error handling pattern
- Type-safe request/response handling

### Implementation Pattern

```typescript
// lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function fetchWithAuth<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken(); // from localStorage
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    if (response.status === 401) {
      // Handle token expiration
      clearAuth();
      window.location.href = '/login';
    }
    const error = await response.json();
    throw new ApiError(response.status, error.detail || 'Request failed');
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}
```

### Alternatives Considered
1. **React Query/SWR**: Good for caching but adds dependency; MVP keeps it simple
2. **Axios**: Adds dependency; native fetch is sufficient
3. **Per-component fetch**: Violates DRY, inconsistent error handling

---

## R4: Form Handling and Validation

### Decision
Use controlled components with React useState for form state. Client-side validation before submission mirrors backend constraints.

### Rationale
- No external form library needed for simple forms
- Immediate validation feedback improves UX
- Matches backend Pydantic validation rules
- Keeps bundle size minimal

### Validation Rules (from Backend)

| Field | Rules |
|-------|-------|
| email | Valid email format (EmailStr) |
| password | Min 8 characters |
| name | Max 255 characters (optional) |
| task.title | 1-200 characters, required |
| task.description | Max 1000 characters, optional |

### Implementation Pattern

```typescript
// components/auth/LoginForm.tsx
const [email, setEmail] = useState('');
const [password, setPassword] = useState('');
const [errors, setErrors] = useState<{ email?: string; password?: string }>({});

const validate = () => {
  const newErrors: typeof errors = {};
  if (!email.includes('@')) newErrors.email = 'Invalid email format';
  if (password.length < 8) newErrors.password = 'Password must be at least 8 characters';
  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
};
```

### Alternatives Considered
1. **React Hook Form**: Adds dependency; overkill for 3 simple forms
2. **Formik**: Same reasoning, adds bundle size
3. **Uncontrolled forms**: Harder to implement validation UX

---

## R5: Loading and Error States

### Decision
Each async operation shows a loading spinner. Errors display in a dismissible error message component. Use optimistic updates for task toggle.

### Rationale
- Users expect visual feedback (SC-003: < 2 seconds with feedback)
- Optimistic updates make toggles feel instant
- Error recovery should be graceful, not jarring

### UI State Patterns

**Loading States**:
- Page load: Full-page spinner
- Task operations: Button disabled + spinner icon
- Form submission: Submit button disabled + loading text

**Error States**:
- Network error: "Unable to connect. Please check your connection."
- 401 Unauthorized: Redirect to login
- 400 Bad Request: Show validation message from backend
- 500 Server Error: "Something went wrong. Please try again."

### Optimistic Update Pattern (Toggle)

```typescript
const handleToggle = async (task: Task) => {
  // Optimistic update
  setTasks(tasks.map(t =>
    t.id === task.id ? { ...t, completed: !t.completed } : t
  ));

  try {
    await api.toggleTask(userId, task.id, !task.completed);
  } catch (error) {
    // Revert on failure
    setTasks(tasks.map(t =>
      t.id === task.id ? { ...t, completed: task.completed } : t
    ));
    setError('Failed to update task');
  }
};
```

---

## R6: Responsive Design Strategy

### Decision
Mobile-first approach with Tailwind CSS breakpoints. Single-column layout on mobile, wider task items on desktop.

### Rationale
- 320px minimum width requirement (SC-004)
- Tailwind provides consistent breakpoints
- Mobile-first ensures core functionality works everywhere

### Breakpoint Strategy

| Breakpoint | Width | Layout |
|------------|-------|--------|
| Default (mobile) | < 640px | Single column, full-width cards |
| sm | ≥ 640px | Wider task items, more padding |
| md | ≥ 768px | Centered content, max-width container |
| lg | ≥ 1024px | Sidebar potential (future), comfortable reading width |

### Component Patterns

```typescript
// Task container
<div className="w-full max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">

// Task item
<div className="p-4 sm:p-6 rounded-lg border">

// Form layout
<form className="space-y-4 w-full max-w-md mx-auto">
```

---

## R7: Route Protection

### Decision
Client-side route protection using AuthProvider. Protected pages check auth state and redirect if not authenticated.

### Rationale
- Simple pattern without middleware complexity
- Fast feedback to user (no server round-trip for initial check)
- Works with static export if needed later

### Implementation Pattern

```typescript
// app/tasks/page.tsx
'use client';

import { useAuth } from '@/components/auth/AuthProvider';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function TasksPage() {
  const { auth } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!auth.isAuthenticated) {
      router.push('/login');
    }
  }, [auth.isAuthenticated, router]);

  if (!auth.isAuthenticated) {
    return <LoadingSpinner />; // Brief loading while redirecting
  }

  return <TaskList />;
}
```

### Alternatives Considered
1. **Middleware**: More complex, requires server-side logic
2. **Higher-Order Component**: Works but hooks are cleaner
3. **Layout-level protection**: Could cause flash of protected content

---

## R8: Environment Configuration

### Decision
Use Next.js environment variables with NEXT_PUBLIC_ prefix for client-accessible values.

### Rationale
- Standard Next.js pattern
- Clear distinction between server and client env vars
- Easy local development with .env.local

### Environment Variables

**Frontend (.env.local)**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Frontend (.env.production)**:
```env
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

### Security Note
- No secrets in frontend (no JWT_SECRET, no DATABASE_URL)
- Only public API URL exposed to client
- Backend handles all secret management

---

## Summary of Decisions

| Topic | Decision |
|-------|----------|
| Routing | Next.js 16+ App Router |
| Components | Server by default, Client for interactivity |
| Auth State | React Context + localStorage |
| API Client | Centralized fetch wrapper with auth |
| Forms | Controlled components, inline validation |
| Loading | Spinners, disabled buttons, optimistic updates |
| Responsive | Tailwind CSS, mobile-first |
| Protection | Client-side redirect in useEffect |
| Config | NEXT_PUBLIC_ env vars |

---

**Phase 0 Complete**: All technical questions resolved. Proceeding to Phase 1 design.
