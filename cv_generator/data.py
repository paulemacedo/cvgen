from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import EXAMPLES_FOLDER_NAME
from .paths import DATA_DIR


def is_examples_path(profile_path: Path) -> bool:
    relative_parent = profile_path.parent.relative_to(DATA_DIR)
    return any(part.lower() == EXAMPLES_FOLDER_NAME.lower() for part in relative_parent.parts)


def discover_profile_files() -> list[Path]:
    json_files = sorted(DATA_DIR.rglob("*.json"))
    if not json_files:
        return []

    non_examples_files = [profile_path for profile_path in json_files if not is_examples_path(profile_path)]
    if non_examples_files:
        return non_examples_files

    return [profile_path for profile_path in json_files if is_examples_path(profile_path)]


def load_json_file(file_path: Path) -> dict[str, Any]:
    with file_path.open(encoding="utf-8") as file_handle:
        return json.load(file_handle)
