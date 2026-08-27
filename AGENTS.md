# AGENTS.md

## Project scope

This repository is intentionally a minimal LangGraph agent scaffold. Keep the default runtime free of tools, sandboxes, persistence, databases, MCP, subagents, HTTP services, and frontend code unless the project owner explicitly asks to add one of them.

## Architecture

- `src/agent_harness/config.py` reads model configuration from environment variables.
- `src/agent_harness/agent.py` builds a single-node LangGraph graph.
- `src/agent_harness/cli.py` owns the process-local conversation loop.
- `tests/` contains offline tests and must never call a real model API.

## Commands

```powershell
uv sync
uv run agent-harness
uv run pytest
```

Add or update tests with every behavior change. Keep `README.md` synchronized with user-facing changes and this file synchronized with architecture or workflow changes.
