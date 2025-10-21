"""
Data Query Framework
A framework for extracting data from various sources (web, Excel) and managing it in SQLite.
"""

__version__ = "1.0.0"
__author__ = "Data Query Team"

from .database.sqlite_manager import SQLiteManager
from .extractors.web_extractor import WebExtractor
from .extractors.excel_extractor import ExcelExtractor
from .workflow import DataQueryWorkflow

__all__ = [
    "SQLiteManager",
    "WebExtractor",
    "ExcelExtractor",
    "DataQueryWorkflow",
]
