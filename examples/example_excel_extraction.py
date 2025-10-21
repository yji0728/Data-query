"""
Example: Excel Data Extraction
This example demonstrates how to extract data from Excel files and save it to SQLite.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_query import DataQueryWorkflow
import pandas as pd


def create_sample_excel():
    """Create a sample Excel file for demonstration."""
    # Create sample data
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Age': [25, 30, 35, 40, 45],
        'City': ['New York', 'London', 'Paris', 'Tokyo', 'Sydney'],
        'Salary': [50000, 60000, 70000, 80000, 90000]
    }
    
    df = pd.DataFrame(data)
    
    # Save to Excel
    output_path = Path(__file__).parent / "sample_data.xlsx"
    df.to_excel(output_path, index=False, sheet_name='Employees')
    
    return str(output_path)


def main():
    # Initialize workflow
    workflow = DataQueryWorkflow(db_path="example_excel.db")
    
    print("=" * 60)
    print("Excel Data Extraction Example")
    print("=" * 60)
    
    # Create sample Excel file
    print("\n1. Creating sample Excel file...")
    excel_path = create_sample_excel()
    print(f"   Created: {excel_path}")
    
    # Example 1: Extract data from Excel
    print("\n2. Extracting data from Excel...")
    try:
        data = workflow.extract_from_excel(excel_path, sheet_name='Employees')
        print(f"   Extracted {len(data)} rows")
        print(f"   Sample data: {data[0] if data else 'None'}")
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Example 2: Save to database
    print("\n3. Saving to database...")
    try:
        schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "Name": "TEXT",
            "Age": "INTEGER",
            "City": "TEXT",
            "Salary": "INTEGER"
        }
        workflow.save_to_database("employees", data, schema=schema)
        print("   Saved to database table 'employees'")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 3: Query saved data
    print("\n4. Querying saved data...")
    try:
        # Query all employees
        results = workflow.query_database("SELECT * FROM employees")
        print(f"   Total employees: {len(results)}")
        
        # Query with filter
        results = workflow.query_database(
            "SELECT * FROM employees WHERE Age > ?", (30,)
        )
        print(f"   Employees older than 30: {len(results)}")
        for row in results:
            print(f"   - {row['Name']}, {row['Age']} years old, {row['City']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 4: Get table information
    print("\n5. Getting table information...")
    try:
        info = workflow.get_table_info("employees")
        print(f"   Table exists: {info['exists']}")
        print(f"   Row count: {info['row_count']}")
        print(f"   Schema: {len(info['schema'])} columns")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
