"""
CLI interface for json-tabulate.
"""

import sys
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from .main import process_json, process_json_from_stdin
from importlib.metadata import version

app = typer.Typer(
    name="json-tabulate",
    help="Translate arbitrarily-nested JSON into CSV",
    no_args_is_help=True,
)



@app.command(name="convert")
def convert(
    json_string: Annotated[
        Optional[str],
        typer.Argument(
            help="JSON string to process. If not provided, reads from STDIN."
        ),
    ] = None,
    output: Annotated[
        Optional[Path],
        typer.Option(
            "--output",
            "-o",
            help="Output file path. If not provided, prints to STDOUT.",
        ),
    ] = None,
) -> None:
    """
    Convert JSON to CSV format.

    Examples:
        echo '{"name": "John", "age": 30}' | json-tabulate
        json-tabulate '{"name": "John", "age": 30}'
        cat data.json | json-tabulate --output result.csv
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

        if output is None:
            typer.echo(result)
        else:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            typer.echo(f"Output written to {output}")

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
