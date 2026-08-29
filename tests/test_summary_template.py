import unittest
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from generate import render_profile, DEFAULT_LABELS


class SummaryTemplateTests(unittest.TestCase):
    def test_summary_is_rendered_in_ivory_template(self):
        profile = {
            "name": {"pt": "Paule Macedo"},
            "location": {"pt": "Rio de Janeiro"},
            "headline": {"pt": "Estoquista"},
            "summary": {"pt": "Resumo de teste para o currículo."},
            "contact": {"linkedin": "https://example.com", "phone": "123", "website": "https://example.com", "email": "a@b.com", "github": "https://github.com/example"},
            "skills": [],
            "experience": [],
            "projects": [],
            "education": [],
            "certifications": [],
            "publications": [],
        }

        template = Environment(loader=FileSystemLoader(str(Path(__file__).resolve().parents[1] / "templates"))).get_template("Ivory.html")
        html = render_profile(
            template,
            profile,
            "pt",
            DEFAULT_LABELS["pt"],
            "common.css",
            "Ivory.css",
        )

        self.assertIn("Resumo de teste para o currículo.", html)

    def test_summary_is_rendered_in_paule_template(self):
        profile = {
            "name": {"pt": "Paule Macedo"},
            "location": {"pt": "Rio de Janeiro"},
            "headline": {"pt": "Estoquista"},
            "summary": {"pt": "Resumo de teste para o currículo."},
            "contact": {"linkedin": "https://example.com", "phone": "123", "website": "https://example.com", "email": "a@b.com", "github": "https://github.com/example"},
            "skills": [],
            "experience": [],
            "projects": [],
            "education": [],
            "certifications": [],
            "publications": [],
        }

        template = Environment(loader=FileSystemLoader(str(Path(__file__).resolve().parents[1] / "templates"))).get_template("Paule.html")
        html = render_profile(
            template,
            profile,
            "pt",
            DEFAULT_LABELS["pt"],
            "common.css",
            "Paule.css",
        )

        self.assertIn("Resumo de teste para o currículo.", html)

    def test_missing_social_links_are_hidden(self):
        profile = {
            "name": {"pt": "Paule Macedo"},
            "location": {"pt": "Rio de Janeiro"},
            "headline": {"pt": "Estoquista"},
            "summary": {"pt": "Resumo de teste para o currículo."},
            "contact": {"linkedin": "", "phone": "123", "website": "", "email": "a@b.com", "github": ""},
            "skills": [],
            "experience": [],
            "projects": [],
            "education": [],
            "certifications": [],
            "publications": [],
        }

        template = Environment(loader=FileSystemLoader(str(Path(__file__).resolve().parents[1] / "templates"))).get_template("Ivory.html")
        html = render_profile(
            template,
            profile,
            "pt",
            DEFAULT_LABELS["pt"],
            "common.css",
            "Ivory.css",
        )

        self.assertNotIn("LinkedIn", html)
        self.assertNotIn("Portifolio", html)
        self.assertNotIn("GitHub", html)
        self.assertIn("a@b.com", html)

    def test_black_luxury_template_renders_without_dual_columns(self):
        profile = {
            "name": {"pt": "Paule Macedo"},
            "location": {"pt": "Rio de Janeiro"},
            "headline": {"pt": "Estoquista"},
            "summary": {"pt": "Resumo de teste para o currículo."},
            "contact": {"linkedin": "https://example.com", "phone": "123", "website": "https://example.com", "email": "a@b.com", "github": "https://github.com/example"},
            "skills": [{"label": {"pt": "Habilidades"}, "items": ["Gestão de Estoque"], "priority": 1}],
            "experience": [{"role": {"pt": "Atendimento"}, "company": "Loja", "location": "Rio", "date": {"pt": "2024"}, "bullets": {"pt": ["Foco em atendimento."]}}],
            "projects": [],
            "education": [{"degree": {"pt": "Ensino Superior"}, "institution": "IBMR", "location": "Rio", "date": {"pt": "2027"}, "details": {"pt": ["Em andamento."]}}],
            "certifications": [],
            "publications": [],
        }

        template = Environment(loader=FileSystemLoader(str(Path(__file__).resolve().parents[1] / "templates"))).get_template("BlackLuxury.html")
        html = render_profile(
            template,
            profile,
            "pt",
            DEFAULT_LABELS["pt"],
            "common.css",
            "BlackLuxury.css",
        )

        self.assertIn("Resumo de teste para o currículo.", html)
        self.assertIn("Habilidades", html)
        self.assertNotIn("grid-template-columns", html)

    def test_black_luxury_print_css_forces_dark_page_background(self):
        css_path = Path(__file__).resolve().parents[1] / "templates" / "BlackLuxury.css"
        css_text = css_path.read_text(encoding="utf-8")

        self.assertIn("background: #1b1b1b;", css_text)
        self.assertIn("margin: 8mm;", css_text)
        self.assertIn("background: #1b1b1b !important;", css_text)
        self.assertIn("break-inside: avoid;", css_text)


if __name__ == "__main__":
    unittest.main()
