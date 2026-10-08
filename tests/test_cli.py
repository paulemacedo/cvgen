import unittest
from pathlib import Path

from src import cli
from src.data import load_json_file
from src.data import resolve_profile_templates
from src.prepare import prepare_experience, prepare_skills


class CliCommandTests(unittest.TestCase):
    def test_generate_command_accepts_profile_template_and_language(self):
        parser = cli.build_parser()
        parsed = parser.parse_args([
            "generate",
            "--profile",
            "paule",
            "--template",
            "blackluxury",
            "--language",
            "pt",
            "--format",
            "pdf",
        ])

        self.assertEqual(parsed.command, "generate")
        self.assertEqual(parsed.profile, "paule")
        self.assertEqual(parsed.template, "blackluxury")
        self.assertEqual(parsed.language, "pt")
        self.assertEqual(parsed.format, "pdf")

    def test_templates_command_lists_available_templates(self):
        parser = cli.build_parser()
        parsed = parser.parse_args(["templates"])
        self.assertEqual(parsed.command, "templates")

    def test_it_profile_preserves_spanish_translations(self):
        profile_path = Path(__file__).resolve().parents[1] / "data" / "IT.json"
        profile = load_json_file(profile_path)

        experience = prepare_experience(profile, "es")
        skills = prepare_skills(profile, "es")

        self.assertEqual(experience[0]["role"]["es"], "Técnico en Mantenimiento de Dispositivos Móviles")
        self.assertEqual(skills[0]["label"]["es"], "Sistemas, Redes y Soporte")
        self.assertEqual(skills[-1]["items"][1], "Español (Básico)")

    def test_profile_template_is_used_when_cli_does_not_override_it(self):
        profile = {"template": "ivory"}

        self.assertEqual(
            resolve_profile_templates(profile, ["ivory", "burgundy", "blackluxury"], False),
            ["ivory"],
        )
        self.assertEqual(
            resolve_profile_templates(profile, ["blackluxury"], True),
            ["blackluxury"],
        )

    def test_invalid_profile_template_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "not available"):
            resolve_profile_templates({"template": "unknown"}, ["blackluxury"], False)


if __name__ == "__main__":
    unittest.main()
