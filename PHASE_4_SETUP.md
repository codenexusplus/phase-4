# Phase 4: Containerization and Kubernetes Deployment

## Overview
Phase 4 involves containerizing the AI Todo Agentic System and deploying it to a Kubernetes cluster using Helm charts. The system consists of a FastAPI backend with AI agents and a React frontend.

## Prerequisites
- Docker and Docker Compose
- Kubernetes cluster (Minikube recommended for local development)
- Helm 3.x
- kubectl

## Containerization

### Docker Images
The system includes two main services:

#### Backend Service
- Base image: `python:3.11-slim`
- Port: 8000
- Environment variables:
  - `PYTHONPATH=/app`
  - `DATABASE_URL` (from Kubernetes secret)
  - `OPENAI_API_KEY` (from Kubernetes secret)

#### Frontend Service
- Base image: `node:20-alpine` (multi-stage build)
- Port: 3000
- Environment variables:
  - `NEXT_PUBLIC_API_URL` (points to backend service)

### Docker Compose Setup
The `docker-compose-no-version.yml` file orchestrates the local development environment:
- Backend service (FastAPI)
- Frontend service (React)
- PostgreSQL database

## Kubernetes Deployment

### Namespace
All resources are deployed to the `todo-system` namespace.

### Services
- Backend: ClusterIP service for internal communication
- Frontend: NodePort service for external access
- PostgreSQL: ClusterIP service for internal database access

### Deployments
- Backend: 2 replicas for high availability
- Frontend: 2 replicas for high availability
- PostgreSQL: 1 replica with persistent volume claim

### Configuration and Secrets
- Database URL stored in Kubernetes secret
- OpenAI API key stored in Kubernetes secret
- Other configuration managed via ConfigMaps

## Helm Chart

The Helm chart is located at `phase-4-infrastructure/charts/todo-chatbot` and includes:

### Values
- Replica counts for backend and frontend
- Image repositories and tags
- Resource limits and requests
- Service types and ports

### Templates
- Backend and frontend deployments
- Backend and frontend services
- Database deployment, service, and PVC
- ConfigMaps and secrets

## Deployment Steps

### 1. Local Testing
```bash
# Build and run with Docker Compose
docker-compose -f docker-compose-no-version.yml up --build
```

### 2. Kubernetes Setup
```bash
# Start Minikube (if using local cluster)
minikube start

# Create namespace
kubectl create namespace todo-system

# Apply secrets (replace with actual values)
kubectl create secret generic neon-db-secret \
  --from-literal=DATABASE_URL=<your-database-url> \
  --namespace=todo-system

kubectl create secret generic openai-api-secret \
  --from-literal=OPENAI_API_KEY=<your-openai-api-key> \
  --namespace=todo-system
```

### 3. Helm Deployment
```bash
# Navigate to the charts directory
cd phase-4-infrastructure/charts

# Install the Helm chart
helm install todo-chatbot todo-chatbot/ --namespace todo-system

# Verify the installation
kubectl get pods -n todo-system
kubectl get services -n todo-system
```

### 4. Access the Application
```bash
# Get the frontend service URL
kubectl get service -n todo-system

# If using Minikube, you can access the service with:
minikube service <frontend-service-name> -n todo-system
```

## Troubleshooting

### Common Issues
1. **Image Pull Errors**: Ensure your image repository and tags are correct in values.yaml
2. **Database Connection Issues**: Verify that the DATABASE_URL secret is correctly set
3. **API Key Issues**: Ensure the OPENAI_API_KEY secret is properly configured
4. **Service Discovery**: Verify that services can communicate using their DNS names

### Useful Commands
```bash
# Check pod status
kubectl get pods -n todo-system

# Check service status
kubectl get services -n todo-system

# View pod logs
kubectl logs -n todo-system <pod-name>

# Port forward for debugging
kubectl port-forward -n todo-system svc/<service-name> <local-port>:<service-port>
```

## Scaling
The application supports horizontal scaling:
```bash
# Scale backend replicas
kubectl scale deployment -n todo-system <backend-deployment-name> --replicas=3

# Scale frontend replicas
kubectl scale deployment -n todo-system <frontend-deployment-name> --replicas=3
```

## Updating Configuration
To update configuration values:
```bash
# Update values in values.yaml or pass new values
helm upgrade todo-chatbot todo-chatbot/ --namespace todo-system --set backend.replicaCount=3
```

## Cleanup
To remove the deployment:
```bash
# Uninstall the Helm release
helm uninstall todo-chatbot -n todo-system

# Delete the namespace (optional)
kubectl delete namespace todo-system
```