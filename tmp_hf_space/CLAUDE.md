# Backend Module - Claude Code Guidance

## Module Context
This is the backend module for Phase V of the Todo application with Advanced Features and Event Architecture.

## Active Work
- **Phase II (Database, API, Auth)**: COMPLETE
- **Phase III (Chat Database, MCP Server, Chat Endpoint)**: COMPLETE
- **Phase V (Advanced Features + Events)**: COMPLETE

## Technology Stack
- **Python**: 3.13+
- **Web Framework**: FastAPI
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **Database**: Neon Serverless PostgreSQL
- **Driver**: asyncpg (async PostgreSQL driver)
- **Package Manager**: UV
- **Auth**: python-jose (JWT), passlib[bcrypt] (password hashing)
- **MCP**: mcp[cli] (official Anthropic MCP SDK with FastMCP)
- **HTTP Client**: httpx (for Dapr HTTP API calls)
- **Events**: Dapr Pub/Sub via HTTP API (localhost:3500)

## File Structure
```
phase-5/backend/
├── pyproject.toml         # UV project config
├── .env.example           # Environment template
├── main.py                # FastAPI app entry point
├── schemas.py             # Pydantic request/response models (extended Phase V)
├── db.py                  # Database connection & session management
├── models.py              # SQLModel: Task, User, Conversation, Message, Tag, TaskTag, Notification
├── events.py              # NEW: Dapr event publisher with graceful degradation
├── init_db.py             # Database initialization (creates all tables)
├── mcp_server.py          # MCP server with 7 task/tag/notification tools
├── auth/
│   ├── __init__.py
│   ├── password.py        # bcrypt password hashing
│   ├── jwt.py             # JWT creation and verification
│   └── middleware.py      # JWT verification dependency
└── routes/
    ├── __init__.py         # Router exports (tasks, auth, chat, tags, notifications)
    ├── tasks.py            # Task CRUD with search/filter/sort, tags, recurrence, events
    ├── auth.py             # Auth endpoints (signup, login, logout, profile)
    ├── chat.py             # AI chat endpoints
    ├── tags.py             # NEW: Tag CRUD endpoints
    └── notifications.py    # NEW: Notification listing endpoint
```

## Key Patterns

### Database Models (Phase V additions)
- **Task** extended with: priority (str), due_date (str), reminder_offset (int), recurrence_rule (JSON), next_occurrence (str), parent_task_id (self-referencing FK)
- **Tag** model: id, user_id, name, created_at. Unique constraint on (user_id, name)
- **TaskTag** junction model: task_id, tag_id (composite PK)
- **Notification** model: id, user_id, task_id, message, read, created_at

### Event Publishing
- `events.py` publishes to Dapr Pub/Sub via HTTP POST to `localhost:3500/v1.0/publish/pubsub/{topic}`
- Topics: `task-events` (task.created/updated/deleted/completed), `reminders`
- Graceful degradation: publish failures are logged but never fail the HTTP request

### Task Routes (Phase V)
- Search: ILIKE on title and description
- Filter: status, priority, tags (AND logic via subqueries), due_date range
- Sort: created_at, title, due_date (nulls last), priority (CASE expression)
- Tags: sync via replace pattern in task_tags junction table
- Recurrence: auto-creates next occurrence on completion (copies task + tags)

### MCP Tools (Phase V - 7 tools)
| Tool | Purpose | Parameters |
|------|---------|------------|
| add_task | Create task | user_id, title, description, priority, due_date, tag_names |
| list_tasks | List tasks | user_id, status, priority, search |
| complete_task | Mark done | user_id, task_id |
| delete_task | Remove task | user_id, task_id |
| update_task | Modify task | user_id, task_id, title, description, priority, due_date |
| list_tags | List tags | user_id |
| list_notifications | List notifications | user_id |

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
| GET | /api/{user_id}/tasks | List tasks (+ search/filter/sort params) |
| GET | /api/{user_id}/tasks/{id} | Get task |
| POST | /api/{user_id}/tasks | Create task (+ priority/due_date/tags/recurrence) |
| PUT | /api/{user_id}/tasks/{id} | Update task |
| DELETE | /api/{user_id}/tasks/{id} | Delete task |
| PATCH | /api/{user_id}/tasks/{id}/complete | Toggle completion (+ recurring auto-create) |
| GET | /api/{user_id}/tags | List tags |
| POST | /api/{user_id}/tags | Create tag |
| DELETE | /api/{user_id}/tags/{tag_id} | Delete tag |
| GET | /api/{user_id}/notifications | List notifications |
| GET | /api/auth/profile | Get user profile |
| PUT | /api/auth/profile | Update profile |
| PUT | /api/auth/password | Change password |

## Commands
```bash
# Run development server
uv run uvicorn main:app --reload --port 8000

# Initialize database (creates all tables)
uv run python init_db.py

# Run MCP server
uv run python mcp_server.py
```

## Environment Variables
- `DATABASE_URL`: Neon PostgreSQL connection string (required)
- `JWT_SECRET_KEY`: JWT signing secret (min 32 chars, required)
- `OPENAI_API_KEY`: OpenAI API key for chat (optional)
