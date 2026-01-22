# Implementation Plan: Frontend Web Application

**Branch**: `005-frontend-web-app` | **Date**: 2026-01-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-frontend-web-app/spec.md`

## Summary

Build a responsive Next.js 16+ frontend for the Todo application that integrates with the existing FastAPI backend (Module 2/3). The frontend will provide user registration, login, and complete task CRUD operations through an intuitive browser-based interface with JWT authentication.

## Technical Context

**Language/Version**: TypeScript 5.x with Node.js 22+ (LTS)
**Primary Dependencies**: Next.js 16+ (App Router), React 19, Tailwind CSS 4
**Storage**: N/A (consumes backend API; Neon PostgreSQL via FastAPI)
**Testing**: Vitest for unit tests, Playwright for E2E (optional for MVP)
**Target Platform**: Modern browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
**Project Type**: Web frontend (monorepo structure: phase-2/frontend/)
**Performance Goals**:
- Initial page load < 3 seconds (LCP)
- Task operations complete with visual feedback < 2 seconds
- Time to Interactive < 3 seconds on 3G
**Constraints**:
- Must integrate with existing backend at http://localhost:8000 (dev) or deployed URL
- JWT tokens must be stored securely (httpOnly cookie preferred, localStorage acceptable for MVP)
- Must handle token expiration gracefully
**Scale/Scope**: Single-user task management, ~100 tasks per user, responsive from 320px to 1920px+

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase II Constitution Compliance

| Principle | Status | Notes |
|-----------|--------|-------|
| VIII. Monorepo Structure | ✅ PASS | Frontend in `phase-2/frontend/` |
| IX. API-First Design | ✅ PASS | Frontend consumes FastAPI REST endpoints exclusively |
| X. Database Persistence | ✅ PASS | Backend handles PostgreSQL; frontend is stateless |
| XI. Multi-User Support | ✅ PASS | JWT-based user isolation via backend |
| XII. Authentication Required | ✅ PASS | All task endpoints require JWT via Authorization header |

### Phase I Principles (Continued)

| Principle | Status | Notes |
|-----------|--------|-------|
| I. AI-Native Development | ✅ PASS | All code via Claude Code + Spec-Kit Plus |
| II. Specification-First | ✅ PASS | This plan follows approved spec.md |
| III. Clean Code & Standards | ✅ PASS | TypeScript strict mode, ESLint, Prettier |
| V. Graceful Error Handling | ✅ PASS | User-friendly error messages, no raw exceptions |
| VII. User-Centric Design | ✅ PASS | Intuitive UI with loading states and feedback |

### Security Requirements Check

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| JWT in Authorization header | ✅ PASS | Custom fetch wrapper adds Bearer token |
| Secure token storage | ✅ PASS | localStorage for MVP; httpOnly cookie for production |
| Environment variables for secrets | ✅ PASS | NEXT_PUBLIC_API_URL only; no secrets in frontend |
| No hardcoded credentials | ✅ PASS | API URL from env; JWT from auth flow |

**GATE RESULT**: ✅ All checks pass. Proceeding to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/005-frontend-web-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
phase-2/frontend/
├── src/
│   ├── app/                      # Next.js App Router pages
│   │   ├── layout.tsx            # Root layout with providers
│   │   ├── page.tsx              # Home page (redirect to /tasks or /login)
│   │   ├── login/
│   │   │   └── page.tsx          # Login page
│   │   ├── signup/
│   │   │   └── page.tsx          # Signup page
│   │   └── tasks/
│   │       └── page.tsx          # Task list (protected)
│   ├── components/
│   │   ├── auth/                 # Auth-related components
│   │   │   ├── LoginForm.tsx
│   │   │   ├── SignupForm.tsx
│   │   │   └── AuthProvider.tsx
│   │   ├── tasks/                # Task-related components
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── TaskEditForm.tsx
│   │   └── ui/                   # Shared UI components
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       ├── LoadingSpinner.tsx
│   │       └── ErrorMessage.tsx
│   └── lib/
│       ├── api.ts                # API client with auth
│       ├── auth.ts               # Auth utilities (token storage)
│       └── types.ts              # TypeScript interfaces
├── public/                       # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.ts
├── .env.example
├── .env.local                    # Local environment (gitignored)
└── CLAUDE.md                     # Frontend-specific guidance
```

