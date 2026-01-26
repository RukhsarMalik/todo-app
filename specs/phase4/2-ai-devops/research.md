# Research: Phase IV Module 2 - AI-Powered DevOps

**Date**: 2026-01-25
**Feature**: AI-Powered DevOps Tools
**Status**: Complete

## Research Questions

### RQ-1: kubectl-ai Installation and Configuration

**Question**: How do we install and configure kubectl-ai for natural language Kubernetes commands?

**Decision**: Install kubectl-ai globally via npm with OpenAI API key configuration.

**Findings**:

1. **Installation Method**:
   ```bash
   npm install -g kubectl-ai
   ```

2. **Configuration**:
   - Requires OpenAI API key set as environment variable
   - Environment variable: `OPENAI_API_KEY`
   - Optionally configure model: `KUBECTL_AI_MODEL=gpt-4` (defaults to gpt-3.5-turbo)

3. **Basic Usage Pattern**:
   ```bash
   kubectl-ai "natural language command"
   ```

4. **How It Works**:
   - Translates natural language to kubectl commands
   - Shows the generated command before execution
   - Asks for confirmation before executing (safety feature)
   - Can be configured for auto-execution with `--yes` flag

**Alternatives Considered**:
- `k8sgpt`: Alternative AI tool but requires different setup
- Manual kubectl: Works but lacks natural language interface
- ChatGPT direct: Requires copy-paste, no direct execution

**Rationale**: kubectl-ai is the most straightforward option with npm installation and direct kubectl integration. It's specifically designed for Kubernetes natural language commands.

---

### RQ-2: kubectl-ai Command Patterns

**Question**: What natural language patterns work best with kubectl-ai?

**Decision**: Use clear, action-oriented phrases that map to kubectl operations.

**Findings**:

| Natural Language | kubectl Equivalent |
|-----------------|-------------------|
| "show me all pods" | `kubectl get pods` |
| "list all running pods" | `kubectl get pods --field-selector=status.phase=Running` |
| "scale backend to 3 replicas" | `kubectl scale deployment backend --replicas=3` |
| "check pod logs for errors" | `kubectl logs <pod> | grep -i error` |
| "describe the frontend service" | `kubectl describe service frontend` |
| "why are my pods failing?" | `kubectl describe pod <failing-pod>` + event analysis |
| "show resource usage" | `kubectl top pods` |
| "delete failed pods" | `kubectl delete pods --field-selector=status.phase=Failed` |

**Best Practices**:
- Be specific about resource names when possible
- Include namespace if not using default
- Use action verbs (show, list, scale, check, describe, delete)

---

### RQ-3: kagent Installation and Capabilities

**Question**: How do we install kagent and what capabilities does it provide?

**Decision**: Install kagent via pip for advanced cluster analysis.

**Findings**:

1. **Installation**:
   ```bash
   pip install kagent
   ```

2. **Configuration**:
   - Requires OpenAI API key: `OPENAI_API_KEY`
   - Uses existing kubectl context
   - No additional Kubernetes permissions needed beyond kubectl

3. **Capabilities**:
   - **Cluster Health Analysis**: Evaluates overall cluster state
   - **Resource Optimization**: Suggests resource limit adjustments
   - **Performance Analysis**: Identifies bottlenecks
   - **Best Practices**: Recommends configuration improvements
   - **Troubleshooting**: Diagnoses pod failures and issues

4. **Usage Patterns**:
   ```bash
   kagent "analyze my cluster"
   kagent "check for security issues"
   kagent "optimize my deployments"
   kagent "suggest improvements"
   kagent "why is my pod crashing?"
   ```

**Alternatives Considered**:
- `k8sgpt`: Similar capabilities but different interface
- Manual analysis: Time-consuming and requires expertise
- Prometheus/Grafana: Requires additional setup for monitoring

**Rationale**: kagent provides deeper analysis than kubectl-ai, complementing it for cluster insights and optimization recommendations.

---

### RQ-4: Docker AI (Gordon) Integration

**Question**: How do we enable and use Docker AI (Gordon)?

**Decision**: Optional feature requiring Docker Desktop 4.53+.

**Findings**:

1. **Prerequisites**:
   - Docker Desktop version 4.53 or higher
   - Docker Desktop Pro, Team, or Business subscription (feature may require paid tier)

2. **Enabling Gordon**:
   - Open Docker Desktop Settings
   - Navigate to Features in development or Beta features
   - Enable "Docker AI" or "Gordon" option
   - Restart Docker Desktop

3. **Usage**:
   ```bash
   docker ai "What can you do?"
   docker ai "build my images"
   docker ai "show running containers"
   docker ai "help me debug my container"
   ```

4. **Capabilities**:
   - Docker command generation
   - Dockerfile assistance
   - Container debugging
   - Image optimization suggestions

**Note**: Gordon is marked as OPTIONAL because:
- Requires specific Docker Desktop version
- May require paid subscription
- Not essential for Kubernetes operations (kubectl-ai covers that)

---

### RQ-5: OpenAI API Configuration

**Question**: What OpenAI API setup is required for these tools?

**Decision**: Use single OpenAI API key for all tools.

**Findings**:

1. **API Key Setup**:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

2. **Shared Configuration**:
   - Both kubectl-ai and kagent use the same `OPENAI_API_KEY` environment variable
   - No separate configurations needed
   - API key must have chat completions access

3. **Cost Considerations**:
   - Each command incurs API costs
   - Commands typically use gpt-3.5-turbo by default (lower cost)
   - Complex analysis may use gpt-4 (higher cost)
   - Expected usage: ~$0.01-0.05 per command

4. **Rate Limits**:
   - Standard OpenAI rate limits apply
   - For demo purposes, unlikely to hit limits
   - If rate limited, wait and retry

---

### RQ-6: Demo Video Requirements

**Question**: What should the demo video include and how should it be structured?

**Decision**: 90-second video with 6 segments as specified.

**Findings**:

| Segment | Duration | Content |
|---------|----------|---------|
| 1. kubectl-ai scaling | 15s | `kubectl-ai "scale backend to 3 replicas"` |
| 2. kubectl-ai logs | 10s | `kubectl-ai "check logs of frontend pods"` |
| 3. kagent analysis | 15s | `kagent "analyze cluster health"` |
| 4. App verification | 20s | Browser showing Todo app working |
| 5. Minikube dashboard | 10s | `minikube dashboard` view |
| 6. Gordon demo (optional) | 20s | `docker ai "What can you do?"` |

**Recording Tips**:
- Use screen recording tool (OBS, QuickTime, etc.)
- Pre-type commands to avoid typos
- Ensure terminal font is readable
- Show command and result clearly
- Keep narration concise

---

## Summary

| Tool | Installation | Purpose | Required |
|------|-------------|---------|----------|
| kubectl-ai | `npm install -g kubectl-ai` | Natural language kubectl | Yes |
| kagent | `pip install kagent` | Cluster analysis | Yes |
| Gordon | Docker Desktop 4.53+ | Docker AI | Optional |

**Environment Variables Required**:
```bash
export OPENAI_API_KEY="sk-..."
```

**Prerequisites from Module 1**:
- Minikube cluster running
- Todo app deployed
- kubectl configured
- Helm charts installed

All research questions resolved. Ready for Phase 1 design.
