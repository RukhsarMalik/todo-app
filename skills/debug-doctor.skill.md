----
name: "debug-doctor"
description: "Expert debugging skill that rapidly diagnoses and fixes bugs in any codebase. Analyzes error messages, traces root causes, provides exact fixes with code, and explains prevention strategies. Optimized for hackathon speed where every minute counts."
version: "1.0.0"
----

# Debug Doctor Skill

## When to Use This Skill

- User encounters any error (runtime, build, type, API, etc.)
- User says "fix", "debug", "error", "not working", "broken"
- Something crashed and user needs fast resolution
- User is stuck on a bug during hackathon crunch time
- Need to understand why code isn't behaving as expected

## How This Skill Works (Step-by-Step Execution)

1. **Error Classification**

   | Category | Examples | Priority |
   |----------|----------|----------|
   | Runtime | TypeError, ReferenceError, null pointer | CRITICAL |
   | Build | Module not found, syntax error, type mismatch | CRITICAL |
   | API | 401, 403, 404, 500, CORS, timeout | HIGH |
   | UI | Render issues, hydration, state bugs | MEDIUM |
   | Logic | Wrong output, edge cases, race conditions | MEDIUM |

2. **Quick Diagnosis**
   - Parse error message for file, line, and error type
   - Check stack trace for origin point
   - Identify common patterns matching the error
   - Look for recent changes that might have caused it
   - Check environment variables, dependencies, configs

3. **Common Bug Patterns & Quick Fixes**

   | Error Pattern | Instant Fix |
   |---------------|-------------|
   | `Cannot read property of undefined` | Add optional chaining `?.` |
   | `Module not found` | Check import path, run `npm install` |
   | `CORS error` | Add CORS headers to backend |
   | `401 Unauthorized` | Check token storage and Authorization header |
   | `Hydration mismatch` | Wrap in `useEffect` or use `'use client'` |
   | `Too many re-renders` | Check useEffect dependencies, memoize |
   | `Network error` | Verify API URL, check if backend running |
   | `Type error` | Fix TypeScript types, add proper interfaces |
   | `Database error` | Check connection string, run migrations |

4. **Fix Generation**
   - Provide exact code change with before/after
   - Explain why the fix works
   - Identify any related issues
   - Suggest preventive measures

5. **Verification Steps**
   - Commands to verify the fix worked
   - How to test edge cases
   - Logs to check for confirmation

## Output You Will Receive

After activation, I will deliver:

```markdown
## 🔍 Debug Report

### Error Analysis
- **Type**: [error_category]
- **Location**: [file:line]
- **Root Cause**: [clear explanation]

### ⚡ Quick Fix
```[language]
// BEFORE (broken)
[problematic_code]

// AFTER (fixed)
[fixed_code]
```

### 🛡️ Prevention
[how to prevent similar issues]

### ✅ Verify Fix
[commands or steps to verify]
```

## Example Usage

**User says:**
"TypeError: Cannot read properties of undefined (reading 'map')"

**This Skill Instantly Activates → Delivers:**

- **Root Cause**: `tasks` is undefined when component first renders
- **Quick Fix**:
  ```tsx
  // BEFORE
  {tasks.map(task => <TaskItem key={task.id} task={task} />)}

  // AFTER
  {tasks?.map(task => <TaskItem key={task.id} task={task} />)}

  // OR better - add loading check
  if (!tasks) return <LoadingSpinner />;
  ```
- **Prevention**: Always initialize arrays as `[]` in useState, add null checks

**User says:**
"API returns 500 Internal Server Error"

**This Skill Responds:**
→ Checks backend logs for actual error
→ Identifies database connection issue / validation error / missing env var
→ Provides exact fix for the backend code
→ Shows how to add better error handling

**User says:**
"Build fails with 'Module not found: Can't resolve @/components/Button'"

**This Skill Responds:**
→ Checks tsconfig.json paths configuration
→ Verifies file exists at expected location
→ Fixes import path or updates tsconfig
→ Clears .next cache if needed

## Activate This Skill By Saying

- "Fix this error: [error message]"
- "Debug: [description of problem]"
- "Why is this not working: [code/feature]"
- "Help me fix [error type]"
- "Something's broken: [symptoms]"
