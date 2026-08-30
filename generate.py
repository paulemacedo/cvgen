from cv_generator.cli import main, parse_cli_arguments
from cv_generator.config import (
    AVAILABLE_LANGUAGES,
    AVAILABLE_TEMPLATES,
    DEFAULT_CONTACT,
    DEFAULT_LABELS,
    DEFAULT_TEMPLATE,
)
from cv_generator.generator import generate_cv_files
from cv_generator.prepare import render_profile

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
