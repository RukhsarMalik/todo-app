----
name: "code-reviewer"
description: "Expert code review skill that performs comprehensive analysis focusing on hackathon-critical aspects: demo readiness, security, performance, and code quality. Provides actionable feedback with severity levels and exact fixes. Catches issues before they break your demo."
version: "1.0.0"
----

# Code Reviewer Skill

## When to Use This Skill

- User wants code review before demo or submission
- User says "review", "check my code", "is this good", "any issues"
- Need to catch bugs before they appear in demo
- Want security/performance audit
- Preparing for code submission or PR

## How This Skill Works (Step-by-Step Execution)

1. **Scope Detection**
   - Single file review
   - Directory/feature review
   - Full project review
   - Git staged changes review

2. **Multi-Layer Analysis**

   ### Layer 1: Critical Issues (Must Fix Before Demo)
   - [ ] Security vulnerabilities (XSS, injection, exposed secrets)
   - [ ] Runtime errors waiting to happen (null refs, type issues)
   - [ ] Data loss risks (missing validation, race conditions)
   - [ ] Auth bypasses or broken access control
   - [ ] API keys or secrets in code

   ### Layer 2: Demo Breakers
   - [ ] Console errors or warnings
   - [ ] Broken UI on edge cases (empty states, long text)
   - [ ] Non-responsive mobile views
   - [ ] Slow loading without feedback
   - [ ] Confusing error messages

   ### Layer 3: Code Quality
   - [ ] TypeScript `any` usage
   - [ ] Missing error handling
   - [ ] Hardcoded values (should be env/constants)
   - [ ] Dead code or console.logs
   - [ ] DRY violations

   ### Layer 4: Performance
   - [ ] N+1 database queries
   - [ ] Missing pagination
   - [ ] Unnecessary re-renders
   - [ ] Large bundle imports
   - [ ] Missing loading states

3. **Severity Classification**

   | Level | Icon | Meaning |
   |-------|------|---------|
   | CRITICAL | 🔴 | Will break demo, must fix |
   | WARNING | 🟡 | Should fix, might cause issues |
   | SUGGESTION | 🔵 | Nice to have, improves quality |

4. **Fix Generation**
   - Exact line numbers
   - Before/after code
   - Copy-paste ready fixes

## Output You Will Receive

After activation, I will deliver:

```markdown
## 📋 Code Review: [target]

### 🔴 Critical Issues (X found)
**[file:line]** - [issue description]
```[language]
// Fix:
[exact code fix]
```

### 🟡 Warnings (X found)
**[file:line]** - [issue description]
- Suggestion: [improvement]

### 🔵 Suggestions (X found)
- [file:line] - [improvement idea]

### 📊 Summary
| Category | Count |
|----------|-------|
| Critical | X |
| Warnings | X |
| Suggestions | X |

### ✅ Verdict: [PASS / NEEDS FIXES / CRITICAL ISSUES]
```

## Example Usage

**User says:**
"Review my TaskList component"

**This Skill Instantly Activates → Delivers:**

```markdown
## 📋 Code Review: src/components/tasks/TaskList.tsx

### 🔴 Critical Issues (1 found)
**Line 45** - Possible crash when tasks is undefined
```tsx
// BEFORE
{tasks.map(task => ...)}

// AFTER
{tasks?.map(task => ...) ?? <EmptyState />}
```

### 🟡 Warnings (2 found)
**Line 12** - Console.log left in code
- Remove before demo

**Line 67** - Missing loading state
- Add LoadingSpinner when isLoading is true

### 🔵 Suggestions (1 found)
- Line 30 - Could memoize expensive filter operation

### ✅ Verdict: NEEDS FIXES (1 critical)
```

**User says:**
"Check my auth routes for security issues"

**This Skill Responds:**
→ Scans for common auth vulnerabilities
→ Checks password hashing strength
→ Verifies JWT token handling
→ Reviews session management
→ Flags any exposed secrets

**User says:**
"Review everything before I submit"

**This Skill Responds:**
→ Full project scan
→ Prioritized list of all issues
→ Demo-critical fixes first
→ Quick wins highlighted
→ Overall readiness score

## Activate This Skill By Saying

- "Review my code"
- "Check [file/feature] for issues"
- "Is my code demo-ready?"
- "Security review of [area]"
- "Any bugs in [component]?"
