"""
json-tabulate: Python library and CLI program that translates arbitrarily-nested JSON into CSV.
"""

__version__ = "0.1.0"

from .main import process_json

__all__ = ["process_json"]