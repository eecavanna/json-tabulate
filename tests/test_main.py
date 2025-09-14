"""
Tests for json-tabulate main module.
"""

import json
import tempfile
from pathlib import Path
import pytest

from json_tabulate.main import process_json


class TestProcessJson:
    """Test cases for process_json function."""
    
    def test_process_json_string(self):
        """Test processing a JSON string."""
        json_input = '{"name": "John", "age": 30}'
        result = process_json(json_input=json_input)
        assert "Hello!" in result
        assert "Processed JSON string" in result
        assert "characters" in result
    
    def test_process_json_file(self):
        """Test processing a JSON file."""
        # Create a temporary JSON file
        test_data = {"name": "Jane", "age": 25, "city": "New York"}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_file = Path(f.name)
        
        try:
            result = process_json(file_path=temp_file)
            assert "Hello!" in result
            assert "Processed JSON file" in result
            assert temp_file.name in result
            assert "characters" in result
        finally:
            temp_file.unlink()
    
    def test_process_json_no_input(self):
        """Test that providing no input raises ValueError."""
        with pytest.raises(ValueError, match="Either json_input or file_path must be provided"):
            process_json()
    
    def test_process_json_both_inputs(self):
        """Test that providing both inputs raises ValueError."""
        with pytest.raises(ValueError, match="Only one of json_input or file_path should be provided"):
            process_json(json_input='{"test": true}', file_path="test.json")
    
    def test_process_json_invalid_string(self):
        """Test processing an invalid JSON string."""
        invalid_json = '{"name": "John", "age":}'
        with pytest.raises(json.JSONDecodeError):
            process_json(json_input=invalid_json)
    
    def test_process_json_nonexistent_file(self):
        """Test processing a nonexistent file."""
        with pytest.raises(FileNotFoundError):
            process_json(file_path="nonexistent_file.json")
    
    def test_process_json_invalid_file(self):
        """Test processing a file with invalid JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": json}')
            temp_file = Path(f.name)
        
        try:
            with pytest.raises(json.JSONDecodeError):
                process_json(file_path=temp_file)
        finally:
            temp_file.unlink()
    
    def test_process_json_empty_object(self):
        """Test processing an empty JSON object."""
        result = process_json(json_input='{}')
        assert "Hello!" in result
        assert "Processed JSON string" in result
    
    def test_process_json_complex_object(self):
        """Test processing a complex JSON object."""
        complex_json = {
            "users": [
                {"name": "John", "age": 30, "hobbies": ["reading", "swimming"]},
                {"name": "Jane", "age": 25, "hobbies": ["coding", "hiking"]}
            ],
            "metadata": {
                "version": "1.0",
                "created": "2024-01-01"
            }
        }
        
        result = process_json(json_input=json.dumps(complex_json))
        assert "Hello!" in result
        assert "Processed JSON string" in result
        assert "characters" in result