# Frontend Module - Claude Code Guidance

## Module Context
This is the frontend module for Phase II of the Todo application (Module 4).

## Active Work
- **Module 4 (Frontend Web App)**: IN PROGRESS

## Technology Stack
- **Language**: TypeScript 5.x
- **Runtime**: Node.js 22+ (LTS)
- **Framework**: Next.js 15+ (App Router)
- **UI Library**: React 19
- **Styling**: Tailwind CSS 3.4
- **Package Manager**: npm

## File Structure
```
phase-2/frontend/
├── src/
│   ├── app/                      # Next.js App Router pages
│   │   ├── layout.tsx            # Root layout with AuthProvider
│   │   ├── page.tsx              # Home page (redirect)
│   │   ├── login/page.tsx        # Login page
│   │   ├── signup/page.tsx       # Signup page
│   │   └── tasks/page.tsx        # Task list (protected)
│   ├── components/
│   │   ├── auth/                 # Auth components
│   │   │   ├── AuthProvider.tsx
│   │   │   ├── LoginForm.tsx
│   │   │   └── SignupForm.tsx
│   │   ├── tasks/                # Task components
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── TaskEditForm.tsx
│   │   └── ui/                   # Shared UI components
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       ├── LoadingSpinner.tsx
│   │       ├── ErrorMessage.tsx
│   │       └── ConfirmDialog.tsx
│   └── lib/
│       ├── api.ts                # API client with auth
│       ├── auth.ts               # Token storage utilities
│       ├── types.ts              # TypeScript interfaces
│       └── constants.ts          # Validation constants
├── public/                       # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.ts
├── .env.example
└── .env.local                    # Local environment (gitignored)
```

## Key Patterns

### Client Components
All interactive components use `'use client'` directive:
- Forms (LoginForm, SignupForm, TaskForm)
- Task interactions (TaskItem, TaskList)
- Auth state (AuthProvider)

### Auth State Management
- AuthProvider context wraps the app
- Token stored in localStorage
- useAuth() hook for consuming auth state

### API Client
- fetchWithAuth() wrapper handles JWT injection
- Automatic 401 handling with redirect
- ApiError class for typed error handling

## API Endpoints (Backend)

### Public Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /api/auth/signup | User registration |
| POST | /api/auth/login | User login |
| POST | /api/auth/logout | User logout |

### Protected Endpoints (require JWT)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /api/{user_id}/tasks | List tasks |
| POST | /api/{user_id}/tasks | Create task |
| PUT | /api/{user_id}/tasks/{id} | Update task |
| DELETE | /api/{user_id}/tasks/{id} | Delete task |
| PATCH | /api/{user_id}/tasks/{id}/complete | Toggle completion |

## Commands
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run linting
npm run lint
```

## Environment Variables
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

## Code Standards
- TypeScript strict mode enabled
- No `any` types
- ESLint + Prettier formatting
- Tailwind CSS for styling
- Mobile-first responsive design
