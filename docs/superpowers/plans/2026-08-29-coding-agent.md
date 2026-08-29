# Coding Agent CLI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a no-framework CLI coding agent under `3.AgentsIntro/coding_agent/` that can read and write files only inside `workspace/`, using the same OpenAI tool-loop pattern as `weather_app`.

**Architecture:** Nested `coding_agent` package beside `app.py`. JSON tool schemas + `TOOL_FUNCTIONS` registry + `run_agent_turns`. Paths resolved with `Path.resolve()` and `relative_to(workspace)`.

**Tech Stack:** Python 3.12+, OpenAI SDK, python-dotenv, Jinja2, unittest.

**Spec:** `docs/superpowers/specs/2026-08-29-coding-agent-design.md`

## Global Constraints

- No LangChain / LangGraph
- Tools: `read_file`, `write_file` only
- Sandbox: `3.AgentsIntro/coding_agent/workspace/`
- Same fallback string as weather: `Stopped after hitting max_turns without a final answer`
- Load `.env` by walking from the app root up to the repo root
- Do not import `weather_agent`

## File map

- Create: `3.AgentsIntro/coding_agent/coding_agent/` package files listed in the spec
- Create: `3.AgentsIntro/coding_agent/tests/test_paths.py`, `test_files.py`
- Create: `3.AgentsIntro/coding_agent/workspace/.gitkeep`
- Modify: `3.AgentsIntro/coding_agent/app.py` (CLI)
- Delete: empty stubs at `3.AgentsIntro/coding_agent/tools/`

---

### Task 1: Path sandbox

**Files:**
- Create: `3.AgentsIntro/coding_agent/coding_agent/config.py`
- Create: `3.AgentsIntro/coding_agent/coding_agent/tools/paths.py`
- Test: `3.AgentsIntro/coding_agent/tests/test_paths.py`

**Interfaces:**
- Produces: `APP_ROOT`, `WORKSPACE_DIR`, `ensure_workspace()`, `load_env()`, `resolve_work_path(path: str, work_dir: Path | None = None) -> Path` (raises `ValueError`)

- [ ] Tests then `resolve_work_path` (empty path, `../` escape, nested relative OK)

### Task 2: read_file / write_file + registry

**Files:**
- Create: `tools/read_file.py`, `write_file.py`, `tools/__init__.py`
- Test: `tests/test_files.py`

**Interfaces:**
- Produces: `read_file(path: str) -> str`, `write_file(path: str, content: str) -> str`, `TOOL_FUNCTIONS: dict[str, callable]`

### Task 3: Schemas, prompts, client, agent, CLI

**Files:**
- Create: `schemas.py`, `prompts.py`, `prompts/system.jinja`, `client.py`, `agent.py`, `__init__.py`, `app.py`

**Interfaces:**
- Produces: `TOOL_MENU`, `tool_catalog()`, `build_system_prompt()`, `get_client_and_model()`, `run_agent_turns(messages, max_turns=..., on_tool_call=None) -> str`

- [ ] `parse_tool_arguments` accepts str or dict
- [ ] REPL: quit/exit/EOF, print `→ name(args)`, catch API errors
- [ ] Delete leftover top-level `tools/` stubs

### Task 4: Verify

- [ ] `uv run python -m unittest discover -s tests` from `3.AgentsIntro/coding_agent`
- [ ] Import `app` / `run_agent_turns` without calling the API
