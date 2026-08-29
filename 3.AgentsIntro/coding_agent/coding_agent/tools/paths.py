from pathlib import Path

from coding_agent.config import WORKSPACE_DIR


def resolve_work_path(path: str, work_dir: Path | None = None) -> Path:
    if not path or not str(path).strip():
        raise ValueError("Path is required")

    root = (work_dir if work_dir is not None else WORKSPACE_DIR).resolve()
    candidate = Path(path)
    if candidate.is_absolute():
        resolved = candidate.resolve()
    else:
        resolved = (root / path).resolve()

    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("Path escapes workspace") from exc

    return resolved
