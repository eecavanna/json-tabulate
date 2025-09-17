import re

from typer.testing import CliRunner

from json_tabulate.cli import app


class TestCLI:
    """Test cases for CLI interface."""

    def setup_method(self):
        # Set up test runner.
        #
        # References:
        # - https://docs.pytest.org/en/stable/how-to/xunit_setup.html#method-and-function-level-setup-teardown
        # - https://typer.tiangolo.com/tutorial/testing/#import-and-create-a-clirunner
        #
        self.runner = CliRunner()

    def test_version_option(self):
        result = self.runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        output_str = result.output

        # Assert that the version string contains (at least somewhere within it)
        # "digit(s), dot, digit(s), dot, digit(s)" (e.g. "1.2.3"). This allows for
        # suffixes like "rc1", as in "1.2.3rc1".
        assert re.search(r"\d+\.\d+\.\d+", output_str) is not None

    def test_help_option(self):
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output

    def test_specifying_json_via_argument(self):
        json_str = r'{"name": "Ryu", "age": 25}'
        result = self.runner.invoke(app, [json_str])
        assert result.exit_code == 0
        assert result.output == "$.age,$.name\n25,Ryu\n"

    def test_specifying_json_via_stdin(self):
        json_str = r'{"name": "Ryu", "age": 25}'
        result = self.runner.invoke(app, input=json_str)
        assert result.exit_code == 0
        assert result.output == "$.age,$.name\n25,Ryu\n"

    def test_specifying_invalid_json(self):
        invalid_json_string = r'{"name": "Ryu",, "age": 25}'
        result = self.runner.invoke(app, [invalid_json_string])
        assert result.exit_code == 1
        assert "Invalid JSON string" in result.output

        result = self.runner.invoke(app, input=invalid_json_string)
        assert result.exit_code == 1
        assert "Invalid JSON string" in result.output

    def test_specifying_empty_string(self):
        result = self.runner.invoke(app, [r""])
        assert result.exit_code == 1
        assert "Invalid JSON string" in result.output

        result = self.runner.invoke(app, input=r"")
        assert result.exit_code == 1
        assert "No JSON was provided via STDIN" in result.output

    def test_output_format_csv_default(self):
        json_str = r'{"name": "Ryu", "age": 25}'
        result = self.runner.invoke(app, [json_str])
        assert result.exit_code == 0
        assert result.output == "$.age,$.name\n25,Ryu\n"

    def test_output_format_csv_explicit(self):
        json_str = r'{"name": "Ryu", "age": 25}'
        result = self.runner.invoke(app, ["--output-format", "csv", json_str])
        assert result.exit_code == 0
        assert result.output == "$.age,$.name\n25,Ryu\n"

    def test_output_format_tsv(self):
        json_str = r'{"name": "Ryu", "age": 25}'
        result = self.runner.invoke(app, ["--output-format", "tsv", json_str])
        assert result.exit_code == 0
        assert result.output == "$.age\t$.name\n25\tRyu\n"

    def test_output_format_tsv_via_stdin(self):
        json_str = r'{"name": "Ryu", "age": 25}'
        result = self.runner.invoke(app, ["--output-format", "tsv"], input=json_str)
        assert result.exit_code == 0
        assert result.output == "$.age\t$.name\n25\tRyu\n"

    def test_output_format_tsv_complex(self):
        json_str = r'[{"a": 1}, {"a": 2, "b": 3}]'
        result = self.runner.invoke(app, ["--output-format", "tsv", json_str])
        assert result.exit_code == 0
        expected_lines = result.output.splitlines()
        assert len(expected_lines) == 3  # 1 header + 2 data lines
        assert expected_lines[0] == "$.a\t$.b"
        assert expected_lines[1] == "1\t"
        assert expected_lines[2] == "2\t3"

    def test_output_format_invalid(self):
        json_str = r'{"name": "Ryu", "age": 25}'
        result = self.runner.invoke(app, ["--output-format", "invalid", json_str])
        assert result.exit_code == 1
        assert "Invalid output format 'invalid'" in result.output
        assert "Must be 'csv' or 'tsv'" in result.output
