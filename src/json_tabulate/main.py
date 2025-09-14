"""
Main module for json-tabulate.

This module provides functionality to process JSON input and return formatted output.
For now, it returns a simple "hello" message as a placeholder.
"""

import json
import sys
from pathlib import Path
from typing import Union, Optional


def process_json(
    json_input: Optional[str] = None, file_path: Optional[Union[str, Path]] = None
) -> str:
    """
    Process JSON input from either a string or file path.

    Args:
        json_input: JSON string to process
        file_path: Path to JSON file to process

    Returns:
        A greeting message (placeholder for actual JSON-to-CSV conversion)

    Raises:
        ValueError: If neither json_input nor file_path is provided, or if both are provided
        FileNotFoundError: If the specified file doesn't exist
        json.JSONDecodeError: If the JSON is invalid
    """
    if json_input is None and file_path is None:
        raise ValueError("Either json_input or file_path must be provided")

    if json_input is not None and file_path is not None:
        raise ValueError("Only one of json_input or file_path should be provided")

    # Process JSON input
    if json_input is not None:
        # Validate JSON
        try:
            parsed = json.loads(json_input)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON string: {e}", e.doc, e.pos)
        return f"Hello! Processed JSON string with {len(str(parsed))} characters."

    # Process JSON file
    if file_path is not None:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                parsed = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in file {file_path}: {e}", e.doc, e.pos
            )

        return f"Hello! Processed JSON file '{file_path.name}' with {len(str(parsed))} characters."

    return ""


def process_json_from_stdin() -> str:
    """
    Process JSON input from STDIN.

    Returns:
        A greeting message after processing STDIN input

    Raises:
        json.JSONDecodeError: If the JSON from STDIN is invalid
    """
    stdin_content = sys.stdin.read().strip()
    if not stdin_content:
        raise ValueError("No input provided via STDIN")

    return process_json(json_input=stdin_content)
