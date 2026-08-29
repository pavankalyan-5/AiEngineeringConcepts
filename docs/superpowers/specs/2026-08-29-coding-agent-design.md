# Coding agent (CLI, no frameworks)

Date: 2026-08-29  
Location: `3.AgentsIntro/coding_agent/`

## Goal

A small coding agent that uses the same pattern as `weather_app`: OpenAI SDK, JSON tool schemas, a name-to-function registry, and a turn loop. No LangChain, LangGraph, or other agent frameworks.

The user talks to it in the terminal. The model may only read and write files inside a sandbox folder.

## Out of scope

- Streamlit UI
- `list_files`, `edit_file`, shell / `run_command`
- Paths outside the sandbox
- Sharing packages with `weather_agent` (copy the client/loop pattern, do not import it)

## Layout

Mirror `weather_app/` (`app.py` next to a package):

```
3.AgentsIntro/coding_agent/
  app.py
  workspace/                 # created on startup if missing
  coding_agent/
    __init__.py
    config.py
    client.py
    schemas.py
    agent.py
    prompts.py
    prompts/system.jinja
    tools/
      __init__.py            # TOOL_FUNCTIONS registry
      read_file.py
      write_file.py
      paths.py               # resolve_work_path
```

Existing empty stubs at `coding_agent/tools/` and root `app.py` are replaced by this layout (tools move into the package).

Run from `3.AgentsIntro/coding_agent/`:

```bash
uv run python app.py
```

`PYTHONPATH` is the app root (current directory), same as weather. In `config.py`, call `load_dotenv` on the first `.env` found by walking from `coding_agent/` up to the repo root so keys in the existing root `.env` work when the CLI cwd is `3.AgentsIntro/coding_agent/`.

## Components

| Unit | Role | Depends on |
|---|---|---|
| `client.py` | Pick provider from env (`OPENAI_API_KEY` first, same `Provider` dataclass as weather). Return `OpenAI` client, model name, provider. | `openai`, dotenv |
| `config.py` | `WORKSPACE_DIR`, `PROMPTS_DIR`, `MAX_TURNS`, `MAX_TOKENS` | pathlib, os |
| `schemas.py` | `read_file` / `write_file` OpenAI function schemas; `TOOL_MENU`; `tool_catalog()` | — |
| `tools/paths.py` | Resolve a relative path under `WORKSPACE_DIR`; reject escape via `Path.resolve()` + `relative_to` | `config` |
| `tools/read_file.py` | Read UTF-8 text; return error strings (not raise) so the model can recover | `paths` |
| `tools/write_file.py` | Create/overwrite UTF-8; `mkdir` parents; return success or error string | `paths` |
| `tools/__init__.py` | `TOOL_FUNCTIONS = {"read_file": ..., "write_file": ...}` | tool modules |
| `prompts.py` + `system.jinja` | System prompt: coding assistant, use tools, stay in workspace, no markdown fences in `write_file` content | jinja2, `tool_catalog` |
| `agent.py` | `run_agent_turns(messages)` — copy weather loop; `tools=TOOL_MENU`; dispatch `TOOL_FUNCTIONS` | client, prompts, tools, schemas, config |
| `app.py` | REPL: intro, `You:` / `Agent:`, print `→ tool_name(args)` on each tool call, `quit`/`exit`/EOF | agent, client (fail fast if no key) |

## Data flow

1. User line appended as `{"role": "user", "content": ...}` to a session `messages` list.
2. `run_agent_turns` prepends a system message from Jinja and calls `chat.completions.create` with `tools=TOOL_MENU`.
3. If `message.tool_calls` is empty, append assistant content to `messages`, return it; CLI prints it.
4. Else append assistant tool-call message, run each function, append `role: tool` with `tool_call_id`, repeat until a final answer or `MAX_TURNS`.
5. Tool names from the model must match keys in `TOOL_FUNCTIONS`. Unknown names return `"Unknown tool: {name}"`.

JSON argument parsing matches weather: `json.loads` on `call.function.arguments` (string). If the SDK already returns a dict, accept both.

## Path sandbox

- `workspace/` is `Path(__file__).parent.parent / "workspace"` (next to `app.py`).
- `resolve_work_path(path)`:
  - reject empty path
  - `candidate = (WORKSPACE_DIR / path).resolve()`
  - `candidate.relative_to(WORKSPACE_DIR.resolve())` must succeed
- No extra blocked-filename list in v1 (sandbox already excludes the rest of the repo).

## CLI behavior

- Startup: ensure workspace exists; print provider/model; print that files live in `workspace/`.
- Commands: `quit`, `exit` (case-insensitive), Ctrl+D.
- Empty input: ignore and prompt again.
- One conversation per process (history kept in memory until exit).
- Optional `Clear` is not required in v1.

## Error handling

- Missing provider: `RuntimeError` at startup, print and exit non-zero.
- Tool I/O errors: string returned to the model (`File not found`, `Path escapes workspace`, write failures).
- API/network exceptions in the loop: catch in `app.py`, print the error, keep the REPL alive.
- `MAX_TURNS` exceeded: same fallback string as weather (`Stopped after hitting max_turns without a final answer`).

## Testing / verification

- Manual: `uv run python app.py`, ask to write `hello.py` with a function, then ask to read it back; confirm the file exists under `workspace/`.
- Manual: ask to read `../pyproject.toml` or `/etc/passwd`; agent should report a sandbox error, file must not be read.
- No automated test suite required for this lesson unless added later.

## Success criteria

- Same mental model as weather: schemas vs registry vs loop.
- Agent can create a file in `workspace/` and read it in a later turn in the same session.
- Agent cannot read or write outside `workspace/`.
