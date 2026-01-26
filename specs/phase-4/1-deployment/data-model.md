# Data Model: Phase IV Module 1 - Containerization & Kubernetes Deployment

## Overview
This phase is primarily deployment-focused, so the data model remains largely unchanged from Phase III. The containerization and orchestration layers don't introduce new persistent data entities, but rather focus on packaging and deploying existing services.

## Existing Data Models (Preserved from Phase III)

### Task Entity
```python
class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255)
    description: str | None = None
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Conversation Entity
```python
class Conversation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str | None = Field(max_length=255, default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Message Entity
```python
class Message(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=50)  # 'user', 'assistant', 'system'
    content: str
    tool_calls: dict[str, Any] | None = Field(default=None, sa_type=JSONB)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Deployment Configuration Models (New for Phase IV)

### Kubernetes Resource Configuration
The following configuration models will be used in Kubernetes manifests and Helm charts:

#### Deployment Configuration
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service-name}
spec:
  replicas: 2
  selector:
    matchLabels:
      app: {service-name}
  template:
    metadata:
      labels:
        app: {service-name}
    spec:
      containers:
      - name: {service-name}
        image: {image-name}:{tag}
        ports:
        - containerPort: {port}
        envFrom:
        - configMapRef:
            name: {configmap-name}
        - secretRef:
            name: {secret-name}
        resources:
          requests:
            memory: "{memory-request}"
            cpu: "{cpu-request}"
          limits:
            memory: "{memory-limit}"
            cpu: "{cpu-limit}"
        livenessProbe:
          httpGet:
            path: /health
            port: {port}
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: {port}
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### Service Configuration
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {service-name}
spec:
  selector:
    app: {service-name}
  ports:
    - protocol: TCP
      port: {port}
      targetPort: {container-port}
  type: {ServiceType}  # ClusterIP for backend, NodePort for frontend
```

### Helm Values Structure
```yaml
# values.yaml
replicaCount: 2

image:
  repository: {image-repository}
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: {ServiceType}
  port: {port}

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

env:
  FRONTEND_URL: ""
  DATABASE_URL: ""
  JWT_SECRET_KEY: ""

nodeSelector: {}

tolerations: []

affinity: {}
```

## Validation Rules
All existing validation rules from previous phases remain unchanged:
- Task.title is required and limited to 255 characters
- Task.user_id must reference an existing user
- Message.role must be one of 'user', 'assistant', or 'system'
- Conversation.user_id must reference an existing user

## State Transitions
State transitions remain unchanged from Phase III:
- Task.is_completed can transition from False to True (completed) or True to False (uncompleted)
- All timestamp fields are automatically updated by the database

## Relationships
Entity relationships remain unchanged:
- User (1) : (Many) Task
- User (1) : (Many) Conversation
- Conversation (1) : (Many) Message
- Task and Message entities are isolated by user_id for data security