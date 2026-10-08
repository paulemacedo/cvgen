from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import ARCHIVE_FOLDER_NAME, AVAILABLE_TEMPLATES, EXAMPLES_FOLDER_NAME
from .paths import DATA_DIR


def is_examples_path(profile_path: Path) -> bool:
    relative_parent = profile_path.parent.relative_to(DATA_DIR)
    return any(part.lower() == EXAMPLES_FOLDER_NAME.lower() for part in relative_parent.parts)


def is_archive_path(profile_path: Path) -> bool:
    relative_parent = profile_path.parent.relative_to(DATA_DIR)
    return any(part.lower() == ARCHIVE_FOLDER_NAME.lower() for part in relative_parent.parts)


def discover_profile_files() -> list[Path]:
    json_files = sorted(DATA_DIR.rglob("*.json"))
    if not json_files:
        return []

    non_examples_files = [profile_path for profile_path in json_files if not is_examples_path(profile_path) and not is_archive_path(profile_path)]
    if non_examples_files:
        return non_examples_files

    return [profile_path for profile_path in json_files if is_examples_path(profile_path)]


def load_json_file(file_path: Path) -> dict[str, Any]:
    with file_path.open(encoding="utf-8") as file_handle:
        return json.load(file_handle)


def resolve_profile_templates(
    profile: dict[str, Any],
    requested_templates: list[str],
    explicit_template_request: bool,
) -> list[str]:
    if explicit_template_request or "template" not in profile:
        return requested_templates

    configured_template = profile["template"]
    if not isinstance(configured_template, str):
        raise ValueError("The 'template' field must be a string.")

    template_name = configured_template.strip().lower()
    if template_name not in AVAILABLE_TEMPLATES:
        raise ValueError(
            f"Template '{configured_template}' from profile is not available. "
            f"Available: {', '.join(AVAILABLE_TEMPLATES)}"
        )

    return [template_name]
