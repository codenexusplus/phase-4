# Data Model: Containerize AI Todo Agentic System with Kubernetes and Helm

## Kubernetes Resources

### Backend Deployment
- **apiVersion**: apps/v1
- **kind**: Deployment
- **metadata**: 
  - name: backend-deployment
  - namespace: todo-system
- **spec**:
  - replicas: 2 (for high availability)
  - selector: matchLabels: app=backend
  - template: 
    - metadata: labels: app=backend
    - spec:
      - containers:
        - name: backend
        - image: todo-backend:latest
        - ports: [{containerPort: 8000}]
        - envFrom: [{secretRef: {name: backend-secrets}}]

### Frontend Deployment
- **apiVersion**: apps/v1
- **kind**: Deployment
- **metadata**: 
  - name: frontend-deployment
  - namespace: todo-system
- **spec**:
  - replicas: 2 (for high availability)
  - selector: matchLabels: app=frontend
  - template:
    - metadata: labels: app=frontend
    - spec:
      - containers:
        - name: frontend
        - image: todo-frontend:latest
        - ports: [{containerPort: 3000}]
        - envFrom: [{secretRef: {name: frontend-secrets}}]

### Backend Service
- **apiVersion**: v1
- **kind**: Service
- **metadata**:
  - name: backend-service
  - namespace: todo-system
- **spec**:
  - selector: app=backend
  - ports: [{protocol: TCP, port: 80, targetPort: 8000}]
  - type: ClusterIP (internal access only)

### Frontend Service
- **apiVersion**: v1
- **kind**: Service
- **metadata**:
  - name: frontend-service
  - namespace: todo-system
- **spec**:
  - selector: app=frontend
  - ports: [{protocol: TCP, port: 80, targetPort: 3000}]
  - type: NodePort (external access)

### Namespace
- **apiVersion**: v1
- **kind**: Namespace
- **metadata**:
  - name: todo-system

### Secrets
- **apiVersion**: v1
- **kind**: Secret
- **metadata**:
  - name: backend-secrets
  - namespace: todo-system
- **type**: Opaque
- **data**:
  - DATABASE_URL: [base64 encoded]
  - OPENAI_API_KEY: [base64 encoded]

## Helm Chart Values

### Global Configuration
- **imageRegistry**: ""
- **imagePullSecrets**: []
- **nameOverride**: ""
- **fullnameOverride**: ""

### Backend Configuration
- **backend.replicaCount**: 2
- **backend.image.repository**: todo-backend
- **backend.image.pullPolicy**: IfNotPresent
- **backend.service.type**: ClusterIP
- **backend.service.port**: 80

### Frontend Configuration
- **frontend.replicaCount**: 2
- **frontend.image.repository**: todo-frontend
- **frontend.image.pullPolicy**: IfNotPresent
- **frontend.service.type**: NodePort
- **frontend.service.port**: 80

### Resource Limits
- **resources.limits.cpu**: 100m
- **resources.limits.memory**: 128Mi
- **resources.requests.cpu**: 100m
- **resources.requests.memory**: 128Mi