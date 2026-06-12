# AI Development Orchestration Review

## Background

I am a senior software engineer/SRE working primarily with:

- Python
- AWS
- Terraform
- Kubernetes
- Jenkins
- Serverless applications

I currently use:

- Claude Code
- OpenAI Codex
- Marvin

My goal is to determine the best way to orchestrate multiple AI coding agents.

---

## Discussion

### Question

What can Codex do that Claude Code cannot do, or does better?

### Findings

Codex strengths:

- Long-running autonomous work
- Parallel agents
- Bulk implementation
- Large-scale code migrations
- Automated PR review

Claude strengths:

- Architecture understanding
- Infrastructure reasoning
- Terraform reviews
- AWS design discussions
- Interactive pair programming

Proposed usage:

- Claude = Architect
- Codex = Implementer
- Marvin = Orchestrator

---

## Proposed Architecture

Marvin coordinates work.

Claude performs:

- Architecture reviews
- Security reviews
- Terraform reviews
- AWS reviews

Codex performs:

- Implementation
- Refactoring
- Test creation
- Documentation generation

---

## Initial Prototype

### tasks.yaml

```yaml
project: recipe-app

tasks:
  - id: architecture-review
    tool: claude
    goal: Review AWS architecture

  - id: implement-tests
    tool: codex
    goal: Add pytest coverage
```

### orchestrate.py

```python
from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path

import yaml
from pydantic import BaseModel

# Prototype orchestrator omitted for brevity
```

Concept:

1. Read YAML
2. Build prompt
3. Route to Claude or Codex
4. Save outputs
5. Track status

---

## Marvin Notes

Marvin appears to support:

- Tasks
- Agents
- Threads
- Structured outputs
- Planning

---

## Review Request

Please review this design.

### Questions

1. What are the biggest flaws?
2. What scalability issues exist?
3. How would you prevent agent collisions?
4. How would you persist state?
5. How would you support retries?
6. How would you support parallel execution?
7. How would you support multiple repositories?
8. What would you change before production use?
9. Is Marvin the correct orchestrator?
10. Should another framework be considered?

### Additional Critical Question

Why should I use Marvin instead of:

- Temporal
- Prefect
- Dagster
- Airflow
- A custom SQLite task queue
- A GitHub Issues + Worktree based workflow

Please compare:
- Complexity
- Reliability
- Cost
- Scalability
- Observability
- Multi-agent support
- Long-term maintainability

### Deliverables

Provide:

- Architecture critique
- Risk assessment
- Suggested directory structure
- Suggested data model
- Suggested task state machine
- Suggested MVP
- Suggested production architecture
- Recommended technology stack
