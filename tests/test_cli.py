"""
Tests for json-tabulate CLI interface.
"""

import json
import tempfile
from pathlib import Path
from typer.testing import CliRunner

from json_tabulate.cli import app


class TestCLI:
    """Test cases for CLI interface."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_version_command(self):
        """Test version command."""
        result = self.runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "json-tabulate" in result.stdout
        assert "0.1.0" in result.stdout

    def test_convert_with_file(self):
        """Test converting a JSON file."""
        # Create a temporary JSON file
        test_data = {"name": "John", "age": 30}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_data, f)
            temp_file = Path(f.name)

        try:
            result = self.runner.invoke(app, ["convert", str(temp_file)])
            assert result.exit_code == 0
            assert "Hello!" in result.stdout
            assert "Processed JSON file" in result.stdout
        finally:
            temp_file.unlink()

    def test_convert_nonexistent_file(self):
        """Test converting a nonexistent file."""
        result = self.runner.invoke(app, ["convert", "nonexistent.json"])
        assert result.exit_code == 1

    def test_convert_with_output_file(self):
        """Test converting with output file."""
        # Create a temporary JSON file
        test_data = {"name": "Jane", "age": 25}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_data, f)
            temp_file = Path(f.name)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as out_f:
            output_file = Path(out_f.name)

        try:
            result = self.runner.invoke(
                app, ["convert", str(temp_file), "--output", str(output_file)]
            )
            assert result.exit_code == 0
            assert f"Output written to {output_file}" in result.stdout

            # Check that output file was created and contains expected content
            assert output_file.exists()
            content = output_file.read_text()
            assert "Hello!" in content
            assert "Processed JSON file" in content

        finally:
            temp_file.unlink()
            if output_file.exists():
                output_file.unlink()

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
