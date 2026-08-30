import unittest

from src import cli


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


if __name__ == "__main__":
    unittest.main()