**Structure Decision**: Web application structure per Constitution VIII. Frontend in `phase-2/frontend/` alongside existing `phase-2/backend/`. Next.js App Router for server/client component optimization.

## Complexity Tracking

No constitution violations identified. Standard Next.js patterns apply.

---

## Backend API Reference (Existing)

The frontend integrates with the completed backend (Modules 2 & 3).

### Authentication Endpoints

| Method | Endpoint | Purpose | Request | Response |
|--------|----------|---------|---------|----------|
| POST | /api/auth/signup | User registration | `{email, password, name?}` | `{access_token, token_type, user_id, email}` |
| POST | /api/auth/login | User login | `{email, password}` | `{access_token, token_type, user_id, email}` |
| POST | /api/auth/logout | User logout | - | `{message}` |

### Task Endpoints (JWT Required)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /api/{user_id}/tasks | List tasks |
| GET | /api/{user_id}/tasks/{id} | Get task |
| POST | /api/{user_id}/tasks | Create task |
| PUT | /api/{user_id}/tasks/{id} | Update task |
| DELETE | /api/{user_id}/tasks/{id} | Delete task |
| PATCH | /api/{user_id}/tasks/{id}/complete | Toggle completion |

### Response Formats

**Task Object**:
```json
{
  "id": 1,
  "user_id": "uuid-string",
  "title": "Task title",
  "description": "Optional description",
  "completed": false,
  "created_at": "2026-01-19T12:00:00",
  "updated_at": "2026-01-19T12:00:00"
}
```

**Error Response**:
```json
{
  "detail": "Error message"
}
```

---

## Post-Design Constitution Check

*Re-evaluation after Phase 1 design completion.*

### Phase II Constitution Compliance (Post-Design)

| Principle | Status | Verification |
|-----------|--------|--------------|
| VIII. Monorepo Structure | ✅ PASS | `phase-2/frontend/` defined in project structure |
| IX. API-First Design | ✅ PASS | API client contracts define all backend interactions |
| X. Database Persistence | ✅ PASS | Backend handles; frontend is stateless |
| XI. Multi-User Support | ✅ PASS | userId in all API calls; AuthProvider context |
| XII. Authentication Required | ✅ PASS | JWT via Authorization header in api.ts |

### Technical Standards Verification

| Standard | Status | Evidence |
|----------|--------|----------|
| TypeScript strict mode | ✅ PASS | tsconfig.json with strict: true |
| No `any` types | ✅ PASS | All interfaces fully typed in data-model.md |
| Responsive design | ✅ PASS | Tailwind mobile-first approach in research.md |
| Loading states | ✅ PASS | Component contracts specify loading behavior |
| Error handling | ✅ PASS | ApiError class and error UI components defined |
| Environment variables | ✅ PASS | NEXT_PUBLIC_API_URL only; no secrets |

### Security Verification

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| JWT storage | ✅ PASS | localStorage with AuthProvider |
| Token injection | ✅ PASS | fetchWithAuth wrapper |
| 401 handling | ✅ PASS | Clear auth, redirect to login |
| User isolation | ✅ PASS | userId in all task API calls |
| No secrets in frontend | ✅ PASS | Only NEXT_PUBLIC_API_URL exposed |

**POST-DESIGN GATE RESULT**: ✅ All checks pass. Ready for task generation.

---

## Artifacts Generated

| Artifact | Status | Path |
|----------|--------|------|
| plan.md | ✅ Complete | specs/005-frontend-web-app/plan.md |
| research.md | ✅ Complete | specs/005-frontend-web-app/research.md |
| data-model.md | ✅ Complete | specs/005-frontend-web-app/data-model.md |
| api-client.md | ✅ Complete | specs/005-frontend-web-app/contracts/api-client.md |
| component-contracts.md | ✅ Complete | specs/005-frontend-web-app/contracts/component-contracts.md |
| quickstart.md | ✅ Complete | specs/005-frontend-web-app/quickstart.md |
| tasks.md | ✅ Complete | specs/005-frontend-web-app/tasks.md |

---

## Next Steps

1. ~~Run `/sp.tasks` to generate implementation tasks from this plan~~ ✅ Complete (66 tasks generated)
2. Execute tasks following the Spec-Driven Development workflow
3. Validate against acceptance criteria in spec.md
