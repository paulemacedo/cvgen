from __future__ import annotations

import argparse
import sys

from .config import AVAILABLE_LANGUAGES, AVAILABLE_TEMPLATES, DEFAULT_TEMPLATE
from .data import discover_profile_files, load_json_file


def parse_cli_arguments(arguments: list[str]) -> tuple[list[str], list[str], bool]:
    explicit_language_request = bool(arguments) and arguments[0] != "all"
    requested_languages = AVAILABLE_LANGUAGES if not arguments or arguments[0] == "all" else [arguments[0]]

    if len(arguments) > 1:
        selected_templates = AVAILABLE_TEMPLATES if arguments[1] == "all" else [arguments[1]]
    else:
        selected_templates = [DEFAULT_TEMPLATE]

    invalid_templates = [template_name for template_name in selected_templates if template_name not in AVAILABLE_TEMPLATES]
    if invalid_templates:
        print(
            f"Template(s) not found: {', '.join(invalid_templates)}. "
            f"Available: {', '.join(AVAILABLE_TEMPLATES)}"
        )
        sys.exit(1)

    invalid_languages = [language for language in requested_languages if language not in AVAILABLE_LANGUAGES]
    if invalid_languages:
        print(
            f"Language(s) not found: {', '.join(invalid_languages)}. "
            f"Available: {', '.join(AVAILABLE_LANGUAGES)}"
        )
        sys.exit(1)

    return requested_languages, selected_templates, explicit_language_request


def _resolve_profile_paths(profile_name: str | None) -> list:
    all_profiles = discover_profile_files()
    if not profile_name or profile_name.lower() == "all":
        return all_profiles

    target = profile_name.lower().strip()
    matches = [profile for profile in all_profiles if target in profile.stem.lower() or profile.stem.lower() == target]
    if not matches:
        raise ValueError(f"Profile '{profile_name}' not found in data folder.")
    return matches


def _run_generate_command(args: argparse.Namespace) -> None:
    from .generator import run_generation

    requested_languages = AVAILABLE_LANGUAGES if args.language == "all" else [args.language]
    template_names = AVAILABLE_TEMPLATES if args.template == "all" else [args.template]
    selected_profiles = _resolve_profile_paths(args.profile)

    for profile_path in selected_profiles:
        if args.profile.lower() == "all":
            profile_files = selected_profiles
        else:
            profile_files = [profile_path]
        for current_profile in profile_files:
            from .generator import generate_cv_files

            generate_cv_files(
                current_profile,
                requested_languages,
                template_names,
                explicit_language_request=False,
                include_pdf=args.format == "pdf",
            )

    if args.profile.lower() != "all":
        return

    run_generation(requested_languages, template_names, explicit_language_request=False, include_pdf=args.format == "pdf")


def _list_templates(_: argparse.Namespace) -> None:
    print("Available templates:")
    for template_name in AVAILABLE_TEMPLATES:
        print(f"  - {template_name}")


def _list_profiles(_: argparse.Namespace) -> None:
    profiles = [path.stem for path in discover_profile_files()]
    print("Available profiles:")
    for profile_name in profiles:
        print(f"  - {profile_name}")


def _validate_profiles(_: argparse.Namespace) -> None:
    errors: list[str] = []
    for profile_path in discover_profile_files():
        try:
            load_json_file(profile_path)
        except Exception as exception:  # pragma: no cover - CLI validation feedback
            errors.append(f"{profile_path.name}: {exception}")

    if errors:
        print("Profile validation failed:")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)

    print(f"Validated {len(discover_profile_files())} profile(s).")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CV Generator CLI")

    parser.add_argument("-p", "--profile", default="all", help="Profile name or 'all'")
    parser.add_argument("-t", "--template", default="all", choices=["all", *AVAILABLE_TEMPLATES], help="Template to use")
    parser.add_argument("-l", "--language", default="all", choices=["all", *AVAILABLE_LANGUAGES], help="Language to render")
    parser.add_argument("-f", "--format", choices=["pdf", "html"], default="pdf", help="Output format")

    subparsers = parser.add_subparsers(dest="command")

    generate_parser = subparsers.add_parser("generate", help="Generate a CV from a profile and template")
    generate_parser.add_argument("-p", "--profile", default="all", help="Profile name or 'all'")
    generate_parser.add_argument("-t", "--template", default="all", choices=["all", *AVAILABLE_TEMPLATES], help="Template to use")
    generate_parser.add_argument("-l", "--language", default="all", choices=["all", *AVAILABLE_LANGUAGES], help="Language to render")
    generate_parser.add_argument("-f", "--format", choices=["pdf", "html"], default="pdf", help="Output format")
    generate_parser.set_defaults(command="generate", func=_run_generate_command)

    templates_parser = subparsers.add_parser("templates", help="List available templates")
    templates_parser.set_defaults(command="templates", func=_list_templates)

    profiles_parser = subparsers.add_parser("profiles", help="List available profiles")
    profiles_parser.set_defaults(command="profiles", func=_list_profiles)

    validate_parser = subparsers.add_parser("validate", help="Validate profile JSON files")
    validate_parser.set_defaults(command="validate", func=_validate_profiles)

    return parser


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv[1:]

    if argv and argv[0] not in {"generate", "templates", "profiles", "validate"} and not argv[0].startswith("-"):
        requested_languages, template_names, explicit_language_request = parse_cli_arguments(argv)
        from .generator import run_generation

        run_generation(requested_languages, template_names, explicit_language_request)
        return

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        args.command = "generate"
        args.func = _run_generate_command

    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)
