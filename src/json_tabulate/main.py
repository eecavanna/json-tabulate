"""
Main module for json-tabulate.

This module provides functionality to process JSON input and return formatted output.
"""

import json
import sys
from typing import Optional


def process_json(
    json_input: Optional[str] = None
) -> str:
    """
    Process JSON input from a string.

    Args:
        json_input: JSON string to process

    Returns:
        A greeting message (placeholder for actual JSON-to-CSV conversion)

    Raises:
        ValueError: If no input is provided
        json.JSONDecodeError: If the JSON is invalid
    """
    if json_input is None:
        raise ValueError("No input provided")

    try:
        parsed = json.loads(json_input)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON string: {e}", e.doc, e.pos)
    return f"Hello! Processed JSON string with {len(str(parsed))} characters."


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
