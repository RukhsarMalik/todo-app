<!--
Sync Impact Report:
- Version: None → 1.0.0 (Initial constitution for Evolution of Todo Hackathon Phase I)
- Principles added: 7 core principles established
- Sections added: Project Vision, Core Principles, Technical Standards, Development Workflow, Quality Gates, Governance
- Templates status:
  ✅ plan-template.md: Aligned with Python 3.13+, CLI architecture, in-memory constraints
  ✅ spec-template.md: Aligned with 5 basic features and user scenario requirements
  ✅ tasks-template.md: Aligned with spec-driven workflow and TDD approach
- Follow-up: None - all placeholders filled
-->

# Evolution of Todo - Phase I Constitution

## Project Vision & Purpose

**What**: A command-line todo application that stores tasks in memory, serving as the foundation
for mastering Spec-Driven Development (SDD) and AI-assisted coding workflows.

**Why**: To provide individual learners with hands-on experience in the Agentic Dev Stack
(Claude Code + Spec-Kit Plus) through a concrete, achievable project with clear success criteria.

**Who**: Individual learners participating in the "Evolution of Todo" hackathon, building
competency in AI-native development practices.

**Phase I Scope**: Basic in-memory CLI todo application with 5 core features, demonstrable
in a 90-second video, requiring zero external dependencies.

## Core Principles

### I. AI-Native Development (NON-NEGOTIABLE)

All code MUST be generated through Claude Code + Spec-Kit Plus workflow. Manual coding is
strictly prohibited. Every line of implementation code must trace back to an approved task in
the specification artifacts.

**Rationale**: Phase I is designed to teach disciplined AI-assisted development. Manual coding
bypasses the learning objective and breaks traceability between specifications and implementation.

**Enforcement**: Code reviews MUST verify that every function/class maps to a task ID. Commits
without task references will be rejected.

### II. Specification-First Development (NON-NEGOTIABLE)

No implementation work may begin without completed and approved specification artifacts following
the Spec-Driven Development loop: Specify → Plan → Tasks → Implement.

**Workflow Requirements**:
- All specifications stored in `/specs/<feature>/` directory
- Specifications MUST be approved before task generation
- Tasks MUST be approved before implementation begins
- No "code first, document later" permitted

**Rationale**: SDD ensures requirements are understood, architectures are validated, and tasks
are testable before any code is written. This prevents rework and maintains alignment with goals.

### III. Clean Code & Python Standards (NON-NEGOTIABLE)

All Python code MUST adhere to clean code principles with strict type safety and documentation.

**Mandatory Requirements**:
- Type hints on ALL functions, parameters, and return values (Python 3.13+ typing)
- Docstrings (Google or NumPy style) for ALL public functions and classes
- Single Responsibility Principle: one function = one clear purpose
- DRY: No duplicated logic; extract to functions when repeated
- Meaningful names: no single-letter variables except loop counters
- Maximum function length: 50 lines (refactor if exceeded)

**Rationale**: Clean code is maintainable code. Type hints catch errors early. Docstrings serve
as inline documentation. These practices are industry standards that AI-assisted development
must not compromise.

### IV. Zero External Dependencies (PHASE I CONSTRAINT)

Phase I implementation MUST use only Python 3.13+ standard library. No third-party packages,
frameworks, or external dependencies permitted except UV for package management.

**Allowed**: Standard library modules (sys, argparse, dataclasses, typing, uuid, datetime, etc.)
**Prohibited**: Any package requiring `pip install` or external downloads

**Rationale**: Simplicity for learning. External dependencies add complexity, version conflicts,
and installation friction. Phase I focuses on core concepts; future phases will add dependencies.

### V. Graceful Error Handling (NON-NEGOTIABLE)

All user inputs MUST be validated. All error conditions MUST produce clear, actionable error
messages. The application MUST NOT crash under any user input.

