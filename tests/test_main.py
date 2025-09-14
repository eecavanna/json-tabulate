"""
Tests for json-tabulate main module.
"""

import json
import pytest

from json_tabulate.main import process_json


class TestProcessJson:
    """Test cases for process_json function."""

    def test_process_json_string(self):
        """Test processing a JSON string."""
        json_input = '{"name": "John", "age": 30}'
        result = process_json(json_input=json_input)
        # The output should be a CSV header and a row
        assert result.strip().startswith("$.age,$.name")
        assert "30,John" in result

    def test_process_json_no_input(self):
        """Test that providing no input raises JSONDecodeError."""
        with pytest.raises(json.JSONDecodeError):
            process_json()

    def test_process_json_invalid_string(self):
        """Test processing an invalid JSON string."""
        invalid_json = '{"name": "John", "age":}'
        with pytest.raises(json.JSONDecodeError):
            process_json(json_input=invalid_json)

    def test_process_json_empty_object(self):
        """Test processing an empty JSON object."""
        result = process_json(json_input="{}")
        # Should produce an empty string (no header, no rows)
        assert result.strip() == ""

    def test_process_json_complex_object(self):
        """Test processing a complex JSON object."""
        complex_json = {
            "users": [
                {"name": "John", "age": 30, "hobbies": ["reading", "swimming"]},
                {"name": "Jane", "age": 25, "hobbies": ["coding", "hiking"]},
            ],
            "metadata": {"version": "1.0", "created": "2024-01-01"},
        }

        result = process_json(json_input=json.dumps(complex_json))
        # Should contain CSV headers for all fields
        assert result.strip().startswith(
            "$.metadata.created,$.metadata.version,$.users[0].age"
        )
        # Should contain both users' data
        assert "John" in result
        assert "Jane" in result
        assert "2024-01-01" in result
