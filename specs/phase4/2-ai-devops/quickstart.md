# Quickstart: Phase IV Module 2 - AI-Powered DevOps

**Prerequisites**: Phase IV Module 1 complete (Todo app running on Minikube)

## Prerequisites Check

Before starting, verify Module 1 is operational:

```bash
# Check Minikube status
minikube status

# Expected output:
# minikube
# type: Control Plane
# host: Running
# kubelet: Running
# apiserver: Running

# Check kubectl connectivity
kubectl get nodes

# Check Todo app deployment
kubectl get pods
kubectl get services
```

## Step 1: OpenAI API Key Configuration

All AI tools require an OpenAI API key:

```bash
# Set environment variable (add to ~/.bashrc or ~/.zshrc for persistence)
export OPENAI_API_KEY="sk-your-api-key-here"

# Verify it's set
echo $OPENAI_API_KEY
```

**Getting an API Key**:
1. Go to https://platform.openai.com/api-keys
2. Create a new secret key
3. Copy and set as environment variable

## Step 2: Install kubectl-ai

```bash
# Install globally via npm
npm install -g kubectl-ai

# Verify installation
kubectl-ai --version

# Test with a simple command
kubectl-ai "show me all pods"
```

**Expected Behavior**:
- kubectl-ai will translate your natural language to kubectl commands
- It shows the generated command before execution
- Press 'y' to confirm execution

## Step 3: Test kubectl-ai Operations

Run at least 5 different natural language commands:

```bash
# 1. List all running pods
kubectl-ai "list all running pods"

# 2. Scale backend deployment
kubectl-ai "scale backend to 3 replicas"

# 3. Check pod logs for errors
kubectl-ai "check pod logs for errors"

# 4. Describe frontend service
kubectl-ai "describe the frontend service"

# 5. Show resource usage
kubectl-ai "show resource usage"

# 6. Diagnose issues (if any)
kubectl-ai "why are my pods failing?"

# 7. Delete failed pods (if any exist)
kubectl-ai "delete failed pods"
```

## Step 4: Install kagent

```bash
# Install via pip
pip install kagent

# Verify installation
kagent --help

# Test basic functionality
kagent "analyze my cluster"
```

## Step 5: Test kagent Operations

```bash
# 1. Analyze cluster health
kagent "analyze cluster health"

# 2. Optimize resource allocation
kagent "optimize resource allocation"

# 3. Find performance issues
kagent "find performance issues"

# 4. Get best practices suggestions
kagent "suggest best practices"

# 5. Check for security issues
kagent "check for security issues"
```

## Step 6: Install Gordon (Optional)

Gordon requires Docker Desktop 4.53+:

1. **Check Docker Desktop Version**:
   ```bash
   docker version
   ```

2. **Enable Gordon**:
   - Open Docker Desktop
   - Go to Settings > Features in development
   - Enable "Docker AI" or "Gordon"
   - Apply & Restart

3. **Test Gordon**:
   ```bash
   docker ai "What can you do?"
   docker ai "build and run my images"
   ```

## Step 7: Verify App Functionality

After running AI operations, verify the Todo app still works:

```bash
# Get frontend URL
minikube service frontend --url

# Or use port-forward
kubectl port-forward svc/frontend 3000:3000
```

Open browser and test:
- Create a task
- View task list
- Update a task
- Toggle task status
- Delete a task
- Test AI chat functionality

## Step 8: Record Demo Video

Record a 90-second demo showing:

| Segment | Duration | What to Show |
|---------|----------|--------------|
| kubectl-ai scaling | 15s | Scale backend to 3 replicas |
| kubectl-ai logs | 10s | Check logs of frontend pods |
| kagent analysis | 15s | Analyze cluster health |
| App verification | 20s | Todo app working in browser |
| Minikube dashboard | 10s | `minikube dashboard` view |
| Gordon demo | 20s | (Optional) Gordon capabilities |

**Recording Tips**:
1. Use OBS Studio, QuickTime, or similar
2. Set terminal font size to be readable
3. Pre-type long commands to avoid typos
4. Keep narration brief and clear

## Troubleshooting

### kubectl-ai not found

```bash
# Check npm global installation
npm list -g kubectl-ai

# Reinstall if needed
npm uninstall -g kubectl-ai
npm install -g kubectl-ai
```

### kagent connection error

```bash
# Verify kubectl context
kubectl config current-context

# Ensure OPENAI_API_KEY is set
echo $OPENAI_API_KEY
```

### OpenAI API rate limit

```bash
# Wait 60 seconds and retry
sleep 60
kubectl-ai "show me all pods"
```

### Minikube not running

```bash
# Start Minikube
minikube start

# Verify
minikube status
```

## Success Checklist

- [ ] OpenAI API key configured
- [ ] kubectl-ai installed and working
- [ ] 5+ kubectl-ai commands executed successfully
- [ ] kagent installed and working
- [ ] Cluster analysis completed
- [ ] Gordon tested (optional)
- [ ] Todo app verified functional
- [ ] Demo video recorded (≤90 seconds)

## Completion

When all items are checked, Phase IV Module 2 is complete!

Run the following to verify everything:

```bash
# Final verification commands
kubectl-ai "show me all pods"
kagent "cluster health summary"
minikube status
```

**Phase IV Complete!** You have successfully:
1. Deployed the Todo app to Kubernetes (Module 1)
2. Managed the cluster using AI-powered tools (Module 2)