**Requirements**:
- Validate all user inputs before processing (type, range, format)
- Catch and handle ALL exceptions with user-friendly messages
- Error messages MUST explain what went wrong AND how to fix it
- No stack traces shown to end users (log them internally if needed)
- Invalid input returns to menu/prompt; never exits abruptly

**Rationale**: Professional software handles errors gracefully. Users should never see Python
tracebacks or cryptic messages. Every error is a teaching moment.

### VI. In-Memory Storage (PHASE I CONSTRAINT)

All task data MUST be stored in memory using Python data structures (lists, dicts, dataclasses).
No file I/O, databases, or persistence mechanisms permitted in Phase I.

**Requirements**:
- Tasks stored in memory (e.g., list of dataclass objects)
- Data resets on application restart (expected and acceptable)
- No pickles, JSON files, SQLite, or external storage

**Rationale**: Simplicity for Phase I. Persistence adds complexity (file locks, corruption,
serialization). In-memory focus teaches data structure design. Future phases add persistence.

### VII. User-Centric CLI Design

Command-line interface MUST be intuitive, with clear prompts, readable output, and helpful
guidance for users unfamiliar with the application.

**Requirements**:
- Main menu displays all available operations with numbered options
- Prompts clearly state expected input format and valid values
- Output formatted for readability (tables, numbered lists, clear sections)
- Confirmation messages for destructive operations (delete, update)
- Help text available for all commands

**Rationale**: CLI doesn't mean user-hostile. Clear interfaces reduce support burden and improve
the demo experience. Users should understand what to do without reading documentation.

## Technical Standards

### Runtime Environment

- **Python Version**: 3.13 or higher (REQUIRED)
- **Package Manager**: UV (for project setup and dependency management)
- **Platform**: Cross-platform (Linux, macOS, Windows via WSL)
- **Execution**: Single-command launch (e.g., `python src/main.py` or `uv run src/main.py`)

### Architecture

- **Type**: Single-file or modular structure (decide in planning phase)
- **Entry Point**: One main entry point that launches the CLI menu
- **Data Model**: Dataclasses for Task entity with typed fields
- **Storage**: In-memory list or dictionary holding Task objects
- **Interface**: Text-based menu with numbered options

### Required Features (Exactly 5 - No More, No Less)

Phase I MUST implement these features and ONLY these features:

1. **Add Task**: Create new task with title (required) and description (optional)
2. **Delete Task**: Remove task by ID with confirmation prompt
3. **Update Task**: Modify title and/or description of existing task by ID
4. **View Task List**: Display all tasks with ID, title, status, and description
5. **Toggle Status**: Mark task as complete/incomplete

**Success Criteria**: All 5 features working correctly, no crashes, demonstrable in 90 seconds.

### Code Quality Gates

Before any commit, code MUST pass:

- **Type Check**: All type hints valid (no `Any` types without justification)
- **Docstring Check**: All public functions documented
- **Validation Check**: All user inputs validated before use
- **Error Handling Check**: No unhandled exceptions possible from user input
- **Name Check**: All variables, functions, classes have descriptive names

## Development Workflow

### Spec-Driven Development Loop (MANDATORY)

```
1. SPECIFY  → Write specification in /specs/<feature>/spec.md
              Define user stories, acceptance criteria, requirements
              ↓
2. PLAN     → Create implementation plan in /specs/<feature>/plan.md
              Define architecture, data model, file structure
              ↓
3. TASKS    → Generate tasks in /specs/<feature>/tasks.md
              Break plan into concrete, testable implementation tasks
              ↓
4. IMPLEMENT → Execute tasks via Claude Code
              Generate code mapped to task IDs
              ↓
5. VERIFY   → Test all acceptance criteria
              Record results, iterate if needed
```

**Gate**: Each phase MUST complete and gain approval before proceeding to next phase.

### Version Control Discipline

- Git repository initialized from day 1
- Meaningful commit messages referencing task IDs (e.g., "T001: Create Task dataclass")
- Atomic commits: one logical unit of work per commit
- No commits with failing code or incomplete features
- Branch strategy: `main` for stable code, feature branches for development

