---
title: Todo API
emoji: 📝
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# Todo API

FastAPI backend for the Todo application with JWT authentication.

## Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/{user_id}/tasks` - List tasks (JWT required)
- `POST /api/{user_id}/tasks` - Create task (JWT required)
- `PUT /api/{user_id}/tasks/{id}` - Update task (JWT required)
- `DELETE /api/{user_id}/tasks/{id}` - Delete task (JWT required)

## Environment Variables

Set these in your Space settings:
- `DATABASE_URL` - Neon PostgreSQL connection string
- `JWT_SECRET_KEY` - JWT signing secret (min 32 chars)
- `FRONTEND_URL` - Frontend URL for CORS
