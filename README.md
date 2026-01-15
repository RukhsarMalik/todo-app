# Evolution of Todo - Hackathon Project

A multi-phase todo application development project built using **Spec-Driven Development (SDD)** methodology with Claude Code + Spec-Kit Plus.

## Project Overview

This repository demonstrates the evolution of a todo application through multiple phases, each building upon the previous:

- **Phase I**: In-memory Python CLI application
- **Phase II**: (Planned) File-based persistence
- **Phase III**: (Planned) Database backend

## Current Status

✅ **Phase I - COMPLETE** (2025-12-25)

## Quick Start

### Phase I - Todo Console App

```bash
cd phase-1
python src/main.py
```

**Features**:
- View all tasks
- Add tasks with title/description
- Toggle task completion status
- Update task details
- Delete tasks with confirmation
- Zero external dependencies

**See**: [phase-1/README.md](phase-1/README.md) for full documentation

## Project Structure

```
hackathon-2/
├── .claude/                    # Claude Code skills/commands
├── .specify/                   # Spec-Kit Plus templates & scripts
│   ├── memory/
│   │   └── constitution.md    # Project principles (7 core rules)
│   ├── templates/             # Templates for spec, plan, tasks, ADR, PHR
│   └── scripts/               # Automation scripts
├── history/                    # Prompt History Records (PHR)
│   ├── prompts/
│   │   ├── constitution/      # Constitution creation records
│   │   ├── 001-todo-console-app/  # Feature-specific records
│   │   └── general/           # General development records
│   └── adr/                   # Architecture Decision Records
├── phase-1/                    # Phase I: In-memory CLI app
│   ├── src/                   # Application source code
│   ├── tests/                 # Comprehensive test suites
│   ├── specs/                 # Specification documents
│   ├── README.md              # Phase I documentation
│   ├── QUICKSTART.md          # 2-minute getting started
│   └── IMPLEMENTATION_SUMMARY.md  # Technical summary
├── CLAUDE.md                   # Project-level instructions for Claude
└── README.md                   # This file
```

## Development Methodology

This project follows **Spec-Driven Development (SDD)**:

1. **Constitution** → Define project principles
2. **Specification** → Detail features and acceptance criteria
3. **Planning** → Design architecture and make decisions
4. **Task Breakdown** → Create actionable, dependency-ordered tasks
5. **Implementation** → Execute tasks systematically
6. **Testing** → Validate against acceptance criteria
7. **Documentation** → Capture decisions and learnings

### Key Artifacts

- **Constitution**: `.specify/memory/constitution.md` (7 non-negotiable principles)
- **Prompt History**: `history/prompts/` (all AI interactions recorded)
- **Architecture Decisions**: `history/adr/` (significant technical choices)

## Constitutional Principles

All phases adhere to these 7 core principles:

1. **AI-Native Development**: All code generated via Claude Code workflow
2. **Specification-First**: Complete spec before implementation
3. **Clean Code**: Type hints, docstrings, SRP, DRY
4. **Zero Dependencies**: Stdlib only (per phase requirements)
5. **Graceful Errors**: Validate inputs, clear messages, no crashes
6. **Storage Strategy**: Appropriate to phase (in-memory → file → database)
7. **User-Centric**: Intuitive interface, helpful feedback

See: [.specify/memory/constitution.md](.specify/memory/constitution.md)

## Phase Summaries

### Phase I: In-Memory CLI App ✅

**Status**: Complete (67/67 tasks)
**Lines of Code**: 835 (excluding init files)
**Test Coverage**: 7/7 test suites passing (100%)
**Duration**: Single session implementation

**Deliverables**:
- Fully functional CLI todo app
- 5 core operations (view, add, update, delete, toggle)
- Comprehensive test suite (60+ tests)
- Complete documentation (README, QUICKSTART, specs)

**Documentation**:
- [Phase I README](phase-1/README.md)
- [Quick Start Guide](phase-1/QUICKSTART.md)
- [Implementation Summary](phase-1/IMPLEMENTATION_SUMMARY.md)
- [Specification](phase-1/specs/001-todo-console-app/spec.md)
- [Implementation Plan](phase-1/specs/001-todo-console-app/plan.md)
- [Task Breakdown](phase-1/specs/001-todo-console-app/tasks.md)

### Phase II: File-Based Persistence (Planned)

**Planned Features**:
- JSON file storage
- Data persistence between sessions
- Task categories and tags
- Search and filter operations
- Import/export functionality

### Phase III: Database Backend (Planned)

**Planned Features**:
- SQLite database
- Multi-user support
- Task priorities and due dates
- Recurring tasks
- Task history and audit logs

## Quick Commands

### Run Phase I Application
```bash
cd phase-1
python src/main.py
```

### Run Phase I Tests
```bash
cd phase-1
python tests/run_all_tests.py
```

### View Phase I Specification
```bash
cat phase-1/specs/001-todo-console-app/spec.md
```

### Check Constitutional Compliance
```bash
cat .specify/memory/constitution.md
```

## Requirements

### Phase I
- **Python**: 3.13+
- **Dependencies**: None (stdlib only)
- **Platform**: Any (Windows, macOS, Linux)

## Documentation

### For Users
- [Phase I Quick Start](phase-1/QUICKSTART.md) - Get running in 2 minutes
- [Phase I README](phase-1/README.md) - Full usage guide

### For Developers
- [Constitution](.specify/memory/constitution.md) - Project principles
- [Phase I Spec](phase-1/specs/001-todo-console-app/spec.md) - Feature specification
- [Phase I Plan](phase-1/specs/001-todo-console-app/plan.md) - Architecture & decisions
- [Phase I Tasks](phase-1/specs/001-todo-console-app/tasks.md) - Implementation breakdown
- [Implementation Summary](phase-1/IMPLEMENTATION_SUMMARY.md) - Technical details

### For AI Assistants
- [CLAUDE.md](CLAUDE.md) - Instructions for Claude Code
- [Templates](.specify/templates/) - Spec, plan, task templates
- [Scripts](.specify/scripts/) - Automation helpers

## Prompt History Records (PHR)

All AI interactions are recorded in `history/prompts/`:

- **Constitution**: Records of project principle creation
- **Feature-Specific**: Records for each feature (e.g., `001-todo-console-app/`)
- **General**: Miscellaneous development records

Each PHR includes:
- Full user prompt (verbatim)
- Assistant response (key outputs)
- Context (stage, feature, files touched)
- Metadata (date, model, command)

## Architecture Decision Records (ADR)

Significant technical decisions are documented in `history/adr/` (when applicable).

## Contributing

This is a hackathon demonstration project following strict SDD methodology:

1. All changes must go through Spec → Plan → Tasks → Implement workflow
2. Constitution principles must be upheld
3. All prompts must be recorded as PHRs
4. Significant decisions must be documented as ADRs

## Testing

Each phase includes comprehensive testing:

- **Unit Tests**: Individual component validation
- **Integration Tests**: Complete workflow verification
- **Smoke Tests**: Quick startup/functionality checks
- **Manual Tests**: Acceptance criteria validation

## License

Built for the Evolution of Todo Hackathon.

## Acknowledgments

- **Methodology**: Spec-Driven Development (SDD)
- **Tools**: Claude Code + Spec-Kit Plus
- **AI Model**: Claude Sonnet 4.5

---

**Current Phase**: Phase I ✅ Complete
**Next Phase**: Phase II (File-based persistence) - Planning
**Last Updated**: 2025-12-25
