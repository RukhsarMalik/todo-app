# Phase III: AI-Powered Todo Application with Chat Interface

An advanced full-stack task management application featuring AI chatbot integration built with Next.js frontend and FastAPI backend.

## Live Demo

- **Frontend**: [https://frontend-ten-opal-98.vercel.app](https://frontend-ten-opal-98.vercel.app)
- **Backend API**: [https://backend-lilac-two-78.vercel.app](https://backend-lilac-two-78.vercel.app)
- **Demo Video**: [Watch Demo](https://youtube.com/watch?v=...) *(Add your video link)*

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15, React 19, TypeScript 5.x, Tailwind CSS |
| Backend | Python 3.12+, FastAPI, SQLModel |
| Database | Neon Serverless PostgreSQL |
| Auth | JWT with python-jose, bcrypt password hashing |
| AI Integration | OpenAI GPT-4o-mini with function calling |
| AI Tools | Anthropic MCP (Model Context Protocol) Server |
| Deployment | Vercel (Frontend & Backend) |

## Features

- User authentication (signup/login/logout)
- Create, read, update, delete tasks
- Toggle task completion
- Multi-user isolation (users only see their own tasks)
- Responsive design
- JWT-based session management
- **AI Chatbot**: Natural language interaction for task management
- **Conversation History**: Persistent chat sessions with AI assistant
- **AI Task Tools**: Direct integration with task management via function calls
- **MCP Server**: Model Context Protocol support for AI tools

## Project Structure

```
hackathon-2/
├── phase-1/                  # Console app (Module 0)
├── phase-2/                  # Previous phase implementation
│   └── ...
├── phase-3/                  # Current phase: AI Chatbot integration
│   ├── backend/              # FastAPI + Auth + AI integration
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── models.py         # SQLModel models (including Conversation/Message)
│   │   ├── routes/           # API endpoints (including chat routes)
│   │   │   ├── tasks.py      # Task CRUD endpoints
│   │   │   ├── auth.py       # Auth endpoints
│   │   │   └── chat.py       # AI chat endpoints
│   │   ├── auth/             # JWT authentication
│   │   ├── mcp_server.py     # MCP server for AI tools
│   │   └── agent.py          # AI agent implementation
│   └── frontend/             # Next.js app with chat interface
│       ├── src/app/          # App Router pages (including /chat)
│       ├── src/components/   # React components (including ChatInterface)
│       └── src/lib/          # API client & chat utilities
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
- OpenAI API key (for AI features)

### Backend Setup

```bash
cd phase-3/backend

# Copy environment template
cp .env.example .env

# Edit .env with your credentials:
# - DATABASE_URL (from Neon dashboard)
# - JWT_SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
# - OPENAI_API_KEY (from OpenAI dashboard)

# Install dependencies
uv sync

# Initialize database
uv run python init_db.py

# Run development server
uv run uvicorn main:app --reload --port 8000

# (Optional) Run MCP server separately
uv run python mcp_server.py
```

### Frontend Setup

```bash
cd phase-3/frontend

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

### Backend (`phase-3/backend/.env`)

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | Neon PostgreSQL connection string | `postgresql+asyncpg://user:pass@host/db?ssl=require` |
| JWT_SECRET_KEY | JWT signing secret (min 32 chars) | Generate with `secrets.token_urlsafe(32)` |
| FRONTEND_URL | Production frontend URL (for CORS) | `https://your-frontend.vercel.app` |
| OPENAI_API_KEY | OpenAI API key for chat functionality | `sk-...` |

### Frontend (`phase-3/frontend/.env.local`)

| Variable | Description | Example |
|----------|-------------|---------|
| NEXT_PUBLIC_API_URL | Backend API URL | `http://localhost:8000` or `https://your-backend.vercel.app` |

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
| POST | `/api/{user_id}/chat` | AI chat endpoint |
| GET | `/api/{user_id}/conversations` | List user's conversations |
| GET | `/api/{user_id}/conversations/{id}` | Get conversation history |
| DELETE | `/api/{user_id}/conversations/{id}` | Delete conversation |

## AI Chat Capabilities

The AI assistant can help with various task management operations using natural language:

- **Add tasks**: "Create a task to buy groceries"
- **List tasks**: "Show me my tasks" or "What do I need to do?"
- **Complete tasks**: "Mark task #1 as done" or "I finished the meeting"
- **Delete tasks**: "Remove the shopping task"
- **Update tasks**: "Change the deadline for task #2 to tomorrow"

The AI uses function calling to interact directly with the database, ensuring all operations are secure and properly authenticated.

## Testing Scenarios

### New User Flow
1. Navigate to frontend URL
2. Click "Sign Up"
3. Enter email and password
4. Account created and logged in
5. Access to both task management and AI chat features

### AI Chat Interaction
1. Navigate to the chat page
2. Type a natural language request (e.g., "Add a task to call John")
3. AI assistant processes the request and executes the appropriate function
4. Response confirms the action and updates the task list
5. Conversations are saved and accessible later

### Task Management
1. Create multiple tasks via both traditional UI and AI chat
2. Toggle completion on tasks
3. Edit and delete tasks
4. Verify that AI chat correctly interacts with existing tasks

## Specifications

All feature specifications are in the `/specs/` folder:
- `specs/phase2/1-database/` - Database module spec
- `specs/phase2/2-backend-api/` - Backend API spec
- `specs/phase2/3-jwt-auth/` - Authentication spec
- `specs/005-frontend-web-app/` - Frontend spec
- `specs/006-chat-database/` - AI chatbot spec

## Demo Video

[Watch the 90-second demo](https://youtube.com/watch?v=...)

The demo covers:
- Signup/Login flow
- Traditional task management
- AI chat interface
- Natural language task creation
- Conversation history
- Task management via AI

## Author

RukhsarMalik - Hackathon 2, Phase 3 Submission

## License

This project is for educational purposes as part of the Hackathon 2 program.
