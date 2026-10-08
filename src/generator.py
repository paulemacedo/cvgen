from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .config import DEFAULT_LABELS
from .data import discover_profile_files, load_json_file, resolve_profile_templates
from .export import copy_template_assets, generate_pdf
from .localization import get_labels_for_language, resolve_profile_languages
from .paths import DATA_DIR, HTML_OUTPUT_DIR, TEMPLATES_DIR, build_html_output_filename, build_output_basename, get_html_output_dir_for_profile, get_template_css_filename, resolve_topic_output_dir
from .prepare import render_profile


def generate_cv_files(
    profile_path: Path,
    requested_languages: list[str],
    template_names: list[str],
    explicit_language_request: bool,
    include_pdf: bool = True,
    explicit_template_request: bool = False,
) -> None:
    profile = load_json_file(profile_path)
    labels_by_language = profile.get("labels", DEFAULT_LABELS)
    environment = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    filename = profile_path.stem.lower()
    prefix = filename.split("-")[0]
    profile_languages = resolve_profile_languages(
        profile,
        profile_path,
        requested_languages,
        explicit_language_request,
    )

    if not profile_languages:
        print(f"⚠️  {profile_path.name}: no languages to generate after filtering.")
        return

    templates_to_use = (
        ["Master"]
        if prefix == "master"
        else resolve_profile_templates(profile, template_names, explicit_template_request)
    )
    pdf_output_dir = resolve_topic_output_dir(profile_path)
    html_output_dir = get_html_output_dir_for_profile(profile_path)
    copy_template_assets(html_output_dir, templates_to_use)
    pdf_output_dir.mkdir(parents=True, exist_ok=True)

    for template_name in templates_to_use:
        template = environment.get_template(f"{template_name}.html")
        template_css_href = get_template_css_filename(template_name)

        for language in profile_languages:
            labels = get_labels_for_language(labels_by_language, language)
            html = render_profile(
                template,
                profile,
                language,
                labels,
                common_css_href="common.css",
                template_css_href=template_css_href,
            )
            output_basename = build_output_basename(profile, profile_path, language)
            if len(templates_to_use) > 1:
                output_basename = f"{output_basename}-{template_name.title()}"
            html_filename = build_html_output_filename(profile_path, output_basename)

            html_path = html_output_dir / f"{html_filename}.html"
            html_path.write_text(html, encoding="utf-8")
            print(f"CV gerado:  {html_path.relative_to(DATA_DIR.parent)}")

            try:
                from .export import PDF_ENABLED

                if include_pdf and PDF_ENABLED:
                    pdf_path = pdf_output_dir / f"{output_basename}.pdf"
                    generate_pdf(html_path, pdf_path)
                    print(f"PDF gerado: {pdf_path.relative_to(DATA_DIR.parent)}")
            except Exception as exception:
                print(f"⚠️  Erro ao gerar PDF ({html_path.relative_to(DATA_DIR.parent)}): {exception}")


def run_generation(
    profile_paths: list[Path] | None = None,
    requested_languages: list[str] | None = None,
    template_names: list[str] | None = None,
    explicit_language_request: bool = False,
    include_pdf: bool = True,
    explicit_template_request: bool = False,
) -> None:
    if profile_paths is None:
        profile_paths = discover_profile_files()
    if requested_languages is None:
        from .config import AVAILABLE_LANGUAGES
        requested_languages = AVAILABLE_LANGUAGES
    if template_names is None:
        from .config import AVAILABLE_TEMPLATES
        template_names = AVAILABLE_TEMPLATES

    if not profile_paths:
        print("No data files found in the 'data' folder.")
        return

    for profile_path in profile_paths:
        generate_cv_files(
            profile_path,
            requested_languages,
            template_names,
            explicit_language_request,
            include_pdf=include_pdf,
            explicit_template_request=explicit_template_request,
        )
