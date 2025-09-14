"""
CLI interface for json-tabulate.
"""

import sys
from importlib.metadata import version
from typing import Optional

import typer
from typing_extensions import Annotated

from .main import process_json, process_json_from_stdin

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
def translate(
    json_string: Annotated[
        Optional[str],
        typer.Argument(help="JSON string to translate. If not provided, program will read from STDIN."),
    ] = None,
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
    - `json-tabulate '{"name": "Aiden", "age": 13}'` (specify JSON via argument)
    - `echo '{"name": "Aiden", "age": 13}' | json-tabulate` (specify JSON via STDIN)
    - `cat input.json | json-tabulate > output.csv` (write CSV to file)
    """
    try:
        if json_string is not None:
            result = process_json(json_input=json_string)
        else:
            if sys.stdin.isatty():
                typer.echo(
                    "Error: No input provided. Provide a JSON string as an argument or pipe JSON to STDIN.",
                    err=True,
                )
                raise typer.Exit(1)
            result = process_json_from_stdin()

        typer.echo(result)

    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    # Run the CLI application.
    app()
