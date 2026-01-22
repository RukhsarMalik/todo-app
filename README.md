# Phase II: Full-Stack Todo Application

A complete full-stack task management application built with Next.js frontend and FastAPI backend.

## Live Demo

- **Frontend**: [https://your-frontend.vercel.app](https://your-frontend.vercel.app)
- **Backend API**: [https://your-backend.vercel.app](https://your-backend.vercel.app)
- **Demo Video**: [Watch Demo](https://youtube.com/watch?v=...)

> Update these URLs after deployment

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15, React 19, TypeScript 5.x, Tailwind CSS |
| Backend | Python 3.12+, FastAPI, SQLModel |
| Database | Neon Serverless PostgreSQL |
| Auth | JWT with python-jose, bcrypt password hashing |
| Deployment | Vercel (Frontend & Backend) |

## Features

- User authentication (signup/login/logout)
- Create, read, update, delete tasks
- Toggle task completion
- Multi-user isolation (users only see their own tasks)
- Responsive design
- JWT-based session management

## Project Structure

```
hackathon-2/
├── phase-1/                  # Console app (Module 0)
├── phase-2/
│   ├── database/             # Module 1: Database schema
│   ├── backend/              # Module 2 & 3: FastAPI + Auth
│   │   ├── main.py           # FastAPI entry point
│   │   ├── models.py         # SQLModel models
│   │   ├── routes/           # API endpoints
│   │   ├── auth/             # JWT authentication
│   │   └── vercel.json       # Vercel deployment config
│   └── frontend/             # Module 4: Next.js app
│       ├── src/app/          # App Router pages
│       ├── src/components/   # React components
│       └── src/lib/          # API client & utilities
├── specs/                    # Feature specifications
└── README.md                 # This file
```

## Local Development Setup

### Prerequisites

- Python 3.12+
- Node.js 22+ (LTS)
- uv (Python package manager)
- npm
- Neon PostgreSQL database

### Backend Setup

```bash
cd phase-2/backend

# Copy environment template
cp .env.example .env

# Edit .env with your credentials:
# - DATABASE_URL (from Neon dashboard)
# - JWT_SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")

# Install dependencies
uv sync

# Initialize database
uv run python init_db.py

# Run development server
uv run uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd phase-2/frontend

# Copy environment template
cp .env.example .env.local

# Edit .env.local:
# - NEXT_PUBLIC_API_URL=http://localhost:8000

# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the app.

## Environment Variables

### Backend (`phase-2/backend/.env`)

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | Neon PostgreSQL connection string | `postgresql+asyncpg://user:pass@host/db?ssl=require` |
| JWT_SECRET_KEY | JWT signing secret (min 32 chars) | Generate with `secrets.token_urlsafe(32)` |
| FRONTEND_URL | Production frontend URL (for CORS) | `https://your-frontend.vercel.app` |

### Frontend (`phase-2/frontend/.env.local`)

| Variable | Description | Example |
|----------|-------------|---------|
| NEXT_PUBLIC_API_URL | Backend API URL | `http://localhost:8000` or `https://your-backend.vercel.app` |

## Deployment

### Backend (Vercel)

1. Create new project on [Vercel](https://vercel.com)
2. Import GitHub repository
3. Set root directory: `phase-2/backend`
4. Add environment variables:
   - `DATABASE_URL`
   - `JWT_SECRET_KEY`
   - `FRONTEND_URL` (your frontend Vercel URL)
5. Deploy

### Frontend (Vercel)

1. Create new project on [Vercel](https://vercel.com)
2. Import GitHub repository
3. Set root directory: `phase-2/frontend`
4. Add environment variables:
   - `NEXT_PUBLIC_API_URL` (your backend Vercel URL)
5. Deploy

## API Endpoints

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/api/auth/signup` | User registration |
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/logout` | User logout |

### Protected Endpoints (require JWT)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

## Testing Scenarios

### New User Flow
1. Navigate to frontend URL
2. Click "Sign Up"
3. Enter email and password
4. Account created and logged in
5. Empty tasks page displayed

### Task Management
1. Create multiple tasks
2. Toggle completion on a task
3. Edit a task
4. Delete a task
5. Logout and login again
6. Tasks persist correctly

### Multi-user Isolation
1. Create User A, add tasks
2. Logout
3. Create User B, add tasks
4. User B cannot see User A's tasks

## Specifications

All feature specifications are in the `/specs/` folder:
- `specs/phase2/1-database/` - Database module spec
- `specs/phase2/2-backend-api/` - Backend API spec
- `specs/phase2/3-jwt-auth/` - Authentication spec
- `specs/005-frontend-web-app/` - Frontend spec

## Demo Video

[Watch the 90-second demo](https://youtube.com/watch?v=...)

The demo covers:
- Signup/Login flow
- Creating tasks
- Viewing tasks
- Updating tasks
- Toggle completion
- Deleting tasks
- Logout
- Deployed URLs

## Author

RukhsarMalik - Hackathon II Submission

## License

This project is for educational purposes as part of the Hackathon II program.
