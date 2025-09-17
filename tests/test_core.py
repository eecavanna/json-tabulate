"""
Tests for json-tabulate main module.
"""

import json

import pytest

from json_tabulate.core import translate_json


class TestTranslateJson:
    def test_translate_json_string(self):
        json_str = r'{"name": "Ryu", "age": 25}'
        assert translate_json(json_str=json_str) == "$.age,$.name\n25,Ryu\n"

    def test_translate_json_empty_string(self):
        with pytest.raises(json.JSONDecodeError):
            translate_json(json_str="")

    def test_translate_json_invalid_json_string(self):
        invalid_json = r'{"name": "Ryu",, "age": 25}'
        with pytest.raises(json.JSONDecodeError):
            translate_json(json_str=invalid_json)

    def test_translate_json_valid_empty_object_json_string(self):
        assert translate_json(json_str="{}") == ""

    def test_translate_json_valid_empty_array_json_string(self):
        assert translate_json(json_str="[]") == ""

    def test_translate_json_complex_object(self):
        json_str = r"""
            [
                {"a": 1                                                },
                {"a": 2, "b": 3                                        },
                {                "c": {"foo": "bar"}                   },
                {                                     "d": [4, null, 5]}
            ]
        """
        result = translate_json(json_str=json_str)
        result_lines = result.splitlines()
        assert len(result_lines) == 5  # 1 header line + 4 data lines
        assert result_lines[0] == "$.a,$.b,$.c.foo,$.d[0],$.d[1],$.d[2]"
        assert result_lines[1] == "1,,,,,"
        assert result_lines[2] == "2,3,,,,"
        assert result_lines[3] == ",,bar,,,"
        assert result_lines[4] == ",,,4,,5"

    def test_translate_json_with_tab_delimiter(self):
        json_str = r'{"name": "Ryu", "age": 25}'
        result = translate_json(json_str=json_str, delimiter="\t")
        assert result == "$.age\t$.name\n25\tRyu\n"

    def test_translate_json_tsv_complex_object(self):
        json_str = r"""
            [
                {"a": 1                                                },
                {"a": 2, "b": 3                                        },
                {                "c": {"foo": "bar"}                   },
                {                                     "d": [4, null, 5]}
            ]
        """
        result = translate_json(json_str=json_str, delimiter="\t")
        result_lines = result.splitlines()
        assert len(result_lines) == 5  # 1 header line + 4 data lines
        assert result_lines[0] == "$.a\t$.b\t$.c.foo\t$.d[0]\t$.d[1]\t$.d[2]"
        assert result_lines[1] == "1\t\t\t\t\t"
        assert result_lines[2] == "2\t3\t\t\t\t"
        assert result_lines[3] == "\t\tbar\t\t\t"
        assert result_lines[4] == "\t\t\t4\t\t5"

    def test_translate_json_custom_delimiter(self):
        json_str = r'{"name": "Ryu", "age": 25}'
        result = translate_json(json_str=json_str, delimiter="|")
        assert result == "$.age|$.name\n25|Ryu\n"
