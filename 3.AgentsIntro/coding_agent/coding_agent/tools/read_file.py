from coding_agent.tools.paths import resolve_work_path


def read_file(path: str) -> str:
    try:
        file_path = resolve_work_path(path)
    except ValueError as err:
        return f"Error: {err}"

    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"Error: File not found: {path}"
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except OSError as err:
        return f"Error: Failed to read {path!r}: {err}"
