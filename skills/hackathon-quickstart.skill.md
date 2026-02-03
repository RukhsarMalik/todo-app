----
name: "hackathon-quickstart"
description: "Expert skill that rapidly scaffolds new features for hackathon projects. Analyzes existing codebase structure, identifies patterns and conventions, then generates complete feature scaffolding with components, API routes, types, and tests following project standards. Works with Next.js, FastAPI, React, Python, or any modern stack."
version: "1.0.0"
----

# Hackathon Quick Start Skill

## When to Use This Skill

- User wants to add a new feature/module quickly during a hackathon
- User says "create feature", "add module", "scaffold", "quickstart"
- Need to generate boilerplate code that follows existing project patterns
- Want to avoid manual file creation and focus on logic
- Building MVP features under time pressure

## How This Skill Works (Step-by-Step Execution)

1. **Project Analysis Phase**
   - Scan project structure to detect framework (Next.js, FastAPI, React, etc.)
   - Identify existing patterns (folder structure, naming conventions, imports)
   - Check for shared components, utilities, and types
   - Detect styling approach (Tailwind, CSS Modules, styled-components)
   - Find authentication patterns if protected routes needed

2. **Feature Planning Phase**
   - Determine feature type (CRUD, display, form, dashboard, etc.)
   - Map required files based on project conventions
   - Identify dependencies on existing components
   - Plan API endpoints if backend needed
   - Consider mobile responsiveness requirements

3. **Frontend Scaffolding (if applicable)**
   ```
   src/
   ├── app/{feature}/page.tsx           # Main page
   ├── components/{feature}/
   │   ├── {Feature}List.tsx            # List component
   │   ├── {Feature}Item.tsx            # Item component
   │   ├── {Feature}Form.tsx            # Create/Edit form
   │   └── {Feature}Modal.tsx           # Modal (if needed)
   ├── lib/{feature}-api.ts             # API client functions
   └── lib/{feature}-types.ts           # TypeScript interfaces
   ```

4. **Backend Scaffolding (if applicable)**
   ```
   routes/{feature}.py                   # API routes (CRUD)
   schemas/{feature}.py                  # Pydantic schemas
   models.py                             # Add to existing models
   ```

5. **Code Generation**
   - Generate components using existing UI library (Button, Input, Card, etc.)
   - Add proper TypeScript types for all interfaces
   - Include loading states, error handling, empty states
   - Apply existing color theme and styling patterns
   - Add responsive classes for mobile

6. **Integration Phase**
   - Update route imports in main app
   - Add navigation links in sidebar/header
   - Register API routes in main.py
   - Update any necessary configs

## Output You Will Receive

After activation, I will deliver:

- Complete file structure for the new feature
- All component files with proper TypeScript types
- API client with typed functions
- Backend routes with validation
- Pydantic/Zod schemas for data validation
- Integration code (imports, routes, navigation)
- List of manual steps if any required

## Example Usage

**User says:**
"Add a notifications feature to my todo app"

**This Skill Instantly Activates → Delivers:**

- `src/app/notifications/page.tsx` - Notifications page
- `src/components/notifications/NotificationList.tsx` - List with loading/empty states
- `src/components/notifications/NotificationItem.tsx` - Individual notification card
- `src/lib/notifications-api.ts` - API client (list, markRead, delete)
- `src/lib/notifications-types.ts` - TypeScript interfaces
- `routes/notifications.py` - Backend CRUD endpoints
- `schemas.py` updates - NotificationCreate, NotificationResponse
- Sidebar navigation update

**User says:**
"Create a settings page with user preferences"

**This Skill Responds:**
→ Creates settings page with tabs (Profile, Preferences, Security)
→ Form components for each section
→ API endpoints for updating preferences
→ Proper validation and error handling
→ Mobile-responsive layout

## Activate This Skill By Saying

- "Quickstart a new feature called [name]"
- "Scaffold [feature] for my project"
- "Add [feature] module to my app"
- "Create boilerplate for [feature]"
- "Generate [feature] with all files"
