"""
Tests for json-tabulate main module.
"""

import json

import pytest

from json_tabulate.main import translate_json


class TestTranslateJson:
    def test_translate_json_string(self):
        json_input = '{"name": "John", "age": 30}'
        result = translate_json(json_input=json_input)
        # The output should be a CSV header and a row
        assert result.strip().startswith("$.age,$.name")
        assert "30,John" in result

    def test_translate_json_no_input(self):
        with pytest.raises(json.JSONDecodeError):
            translate_json()

    def test_translate_json_invalid_string(self):
        invalid_json = '{"foo": "bar": 1}'
        with pytest.raises(json.JSONDecodeError):
            translate_json(json_input=invalid_json)

    def test_translate_json_empty_object(self):
        result = translate_json(json_input="{}")
        assert result.strip() == ""

    def test_translate_json_complex_object(self):
        complex_json = {
            "users": [
                {"name": "John", "age": 30, "hobbies": ["reading", "swimming"]},
                {"name": "Jane", "age": 25, "hobbies": ["coding", "hiking"]},
            ],
            "metadata": {"version": "1.0", "created": "2024-01-01"},
        }

        result = translate_json(json_input=json.dumps(complex_json))
        # Should contain CSV headers for all fields
        assert result.strip().startswith("$.metadata.created,$.metadata.version,$.users[0].age")
        # Should contain both users' data
        assert "John" in result
        assert "Jane" in result
        assert "2024-01-01" in result
