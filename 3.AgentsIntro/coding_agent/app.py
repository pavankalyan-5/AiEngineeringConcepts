from coding_agent.agent import run_agent_turns
from coding_agent.client import get_client_and_model
from coding_agent.config import WORKSPACE_DIR, ensure_workspace


def _print_tool(name: str, arguments: dict) -> None:
    preview = ", ".join(f"{key}={value!r}" for key, value in arguments.items())
    if len(preview) > 160:
        preview = preview[:157] + "..."
    print(f"  → {name}({preview})")


def main() -> None:
    try:
        _, model, provider = get_client_and_model()
    except RuntimeError as err:
        print(err)
        raise SystemExit(1) from err

    workspace = ensure_workspace()
    print(f"Coding agent ({provider.name}, {model})")
    print(f"Files are sandboxed to: {workspace}")
    print("Type quit or exit to stop.\n")

    messages: list[dict] = []

    while True:
        try:
            user_text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_text:
            continue
        if user_text.lower() in {"quit", "exit"}:
            break

        messages.append({"role": "user", "content": user_text})
        try:
            answer = run_agent_turns(messages, on_tool_call=_print_tool)
        except Exception as err:
            print(f"Error: {err}")
            messages.pop()
            continue

        print(f"Agent: {answer}\n")


if __name__ == "__main__":
    main()
