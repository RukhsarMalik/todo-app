# Backend Module - Claude Code Guidance

## Module Context
This is the backend module for Phase III of the Todo application with AI Chatbot capabilities.

## Active Work
- **Phase II Module 1 (Database)**: COMPLETE
- **Phase II Module 2 (Backend API)**: COMPLETE
- **Phase II Module 3 (Authentication)**: COMPLETE (see specs/004-jwt-auth/)
- **Phase III Module 1 (Chat Database)**: COMPLETE - Conversation and Message models added
- **Phase III Module 2 (MCP Server)**: COMPLETE - MCP server with 5 task tools

## Technology Stack
- **Python**: 3.12+
- **Web Framework**: FastAPI
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **Database**: Neon Serverless PostgreSQL
- **Driver**: asyncpg (async PostgreSQL driver)
- **Package Manager**: UV
- **Auth (Module 3)**: python-jose (JWT), passlib[bcrypt] (password hashing)
- **MCP (Module 2)**: mcp[cli] (official Anthropic MCP SDK with FastMCP)

## File Structure
```
phase-3/backend/
├── pyproject.toml         # UV project config
├── .env.example           # Environment template
├── .env                   # Local environment (gitignored)
├── main.py                # FastAPI app entry point
├── schemas.py             # Pydantic request/response models
├── db.py                  # Database connection & session management
├── models.py              # SQLModel Task, User, Conversation, Message classes
├── init_db.py             # Database initialization script
├── test_db.py             # Task/User validation script
├── test_conversations.py  # Conversation/Message validation script
├── mcp_server.py          # MCP server with task tools (Phase III Module 2)
├── auth/                  # Module 3: Authentication
│   ├── __init__.py        # Auth exports
│   ├── password.py        # bcrypt password hashing
│   ├── jwt.py             # JWT creation and verification
│   └── middleware.py      # JWT verification dependency
└── routes/
    ├── __init__.py        # Router exports
    ├── tasks.py           # Task CRUD endpoints (JWT protected)
    └── auth.py            # Auth endpoints (signup, login, logout)
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

### Conversation Model (Phase III)
- Inherits from `SQLModel` with `table=True`
- Fields: id (UUID), user_id (FK to users), title, created_at, updated_at
- Explicit table name: `__tablename__ = "conversations"`
- Foreign key to users with CASCADE delete (deleting user removes all conversations)

### Message Model (Phase III)
- Inherits from `SQLModel` with `table=True`
- Fields: id (UUID), conversation_id (FK to conversations), role, content, created_at
- Explicit table name: `__tablename__ = "messages"`
- Foreign key to conversations with CASCADE delete (deleting conversation removes all messages)
- **Validators** (use `model_validate()` to trigger):
  - `role`: Must be one of "user", "assistant", "system"
  - `content`: Non-empty, max 10,000 characters

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

### MCP Server Patterns (Phase III Module 2)
- FastMCP from `mcp.server.fastmcp` for server initialization
- `@mcp.tool()` decorator for defining tools
- Tools use `_get_session_maker()` for database access (not FastAPI's `get_session`)
- NEVER use `print()` in MCP server - corrupts JSON-RPC protocol
- All tools return JSON strings via `json.dumps()`
- All tools validate `user_id` before any operation
- Ownership check: query by task_id AND user_id for security

### MCP Tools Available
| Tool | Purpose | Parameters |
|------|---------|------------|
| add_task | Create new task | user_id, title, description (optional) |
| list_tasks | List user's tasks | user_id, status (all/pending/completed) |
| complete_task | Mark task done | user_id, task_id |
| delete_task | Remove task | user_id, task_id |
| update_task | Modify task | user_id, task_id, title (opt), description (opt) |

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

# Run init_db script (creates all tables: users, tasks, conversations, messages)
uv run python init_db.py

# Run Task/User validation script
uv run python test_db.py

# Run Conversation/Message validation script (Phase III)
uv run python test_conversations.py

# Run MCP server (Phase III Module 2)
uv run python mcp_server.py
```

## Environment Variables
- `DATABASE_URL`: Neon PostgreSQL connection string (required)
- `JWT_SECRET_KEY`: JWT signing secret (min 32 chars, required for Module 3)

## Code Standards
- Type hints on all functions and variables
- Docstrings for modules, classes, and functions
- Async/await for all database operations
- No hardcoded credentials
