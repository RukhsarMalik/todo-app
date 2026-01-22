# Quickstart: Frontend Web Application

**Feature**: 005-frontend-web-app
**Date**: 2026-01-19
**Phase**: 1 - Design

---

## Prerequisites

- **Node.js**: 22+ (LTS)
- **npm** or **pnpm**: Package manager
- **Backend API**: Running at http://localhost:8000 (see phase-2/backend)

---

## Setup

### 1. Create Next.js Project

```bash
cd phase-2

# Create Next.js 16+ app with TypeScript and Tailwind
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"

cd frontend
```

### 2. Configure Environment

Create `.env.local`:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Create `.env.example` (for version control):

```env
# Backend API URL (required)
NEXT_PUBLIC_API_URL=http://localhost:8000

# For production:
# NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

### 3. Install Dependencies

```bash
# No additional dependencies needed for MVP
# Next.js 16+ includes React 19 and Tailwind CSS 4
npm install
```

### 4. Project Structure

```
phase-2/frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── signup/
│   │   │   └── page.tsx
│   │   └── tasks/
│   │       └── page.tsx
│   ├── components/
│   │   ├── auth/
│   │   ├── tasks/
│   │   └── ui/
│   └── lib/
│       ├── api.ts
│       ├── auth.ts
│       └── types.ts
├── public/
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.ts
├── .env.local
├── .env.example
└── CLAUDE.md
```

---

## Development

### Start Development Server

```bash
# Start Next.js dev server
npm run dev
```

**URL**: http://localhost:3000

### Start Backend (required)

In a separate terminal:

```bash
cd phase-2/backend
uv run uvicorn main:app --reload --port 8000
```

**URL**: http://localhost:8000

### Development Flow

1. Ensure backend is running at http://localhost:8000
2. Start frontend at http://localhost:3000
3. Navigate to http://localhost:3000/signup to create account
4. After signup, you'll be redirected to /tasks
5. Create, edit, toggle, and delete tasks

---

## Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |

---

## Configuration Files

### next.config.ts

```typescript
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Enable strict mode for React
  reactStrictMode: true,
};

export default nextConfig;
```

### tsconfig.json

Default from create-next-app with these important settings:

```json
{
  "compilerOptions": {
    "strict": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### tailwind.config.ts

Default from create-next-app. Custom colors can be added as needed.

---

## Testing the Integration

### 1. Backend Health Check

```bash
curl http://localhost:8000/health
# Expected: {"status":"ok"}
```

### 2. Frontend Health Check

Navigate to http://localhost:3000
- Should redirect to /login if not authenticated

### 3. Full Flow Test

1. Go to http://localhost:3000/signup
2. Create account (email, password 8+ chars)
3. Verify redirect to /tasks
4. Create a task
5. Toggle task completion
6. Edit task
7. Delete task
8. Logout
9. Verify redirect to /login
10. Login with created credentials
11. Verify tasks are still there (persistence)

---

## Environment Variables

### Development (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Production (Vercel Dashboard)

```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

**Note**: `NEXT_PUBLIC_` prefix exposes variable to browser. Only use for public values.

---

## Deployment (Vercel)

### 1. Push to GitHub

```bash
git add .
git commit -m "Frontend: Initial Next.js setup"
git push origin 005-frontend-web-app
```

### 2. Connect to Vercel

1. Go to https://vercel.com
2. Import repository
3. Select `phase-2/frontend` as root directory
4. Add environment variables:
   - `NEXT_PUBLIC_API_URL`: Your deployed backend URL

### 3. Deploy

Vercel will automatically build and deploy on push to main/branch.

---

## Troubleshooting

### CORS Errors

If you see CORS errors in browser console:

1. Verify backend is running
2. Check backend CORS config in `main.py` includes `http://localhost:3000`
3. For production, update `FRONTEND_URL` in backend .env

### 401 Unauthorized

1. Check if token is stored in localStorage
2. Verify token hasn't expired (7-day expiration)
3. Clear localStorage and login again

### API Connection Refused

1. Verify backend is running: `curl http://localhost:8000/health`
2. Check `NEXT_PUBLIC_API_URL` in .env.local
3. Restart Next.js dev server after changing .env

### Build Errors

```bash
# Clean and rebuild
rm -rf .next
npm run build
```

---

## Next Steps

After setup, implement components in this order:

1. **lib/types.ts** - TypeScript interfaces
2. **lib/api.ts** - API client
3. **lib/auth.ts** - Auth utilities
4. **components/ui/** - Reusable UI components
5. **components/auth/AuthProvider.tsx** - Auth context
6. **app/layout.tsx** - Root layout with AuthProvider
7. **components/auth/LoginForm.tsx** - Login form
8. **components/auth/SignupForm.tsx** - Signup form
9. **app/login/page.tsx** - Login page
10. **app/signup/page.tsx** - Signup page
11. **components/tasks/** - Task components
12. **app/tasks/page.tsx** - Task list page
13. **app/page.tsx** - Home redirect

---

**Quickstart Complete**: Ready to implement.
