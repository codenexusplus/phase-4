# Tasks: AI Todo Agentic System

**Input**: Design documents from `/specs/001-ai-todo-agent/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume web app structure based on plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in backend/
- [X] T002 Initialize Python 3.10+ project with requirements.txt containing: fastapi, uvicorn, sqlmodel, psycopg2-binary, mcp, openai-agents, python-dotenv, pydantic-settings, pydantic-v2
- [X] T003 [P] Configure linting and formatting tools for Python (black, flake8, mypy)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Setup database schema and migrations framework in backend/database/connection.py
- [ ] T005 [P] Implement database models in backend/models/ (task.py, conversation.py, message.py)
- [ ] T006 [P] Setup async engine for Neon PostgreSQL in backend/database/connection.py
- [ ] T007 Create get_session dependency in backend/database/session.py
- [ ] T008 Configure environment configuration management in backend/config/settings.py
- [ ] T009 Setup error handling and logging infrastructure in backend/utils/error_handler.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to communicate with an AI assistant using natural language to manage their tasks, efficiently adding, viewing, updating, and completing tasks without navigating complex interfaces.

**Independent Test**: Can be fully tested by sending natural language commands like "Add buy groceries to my list" and verifying the task is created, or "Mark task #1 as complete" and verifying the task status updates.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for POST /api/{user_id}/chat in tests/contract/test_chat.py
- [ ] T011 [P] [US1] Integration test for task creation via natural language in tests/integration/test_task_creation.py

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create MCP server in backend/mcp_server/server.py
- [ ] T013 [US1] Implement add_task tool in backend/mcp_server/server.py (Accepts title/desc, returns confirmation)
- [ ] T014 [US1] Implement list_tasks tool in backend/mcp_server/server.py (Filters: all, pending, completed)
- [ ] T015 [US1] Implement complete_task tool in backend/mcp_server/server.py
- [ ] T016 [US1] Implement update_task and delete_task tools in backend/mcp_server/server.py
- [ ] T017 [US1] Verify all tools strictly filter by user_id in backend/mcp_server/server.py
- [ ] T018 [US1] Initialize OpenAI Agent in backend/agents/agent_logic.py
- [ ] T019 [US1] Connect MCP tools to the Agent in backend/agents/agent_logic.py
- [ ] T020 [US1] Create run_agent() loop in backend/agents/agent_logic.py to handle user input + history
- [ ] T021 [US1] Implement POST /api/{user_id}/chat endpoint in backend/api/chat_endpoint.py
- [ ] T022 [US1] Add logic to load context, run agent, save messages to DB, return JSON in backend/api/chat_endpoint.py
- [ ] T023 [US1] Add confirmation flow with formatted Markdown in backend/agents/agent_logic.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Conversation Memory and Context (Priority: P2)

**Goal**: Enable the AI assistant to remember previous conversations and maintain context, allowing for continuous, coherent interactions without repetition.

**Independent Test**: Can be tested by having a conversation across multiple exchanges where the AI remembers previous context and references it appropriately.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T024 [P] [US2] Contract test for context retrieval in tests/contract/test_context.py
- [ ] T025 [P] [US2] Integration test for conversation memory in tests/integration/test_conversation_memory.py

### Implementation for User Story 2

- [ ] T026 [P] [US2] Create get_conversation_context() function in backend/utils/context_helper.py (fetches last 10 messages from DB)
- [ ] T027 [US2] Integrate context helper with agent logic in backend/agents/agent_logic.py
- [ ] T028 [US2] Modify run_agent() to include conversation history in backend/agents/agent_logic.py
- [ ] T029 [US2] Update chat endpoint to fetch and provide context to agent in backend/api/chat_endpoint.py
- [ ] T030 [US2] Add conversation tracking to ensure context is properly maintained

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Operations via AI Commands (Priority: P3)

**Goal**: Enable users to perform all standard task operations (create, read, update, delete) through AI commands, managing tasks efficiently without manual interface interactions.

**Independent Test**: Can be tested by performing each operation type (create, read, update, delete) using natural language commands and verifying the correct database changes.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T031 [P] [US3] Contract test for all task operations in tests/contract/test_task_operations.py
- [ ] T032 [P] [US3] Integration test for complete CRUD via AI commands in tests/integration/test_crud_operations.py

### Implementation for User Story 3

- [ ] T033 [P] [US3] Enhance error handling for all MCP tools in backend/mcp_server/server.py
- [ ] T034 [US3] Implement structured exception handling with clear error messages in backend/mcp_server/server.py
- [ ] T035 [US3] Add validation for all MCP tools using Pydantic V2 in backend/mcp_server/server.py
- [ ] T036 [US3] Enhance agent logic to handle ambiguous requests in backend/agents/agent_logic.py
- [ ] T037 [US3] Add retry mechanisms for database unavailable scenarios in backend/database/connection.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T038 [P] Documentation updates in docs/
- [ ] T039 Code cleanup and refactoring
- [ ] T040 Performance optimization across all stories
- [ ] T041 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T042 Security hardening - ensure all queries have WHERE user_id = :user_id
- [ ] T043 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /api/{user_id}/chat in tests/contract/test_chat.py"
Task: "Integration test for task creation via natural language in tests/integration/test_task_creation.py"

# Launch all models for User Story 1 together:
Task: "Create MCP server in backend/mcp_server/server.py"
Task: "Implement add_task tool in backend/mcp_server/server.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence