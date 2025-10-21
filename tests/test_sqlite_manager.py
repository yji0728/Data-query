"""
Unit tests for SQLite Manager
"""

import unittest
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_query.database import SQLiteManager


class TestSQLiteManager(unittest.TestCase):
    """Test cases for SQLiteManager."""
    
    def setUp(self):
        """Set up test database."""
        self.db_path = "/tmp/test_data_query.db"
        self.manager = SQLiteManager(self.db_path)
        self.manager.connect()
        
    def tearDown(self):
        """Clean up test database."""
        self.manager.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            
    def test_create_table(self):
        """Test table creation."""
        schema = {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "age": "INTEGER"
        }
        self.manager.create_table("users", schema)
        self.assertTrue(self.manager.table_exists("users"))
        
    def test_insert_data(self):
        """Test data insertion."""
        schema = {"id": "INTEGER PRIMARY KEY", "name": "TEXT"}
        self.manager.create_table("test_table", schema)
        
        data = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
        self.manager.insert_data("test_table", data)
        
        results = self.manager.query("SELECT * FROM test_table")
        self.assertEqual(len(results), 2)
        
    def test_query(self):
        """Test data querying."""
        schema = {"id": "INTEGER PRIMARY KEY", "value": "TEXT"}
        self.manager.create_table("test_query", schema)
        
        data = [{"id": 1, "value": "test"}]
        self.manager.insert_data("test_query", data)
        
        results = self.manager.query("SELECT * FROM test_query WHERE id = ?", (1,))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["value"], "test")
        
    def test_update_data(self):
        """Test data update."""
        schema = {"id": "INTEGER PRIMARY KEY", "status": "TEXT"}
        self.manager.create_table("test_update", schema)
        
        data = [{"id": 1, "status": "pending"}]
        self.manager.insert_data("test_update", data)
        
        self.manager.update_data("test_update", {"status": "completed"}, "id = ?", (1,))
        
        results = self.manager.query("SELECT * FROM test_update WHERE id = 1")
        self.assertEqual(results[0]["status"], "completed")
        
    def test_delete_data(self):
        """Test data deletion."""
        schema = {"id": "INTEGER PRIMARY KEY", "name": "TEXT"}
        self.manager.create_table("test_delete", schema)
        
        data = [{"id": 1, "name": "temp"}]
        self.manager.insert_data("test_delete", data)
        
        self.manager.delete_data("test_delete", "id = ?", (1,))
        
        results = self.manager.query("SELECT * FROM test_delete")
        self.assertEqual(len(results), 0)
        
    def test_context_manager(self):
        """Test context manager functionality."""
        with SQLiteManager(self.db_path) as manager:
            schema = {"id": "INTEGER PRIMARY KEY"}
            manager.create_table("context_test", schema)
            self.assertTrue(manager.table_exists("context_test"))


if __name__ == "__main__":
    unittest.main()
