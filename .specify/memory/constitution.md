<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 -> 1.1.0
Modified principles: Added Phase 4 Infrastructure Governance section
Added sections: Phase 4 Infrastructure Governance
Removed sections: N/A
Templates requiring updates: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# AI Todo Chatbot Constitution

## Core Principles

### I. Strict Statelessness
The FastAPI server must not hold any in-memory state. Every request cycle must:
1. Authenticate the `user_id`.
2. Retrieve conversation history from Neon DB.
3. Execute the Agentic loop.
4. Persist the new state back to DB.

### II. MCP Protocol Compliance
All business logic for Task CRUD must be encapsulated within an Official MCP Server. The AI Agent must interact with the DB *only* through these MCP tools.

### III. Technical Stack Standardization
- Runtime: Python 3.10+ (FastAPI)
- Agentic Framework: OpenAI Agents SDK (using Agent + Runner patterns)
- Tooling Protocol: Official MCP Python SDK
- ORM & Database: SQLModel with Neon Serverless PostgreSQL (Async Engine)
- Validation: Pydantic V2 for all schemas and tool parameters
- Communication: Asynchronous (async/await) throughout the entire stack

### IV. Coding & Naming Standards
- Classes: `PascalCase`
- Functions/Variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Error Handling: Use structured exceptions. Tools must return clear error messages (e.g., "Task ID {id} not found") so the Agent can explain the issue to the user.
- Type Hinting: Mandatory type hints for all function signatures.

### V. Natural Language Processing Capabilities
- Context Injection: The system must implement a 'Last-N Messages' sliding window (default: 10) for conversation context.
- Natural Language Understanding (NLU): The agent must handle ambiguous commands (e.g., "Remind me to buy milk" -> `add_task`).
- Confirmation Flow: The Agent must use formatted Markdown to confirm actions (e.g., "✅ **Task Added:** Buy groceries").

### VI. Security & Privacy
Every SQL query must include a `WHERE user_id = :user_id` clause to prevent data leakage between users. Sensitive keys (OpenAI, Neon URL) must be read from environment variables only.

## Additional Constraints

### Database Tenancy
All database queries must implement proper user isolation through tenancy controls. Each user's data must be completely isolated from others through the mandatory use of user_id filters.

### Asynchronous Operations
The entire stack must utilize async/await patterns to maximize efficiency and scalability. All database operations, API calls, and external service interactions must be asynchronous.

## Phase 4 Infrastructure Governance

### 1. Tooling Requirements
- **Gordon (Docker AI)**: Must be used for optimizing Docker images
- **kubectl-ai**: Must be used for generating Kubernetes manifests
- **Kagent**: Must be used for health checks and diagnostics

### 2. Statelessness in Containerized Environment
- No local data storage in containers
- All state must be persisted in Neon DB
- Container restarts must not affect application state

### 3. High Availability Requirements
- Minimum 2 replicas per service (backend and frontend)
- Load balancing must distribute traffic across all replicas
- Health checks must monitor service availability

### 4. Infrastructure Automation
- No manual YAML edits allowed
- All infrastructure must be generated via AI agents based on specifications
- Infrastructure changes must follow GitOps principles

### 5. Folder Isolation
- All Phase 4 infrastructure assets must be contained within `/phase-4-infrastructure` directory
- Dockerfiles, Helm charts, and Kubernetes manifests must be organized in designated subdirectories

## Development Workflow

### Error Handling Standards
All tools and services must return structured error messages that allow the AI agent to clearly communicate issues to end users. Error messages should be informative but not expose internal system details.

### Validation Requirements
All input and output must be validated using Pydantic V2 schemas. This includes request parameters, database models, and tool responses to ensure data integrity and prevent injection attacks.

## Governance

This constitution defines the mandatory practices for the AI Todo Chatbot project. All code submissions, reviews, and deployments must comply with these principles. Deviations require explicit approval and documentation of the exception.

**Version**: 1.1.0 | **Ratified**: 2026-01-17 | **Last Amended**: 2026-02-02