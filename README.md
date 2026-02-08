# AI Todo Agentic System

An AI-powered todo management system that transforms a static Todo app into an Agentic System. The AI assistant understands natural language, manages tasks via MCP tools, and maintains long-term conversation memory.

## Features

- Natural language task management (create, read, update, delete tasks)
- Conversation memory and context awareness
- Secure user isolation (each user can only access their own tasks)
- MCP protocol compliance for all database operations
- Stateless architecture with persistent memory

## Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **AI Agent**: OpenAI Agents SDK
- **Protocol**: Official MCP Python SDK
- **Database**: SQLModel + Neon PostgreSQL (Async)
- **Frontend**: React with OpenAI ChatKit components

## Setup

### Backend Setup

1. Clone the repository
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and update with your credentials:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```
5. Start both the main server and WebSocket server:
   ```bash
   # From the project root directory
   python start_both_servers.py
   ```

   Or start them individually:
   ```bash
   # Terminal 1: Start the main backend server
   cd backend
   uvicorn main:app --reload --port 8000

   # Terminal 2: Start the WebSocket server for real-time updates
   cd backend
   python -m websocket_main
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

## Usage

The API endpoint is available at `/api/{user_id}/chat`. Send a POST request with the following JSON:

```json
{
  "message": "Add buy groceries to my tasks",
  "conversation_id": 1
}
```

The frontend provides a user-friendly chat interface to interact with the AI assistant.

## Architecture

The system enforces strict statelessness with every request cycle:
1. Authenticate the `user_id`
2. Retrieve conversation history from Neon DB
3. Execute the Agentic loop
4. Persist the new state back to DB

All database queries include a `WHERE user_id = :user_id` clause to ensure data isolation between users.

## MCP Tools

The system provides the following MCP tools for the AI agent:
- `add_task`: Creates a new task
- `list_tasks`: Lists tasks with optional status filter
- `complete_task`: Marks a task as completed
- `delete_task`: Deletes a task
- `update_task`: Updates task details

## Deployment

### Deploying to Vercel (Frontend)

This application has both frontend and backend components. To deploy to Vercel:

1. **Frontend Deployment**:
   - The React frontend can be deployed directly to Vercel
   - Make sure to update the API endpoint in your frontend to point to your deployed backend
   - Add environment variables in the Vercel dashboard

For detailed frontend deployment instructions, see [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md).

### Deploying the Backend

The FastAPI backend needs to be deployed separately to a platform that supports persistent connections, such as Render, Heroku, or AWS.

1. **Prepare for deployment**:
   - Backend files are in the `backend` directory
   - Requirements file: `backend/requirements.txt`
   - Procfile for Heroku/Render: `backend/Procfile`
   - Runtime specification: `backend/runtime.txt`

2. **Deploy to your chosen platform**:
   - Set environment variables (DATABASE_URL, OPENAI_API_KEY, etc.)
   - Configure the startup command: `uvicorn backend.main:app --host=0.0.0.0 --port=$PORT`

For detailed backend deployment instructions, see [BACKEND_DEPLOYMENT_GUIDE.md](./BACKEND_DEPLOYMENT_GUIDE.md).

### Deploying to Render (Recommended)

For a seamless deployment experience, we recommend deploying your backend to Render:

1. Push your code to a GitHub repository
2. Create a PostgreSQL database on Render
3. Create a new Web Service on Render pointing to your repository
4. Set the environment variables as specified in [DEPLOY_TO_RENDER.md](./DEPLOY_TO_RENDER.md)
5. Your backend will be automatically deployed and updated with each commit

For step-by-step instructions, see [DEPLOY_TO_RENDER.md](./DEPLOY_TO_RENDER.md).

### Quick Deploy to Vercel (Frontend Only)

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-repo/ai-todo-agentic-system&project-name=ai-todo-frontend&repo-name=ai-todo-frontend)

Note: This will only deploy the frontend. You'll need to separately deploy the backend and update the API endpoint.

## Contributing

Contributions are welcome! Please follow the project's constitutional principles:
- Strict Statelessness
- MCP Protocol Compliance
- Technical Stack Standardization
- Coding & Naming Standards
- Natural Language Processing Capabilities
- Security & Privacy