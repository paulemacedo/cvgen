from src.cli import main, parse_cli_arguments
from src.config import (
    AVAILABLE_LANGUAGES,
    AVAILABLE_TEMPLATES,
    DEFAULT_CONTACT,
    DEFAULT_LABELS,
    DEFAULT_TEMPLATE,
)
from src.generator import generate_cv_files
from src.prepare import render_profile

__all__ = [
    "AVAILABLE_LANGUAGES",
    "AVAILABLE_TEMPLATES",
    "DEFAULT_CONTACT",
    "DEFAULT_LABELS",
    "DEFAULT_TEMPLATE",
    "parse_cli_arguments",
    "generate_cv_files",
    "render_profile",
    "main",
]


if __name__ == "__main__":
    main()
