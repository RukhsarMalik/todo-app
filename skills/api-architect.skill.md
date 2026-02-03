----
name: "api-architect"
description: "Expert API design and implementation skill that generates production-ready REST API endpoints with proper validation, error handling, authentication, and documentation. Works with FastAPI (Python), Express/Hono (Node), or any backend framework. Includes frontend API client generation."
version: "1.0.0"
----

# API Architect Skill

## When to Use This Skill

- User wants to create new API endpoints
- User says "create API", "add endpoint", "backend route"
- Need CRUD operations for a resource
- Want properly typed API client for frontend
- Building REST API during hackathon

## How This Skill Works (Step-by-Step Execution)

1. **Backend Detection**
   - Identify framework (FastAPI, Express, Hono, Next.js API routes)
   - Check existing patterns (folder structure, error handling style)
   - Find authentication middleware
   - Detect database/ORM (SQLModel, Prisma, Drizzle)
   - Identify validation approach (Pydantic, Zod)

2. **API Design**
   - Define resource schema (fields, types, validations)
   - Plan endpoints following REST conventions:
     ```
     GET    /api/{resource}s         → List (with pagination)
     GET    /api/{resource}s/{id}    → Get single
     POST   /api/{resource}s         → Create
     PUT    /api/{resource}s/{id}    → Update
     DELETE /api/{resource}s/{id}    → Delete
     ```
   - Add custom endpoints if needed (e.g., `/complete`, `/archive`)

3. **Backend Implementation (FastAPI Example)**

   ```python
   # routes/{resource}.py
   from fastapi import APIRouter, Depends, HTTPException, Query
   from sqlmodel import Session, select
   from db import get_session
   from auth.middleware import get_current_user
   from models import {Resource}, User
   from schemas import {Resource}Create, {Resource}Update, {Resource}Response

   router = APIRouter(prefix="/api/{resource}s", tags=["{Resource}s"])

   @router.get("", response_model=list[{Resource}Response])
   async def list_{resource}s(
       skip: int = Query(0, ge=0),
       limit: int = Query(20, ge=1, le=100),
       session: Session = Depends(get_session),
       user: User = Depends(get_current_user)
   ):
       # Implementation with proper pagination

   @router.post("", response_model={Resource}Response, status_code=201)
   async def create_{resource}(
       data: {Resource}Create,
       session: Session = Depends(get_session),
       user: User = Depends(get_current_user)
   ):
       # Implementation with validation

   # ... update, delete, get
   ```

4. **Schema/Validation Generation**

   ```python
   # schemas.py additions
   class {Resource}Base(SQLModel):
       title: str = Field(min_length=1, max_length=200)
       description: str | None = None

   class {Resource}Create({Resource}Base):
       pass

   class {Resource}Update(SQLModel):
       title: str | None = None
       description: str | None = None

   class {Resource}Response({Resource}Base):
       id: int
       user_id: int
       created_at: datetime
   ```

5. **Frontend API Client Generation**

   ```typescript
   // lib/{resource}-api.ts
   import { fetchWithAuth } from './api';
   import type { {Resource}, {Resource}Create, {Resource}Update } from './{resource}-types';

   export const {resource}Api = {
     list: (skip = 0, limit = 20) =>
       fetchWithAuth<{Resource}[]>(`/api/{resource}s?skip=${skip}&limit=${limit}`),

     get: (id: number) =>
       fetchWithAuth<{Resource}>(`/api/{resource}s/${id}`),

     create: (data: {Resource}Create) =>
       fetchWithAuth<{Resource}>('/api/{resource}s', {
         method: 'POST',
         body: JSON.stringify(data),
       }),

     update: (id: number, data: {Resource}Update) =>
       fetchWithAuth<{Resource}>(`/api/{resource}s/${id}`, {
         method: 'PUT',
         body: JSON.stringify(data),
       }),

     delete: (id: number) =>
       fetchWithAuth<void>(`/api/{resource}s/${id}`, { method: 'DELETE' }),
   };
   ```

6. **Integration**
   - Register routes in main.py
   - Add to OpenAPI documentation
   - Update frontend types

## Output You Will Receive

After activation, I will deliver:

- Complete route file with all CRUD endpoints
- Pydantic/Zod schemas with validation
- TypeScript types for frontend
- API client with typed functions
- OpenAPI documentation
- Example requests/responses
- Integration instructions

## Example Usage

**User says:**
"Create API for notifications"

**This Skill Instantly Activates → Delivers:**

- `routes/notifications.py` with:
  - `GET /api/notifications` (list with pagination)
  - `GET /api/notifications/{id}` (single)
  - `POST /api/notifications` (create)
  - `PATCH /api/notifications/{id}/read` (mark as read)
  - `DELETE /api/notifications/{id}` (delete)
- `schemas.py` updates with NotificationCreate, NotificationResponse
- `lib/notifications-api.ts` frontend client
- `lib/notifications-types.ts` TypeScript interfaces

**User says:**
"Add tags API with many-to-many relationship to tasks"

**This Skill Responds:**
→ Creates tags routes with proper relationship handling
→ Junction table management
→ Endpoints: list tags, create tag, assign to task, remove from task
→ Proper cascade delete handling

## Activate This Skill By Saying

- "Create API for [resource]"
- "Add [resource] endpoints"
- "Generate CRUD for [resource]"
- "Backend routes for [feature]"
- "API client for [resource]"
