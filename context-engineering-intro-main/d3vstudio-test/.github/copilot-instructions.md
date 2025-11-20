# Copilot / AI assistant instructions — Context Engineering Intro

This file gives focused, actionable guidance so an AI coding assistant can be productive immediately in this repo.

Key goals
- Understand the template-based PRP workflow (INITIAL.md → PRP → execute) and follow `CLAUDE.md` rules.
- Use existing examples and templates under `use-cases/` and `pydantic-ai/examples/` as canonical patterns.

Big-picture architecture (where to look)
- Python agent factory and Pydantic AI patterns: `use-cases/pydantic-ai/` — see `README.md`, `CLAUDE.md`, and `examples/main_agent_reference/` (look at `settings.py`, `providers.py`, `agent.py`).
- Agent factory / subagents orchestration: `use-cases/agent-factory-with-subagents/` — see `CLAUDE.md` and `agents/rag_agent/` for a full RAG example.
- MCP server (Node/TypeScript) templates: `use-cases/mcp-server/` — key files: `src/index.ts`, `src/github-handler.ts`, `wrangler.jsonc`, `.claude/commands/prp-mcp-*`.

Concrete developer workflows & commands
- Python environment (this repo prefers UV):
  - Create venv and run: `uv venv` then `uv sync` / `uv run pytest` / `uv run ruff format .` / `uv run mypy src/`.
  - Use `uv add` to add packages instead of editing pyproject directly.
- Node / MCP work: `npm install`, `wrangler dev` (local), `wrangler deploy` (production). Use `npm run dev` and `npm run type-check` when present.
- Tests/format: Python: `uv run pytest`, `uv run ruff format .`; TypeScript: `npm run dev`, `npx vitest`, `npx tsc --noEmit`.

Project-specific conventions (must follow)
- File size: avoid files > 500 lines. Functions < 50 lines, classes < 100 lines.
- Style: Python: PEP8 with line length 100, double quotes preferred, Google-style docstrings. Use type hints and `pydantic` v2 for models/settings.
- Config: Use `python-dotenv`/`.env` and `load_dotenv()`; never hardcode secrets (use `.env.example`).
- Naming: snake_case for variables/functions, PascalCase for classes, UPPER_SNAKE_CASE for constants.

AI/agent-specific rules (enforced by CLAUDE.md)
- Always start PRP-style work by reading `INITIAL.md` and `CLAUDE.md` in the relevant use-case folder.
- PRP workflow: generate PRP from `INITIAL.md` (`/generate-prp` or repo-specific `/generate-pydantic-ai-prp`) then `/execute-prp` — include planning, prompts.md, tools.md, dependencies.md under `agents/<name>/planning/`.
- Subagents Phase 2: invoke the three planning subagents (prompt-engineer, tool-integrator, dependency-manager) in a single parallel call — do not sequence them.
- When building an agent, follow the agent folder scaffold exactly: `agent.py`, `tools.py`, `prompts.py`, `settings.py`, `providers.py`, `dependencies.py`, `requirements.txt`, `.env.example`, `README.md`, `tests/`.

Integration & example references (use these as templates)
- RAG agent example: `use-cases/agent-factory-with-subagents/agents/rag_agent/` — shows ingestion, cli, providers, SQL and testing patterns.
- Pydantic AI canonical patterns: `use-cases/pydantic-ai/examples/main_agent_reference/` (settings, providers, dependency patterns).
- MCP server example: `use-cases/mcp-server/src/index.ts` and `examples/database-tools.ts` for tool registration and auth patterns.

> Safety for AI actions
- Never invent external APIs or package names. If a required integration is missing, surface it as a TODO in `TASK.md` or `PRPs/` and ask the user.
- Never commit secrets; write `.env.example` and instruct the user to populate `.env`.

If you change code
- Update the agent's `README.md` and the top-level `README.md` when adding or changing public behavior or developer steps.
- Add/adjust tests in the agent's `tests/` folder and run `uv run pytest` (python) or `npx vitest` (TS) until green.

When uncertain, ask (examples of clarifying questions)
- "Should I create the agent under `agents/<snake_case_name>/` or a different folder?"
- "Which LLM provider and model should I wire up in `providers.py` (env var names are `LLM_PROVIDER`, `LLM_API_KEY`)?"

Feedback
- If any section is unclear or you'd like additional examples (e.g., a minimal agent skeleton or MCP tool example), tell me which area to expand and I will iterate.
