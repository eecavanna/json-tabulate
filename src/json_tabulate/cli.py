"""
CLI interface for json-tabulate.
"""

import sys
from typing import Optional

import typer
from typing_extensions import Annotated

from .main import process_json, process_json_from_stdin
from importlib.metadata import version

app = typer.Typer(
    name="json-tabulate",
    help="Translates arbitrarily-nested JSON into CSV",
    no_args_is_help=True,
)


@app.command(name="translate")
def translate(
    json_string: Annotated[
        Optional[str],
        typer.Argument(
            help="JSON string to translate. If not provided, program will read from STDIN."
        ),
    ] = None,
) -> None:
    """
    Translate JSON to CSV format.

    Usage examples:
        echo '{"name": "Aiden", "age": 13}' | json-tabulate translate
        json-tabulate translate '{"name": "Aiden", "age": 13}'
        cat data.json | json-tabulate translate > result.csv
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


@app.command(name="version")
def show_version() -> None:
    """Show version information."""

    version_string = version("json-tabulate")
    typer.echo(f"json-tabulate {version_string}")


if __name__ == "__main__":
    app()
