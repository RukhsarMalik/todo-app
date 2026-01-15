# Quickstart Guide: Todo Console App (Phase I)

**Version**: 1.0.0
**Date**: 2025-12-25
**Audience**: Developers learning Spec-Driven Development with Claude Code

## What is This?

A command-line todo application for managing tasks in memory. Built following Spec-Driven Development principles with Claude Code + Spec-Kit Plus. Demonstrates AI-native development, clean code, and constitutional constraints.

**Key Features**:
- ✅ View all tasks with status indicators
- ✅ Add tasks with title and optional description
- ✅ Update task title/description
- ✅ Delete tasks with confirmation
- ✅ Toggle task completion status (pending ↔ completed)
- ✅ Zero external dependencies (Python stdlib only)
- ✅ Graceful error handling (no crashes)

**Phase I Constraints**:
- In-memory storage (data lost on exit)
- Single user, single session
- Python 3.13+ required
- No persistence, no database

---

## Prerequisites

### System Requirements

- **Python**: 3.13 or higher
- **OS**: Linux, macOS, or Windows WSL
- **Terminal**: Any terminal with UTF-8 support

### Check Python Version

```bash
python --version
# Should output: Python 3.13.x or higher

# If python3 instead:
python3 --version
```

---

## Installation

### Option 1: Clone Repository

```bash
# Clone the repo
git clone <repository-url>
cd hackathon-2

# Verify structure
ls src/
# Should see: main.py models/ services/ cli/ validators/
```

### Option 2: Already Have the Code

```bash
# Navigate to project directory
cd /path/to/hackathon-2

# Verify you're on the right branch
git branch --show-current
# Should show: 001-todo-console-app
```

---

## Running the App

### Start the Application

```bash
# From project root
python src/main.py

# Or if using python3:
python3 src/main.py
```

### Expected Output

```
=== Todo Console App ===
1. View All Tasks
2. Add Task
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit

Enter your choice (1-6):
```

---

## Usage Guide

### 1. Adding Your First Task

```
Enter your choice (1-6): 2

Enter task title: Buy groceries
Enter task description (optional, press Enter to skip): Milk, eggs, bread

Task added successfully! (ID: 1)
```

**Tips**:
- Title is required (1-200 characters)
- Description is optional (max 1000 characters)
- Leading/trailing spaces automatically trimmed

---

### 2. Viewing All Tasks

```
Enter your choice (1-6): 1

=== Your Tasks ===

[ ] 1. Buy groceries
    Milk, eggs, bread
    Created: 2025-12-25 10:30:45

---
Total: 1 task (0 completed, 1 pending)
```

**Status Indicators**:
- `[ ]` = Pending task
- `[✓]` = Completed task

---

### 3. Marking a Task Complete

```
Enter your choice (1-6): 5

Enter task ID to toggle status: 1

Task #1 marked as completed!
```

**Viewing Again**:
```
[ ✓] 1. Buy groceries
     Milk, eggs, bread
```

---

### 4. Updating a Task

```
Enter your choice (1-6): 3

Enter task ID to update: 1

Current task:
  Title: Buy groceries
  Description: Milk, eggs, bread

Enter new title (or press Enter to keep current): Buy groceries and supplies
Enter new description (or press Enter to keep current):

Task #1 updated successfully!
```

**Tips**:
- Press Enter to keep current title/description
- At least one field must be updated

---

### 5. Deleting a Task

```
Enter your choice (1-6): 4

Enter task ID to delete: 1

Are you sure you want to delete task #1: Buy groceries and supplies? (y/n): y

Task #1 deleted successfully!
```

**Confirmation Required**:
- Enter `y` or `yes` to confirm
- Enter `n` or `no` to cancel
- Case-insensitive

---

### 6. Exiting the App

```
Enter your choice (1-6): 6

👋 Goodbye!
```

**Note**: All tasks are lost when you exit (in-memory only)

---

## Common Workflows

### Daily Task Management

