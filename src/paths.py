from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Any

from .config import LANGUAGE_CODE_MAP, OUTPUT_HTML_DIR_NAME, TEMPLATE_CSS_FILES

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = WORKSPACE_ROOT / "data"
TEMPLATES_DIR = WORKSPACE_ROOT / "templates"
OUTPUT_DIR = WORKSPACE_ROOT / "output"
HTML_OUTPUT_DIR = OUTPUT_DIR / OUTPUT_HTML_DIR_NAME


def resolve_topic_output_dir(profile_path: Path) -> Path:
    relative_parent = profile_path.parent.relative_to(DATA_DIR)
    return OUTPUT_DIR.joinpath(*relative_parent.parts)


def get_html_output_dir_for_profile(profile_path: Path) -> Path:
    """Return profile-specific subdirectory for HTML output organization."""
    profile_name = profile_path.stem.lower()
    return HTML_OUTPUT_DIR / profile_name


def get_template_css_filename(template_name: str) -> str:
    return TEMPLATE_CSS_FILES.get(template_name.lower(), f"{template_name}.css")


def slugify_filename_part(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", ascii_value).strip("-")
    return re.sub(r"-+", "-", cleaned)


def format_area_name(raw_stem: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", " ", raw_stem).strip()
    if not normalized:
        return "Area"

    tokens = normalized.split()
    formatted_tokens = [token if token.isupper() else token.capitalize() for token in tokens]
    return "-".join(formatted_tokens)


def build_output_basename(profile: dict[str, Any], profile_path: Path, language: str) -> str:
    from .localization import localize_text

    localized_name = localize_text(profile.get("name", profile.get("nome", "")), language)
    name_part = slugify_filename_part(localized_name) or "Sem-Nome"
    area_part = slugify_filename_part(format_area_name(profile_path.stem)) or "Area"
    language_part = LANGUAGE_CODE_MAP.get(language, language.upper())
    return f"CV-{name_part}-{area_part}-{language_part}"


def build_html_output_filename(profile_path: Path, basename: str) -> str:
    relative_parent = profile_path.parent.relative_to(DATA_DIR)
    if not relative_parent.parts:
        return basename

    topic_prefix = "-".join(slugify_filename_part(format_area_name(part)) for part in relative_parent.parts)
    return f"{topic_prefix}-{basename}" if topic_prefix else basename
