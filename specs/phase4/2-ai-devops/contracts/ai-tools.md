# AI DevOps Tools Interface Contract

**Date**: 2026-01-25
**Feature**: Phase IV Module 2 - AI-Powered DevOps

## Overview

This document defines the interface contracts for AI DevOps tools used in Phase IV Module 2.

## Tool: kubectl-ai

### Installation

```bash
npm install -g kubectl-ai
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for AI processing |
| `KUBECTL_AI_MODEL` | No | Model to use (default: gpt-3.5-turbo) |

### Command Interface

```bash
kubectl-ai "<natural-language-query>" [options]
```

#### Options

| Option | Description |
|--------|-------------|
| `--yes` / `-y` | Auto-confirm execution |
| `--dry-run` | Show command without executing |
| `--namespace <ns>` | Target namespace |

### Input/Output Contract

**Input**: Natural language string describing desired Kubernetes operation

**Output**:
1. Generated kubectl command (displayed to user)
2. Confirmation prompt (unless --yes)
3. Command execution result

### Supported Operations

| Operation | Example Input | Generated Command |
|-----------|---------------|-------------------|
| List pods | "show all pods" | `kubectl get pods` |
| Scale deployment | "scale backend to 3" | `kubectl scale deployment backend --replicas=3` |
| Get logs | "check backend logs" | `kubectl logs -l app=backend` |
| Describe resource | "describe frontend service" | `kubectl describe service frontend` |
| Delete resource | "delete failed pods" | `kubectl delete pods --field-selector=status.phase=Failed` |
| Get resource usage | "show resource usage" | `kubectl top pods` |

### Error Handling

| Error | Response |
|-------|----------|
| Invalid API key | "Error: Invalid OpenAI API key" |
| No kubectl context | "Error: No Kubernetes context configured" |
| Rate limit | "Error: Rate limit exceeded, please wait" |
| Unknown intent | "I couldn't understand that request. Try rephrasing." |

---

## Tool: kagent

### Installation

```bash
pip install kagent
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for AI processing |
| `KUBECONFIG` | No | Path to kubeconfig (default: ~/.kube/config) |

### Command Interface

```bash
kagent "<analysis-query>" [options]
```

#### Options

| Option | Description |
|--------|-------------|
| `--output <format>` | Output format (text, json, yaml) |
| `--namespace <ns>` | Target namespace |
| `--verbose` | Detailed output |

### Input/Output Contract

**Input**: Natural language query about cluster analysis or optimization

**Output**:
1. Analysis results
2. Recommendations (if applicable)
3. Severity indicators

### Analysis Operations

| Operation | Example Input | Output Type |
|-----------|---------------|-------------|
| Health check | "analyze cluster health" | Health report with status indicators |
| Resource optimization | "optimize resources" | Recommendations with before/after comparisons |
| Performance analysis | "find performance issues" | List of issues with severity |
| Best practices | "suggest improvements" | Prioritized recommendation list |
| Security audit | "check security issues" | Security findings with risk levels |

### Output Format

```json
{
  "analysis_type": "health_check",
  "timestamp": "2026-01-25T12:00:00Z",
  "cluster": "minikube",
  "summary": "Cluster is healthy with minor optimization opportunities",
  "findings": [
    {
      "category": "resources",
      "severity": "info",
      "message": "Backend deployment could benefit from resource limits",
      "recommendation": "Add memory limit of 512Mi"
    }
  ],
  "score": 85
}
```

### Error Handling

| Error | Response |
|-------|----------|
| Invalid API key | "Error: OpenAI API key not configured or invalid" |
| Cluster unreachable | "Error: Cannot connect to Kubernetes cluster" |
| Insufficient permissions | "Error: Insufficient RBAC permissions for analysis" |

---

## Tool: Gordon (Docker AI)

### Prerequisites

- Docker Desktop 4.53+
- Docker AI feature enabled in settings

### Command Interface

```bash
docker ai "<query>" [options]
```

### Supported Operations

| Operation | Example Input |
|-----------|---------------|
| Capability info | "What can you do?" |
| Build assistance | "build my images" |
| Run guidance | "run my containers" |
| Debug help | "help me debug this container" |

### Output Format

Natural language responses with:
- Explanations
- Suggested commands
- Step-by-step guidance

---

## Integration Requirements

### Prerequisites Verification

Before using any AI tool, verify:

```bash
# 1. OpenAI API key set
test -n "$OPENAI_API_KEY" && echo "API key configured" || echo "Missing API key"

# 2. Kubernetes cluster accessible
kubectl cluster-info

# 3. Todo app deployed
kubectl get deployments
```

### Tool Interaction Flow

```
┌─────────────────────────────────────────────────────────┐
│                  User Natural Language                   │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  AI Tool (kubectl-ai / kagent)          │
│  - Parse natural language                               │
│  - Generate kubectl/analysis command                    │
│  - Execute or analyze                                   │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Kubernetes Cluster (Minikube)          │
│  - Execute kubectl commands                             │
│  - Return results                                       │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  User-Friendly Response                 │
│  - Formatted output                                     │
│  - Recommendations                                      │
│  - Next steps                                           │
└─────────────────────────────────────────────────────────┘
```

### Rate Limiting

| Tool | Rate Limit | Mitigation |
|------|------------|------------|
| kubectl-ai | OpenAI tier limits | Space commands 1-2 seconds apart |
| kagent | OpenAI tier limits | Cache analysis results |
| Gordon | Docker Desktop limits | Use sparingly |

---

## Verification Commands

### kubectl-ai Verification

```bash
# Should display kubectl get pods output
kubectl-ai "show me all pods"
```

### kagent Verification

```bash
# Should display cluster health analysis
kagent "cluster health"
```

### Gordon Verification

```bash
# Should list capabilities
docker ai "What can you do?"
```
