from coding_agent.tools.paths import resolve_work_path


def write_file(path: str, content: str) -> str:
    if not path:
        return "Error: Path is required"

    try:
        file_path = resolve_work_path(path)
    except ValueError as err:
        return f"Error: {err}"

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
    except OSError as err:
        return f"Error: Failed to write file {path!r}: {err}"

    return f"File {path!r} written successfully"
