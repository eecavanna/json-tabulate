import re

from typer.testing import CliRunner

from json_tabulate.cli import app


class TestCLI:
    """Test cases for CLI interface."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_version_command(self):
        result = self.runner.invoke(app, ["version"])
        assert result.exit_code == 0
        output_str = result.stdout
        assert "json-tabulate" in output_str

        # Assert that the version string contain (at least somewhere within it)
        # "digit(s), dot, digit(s), dot, digit(s)". This allows for suffixes like
        # "rc1", as in "1.0.0rc1".
        assert re.search(r"\d+\.\d+\.\d+", output_str) is not None

    def test_translate_with_argument(self):
        """Test translating a JSON string via argument."""
        json_str = '{"name": "John", "age": 30}'
        result = self.runner.invoke(app, ["translate", json_str])
        assert result.exit_code == 0
        assert result.stdout.strip().startswith("$.age,$.name")
        assert "30,John" in result.stdout

    def test_translate_with_stdin(self):
        """Test translating a JSON string via STDIN."""
        json_str = '{"name": "Jane", "age": 25}'
        result = self.runner.invoke(app, ["translate"], input=json_str)
        assert result.exit_code == 0
        assert result.stdout.strip().startswith("$.age,$.name")
        assert "25,Jane" in result.stdout

    def test_help_command(self):
        """Test help command."""
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Translate JSON into CSV" in result.stdout

    def test_translate_help(self):
        """Test translate command help."""
        result = self.runner.invoke(app, ["translate", "--help"])
        assert result.exit_code == 0
        assert "Usage examples" in result.stdout
