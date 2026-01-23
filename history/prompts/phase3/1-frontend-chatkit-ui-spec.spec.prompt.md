---
id: 1
title: "Frontend ChatKit UI Spec"
stage: spec
date_iso: "2026-01-23"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "frontend-chatkit"
branch: "1-frontend-chatkit"
user: "user"
command: "/sp.specify"
labels: ["spec", "frontend", "chatkit", "ui"]
link_spec: "null"
link_ticket: "null"
link_adr: "null"
link_pr: "null"
files_yaml: |
  - specs/phase3/4-frontend-chatkit/specs.md
  - specs/phase3/4-frontend-chatkit/checklists/requirements.md
  - history/prompts/phase3/1-frontend-chatkit-ui-spec.spec.prompt.md
tests_yaml: |
  - "spec validation completed"
  - "quality checklist verified"
prompt_text: |
  Phase III Module 4: Frontend ChatKit UI.

  Create specs/phase3/4-frontend-chatkit/specification.md

  ## Overview

  - Module: Chat UI Component
  - Purpose: Add OpenAI ChatKit to frontend for conversational interface
  - Dependencies: Module 3 (Chat endpoint ready)
  - Tech: OpenAI ChatKit, React, Next.js

  ## Scope

  INCLUDED:
  - ✅ ChatKit component in frontend
  - ✅ New page: /chat
  - ✅ Send messages to backend chat endpoint
  - ✅ Display conversation history
  - ✅ Protected route (requires login)

  NOT INCLUDED:
  - ❌ Voice input (bonus feature)
  - ❌ Multilingual support (bonus feature)

  ## User Stories

  US-1: Chat page
  - New route: /chat
  - Protected (requires JWT)
  - Shows ChatKit component
  - User can type natural language commands

  US-2: Send message
  - User types: "Add buy groceries"
  - Sends to POST /api/{user_id}/chat
  - Displays assistant response
  - Shows loading state while waiting

  US-3: Display history
  - Load conversation_id from URL or state
  - Fetch messages from backend
  - Display full conversation history
  - Auto-scroll to latest message

  US-4: Natural language examples
  - "Add task: Call mom"
  - "Show my pending tasks"
  - "Mark task 3 as complete"
  - "Delete the groceries task"

  ## ChatKit Setup

  ```typescript
  import { ChatKit } from "@openai/chatkit"

  export default function ChatPage() {
    const session = useSession()

    async function sendMessage(message: string) {
      const res = await fetch(`/api/${session.user.id}/chat`, {
        method: "POST",
        headers: await getAuthHeaders(),
        body: JSON.stringify({ message })
      })
      return res.json()
    }

    return <ChatKit onSendMessage={sendMessage} />
  }
  ```

  ## OpenAI Domain Allowlist

  IMPORTANT: Add frontend URL to OpenAI domain allowlist:
  - Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
  - Add: https://your-frontend.vercel.app
  - Get domain key
  - Add to .env.local: NEXT_PUBLIC_OPENAI_DOMAIN_KEY

  ## File Structure

  phase-2/frontend/
  ├── app/
  │   └── chat/
  │       └── page.tsx (NEW - chat page)
  └── components/
      └── ChatInterface.tsx (NEW - ChatKit wrapper)

  ## Success Criteria

  - ✅ /chat page accessible
  - ✅ Can type natural language commands
  - ✅ Assistant responds
  - ✅ Conversation history visible
  - ✅ All Phase II features still work (/todos page)
  - ✅ Navigation between /todos and /chat

  ## Testing Commands

  - "Add buy milk to my list"
  - "Show me all my tasks"
  - "What's pending?"
  - "Mark task 1 as done"
  - "Delete task 2"
  - "Update task 3 title to Call mom tonight"

  ## Deployment

  - Redeploy frontend to Vercel
  - Redeploy backend to Vercel
  - Test production URLs
  - Record new 90-second demo

  Phase III Complete! 🎉  you will create a folder inside the specs/phase3 folder and will create a spec of this
response_text: |
  Created specification for Frontend ChatKit UI feature (1-frontend-chatkit). The specification includes:
  - User stories for chat interface access, sending commands, viewing history, and navigation
  - Functional requirements covering authentication, messaging, display, and error handling
  - Success criteria with measurable outcomes
  - Quality checklist with all items validated
  - All [NEEDS CLARIFICATION] markers resolved
outcome: "SUCCESS: Specification created and validated according to SDD standards"
evaluation: "The spec follows the template structure, includes all mandatory sections, and has been validated with a quality checklist. Ready for planning phase."
---

# PHR: Frontend ChatKit UI Specification

## Summary
Created comprehensive specification for the Frontend ChatKit UI feature based on user requirements. The specification covers user scenarios, functional requirements, and success criteria for implementing the OpenAI ChatKit component in the frontend.

## Details
- Created feature branch: 1-frontend-chatkit
- Created spec file: specs/phase3/4-frontend-chatkit/specs.md
- Created quality checklist: specs/phase3/4-frontend-chatkit/checklists/requirements.md
- All specification requirements validated and completed
- No outstanding clarifications needed