```bash
# 1. Start app
python src/main.py

# 2. Add tasks for the day
# Choose: 2 (Add Task)
# Add: "Review PR #42"
# Add: "Update documentation"
# Add: "Team meeting at 2pm"

# 3. View your task list
# Choose: 1 (View All Tasks)

# 4. Mark tasks complete as you finish them
# Choose: 5 (Toggle Status)
# Enter task ID

# 5. View progress
# Choose: 1 (View All Tasks)
# See completed [✓] vs pending [ ]

# 6. Clean up completed tasks
# Choose: 4 (Delete Task)
# Delete completed tasks

# 7. Exit when done
# Choose: 6 (Exit)
```

---

## Error Handling Examples

### Invalid Title (Empty)

```
Enter task title:

❌ Title cannot be empty. Please enter a task title (1-200 characters).

Enter task title: Buy groceries
```

### Invalid Title (Too Long)

```
Enter task title: [201-character string]

❌ Title too long. Maximum 200 characters allowed. Current length: 201

Enter task title: Shorter title
```

### Invalid Task ID

```
Enter task ID to update: 999

❌ Task #999 not found. Use 'View Tasks' to see valid task IDs.
```

### Invalid Menu Choice

```
Enter your choice (1-6): 99

❌ Invalid choice. Please select a valid option (1-6).
```

**App Never Crashes**: All errors handled gracefully, always returns to menu

---

## Tips & Tricks

### Keyboard Shortcuts

- **Ctrl+C**: Exit app immediately (data lost)
- **Ctrl+D** (EOF): Exit app gracefully
- **Enter**: Skip optional description when adding tasks

### Best Practices

1. **Keep titles short**: Under 50 characters for readability
2. **Use descriptions for details**: Context, deadlines, notes
3. **Review often**: Check task list frequently
4. **Mark complete quickly**: Builds momentum
5. **Delete completed tasks**: Keeps list focused

### Common Patterns

**Morning Planning**:
```
1. Start app
2. Add all tasks for the day
3. View list to confirm
4. Exit (tasks stay in memory)
5. Re-open throughout day to toggle completion
```

**Quick Task Capture**:
```
1. Start app
2. Add task (title only, skip description)
3. Exit
4. Later: re-open, update task with details
```

---

## Troubleshooting

### "Command not found: python"

**Solution**: Try `python3` instead, or install Python 3.13+

```bash
python3 --version
python3 src/main.py
```

### "ModuleNotFoundError: No module named 'models'"

**Solution**: Run from project root, not from `src/` directory

```bash
# Wrong:
cd src
python main.py

# Correct:
cd /path/to/hackathon-2
python src/main.py
```

### "Python version too old"

**Solution**: Upgrade to Python 3.13+

```bash
# Check version
python --version

# Install Python 3.13+ via:
# - python.org (official installer)
# - Homebrew: brew install python@3.13
# - apt: sudo apt install python3.13
```

### "Tasks disappear after exit"

**Expected Behavior**: Phase I uses in-memory storage. Tasks are intentionally lost on exit.

**Phase II/III**: Will add persistence (file storage, database)

---

## What's Next?

### Phase I Completion

After using the app, verify it meets success criteria:
- [ ] All 5 operations work (view, add, update, delete, toggle)
- [ ] Can complete full workflow in <90 seconds
- [ ] No crashes on invalid input
- [ ] Clear error messages for all validation failures
- [ ] Can run 50+ consecutive operations without issues

### Future Phases

**Phase II** (Planned):
- File-based persistence (JSON storage)
- Task categories and tags
- Search and filter capabilities

**Phase III** (Planned):
- Database backend (SQLite)
- Multi-user support
- Task priorities and due dates

---

## Support & Feedback

**Documentation**:
- Specification: `specs/001-todo-console-app/spec.md`
- Implementation Plan: `specs/001-todo-console-app/plan.md`
- Data Model: `specs/001-todo-console-app/data-model.md`

**Constitutional Guidelines**:
- Project principles: `.specify/memory/constitution.md`
- All code must trace to tasks via /sp.tasks

**Questions?**
- Review acceptance scenarios in spec.md
- Check data model validations in data-model.md
- See contracts/ for module interfaces

---

## License & Attribution

Built following Evolution of Todo Hackathon guidelines using Spec-Driven Development with Claude Code + Spec-Kit Plus.

**Learning Objectives**:
- AI-native development workflow
- Constitutional constraints
- Clean code principles
- Type-safe Python patterns
- User-centric CLI design
