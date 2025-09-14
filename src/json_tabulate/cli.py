"""
CLI interface for json-tabulate using typer.
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
    help="Convert JSON to CSV format",
    no_args_is_help=True,
)


@app.command()
def convert(
    file_path: Annotated[
        Optional[Path],
        typer.Argument(
            help="Path to JSON file to process. If not provided, reads from STDIN."
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
        json-tabulate data.json
        echo '{"name": "John", "age": 30}' | json-tabulate
        json-tabulate data.json --output result.csv
    """
    try:
        if file_path is None:
            # Read from STDIN
            if sys.stdin.isatty():
                typer.echo(
                    "Error: No input provided. Provide a file path or pipe JSON to STDIN.",
                    err=True,
                )
                raise typer.Exit(1)
            result = process_json_from_stdin()
        else:
            # Read from file
            result = process_json(file_path=file_path)

        if output is None:
            # Print to STDOUT
            typer.echo(result)
        else:
            # Write to file
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            typer.echo(f"Output written to {output}")

    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
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
