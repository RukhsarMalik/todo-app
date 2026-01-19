# Backend Module - Claude Code Guidance

## Module Context
This is the backend module for Phase II of the Todo application.

## Active Work
- **Module 1 (Database)**: COMPLETE
- **Module 2 (Backend API)**: COMPLETE
- **Module 3 (Authentication)**: COMPLETE (see specs/004-jwt-auth/)

## Technology Stack
- **Python**: 3.12+
- **Web Framework**: FastAPI
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **Database**: Neon Serverless PostgreSQL
- **Driver**: asyncpg (async PostgreSQL driver)
- **Package Manager**: UV
- **Auth (Module 3)**: python-jose (JWT), passlib[bcrypt] (password hashing)

## File Structure
```
phase-2/backend/
├── pyproject.toml    # UV project config
├── .env.example      # Environment template
├── .env              # Local environment (gitignored)
├── main.py           # FastAPI app entry point
├── schemas.py        # Pydantic request/response models
├── db.py             # Database connection & session management
├── models.py         # SQLModel Task + User classes
├── init_db.py        # Database initialization script
├── test_db.py        # Validation script
├── auth/             # Module 3: Authentication
│   ├── __init__.py   # Auth exports
│   ├── password.py   # bcrypt password hashing
│   ├── jwt.py        # JWT creation and verification
│   └── middleware.py # JWT verification dependency
└── routes/
    ├── __init__.py   # Router exports
    ├── tasks.py      # Task CRUD endpoints (JWT protected)
    └── auth.py       # Auth endpoints (signup, login, logout)
```

## Key Patterns

### Database Connection
- Use `AsyncEngine` from SQLModel
- Connection string format: `postgresql+asyncpg://...?ssl=require`
- Connection pooling: min=1, max=10

### Session Management
- Use `async_sessionmaker` for session factory
- FastAPI dependency injection pattern with `get_session()`
- Always use try/finally for session cleanup

### Task Model
- Inherits from `SQLModel` with `table=True`
- Fields: id, user_id, title, description, completed, created_at, updated_at
- Explicit table name: `__tablename__ = "tasks"`

### API Patterns
- All task endpoints under `/api/{user_id}/tasks`
- JWT authentication required for all task endpoints
- Token user_id must match URL user_id (403 on mismatch)
- Pydantic schemas for request/response validation
- HTTPException for consistent error responses

### Authentication Patterns
- JWT tokens with 7-day expiration (HS256 algorithm)
- Password hashing with bcrypt via passlib
- `get_current_user` dependency for protected routes
- HTTPBearer security scheme for OpenAPI docs

## API Endpoints

### Public Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | / | API info |
| GET | /health | Health check |
| POST | /api/auth/signup | User registration |
| POST | /api/auth/login | User login |
| POST | /api/auth/logout | User logout |

### Protected Endpoints (require JWT)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /api/{user_id}/tasks | List tasks |
| GET | /api/{user_id}/tasks/{id} | Get task |
| POST | /api/{user_id}/tasks | Create task |
| PUT | /api/{user_id}/tasks/{id} | Update task |
| DELETE | /api/{user_id}/tasks/{id} | Delete task |
| PATCH | /api/{user_id}/tasks/{id}/complete | Toggle completion |

## Commands
```bash
# Run development server
uv run uvicorn main:app --reload --port 8000

# Run init_db script
uv run python init_db.py

# Run validation script
uv run python test_db.py
```

## Environment Variables
- `DATABASE_URL`: Neon PostgreSQL connection string (required)
- `JWT_SECRET_KEY`: JWT signing secret (min 32 chars, required for Module 3)

## Code Standards
- Type hints on all functions and variables
- Docstrings for modules, classes, and functions
- Async/await for all database operations
- No hardcoded credentials
