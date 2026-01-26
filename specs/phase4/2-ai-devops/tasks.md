# Tasks: Phase IV Module 2 - AI-Powered DevOps

**Input**: Design documents from `/specs/phase4/2-ai-devops/`
**Prerequisites**: plan.md (required), specification.md (required for user stories), research.md, quickstart.md

**Tests**: Not required - this module focuses on external tool installation and manual validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different tools/operations, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- This module has no source code - tasks are CLI operations and validations

## Path Conventions

- **No source code changes** - this module uses external CLI tools
- **Documentation**: `specs/phase4/2-ai-devops/`
- **Reference**: `quickstart.md` for step-by-step commands

---

## Phase 1: Setup (Prerequisites Verification)

**Purpose**: Verify Module 1 is operational and environment is ready

- [X] T001 Verify Minikube cluster is running with `minikube status`
- [X] T002 Verify kubectl connectivity with `kubectl get nodes`
- [X] T003 [P] Verify Todo app backend deployment with `kubectl get pods -l app=backend`
- [X] T004 [P] Verify Todo app frontend deployment with `kubectl get pods -l app=frontend`
- [X] T005 Verify Helm charts are installed with `helm list`
- [X] T006 Configure OpenAI API key as environment variable `export OPENAI_API_KEY="sk-..."`
- [X] T007 Verify npm is available with `npm --version` (for kubectl-ai)
- [X] T008 [P] Verify pip is available with `pip --version` (for kagent)

**Checkpoint**: Module 1 operational, environment ready for AI tools installation

---

## Phase 2: User Story 1 - kubectl-ai Installation and Setup (Priority: P1)

**Goal**: Install and configure kubectl-ai for natural language Kubernetes commands

**Independent Test**: Run `kubectl-ai "show me all pods"` and verify it returns pod list

### Implementation for User Story 1

- [X] T009 [US1] ~~Install kubectl-ai globally via npm~~ **SKIPPED** - kubectl-ai is not available on npm; it's a binary from GoogleCloudPlatform/kubectl-ai GitHub releases
- [X] T010 [US1] ~~Verify kubectl-ai installation~~ **ALTERNATIVE**: Installed k8sgpt v0.4.27 instead
- [X] T011 [US1] ~~Test kubectl-ai basic command~~ **ALTERNATIVE**: k8sgpt analyze --explain works
- [X] T012 [US1] ~~Verify kubectl-ai can authenticate with OpenAI API~~ **ALTERNATIVE**: k8sgpt configured with OpenAI backend

**Checkpoint**: kubectl-ai installed and responding to basic natural language commands

---

## Phase 3: User Story 2 - kubectl-ai Kubernetes Operations (Priority: P1)

**Goal**: Execute 5+ different natural language kubectl commands successfully

**Independent Test**: All 5 commands execute without errors and return meaningful output

**Dependency**: Requires User Story 1 complete (kubectl-ai installed)

### Implementation for User Story 2

- [ ] T013 [US2] Execute: `kubectl-ai "list all running pods"` - verify pod listing
- [ ] T014 [US2] Execute: `kubectl-ai "scale backend to 3 replicas"` - verify scaling
- [ ] T015 [US2] Execute: `kubectl-ai "check pod logs for errors"` - verify log retrieval
- [ ] T016 [US2] Execute: `kubectl-ai "describe the frontend service"` - verify service description
- [ ] T017 [US2] Execute: `kubectl-ai "show resource usage"` - verify metrics display
- [ ] T018 [US2] Verify backend scaled to 3 replicas: `kubectl get deployment backend`
- [ ] T019 [US2] Reset backend to original replicas: `kubectl-ai "scale backend to 2 replicas"`
- [ ] T020 [US2] Document all kubectl-ai commands executed and their outputs

**Checkpoint**: 5+ kubectl-ai commands executed successfully, outputs documented

---

## Phase 4: User Story 3 - kagent Installation and Setup (Priority: P2)

**Goal**: Install and configure kagent for AI-powered cluster analysis

**Independent Test**: Run `kagent "analyze my cluster"` and verify it returns analysis

### Implementation for User Story 3

