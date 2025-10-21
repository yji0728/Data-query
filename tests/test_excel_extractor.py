"""
Unit tests for Excel Extractor
"""

import unittest
import sys
import os
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_query.extractors import ExcelExtractor


class TestExcelExtractor(unittest.TestCase):
    """Test cases for ExcelExtractor."""
    
    def setUp(self):
        """Set up test Excel file."""
        self.extractor = ExcelExtractor()
        self.test_file = "/tmp/test_data.xlsx"
        
        # Create test data
        data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'London', 'Paris']
        }
        df = pd.DataFrame(data)
        df.to_excel(self.test_file, index=False, sheet_name='TestSheet')
        
    def tearDown(self):
        """Clean up test file."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
            
    def test_read_excel_pandas(self):
        """Test reading Excel with pandas."""
        data = self.extractor.read_excel_pandas(self.test_file, sheet_name='TestSheet')
        self.assertEqual(len(data), 3)
        self.assertIn('Name', data[0])
        self.assertEqual(data[0]['Name'], 'Alice')
        
    def test_read_excel_openpyxl(self):
        """Test reading Excel with openpyxl."""
        data = self.extractor.read_excel_openpyxl(self.test_file, sheet_name='TestSheet')
        self.assertEqual(len(data), 3)
        self.assertIn('Name', data[0])
        
    def test_get_sheet_names(self):
        """Test getting sheet names."""
        sheets = self.extractor.get_sheet_names(self.test_file)
        self.assertIn('TestSheet', sheets)
        
    def test_filter_data(self):
        """Test data filtering."""
        data = self.extractor.read_excel_pandas(self.test_file)
        filtered = self.extractor.filter_data(data, {'City': 'London'})
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['Name'], 'Bob')
        
    def test_select_columns(self):
        """Test column selection."""
        data = self.extractor.read_excel_pandas(self.test_file)
        selected = self.extractor.select_columns(data, ['Name', 'Age'])
        self.assertEqual(len(selected), 3)
        self.assertIn('Name', selected[0])
        self.assertIn('Age', selected[0])
        self.assertNotIn('City', selected[0])
        
    def test_transform_data(self):
        """Test data transformation."""
        data = self.extractor.read_excel_pandas(self.test_file)
        transformations = {
            'Age': lambda x: x + 1
        }
        transformed = self.extractor.transform_data(data, transformations)
        self.assertEqual(transformed[0]['Age'], 26)


if __name__ == "__main__":
    unittest.main()
