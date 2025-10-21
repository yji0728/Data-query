"""
Example: Complete Workflow
This example demonstrates a complete data processing workflow.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_query import DataQueryWorkflow
import pandas as pd


def main():
    # Initialize workflow
    workflow = DataQueryWorkflow(db_path="workflow_example.db")
    
    print("=" * 70)
    print("Complete Data Query Workflow Example")
    print("=" * 70)
    
    # Step 1: Create sample Excel data
    print("\n[Step 1] Creating sample data...")
    sales_data = {
        'Date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
        'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop'],
        'Quantity': [2, 5, 3, 1, 1],
        'Price': [1000, 25, 75, 300, 1000],
        'Region': ['North', 'South', 'East', 'West', 'North']
    }
    
    df = pd.DataFrame(sales_data)
    excel_path = Path(__file__).parent / "sales_data.xlsx"
    df.to_excel(excel_path, index=False, sheet_name='Sales')
    print(f"   Created Excel file: {excel_path}")
    
    # Step 2: Extract from Excel and save to database
    print("\n[Step 2] Extracting data from Excel to database...")
    workflow.excel_to_database(
        file_path=str(excel_path),
        table_name="sales",
        sheet_name="Sales"
    )
    print("   Data saved to 'sales' table")
    
    # Step 3: Query and analyze data
    print("\n[Step 3] Analyzing sales data...")
    
    # Total sales by product
    query = """
        SELECT Product, 
               SUM(Quantity) as TotalQuantity,
               SUM(Quantity * Price) as TotalRevenue
        FROM sales
        GROUP BY Product
        ORDER BY TotalRevenue DESC
    """
    results = workflow.query_database(query)
    print("\n   Sales by Product:")
    for row in results:
        print(f"   - {row['Product']}: {row['TotalQuantity']} units, ${row['TotalRevenue']} revenue")
    
    # Total sales by region
    query = """
        SELECT Region,
               COUNT(*) as Transactions,
               SUM(Quantity * Price) as TotalRevenue
        FROM sales
        GROUP BY Region
    """
    results = workflow.query_database(query)
    print("\n   Sales by Region:")
    for row in results:
        print(f"   - {row['Region']}: {row['Transactions']} transactions, ${row['TotalRevenue']} revenue")
    
    # Step 4: Create a summary table
    print("\n[Step 4] Creating summary table...")
    transformation_query = """
        SELECT 
            Product,
            Region,
            SUM(Quantity) as TotalQuantity,
            SUM(Quantity * Price) as TotalRevenue,
            AVG(Price) as AvgPrice
        FROM sales
        GROUP BY Product, Region
    """
    
    workflow.transform_and_save(
        source_table="sales",
        dest_table="sales_summary",
        transformation_query=transformation_query
    )
    print("   Summary table 'sales_summary' created")
    
    # Step 5: Query summary table
    print("\n[Step 5] Querying summary table...")
    results = workflow.query_database("SELECT * FROM sales_summary")
    print(f"\n   Summary ({len(results)} rows):")
    for row in results:
        print(f"   - {row['Product']} in {row['Region']}: "
              f"{row['TotalQuantity']} units, ${row['TotalRevenue']} revenue")
    
    # Step 6: Get database information
    print("\n[Step 6] Database information...")
    for table in ['sales', 'sales_summary']:
        info = workflow.get_table_info(table)
        if info['exists']:
            print(f"\n   Table: {table}")
            print(f"   - Rows: {info['row_count']}")
            print(f"   - Columns: {', '.join([col['name'] for col in info['schema']])}")
    
    print("\n" + "=" * 70)
    print("Workflow completed successfully!")
    print("=" * 70)
    print("\nYou can now use the database 'workflow_example.db' for further analysis.")


if __name__ == "__main__":
    main()
