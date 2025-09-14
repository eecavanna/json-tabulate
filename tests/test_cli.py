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

    def test_convert_with_argument(self):
        """Test converting a JSON string via argument."""
        json_str = '{"name": "John", "age": 30}'
        result = self.runner.invoke(app, ["convert", json_str])
        assert result.exit_code == 0
        assert "Hello!" in result.stdout
        assert "Processed JSON string" in result.stdout

    def test_convert_with_stdin(self):
        """Test converting a JSON string via STDIN."""
        json_str = '{"name": "Jane", "age": 25}'
        result = self.runner.invoke(app, ["convert"], input=json_str)
        assert result.exit_code == 0
        assert "Hello!" in result.stdout
        assert "Processed JSON string" in result.stdout

    def test_help_command(self):
        """Test help command."""
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Convert JSON to CSV format" in result.stdout

    def test_convert_help(self):
        """Test convert command help."""
        result = self.runner.invoke(app, ["convert", "--help"])
        assert result.exit_code == 0
        assert "Convert JSON to CSV format" in result.stdout
        assert "Examples:" in result.stdout
