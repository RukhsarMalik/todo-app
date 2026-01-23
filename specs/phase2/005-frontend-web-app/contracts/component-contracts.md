# Component Contracts

**Feature**: 005-frontend-web-app
**Date**: 2026-01-19
**Phase**: 1 - Design

---

## Overview

This document defines the component interface contracts for the frontend application. Each component's props, state, and behavior are specified.

---

## Auth Components

### AuthProvider

Context provider for authentication state.

**File**: `components/auth/AuthProvider.tsx`

```typescript
interface AuthContextValue {
  auth: AuthState;
  login: (token: string, userId: string, email: string) => void;
  logout: () => void;
}

interface AuthProviderProps {
  children: React.ReactNode;
}
```

**Behavior**:
- On mount: Check localStorage for existing token, restore auth state
- `login()`: Store token in localStorage, update context state
- `logout()`: Clear localStorage, clear context state, redirect to /login
- Provides `useAuth()` hook for consuming components

**Usage**:
```tsx
// app/layout.tsx
<AuthProvider>
  {children}
</AuthProvider>

// Any component
const { auth, login, logout } = useAuth();
```

---

### LoginForm

User login form component.

**File**: `components/auth/LoginForm.tsx`

```typescript
interface LoginFormProps {
  onSuccess?: () => void;
}
```

**State**:
```typescript
{
  email: string;
  password: string;
  errors: { email?: string; password?: string };
  isSubmitting: boolean;
  apiError: string | null;
}
```

**Behavior**:
1. Validate email format and password length on blur/submit
2. On submit: Call `api.login()`, then `auth.login()` with response
3. On success: Redirect to `/tasks` (or call `onSuccess` prop)
4. On error: Display API error message

**Acceptance Criteria**:
- [ ] Email field with validation
- [ ] Password field (type="password") with min length 8
- [ ] Submit button disabled while submitting
- [ ] Loading spinner during submission
- [ ] Error message for invalid credentials
- [ ] Link to signup page

---

### SignupForm

User registration form component.

**File**: `components/auth/SignupForm.tsx`

```typescript
interface SignupFormProps {
  onSuccess?: () => void;
}
```

**State**:
```typescript
{
  email: string;
  password: string;
  name: string;
  errors: { email?: string; password?: string; name?: string };
  isSubmitting: boolean;
  apiError: string | null;
}
```

**Behavior**:
1. Validate all fields on blur/submit
2. On submit: Call `api.signup()`, then `auth.login()` with response
3. On success: Redirect to `/tasks` (or call `onSuccess` prop)
4. On error: Display API error message

**Acceptance Criteria**:
- [ ] Email field with validation
- [ ] Password field with min length 8
- [ ] Optional name field
- [ ] Submit button disabled while submitting
- [ ] Loading spinner during submission
- [ ] Error message for "Email already registered"
- [ ] Link to login page

---

## Task Components

### TaskList

Main task list container with data fetching.

**File**: `components/tasks/TaskList.tsx`

```typescript
interface TaskListProps {
  initialTasks?: Task[];  // For SSR (optional)
}
```

**State**:
```typescript
{
  tasks: Task[];
  isLoading: boolean;
  error: string | null;
  editingTaskId: number | null;
}
```

**Behavior**:
1. On mount: Fetch tasks from API using `api.getTasks(userId)`
2. Render loading spinner while fetching
3. Render empty state if no tasks
4. Render TaskItem for each task
5. Handle task operations (create, toggle, update, delete)

**Acceptance Criteria**:
- [ ] Loading state while fetching
- [ ] Empty state with "Create your first task" message
- [ ] List of TaskItem components
- [ ] TaskForm at top for creating new tasks
- [ ] Error message if fetch fails
- [ ] Logout button in header

---

### TaskItem

Individual task display with actions.

**File**: `components/tasks/TaskItem.tsx`

```typescript
interface TaskItemProps {
  task: Task;
  isEditing: boolean;
  onToggle: (task: Task) => void;
  onUpdate: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onEditStart: (taskId: number) => void;
  onEditCancel: () => void;
}
```

**State**: None (controlled component)

**Behavior**:
- Display mode: Show checkbox, title, description, edit/delete buttons
- Edit mode: Show TaskEditForm
- Checkbox toggles completion (calls `onToggle`)
- Edit button starts edit mode (calls `onEditStart`)
- Delete button shows confirmation, then calls `onDelete`

**Acceptance Criteria**:
- [ ] Checkbox for completion status
- [ ] Title with strikethrough when completed
- [ ] Description (truncated with "show more" for long text)
- [ ] Edit button (pencil icon)
- [ ] Delete button (trash icon)
- [ ] Confirmation dialog before delete
- [ ] Visual distinction for completed tasks (faded, strikethrough)

---

### TaskForm

Create new task form.

**File**: `components/tasks/TaskForm.tsx`

```typescript
interface TaskFormProps {
  onTaskCreated: (task: Task) => void;
}
```

**State**:
```typescript
{
  title: string;
  description: string;
  errors: { title?: string; description?: string };
  isSubmitting: boolean;
}
```

