# Quick Start Guide - Todo Console App

Get up and running with the Todo Console App in under 2 minutes.

## Prerequisites Check

```bash
# Verify Python 3.13+
python --version
# Should show: Python 3.13.x or higher
```

If you don't have Python 3.13+, [download it here](https://www.python.org/downloads/).

## Installation

```bash
# Clone or navigate to Phase 1 directory
cd hackathon-2/phase-1

# Verify files are present
ls src/
# Should show: main.py models/ services/ cli/ validators/
```

## Run the App

```bash
# Start the application (from phase-1 directory)
python src/main.py
```

You'll see:
```
Welcome to Todo Console App!

=== Todo Console App ===
1. View All Tasks
2. Add Task
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit

Enter your choice (1-6):
```

## Your First Tasks

### 1. Add a Task

```
Enter your choice (1-6): 2
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread
→ Task added successfully! (ID: 1)
```

### 2. View Your Tasks

```
Enter your choice (1-6): 1

=== All Tasks ===
[1] [✗] Buy groceries - Milk, eggs, bread (Created: 2025-12-25 10:30:00)
```

Legend:
- `[✗]` = Incomplete
- `[✓]` = Complete

### 3. Mark Task Complete

```
Enter your choice (1-6): 5
Enter task ID to toggle: 1
→ Task 1 marked as complete.
```

### 4. Update a Task

```
Enter your choice (1-6): 3
Enter task ID to update: 1
Current: [1] Buy groceries - Milk, eggs, bread
Enter new title: Buy groceries and household items
Enter new description (optional): Milk, eggs, bread, soap, paper towels
→ Task 1 updated successfully.
```

### 5. Delete a Task

```
Enter your choice (1-6): 4
Enter task ID to delete: 1
Are you sure you want to delete this task?
[1] Buy groceries and household items - Milk, eggs, bread, soap, paper towels
Confirm deletion (y/n): y
→ Task 1 deleted successfully.
```

### 6. Exit

```
Enter your choice (1-6): 6
→ Thank you for using Todo Console App. Goodbye!
```

## Common Operations

### Add Multiple Tasks Quickly

```
Choice: 2 → Title: Task 1 → Description: [Enter]
Choice: 2 → Title: Task 2 → Description: Details
Choice: 2 → Title: Task 3 → Description: [Enter]
Choice: 1 → (View all 3 tasks)
```

### Mark All Tasks Complete

```
Choice: 5 → ID: 1
Choice: 5 → ID: 2
Choice: 5 → ID: 3
Choice: 1 → (View all complete ✓)
```

## Error Handling

The app validates all inputs and provides helpful error messages:

### Invalid Menu Choice
```
Enter your choice (1-6): 99
Error: Invalid choice. Please select a valid option (1-6).
```

### Empty Title
```
Enter task title: [just hit Enter]
Error: Title cannot be empty. Please enter a task title (1-200 characters).
```

### Invalid Task ID
```
Enter task ID: abc
Error: Invalid task ID. Please enter a numeric ID.
```

### Task Not Found
```
Enter task ID: 999
Error: Task with ID 999 not found. Use 'View All Tasks' to see available task IDs.
```

## Tips & Tricks

1. **Descriptions are Optional**: Just press Enter to skip
2. **View Often**: Use option 1 to see your task IDs before operations
3. **Confirmation for Delete**: Only delete operation asks for confirmation
4. **Toggle is Bidirectional**: Can toggle back and forth between complete/incomplete
5. **IDs Never Reused**: Deleted task IDs won't be reassigned to new tasks

## Running Tests

Verify everything works:

```bash
# Run all tests
python tests/run_all_tests.py

# Quick smoke test
PYTHONPATH=./src python tests/test_smoke.py
```

You should see:
```
All tests passed!
```

## Important Notes

**Data is NOT Saved**: This is Phase I - tasks are stored in memory only. When you exit the app, all tasks are lost. This is by design.

**Phase II will add file-based persistence.**

## Troubleshooting

### "ModuleNotFoundError"
```bash
# Set PYTHONPATH (from phase-1 directory)
export PYTHONPATH=./src
python src/main.py
```

### "python: command not found"
Try `python3` instead:
```bash
python3 --version
python3 src/main.py
```

### Wrong Python Version
Download Python 3.13+ from [python.org](https://www.python.org/downloads/)

## Next Steps

- Read the full README: `README.md`
- View specification: `specs/001-todo-console-app/spec.md`
- Check implementation summary: `IMPLEMENTATION_SUMMARY.md`
- Explore the code: `src/` directory

## Support

For questions or issues:
1. Check `README.md` for detailed documentation
2. Review `specs/001-todo-console-app/spec.md` for features
3. See `IMPLEMENTATION_SUMMARY.md` for technical details

---

**Ready to dive in? Run `python src/main.py` and start organizing your tasks!**
