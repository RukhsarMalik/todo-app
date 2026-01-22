---
id: 006
title: Add Phase III AI Chatbot Constitution
stage: constitution
date: 2026-01-22
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: 005-frontend-web-app
user: RukhsarMalik
command: /sp.constitution
labels: ["phase-iii", "ai-chatbot", "mcp", "constitution"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

I completed Phase II successfully. Now moving to Phase III: AI Chatbot.

UPDATE @constitution.md by ADDING Phase III section (keep all Phase I and II content).

## Phase III: AI-Powered Todo Chatbot

### Evolution
- Phase I: Console app ✅
- Phase II: Web app with auth ✅
- Phase III: Add conversational AI interface

### Core Principles
- Continue Spec-Driven Development (no manual coding)
- Natural language task management
- MCP architecture (stateless server)
- Conversation history in database

### Technology Stack
- AI: OpenAI Agents SDK
- Tools: Official MCP SDK (Python)
- Frontend: OpenAI ChatKit
- Backend: Extend existing FastAPI
- Database: Add conversations & messages tables

### Architecture Constraints
- Stateless chat endpoint: POST /api/{user_id}/chat
- MCP server exposes task operations as tools
- Agent uses MCP tools (add_task, list_tasks, complete_task, etc.)
- Conversation state persists to Neon DB
- ChatKit UI component in frontend

### MCP Tools Required
1. add_task - Create task via natural language
2. list_tasks - Retrieve tasks (all/pending/completed)
3. complete_task - Mark task done
4. delete_task - Remove task
5. update_task - Modify task details

### Agent Behavior
- Understand natural language commands
- Call appropriate MCP tools
- Confirm actions with friendly responses
- Handle errors gracefully
- Maintain conversation context from database

### Success Criteria
- Chatbot understands: "Add buy groceries to my list"
- Works: "Show me pending tasks"
- Works: "Mark task 3 as complete"
- Conversation survives server restart
- All features from Phase II still work

### Security
- Chat endpoint requires JWT (reuse Module 3 auth)
- User can only chat about their own tasks
- MCP tools validate user_id

### Database Extensions
Add tables:
- conversations (id, user_id, created_at)
- messages (id, conversation_id, role, content, created_at)

Keep constitution cumulative - Phase I + II + III all together.

## Response snapshot

Updated constitution from v2.0.0 to v3.0.0 (MAJOR version bump).

Added Phase III section with:
- 5 new principles (XIII-XVII): Natural Language Interface, MCP Architecture, Stateless Chat Design, Conversation Persistence, Agent Tool Safety
- Technical stack specification for AI/Agent components
- Database extensions for conversations and messages tables
- MCP tools specification with 7 required tools
- Agent behavior requirements and intent understanding patterns
- Security requirements for chat endpoint and MCP tools
- Frontend integration guidance with ChatKit
- Success criteria checklist for Phase III completion
- Phase transition notes documenting backward compatibility

All Phase I and Phase II content preserved. Constitution remains cumulative.

## Outcome

- ✅ Impact: Constitution updated to v3.0.0 with comprehensive Phase III guidance
- 🧪 Tests: N/A (documentation change)
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: /sp.specify for Phase III features, /sp.plan for implementation planning
- 🧠 Reflection: Phase III adds significant complexity with AI integration; MCP architecture provides clean separation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