**Behavior**:
1. Validate title (required, 1-200 chars) and description (max 1000 chars)
2. On submit: Call `api.createTask()`, then `onTaskCreated(task)`
3. On success: Clear form
4. On error: Display error message

**Acceptance Criteria**:
- [ ] Title input (required)
- [ ] Description textarea (optional)
- [ ] Submit button disabled if title empty
- [ ] Submit button disabled while submitting
- [ ] Form clears after successful creation
- [ ] Error message if creation fails

---

### TaskEditForm

Edit existing task form (inline).

**File**: `components/tasks/TaskEditForm.tsx`

```typescript
interface TaskEditFormProps {
  task: Task;
  onSave: (task: Task) => void;
  onCancel: () => void;
}
```

**State**:
```typescript
{
  title: string;
  description: string;
  errors: { title?: string; description?: string };
  isSubmitting: boolean;
}
```

**Behavior**:
1. Pre-fill with existing task values
2. Validate on submit
3. On save: Call `api.updateTask()`, then `onSave(updatedTask)`
4. On cancel: Call `onCancel()` (parent reverts to display mode)

**Acceptance Criteria**:
- [ ] Title input pre-filled
- [ ] Description textarea pre-filled
- [ ] Save button
- [ ] Cancel button
- [ ] Remain in edit mode if save fails
- [ ] Validation messages inline

---

## UI Components

### Button

Reusable button component.

**File**: `components/ui/Button.tsx`

```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: React.ReactNode;
}
```

**Variants**:
- `primary`: Blue background, white text
- `secondary`: Gray background, dark text
- `danger`: Red background, white text

**Behavior**:
- Shows loading spinner when `isLoading=true`
- Disabled when `isLoading=true` or `disabled=true`

---

### Input

Reusable text input component.

**File**: `components/ui/Input.tsx`

```typescript
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}
```

**Behavior**:
- Renders label above input if provided
- Shows error message below input if provided
- Red border when error exists

---

### LoadingSpinner

Loading indicator component.

**File**: `components/ui/LoadingSpinner.tsx`

```typescript
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}
```

**Behavior**:
- Animated spinner (CSS animation)
- Size variants for different contexts

---

### ErrorMessage

Error display component.

**File**: `components/ui/ErrorMessage.tsx`

```typescript
interface ErrorMessageProps {
  message: string;
  onDismiss?: () => void;
}
```

**Behavior**:
- Red background, error text
- Optional dismiss button (X icon)
- Auto-dismiss after 5 seconds (optional)

---

### ConfirmDialog

Confirmation modal for destructive actions.

**File**: `components/ui/ConfirmDialog.tsx`

```typescript
interface ConfirmDialogProps {
  isOpen: boolean;
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
}
```

**Behavior**:
- Modal overlay with centered dialog
- Title, message, confirm/cancel buttons
- Escape key closes (calls onCancel)
- Click outside closes (calls onCancel)

---

## Page Components

### HomePage (app/page.tsx)

Landing/redirect page.

**Behavior**:
- If authenticated: Redirect to `/tasks`
- If not authenticated: Redirect to `/login`

---

### LoginPage (app/login/page.tsx)

Login page wrapper.

**Behavior**:
- If already authenticated: Redirect to `/tasks`
- Render LoginForm
- Link to signup

---

### SignupPage (app/signup/page.tsx)

Signup page wrapper.

**Behavior**:
- If already authenticated: Redirect to `/tasks`
- Render SignupForm
- Link to login

---

### TasksPage (app/tasks/page.tsx)

Protected task management page.

**Behavior**:
- If not authenticated: Redirect to `/login`
- Render header with user email and logout button
- Render TaskList

---

## Component Hierarchy

```
RootLayout (Server)
└── AuthProvider (Client)
    ├── HomePage (Client)
    │   └── [Redirect logic]
    │
    ├── LoginPage (Client)
    │   └── LoginForm
    │       ├── Input (email)
    │       ├── Input (password)
    │       ├── Button (submit)
    │       └── ErrorMessage
    │
    ├── SignupPage (Client)
    │   └── SignupForm
    │       ├── Input (email)
    │       ├── Input (password)
    │       ├── Input (name)
    │       ├── Button (submit)
    │       └── ErrorMessage
    │
    └── TasksPage (Client, Protected)
        ├── Header
        │   ├── User email
        │   └── Button (logout)
        │
        └── TaskList
            ├── TaskForm
            │   ├── Input (title)
            │   ├── Textarea (description)
            │   └── Button (submit)
            │
            ├── LoadingSpinner (while loading)
            ├── EmptyState (if no tasks)
            │
            └── TaskItem (for each task)
                ├── Checkbox
                ├── Title/Description
                ├── Button (edit)
                ├── Button (delete)
                │
                └── TaskEditForm (when editing)
                    ├── Input (title)
                    ├── Textarea (description)
                    ├── Button (save)
                    └── Button (cancel)
```

---

**Component Contracts Complete**: Ready for implementation.