### File Organization (REQUIRED)

```
todo-app/
├── .specify/
│   ├── memory/
│   │   └── constitution.md          # This file
│   ├── templates/                   # Spec-Kit Plus templates
│   └── scripts/                     # Spec-Kit Plus scripts
├── specs/
│   └── <feature-name>/
│       ├── spec.md                  # Feature specification
│       ├── plan.md                  # Implementation plan
│       └── tasks.md                 # Task breakdown
├── src/
│   ├── main.py                      # Application entry point
│   ├── models/                      # Data models (Task dataclass)
│   ├── services/                    # Business logic (add, delete, update, etc.)
│   └── cli/                         # CLI interface and menu
├── tests/                           # Future: unit/integration tests
├── history/
│   ├── prompts/                     # Prompt History Records (PHRs)
│   └── adr/                         # Architecture Decision Records
├── CLAUDE.md                        # Claude Code configuration
├── README.md                        # Project documentation
└── pyproject.toml                   # UV project configuration
```

## Quality Gates

### Definition of Done (Per Feature)

A feature is complete when ALL criteria met:

- [ ] Specification approved and frozen
- [ ] Implementation plan reviewed and approved
- [ ] All tasks completed with code referencing task IDs
- [ ] All acceptance criteria pass manual testing
- [ ] No crashes on invalid input
- [ ] Error messages clear and actionable
- [ ] Code has type hints and docstrings
- [ ] Committed to Git with meaningful messages
- [ ] Demonstrable in isolation

### Phase I Success Criteria (Project Complete)

Phase I complete when:

- [ ] All 5 basic features implemented and working
- [ ] Clean console output with user-friendly prompts
- [ ] No application crashes under any user input scenario
- [ ] All code maps to approved specification tasks
- [ ] Git repository with meaningful commit history
- [ ] 90-second demonstration video recorded showing all features
- [ ] README documents how to run and use the application

## Governance

### Constitution Authority

This constitution supersedes all other guidance, conventions, or practices. In case of conflict
between this constitution and any other document (including templates, prior decisions, or
external guidelines), this constitution takes precedence.

### Amendment Process

Constitution amendments MUST:

1. Document the proposed change with rationale and impact analysis
2. Update version number following semantic versioning:
   - MAJOR: Breaking changes to principles or workflow
   - MINOR: New principles or sections added
   - PATCH: Clarifications or wording improvements
3. Propagate changes to dependent templates (spec, plan, tasks)
4. Gain explicit approval before taking effect
5. Record decision in Architecture Decision Record (ADR)

### Compliance Review

All specification artifacts (spec.md, plan.md, tasks.md) MUST include a "Constitution Check"
section verifying compliance with principles defined here.

Code reviews MUST verify:

- Traceability: Every implementation artifact maps to approved tasks
- Type Safety: All functions have type hints
- Documentation: All public APIs have docstrings
- Error Handling: All user inputs validated, all exceptions handled
- Simplicity: No external dependencies, no unnecessary complexity

### Complexity Justification

Any violation of constitutional principles (e.g., external dependency in Phase I, missing type
hints, manual code addition) MUST be explicitly justified in writing with:

- Why the violation is necessary
- What simpler alternative was considered and rejected
- What mitigation reduces the risk/impact
- Approval from project stakeholder (self-approval for solo learning)

Unjustified violations invalidate the Phase I completion criteria.

### Living Document

This constitution is a living document. As you progress through Phases II and III, you will
amend this constitution to reflect new requirements (persistence, authentication, collaboration).

Each amendment MUST:

- Maintain backward compatibility where possible
- Document what changed and why
- Update dependent artifacts (templates, existing specs)
- Increment version number appropriately

**Version**: 1.0.0 | **Ratified**: 2025-12-25 | **Last Amended**: 2025-12-25
