"""
CLI providing access to core functionality of json-tabulate.
"""

import sys
from enum import Enum
from importlib.metadata import version
from typing import Optional

import typer
from typing_extensions import Annotated

from json_tabulate.core import translate_json


class OutputFormat(str, Enum):
    """Output format options."""

    CSV = "csv"
    TSV = "tsv"


# Create a CLI application.
# Reference: https://typer.tiangolo.com/tutorial/commands/#explicit-application
app = typer.Typer(
    name="json-tabulate",
    help="Translates arbitrarily-nested JSON into CSV",
    no_args_is_help=True,  # treats the absence of args like the `--help` arg
    add_completion=False,  # hides the shell completion options from `--help` output
    rich_markup_mode="markdown",  # enables use of Markdown in docstrings and CLI help
)


def show_version_and_exit_if(is_enabled: bool) -> None:
    """Show version information and exit, if `True` is passed in."""

    if is_enabled:
        version_string = version("json-tabulate")
        typer.echo(f"json-tabulate {version_string}")
        raise typer.Exit()


@app.command()
def main(
    json_string: Annotated[
        Optional[str],
        typer.Argument(help="JSON string to translate. If not provided, program will read from STDIN."),
    ] = None,
    # Reference: https://typer.tiangolo.com/tutorial/parameter-types/enum/
    output_format: Annotated[
        OutputFormat,
        typer.Option(
            "--output-format",
            help="Whether you want the output to be comma-delimited or tab-delimited.",
            case_sensitive=False,
        ),
    ] = OutputFormat.CSV,
    # Reference: https://typer.tiangolo.com/tutorial/options/version/#fix-with-is_eager
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version", callback=show_version_and_exit_if, is_eager=True, help="Show version number and exit."
        ),
    ] = None,
) -> None:
    """
    Translate JSON into CSV.

    Usage examples:
    - `json-tabulate '{"name": "Ken", "age": 26}'` (specify JSON via argument)
    - `echo '{"name": "Ken", "age": 26}' | json-tabulate` (specify JSON via STDIN)
    - `cat input.json | json-tabulate > output.csv` (write CSV to file)
    """

    # Determine the output delimiter based upon the specified output format.
    output_delimiter = "\t" if output_format == OutputFormat.TSV else ","

    try:
        # Check whether the JSON was provided via a CLI argument.
        if json_string is not None:
            result = translate_json(json_str=json_string, output_delimiter=output_delimiter)
        else:
            # Check whether STDIN is connected to an interactive terminal,
            # in which case, it would not be receiving any input via a pipe.
            if sys.stdin.isatty():
                raise typer.BadParameter("No JSON was provided via argument or STDIN.")
            else:
                stdin_content = sys.stdin.read().strip()
                if isinstance(stdin_content, str) and stdin_content != "":
                    result = translate_json(json_str=stdin_content, output_delimiter=output_delimiter)
                else:
                    raise typer.BadParameter("No JSON was provided via STDIN.")

        # Print the resulting CSV string, without adding a newline.
        typer.echo(result, nl=False)

    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    # Run the CLI application.
    app()