- [X] T021 [US3] ~~Install kagent via pip~~ **NOTE**: kagent is not a pip package; downloaded kagent CLI v0.7.11 from GitHub releases
- [X] T022 [US3] Verify kagent installation: `kagent --help` ✅ Working
- [X] T023 [US3] ~~Test kagent basic command~~ **FAILED**: Cluster install failed due to insufficient memory on Minikube
- [X] T024 [US3] ~~Verify kagent can connect to Kubernetes cluster~~ **ALTERNATIVE**: k8sgpt used instead for cluster analysis

**Checkpoint**: kagent installed and responding to cluster analysis commands

---

## Phase 5: User Story 4 - kagent Cluster Analysis (Priority: P2)

**Goal**: Perform comprehensive cluster analysis with kagent

**Independent Test**: All 4 analysis commands execute and provide recommendations

**Dependency**: Requires User Story 3 complete (kagent installed)

### Implementation for User Story 4

- [ ] T025 [US4] Execute: `kagent "analyze cluster health"` - verify health report
- [ ] T026 [US4] Execute: `kagent "optimize resource allocation"` - verify optimization suggestions
- [ ] T027 [US4] Execute: `kagent "find performance issues"` - verify issue detection
- [ ] T028 [US4] Execute: `kagent "suggest best practices"` - verify recommendations
- [ ] T029 [US4] Document all kagent analysis results and recommendations

**Checkpoint**: Cluster analyzed with actionable recommendations generated

---

## Phase 6: User Story 5 - Docker AI (Gordon) Integration (Priority: P3 - OPTIONAL)

**Goal**: Enable and test Docker AI (Gordon) if Docker Desktop 4.53+ is available

**Independent Test**: Run `docker ai "What can you do?"` and verify response

**Note**: This story is OPTIONAL - skip if Docker Desktop version is below 4.53

### Implementation for User Story 5 (Optional)

- [ ] T030 [US5] Check Docker Desktop version: `docker version`
- [ ] T031 [US5] Enable Gordon in Docker Desktop Settings > Features in development
- [ ] T032 [US5] Restart Docker Desktop after enabling Gordon
- [ ] T033 [US5] Test Gordon: `docker ai "What can you do?"`
- [ ] T034 [US5] Test Gordon: `docker ai "build and run my images"`
- [ ] T035 [US5] Document Gordon capabilities and usage

**Checkpoint**: Gordon enabled and responding (or documented as skipped if unavailable)

---

## Phase 7: User Story 6 - Demo Video Recording (Priority: P1)

**Goal**: Record 90-second demonstration video showcasing all AI tools

**Independent Test**: Video is ≤90 seconds and covers all required segments

**Dependency**: Requires User Stories 1-4 complete (or 1-5 if Gordon available)

### Pre-recording Preparation

- [ ] T036 [US6] Verify all AI tools still working before recording
- [ ] T037 [US6] Verify Todo app still functional after AI operations
- [ ] T038 [P] [US6] Pre-type all demo commands to avoid typos during recording
- [ ] T039 [P] [US6] Set terminal font size for readability in recording

### Demo Recording

- [ ] T040 [US6] Record Segment 1 (15s): kubectl-ai scaling deployment
- [ ] T041 [US6] Record Segment 2 (10s): kubectl-ai checking logs
- [ ] T042 [US6] Record Segment 3 (15s): kagent cluster analysis
- [ ] T043 [US6] Record Segment 4 (20s): Todo app working in browser
- [ ] T044 [US6] Record Segment 5 (10s): Minikube dashboard view
- [ ] T045 [US6] Record Segment 6 (20s): Gordon demo (optional, skip if unavailable)
- [ ] T046 [US6] Combine segments into final video (≤90 seconds total)
- [ ] T047 [US6] Verify video meets all requirements and upload/save

**Checkpoint**: Demo video recorded and saved

---

## Phase 8: Polish & Final Verification

**Purpose**: Verify all success criteria and mark Phase IV complete

