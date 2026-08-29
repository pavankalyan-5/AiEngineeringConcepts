import os
from pathlib import Path

from dotenv import load_dotenv

APP_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = APP_ROOT / "workspace"
PROMPTS_DIR = PACKAGE_DIR / "prompts"

MAX_TURNS = int(os.getenv("MAX_TURNS", "10"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))


def load_env() -> None:
    for directory in (APP_ROOT, *APP_ROOT.parents):
        candidate = directory / ".env"
        if candidate.is_file():
            load_dotenv(candidate)
            return
    load_dotenv()


def ensure_workspace() -> Path:
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    return WORKSPACE_DIR
