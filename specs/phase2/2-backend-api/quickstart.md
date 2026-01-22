# Quickstart: Backend API

**Feature**: 003-backend-api
**Date**: 2026-01-18

## Prerequisites

- Module 1 (Database) completed and tested
- `.env` file configured with DATABASE_URL
- UV package manager installed

## Setup

### 1. Navigate to Backend Directory

```bash
cd phase-2/backend
```

### 2. Install New Dependencies

```bash
uv add fastapi uvicorn[standard]
```

### 3. Verify Dependencies

Check `pyproject.toml` includes:
- fastapi
- uvicorn[standard]
- sqlmodel (from Module 1)
- asyncpg (from Module 1)
- python-dotenv (from Module 1)

## Running the Server

### Start Development Server

```bash
uv run uvicorn main:app --reload --port 8000
```

### Verify Server Running

```bash
# Health check
curl http://localhost:8000/health
# Expected: {"status":"ok"}

# API info
curl http://localhost:8000/
# Expected: {"name":"Todo API","version":"1.0.0"}
```

## Testing Endpoints

### Create a Task

```bash
curl -X POST http://localhost:8000/api/user123/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

Expected response (201):
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-18T12:00:00",
  "updated_at": "2026-01-18T12:00:00"
}
```

### List Tasks

```bash
# All tasks
curl http://localhost:8000/api/user123/tasks

# Pending only
curl "http://localhost:8000/api/user123/tasks?status=pending"

# Sorted by title ascending
curl "http://localhost:8000/api/user123/tasks?sort=title&order=asc"
```

### Get Single Task

```bash
curl http://localhost:8000/api/user123/tasks/1
```

### Update Task

```bash
curl -X PUT http://localhost:8000/api/user123/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries and snacks"}'
```

### Toggle Completion

```bash
curl -X PATCH http://localhost:8000/api/user123/tasks/1/complete \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### Delete Task

```bash
curl -X DELETE http://localhost:8000/api/user123/tasks/1
# Expected: 204 No Content
```

## API Documentation

FastAPI auto-generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing User Isolation

```bash
# Create task for user1
curl -X POST http://localhost:8000/api/user1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "User 1 task"}'

# Create task for user2
curl -X POST http://localhost:8000/api/user2/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "User 2 task"}'

# List user1 tasks - should only see user1's task
curl http://localhost:8000/api/user1/tasks

# Try to access user2's task as user1 - should get 404
curl http://localhost:8000/api/user1/tasks/2
```

## Error Handling Tests

### Validation Error (400)

```bash
# Title too long (>200 chars)
curl -X POST http://localhost:8000/api/user123/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "'$(python3 -c "print('x'*201)"))'"}'
# Expected: 422 Validation Error
```

### Not Found (404)

```bash
# Non-existent task
curl http://localhost:8000/api/user123/tasks/99999
# Expected: {"detail":"Task not found"}
```

## Stopping the Server

Press `Ctrl+C` in the terminal running uvicorn.

## Troubleshooting

### "Module not found: db" or "models"

Ensure you're running from `phase-2/backend/` directory:
```bash
cd /path/to/project/phase-2/backend
uv run uvicorn main:app --reload
```

### Database Connection Error

Verify `.env` file has correct DATABASE_URL:
```bash
cat .env
# Should show: DATABASE_URL=postgresql+asyncpg://...
```

### Port Already in Use

Kill existing process or use different port:
```bash
uv run uvicorn main:app --reload --port 8001
```

## Files to Create

| File | Purpose |
|------|---------|
| main.py | FastAPI app with CORS, lifecycle |
| schemas.py | Pydantic models |
| routes/__init__.py | Package init |
| routes/tasks.py | Task endpoints |

## Next Steps

After completing Module 2:
1. Test all endpoints manually
2. Verify CORS working with browser
3. Check OpenAPI docs complete
4. Proceed to Module 3 (Authentication)
