# AI Todo Agentic System

An AI-powered todo management system that transforms a static Todo app into an Agentic System. The AI assistant understands natural language, manages tasks via MCP tools, and maintains long-term conversation memory.

## 🚀 Features

- Natural language task management (create, read, update, delete tasks)
- Conversation memory and context awareness
- Secure user isolation (each user can only access their own tasks)
- MCP protocol compliance for all database operations
- Stateless architecture with persistent memory
- Real-time updates via WebSocket connections
- Containerized deployment with Docker and Kubernetes support

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **AI Agent**: OpenAI Agents SDK with local Ollama support
- **Protocol**: Official MCP Python SDK
- **Database**: SQLModel + Neon PostgreSQL (Async)
- **Frontend**: React with OpenAI ChatKit components
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes with Helm Charts

## 📁 Project Structure

```
├── backend/                 # FastAPI backend with AI agents
│   ├── api/                # API endpoints
│   ├── models/             # Database models
│   ├── services/           # Business logic
│   ├── agents/             # AI agent logic
│   └── Dockerfile          # Backend container configuration
├── frontend/               # React frontend
│   ├── src/                # Source code
│   └── Dockerfile          # Frontend container configuration
├── phase-4-infrastructure/ # Kubernetes & Helm configurations
│   └── charts/             # Helm charts for deployment
├── docker-compose.yml      # Multi-container orchestration
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Node.js & npm

### Running Locally

1. Clone the repository
2. Set up environment variables:
   ```bash
   # In backend/.env
   DATABASE_URL=sqlite+aiosqlite:///./todo_app.db
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_API_KEY=dummy-key-for-local
   ```

3. Start the services:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 🤖 AI Assistant Capabilities

The AI assistant can understand and perform various task management operations:

- "Add buy groceries to my tasks"
- "Show me my pending tasks"
- "Mark task #1 as completed"
- "Delete task #2"
- "Update task #3 to 'buy organic groceries'"

## 🐳 Containerization

The application is fully containerized:

- Backend service (FastAPI + AI agents)
- Frontend service (React)
- PostgreSQL database
- WebSocket service for real-time updates

## ☸️ Kubernetes Deployment

The application can be deployed to Kubernetes using Helm charts:

```bash
# Add the Helm repo and install
helm repo add todo-chatbot https://github.com/codenexusplus/phase-4
helm install todo-chatbot todo-chatbot/todo-chatbot
```

## 📊 Architecture

The system enforces strict statelessness with every request cycle:
1. Authenticate the `user_id`
2. Retrieve conversation history from Neon DB
3. Execute the Agentic loop
4. Persist the new state back to DB

All database queries include a `WHERE user_id = :user_id` clause to ensure data isolation between users.

## 🛡️ Security

- JWT-based authentication
- User data isolation
- Secure API endpoints
- Environment-based configuration

## 🤝 Contributing

Contributions are welcome! Please follow the project's constitutional principles:
- Strict Statelessness
- MCP Protocol Compliance
- Technical Stack Standardization
- Coding & Naming Standards
- Natural Language Processing Capabilities
- Security & Privacy

## 📄 License

This project is licensed under the MIT License.

---

## 🏗️ Phase 4: Local Kubernetes Deployment (Agentic Dev Stack)

This repository represents the completion of Phase 4, featuring:
- Containerized frontend and backend applications
- Helm charts for Kubernetes deployment
- AI-assisted operations with kubectl-ai and Kagent
- Docker AI Agent (Gordon) for containerization
- Minikube for local Kubernetes deployment