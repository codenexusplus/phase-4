# Quickstart Guide: Containerize AI Todo Agentic System

## Prerequisites

Before starting, ensure you have the following tools installed:

- Docker (with Docker Compose)
- Minikube
- Helm
- kubectl
- Git

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Build and Run Locally with Docker Compose

For quick testing and development:

```bash
# Navigate to project root
cd /path/to/project

# Build and start services
docker-compose up --build
```

The application will be available at `http://localhost:3000`.

## Kubernetes Deployment

### 1. Start Minikube

```bash
# Start Minikube with Docker driver
minikube start --driver=docker

# Verify cluster is running
kubectl cluster-info
```

### 2. Create Namespace

```bash
# Create the todo-system namespace
kubectl create namespace todo-system
```

### 3. Configure Secrets

Create Kubernetes secrets for the database URL and API keys:

```bash
# Create Neon Database URL secret
kubectl create secret generic neon-db-secret \
  --from-literal=DATABASE_URL=<your-neon-db-url> \
  --namespace=todo-system

# Create OpenAI API key secret
kubectl create secret generic openai-api-secret \
  --from-literal=OPENAI_API_KEY=<your-openai-api-key> \
  --namespace=todo-system
```

### 4. Load Docker Images into Minikube

```bash
# Set Docker environment to Minikube
eval $(minikube docker-env)

# Build images for Minikube
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend
```

### 5. Deploy with Helm

```bash
# Navigate to charts directory
cd charts/todo-app

# Install the Helm chart
helm install todo-chatbot . --namespace todo-system --set backend.image.tag=latest --set frontend.image.tag=latest
```

### 6. Access the Application

```bash
# Get the frontend service URL
minikube service frontend-service --namespace todo-system --url
```

## Verification

### 1. Check Pod Status

```bash
# Verify 4 pods are running (2 backend + 2 frontend)
kubectl get pods --namespace todo-system
```

### 2. Check Logs

```bash
# Check backend logs
kubectl logs -l app=backend --namespace todo-system

# Check frontend logs
kubectl logs -l app=frontend --namespace todo-system
```

### 3. Test Application Functionality

- Access the application via the Minikube service URL
- Test the AI Chatbot functionality
- Verify that tasks created via the AI interface appear in the dashboard
- Test the task creation and completion features