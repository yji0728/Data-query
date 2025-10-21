"""
SQLite Database Manager
Manages SQLite database operations for storing extracted data.
"""

import sqlite3
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging


class SQLiteManager:
    """Manager for SQLite database operations."""
    
    def __init__(self, db_path: str = "data_query.db"):
        """
        Initialize SQLite manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish connection to the database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            self.logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            self.logger.error(f"Error connecting to database: {e}")
            raise
            
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed")
            
    def create_table(self, table_name: str, schema: Dict[str, str]):
        """
        Create a table with the specified schema.
        
        Args:
            table_name: Name of the table to create
            schema: Dictionary of column names and their types
        """
        columns = ", ".join([f"{col} {dtype}" for col, dtype in schema.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        
        try:
            self.cursor.execute(query)
            self.connection.commit()
            self.logger.info(f"Table '{table_name}' created successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Error creating table: {e}")
            raise
            
    def insert_data(self, table_name: str, data: List[Dict[str, Any]]):
        """
        Insert data into a table.
        
        Args:
            table_name: Name of the table
            data: List of dictionaries containing row data
        """
        if not data:
            self.logger.warning("No data to insert")
            return
            
        columns = list(data[0].keys())
        placeholders = ", ".join(["?" for _ in columns])
        column_names = ", ".join(columns)
        
        query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        
        try:
            values = [[row.get(col) for col in columns] for row in data]
            self.cursor.executemany(query, values)
            self.connection.commit()
            self.logger.info(f"Inserted {len(data)} rows into '{table_name}'")
        except sqlite3.Error as e:
            self.logger.error(f"Error inserting data: {e}")
            raise
            
    def query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results.
        
        Args:
            query: SQL query string
            params: Optional parameters for the query
            
        Returns:
            List of dictionaries containing query results
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
                
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            self.logger.error(f"Error executing query: {e}")
            raise
            
    def update_data(self, table_name: str, updates: Dict[str, Any], 
                    condition: str, params: Optional[tuple] = None):
        """
        Update data in a table.
        
        Args:
            table_name: Name of the table
            updates: Dictionary of columns to update and their new values
            condition: WHERE clause condition
            params: Parameters for the condition
        """
        set_clause = ", ".join([f"{col} = ?" for col in updates.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        
        try:
            values = list(updates.values())
            if params:
                values.extend(params)
            self.cursor.execute(query, values)
            self.connection.commit()
            self.logger.info(f"Updated rows in '{table_name}'")
        except sqlite3.Error as e:
            self.logger.error(f"Error updating data: {e}")
            raise
            
    def delete_data(self, table_name: str, condition: str, params: Optional[tuple] = None):
        """
        Delete data from a table.
        
        Args:
            table_name: Name of the table
            condition: WHERE clause condition
            params: Parameters for the condition
        """
        query = f"DELETE FROM {table_name} WHERE {condition}"
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            self.logger.info(f"Deleted rows from '{table_name}'")
        except sqlite3.Error as e:
            self.logger.error(f"Error deleting data: {e}")
            raise
            
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.
        
        Args:
            table_name: Name of the table to check
            
        Returns:
            True if table exists, False otherwise
        """
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        self.cursor.execute(query, (table_name,))
        return self.cursor.fetchone() is not None
        
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get the schema of a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of column information
        """
        query = f"PRAGMA table_info({table_name})"
        self.cursor.execute(query)
        return [dict(row) for row in self.cursor.fetchall()]
        
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