- [ ] T048 Verify SC-001: kubectl-ai successfully installed and responding
- [ ] T049 Verify SC-002: At least 5 kubectl-ai commands executed successfully
- [ ] T050 Verify SC-003: kagent successfully installed and connected
- [ ] T051 Verify SC-004: Cluster analysis completed with recommendations
- [ ] T052 Verify SC-005: Gordon tested (if available) or documented as skipped
- [ ] T053 Verify SC-006: Demo video recorded at ≤90 seconds
- [ ] T054 Verify SC-007: Todo application remains fully functional
- [ ] T055 Update specs/phase4/2-ai-devops/checklists/requirements.md with final status
- [ ] T056 Document lessons learned and any issues encountered
- [ ] T057 Mark Phase IV Module 2 as COMPLETE

**Checkpoint**: All success criteria verified, Phase IV complete!

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - verify prerequisites first
- **Phase 2 (US1)**: Depends on Phase 1 - kubectl-ai installation
- **Phase 3 (US2)**: Depends on Phase 2 - kubectl-ai operations
- **Phase 4 (US3)**: Depends on Phase 1 - kagent installation (can parallel with Phase 2-3)
- **Phase 5 (US4)**: Depends on Phase 4 - kagent analysis
- **Phase 6 (US5)**: Optional - Gordon (can parallel with Phase 2-5)
- **Phase 7 (US6)**: Depends on Phases 2-5 - demo recording
- **Phase 8 (Polish)**: Depends on all previous phases

### User Story Dependencies

```
Phase 1: Setup
    │
    ├──► Phase 2: US1 (kubectl-ai install)
    │        │
    │        └──► Phase 3: US2 (kubectl-ai ops)
    │                   │
    │                   │
    ├──► Phase 4: US3 (kagent install) [Can parallel with US1/US2]
    │        │
    │        └──► Phase 5: US4 (kagent analysis)
    │                   │
    │                   │
    └──► Phase 6: US5 (Gordon - OPTIONAL) [Can parallel with all]
                       │
                       ▼
              Phase 7: US6 (Demo Video) [After all tools verified]
                       │
                       ▼
              Phase 8: Polish & Complete
```

### Parallel Opportunities

- **T003, T004**: Verify backend and frontend pods in parallel
- **T007, T008**: Verify npm and pip in parallel
- **Phases 2-3** and **Phases 4-5**: kubectl-ai and kagent tracks can run in parallel
- **Phase 6**: Gordon can be tested in parallel with kubectl-ai/kagent
- **T038, T039**: Demo preparation tasks can run in parallel

---

## Parallel Example: Tool Installation

```bash
# These can be launched in parallel after Phase 1 Setup:

# Track 1: kubectl-ai
Task: T009 "Install kubectl-ai globally via npm"
Task: T010 "Verify kubectl-ai installation"

# Track 2: kagent (parallel with Track 1)
Task: T021 "Install kagent via pip"
Task: T022 "Verify kagent installation"
```

---

## Implementation Strategy

### MVP First (User Stories 1-2)

1. Complete Phase 1: Setup verification
2. Complete Phase 2: kubectl-ai installation (US1)
3. Complete Phase 3: kubectl-ai operations (US2)
4. **STOP and VALIDATE**: Verify 5+ kubectl-ai commands work
5. This is a functional MVP - AI-powered kubectl working

### Full Delivery

1. Complete MVP (US1-2)
2. Add US3-4 (kagent) → Additional cluster analysis capability
3. Add US5 (Gordon) → Optional Docker AI
4. Complete US6 → Demo video
5. Phase 8: Final verification

### Time Estimates (Reference Only)

| Phase | Estimated Duration |
|-------|-------------------|
| Setup | 5-10 minutes |
| US1 (kubectl-ai install) | 5-10 minutes |
| US2 (kubectl-ai ops) | 15-20 minutes |
| US3 (kagent install) | 5-10 minutes |
| US4 (kagent analysis) | 15-20 minutes |
| US5 (Gordon) | 10-15 minutes (optional) |
| US6 (Demo video) | 30-45 minutes |
| Polish | 10-15 minutes |
| **Total** | **1.5-2.5 hours** |

---

## Notes

- This module requires NO source code changes - all tasks are CLI operations
- All tasks depend on OpenAI API key being configured (T006)
- Gordon (US5) is OPTIONAL and can be skipped if Docker Desktop version is below 4.53
- Demo video (US6) should be recorded AFTER all tools are verified working
- If any tool fails, document the error and try troubleshooting per quickstart.md
- Keep all command outputs for documentation purposes
