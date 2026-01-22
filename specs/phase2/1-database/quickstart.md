# Quickstart: Database Setup & Models

**Module**: Phase II - Module 1 of 5
**Date**: 2026-01-16

---

## Prerequisites

Before starting, ensure you have:

- [ ] Python 3.13+ installed
- [ ] UV package manager installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [ ] Neon account created at [neon.tech](https://neon.tech)
- [ ] Neon database provisioned
- [ ] Database connection string copied

---

## Step 1: Create Backend Directory

```bash
# From project root
mkdir -p backend
cd backend
```

---

## Step 2: Initialize UV Project

```bash
# Initialize Python project
uv init

# Add dependencies
uv add sqlmodel asyncpg python-dotenv
```

This creates:
- `pyproject.toml` - Project configuration
- `.python-version` - Python version lock
- `uv.lock` - Dependency lock file

---

## Step 3: Create Environment File

```bash
# Create .env file
cat > .env << 'EOF'
# Neon PostgreSQL Connection
DATABASE_URL=postgresql+asyncpg://YOUR_USER:YOUR_PASSWORD@YOUR_HOST/YOUR_DATABASE?sslmode=require
EOF

# Create .env.example template
cat > .env.example << 'EOF'
# Neon PostgreSQL Connection
# Get your connection string from Neon dashboard
DATABASE_URL=postgresql+asyncpg://username:password@ep-example-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
EOF
```

**Important**: Replace the DATABASE_URL with your actual Neon connection string.

### Getting Your Neon Connection String

1. Go to [Neon Console](https://console.neon.tech)
2. Select your project
3. Click "Connection Details"
4. Select "Connection string" tab
5. Copy the connection string
6. Replace `postgresql://` with `postgresql+asyncpg://`
7. Ensure `?sslmode=require` is at the end

---

## Step 4: Add to .gitignore

```bash
# Append to .gitignore
cat >> ../.gitignore << 'EOF'

# Backend environment
backend/.env
backend/.venv/
backend/__pycache__/
EOF
```

---

## Step 5: Create Database Files

The following files will be created by `/sp.tasks` and implemented by Claude Code:

| File | Purpose |
|------|---------|
| `models.py` | Task SQLModel class |
| `db.py` | Database connection and session management |
| `init_db.py` | Table initialization script |
| `test_db.py` | Validation test script |

---

## Step 6: Initialize Database

After implementation, run:

```bash
cd backend
uv run python init_db.py
```

Expected output:
```
Loading environment variables...
DATABASE_URL found
Creating database engine...
Creating tables...
Tables created successfully!
- tasks table ready
```

---

## Step 7: Verify Setup

Run the test script:

```bash
uv run python test_db.py
```

Expected output:
```
Testing database connection...
Connection successful!

Testing table creation...
Tasks table exists: True

Testing task creation...
Created task: id=1, title="Test Task"

Testing task retrieval...
Retrieved task: Test Task

Cleaning up test data...
Test data removed

All tests passed!
```

---

## Step 8: Verify in Neon Console

1. Go to [Neon Console](https://console.neon.tech)
2. Select your database
3. Open "Tables" section
4. Verify `tasks` table exists with columns:
   - id (integer, primary key)
   - user_id (varchar)
   - title (varchar)
   - description (text)
   - completed (boolean)
   - created_at (timestamp)
   - updated_at (timestamp)
5. Open "Indexes" section and verify:
   - idx_tasks_user_id
   - idx_tasks_completed

---

## Troubleshooting

### Connection Refused

```
Error: Connection refused
```

**Solution**:
- Check DATABASE_URL is correct
- Ensure `sslmode=require` is set
- Verify Neon project is not suspended

### Invalid Password

```
Error: password authentication failed
```

**Solution**:
- Reset password in Neon dashboard
- Update DATABASE_URL in .env

### Module Not Found

```
ModuleNotFoundError: No module named 'sqlmodel'
```

**Solution**:
```bash
cd backend
uv add sqlmodel asyncpg python-dotenv
```

### SSL Required

```
Error: SSL required
```

**Solution**:
- Add `?sslmode=require` to DATABASE_URL
- Use `postgresql+asyncpg://` prefix

---

## File Structure After Setup

```
backend/
├── .env                 # Your DATABASE_URL (git ignored)
├── .env.example         # Template for others
├── pyproject.toml       # UV project config
├── uv.lock              # Dependency lock
├── models.py            # Task SQLModel class
├── db.py                # Database module
├── init_db.py           # Initialization script
└── test_db.py           # Validation script
```

---

## Next Steps

After completing this module:

1. ✅ Database connection working
2. ✅ Tasks table created
3. ✅ Test script passes
4. ➡️ Proceed to Module 2: Backend API (`/sp.specify` for API endpoints)

---

## Quick Reference

### Run Initialization
```bash
cd backend && uv run python init_db.py
```

### Run Tests
```bash
cd backend && uv run python test_db.py
```

### Check Neon Console
[https://console.neon.tech](https://console.neon.tech)

### Add New Dependency
```bash
cd backend && uv add <package-name>
```
