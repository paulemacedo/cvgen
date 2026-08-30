from __future__ import annotations

import shutil
from pathlib import Path

from .paths import TEMPLATES_DIR, get_template_css_filename


try:
    from playwright.sync_api import sync_playwright

    PDF_ENABLED = True
except ImportError:
    PDF_ENABLED = False


def copy_template_assets(output_dir: Path, template_names: list[str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TEMPLATES_DIR / "common.css", output_dir / "common.css")

    for template_name in dict.fromkeys(template_names):
        css_filename = get_template_css_filename(template_name)
        css_source = TEMPLATES_DIR / css_filename
        if css_source.exists():
            shutil.copy2(css_source, output_dir / css_filename)


def generate_pdf(html_path: Path, pdf_path: Path) -> None:
    """Render an HTML file to PDF using a headless Chromium browser."""
    if not PDF_ENABLED:
        raise RuntimeError("Playwright not installed. PDF output disabled.")

    abs_html_path = html_path.resolve()

    with sync_playwright() as browser_context:
        browser = browser_context.chromium.launch()
        page = browser.new_page()

        page.goto(
            abs_html_path.as_uri(),
            wait_until="domcontentloaded",
            timeout=30000,
        )

        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={
                "top": "8mm",
                "right": "8mm",
                "bottom": "8mm",
                "left": "8mm",
            },
        )

        browser.close()
