"""
Data Query Workflow
Main workflow orchestrator for extracting and managing data.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

from .database.sqlite_manager import SQLiteManager
from .extractors.web_extractor import WebExtractor
from .extractors.excel_extractor import ExcelExtractor
from .utils.logger import setup_logger


class DataQueryWorkflow:
    """
    Main workflow class for data extraction and management.
    """
    
    def __init__(self, db_path: str = "data_query.db", log_level: int = logging.INFO):
        """
        Initialize the data query workflow.
        
        Args:
            db_path: Path to SQLite database
            log_level: Logging level
        """
        self.logger = setup_logger("DataQueryWorkflow", log_level)
        self.db_manager = SQLiteManager(db_path)
        self.web_extractor = WebExtractor()
        self.excel_extractor = ExcelExtractor()
        self.logger.info("Data Query Workflow initialized")
        
    def extract_from_web(self, url: str, extraction_type: str = "table",
                        **kwargs) -> List[Dict[str, Any]]:
        """
        Extract data from a web source.
        
        Args:
            url: URL to extract data from
            extraction_type: Type of extraction (table, elements, links, custom)
            **kwargs: Additional arguments for specific extraction types
            
        Returns:
            Extracted data as list of dictionaries
        """
        self.logger.info(f"Extracting data from web: {url}")
        
        if extraction_type == "table":
            data = self.web_extractor.extract_table(url, **kwargs)
        elif extraction_type == "elements":
            data = self.web_extractor.extract_elements(url, **kwargs)
        elif extraction_type == "links":
            data = self.web_extractor.extract_links(url, **kwargs)
        elif extraction_type == "custom":
            result = self.web_extractor.extract_custom(url, **kwargs)
            data = [result] if isinstance(result, dict) else result
        else:
            self.logger.error(f"Unknown extraction type: {extraction_type}")
            data = []
            
        self.logger.info(f"Extracted {len(data)} items from web")
        return data
        
    def extract_from_excel(self, file_path: str, sheet_name: Optional[str] = None,
                          **kwargs) -> List[Dict[str, Any]]:
        """
        Extract data from an Excel file.
        
        Args:
            file_path: Path to Excel file
            sheet_name: Optional sheet name
            **kwargs: Additional arguments for extraction
            
        Returns:
            Extracted data as list of dictionaries
        """
        self.logger.info(f"Extracting data from Excel: {file_path}")
        
        if sheet_name:
            data = self.excel_extractor.read_excel_pandas(file_path, sheet_name=sheet_name, **kwargs)
        else:
            data = self.excel_extractor.read_excel_pandas(file_path, **kwargs)
            
        self.logger.info(f"Extracted {len(data)} rows from Excel")
        return data
        
    def save_to_database(self, table_name: str, data: List[Dict[str, Any]],
                        schema: Optional[Dict[str, str]] = None,
                        create_table: bool = True):
        """
        Save extracted data to SQLite database.
        
        Args:
            table_name: Name of the table to save to
            data: Data to save
            schema: Optional table schema (for table creation)
            create_table: Whether to create the table if it doesn't exist
        """
        if not data:
            self.logger.warning("No data to save")
            return
            
        self.logger.info(f"Saving {len(data)} rows to table '{table_name}'")
        
        with self.db_manager:
            if create_table:
                if schema:
                    self.db_manager.create_table(table_name, schema)
                else:
                    # Auto-generate schema from first row
                    schema = {col: "TEXT" for col in data[0].keys()}
                    self.db_manager.create_table(table_name, schema)
                    
            self.db_manager.insert_data(table_name, data)
            
        self.logger.info("Data saved successfully")
        
    def query_database(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Query data from the database.
        
        Args:
            query: SQL query string
            params: Optional query parameters
            
        Returns:
            Query results as list of dictionaries
        """
        self.logger.info(f"Executing query: {query}")
        
        with self.db_manager:
            results = self.db_manager.query(query, params)
            
        self.logger.info(f"Query returned {len(results)} rows")
        return results
        
    def web_to_database(self, url: str, table_name: str, 
                       extraction_type: str = "table",
                       schema: Optional[Dict[str, str]] = None,
                       **kwargs):
        """
        Extract data from web and save directly to database.
        
        Args:
            url: URL to extract data from
            table_name: Name of database table
            extraction_type: Type of extraction
            schema: Optional table schema
            **kwargs: Additional extraction arguments
        """
        data = self.extract_from_web(url, extraction_type, **kwargs)
        if data:
            self.save_to_database(table_name, data, schema)
            
    def excel_to_database(self, file_path: str, table_name: str,
                         sheet_name: Optional[str] = None,
                         schema: Optional[Dict[str, str]] = None,
                         **kwargs):
        """
        Extract data from Excel and save directly to database.
        
        Args:
            file_path: Path to Excel file
            table_name: Name of database table
            sheet_name: Optional sheet name
            schema: Optional table schema
            **kwargs: Additional extraction arguments
        """
        data = self.extract_from_excel(file_path, sheet_name, **kwargs)
        if data:
            self.save_to_database(table_name, data, schema)
            
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        Get information about a table in the database.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary containing table information
        """
        with self.db_manager:
            if not self.db_manager.table_exists(table_name):
                return {"exists": False, "schema": []}
                
            schema = self.db_manager.get_table_schema(table_name)
            count_query = f"SELECT COUNT(*) as count FROM {table_name}"
            count = self.db_manager.query(count_query)[0]['count']
            
            return {
                "exists": True,
                "schema": schema,
                "row_count": count
            }
            
    def transform_and_save(self, source_table: str, dest_table: str,
                          transformation_query: str,
                          schema: Optional[Dict[str, str]] = None):
        """
        Transform data from one table and save to another.
        
        Args:
            source_table: Source table name
            dest_table: Destination table name
            transformation_query: SQL query for transformation
            schema: Optional schema for destination table
        """
        self.logger.info(f"Transforming data from '{source_table}' to '{dest_table}'")
        
        with self.db_manager:
            # Get transformed data
            data = self.db_manager.query(transformation_query)
            
            if not data:
                self.logger.warning("No data to transform")
                return
                
            # Create destination table if needed
            if schema:
                self.db_manager.create_table(dest_table, schema)
            else:
                schema = {col: "TEXT" for col in data[0].keys()}
                self.db_manager.create_table(dest_table, schema)
                
            # Insert transformed data
            self.db_manager.insert_data(dest_table, data)
            
        self.logger.info(f"Transformed {len(data)} rows")
