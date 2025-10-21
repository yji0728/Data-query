"""
Example: Web Data Extraction
This example demonstrates how to extract data from a web page and save it to SQLite.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_query import DataQueryWorkflow


def main():
    # Initialize workflow
    workflow = DataQueryWorkflow(db_path="example_web.db")
    
    print("=" * 60)
    print("Web Data Extraction Example")
    print("=" * 60)
    
    # Example 1: Extract table from Wikipedia
    print("\n1. Extracting table from Wikipedia...")
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
    
    try:
        # Extract table data
        data = workflow.extract_from_web(
            url=url,
            extraction_type="table",
            table_selector="table.wikitable"
        )
        
        if data:
            print(f"   Extracted {len(data)} rows")
            print(f"   Sample data: {data[0] if data else 'None'}")
            
            # Save to database
            schema = {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "country": "TEXT",
                "population": "TEXT"
            }
            workflow.save_to_database("countries", data[:5], create_table=True)
            print("   Saved to database table 'countries'")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 2: Extract links
    print("\n2. Extracting links from a page...")
    try:
        links = workflow.extract_from_web(
            url="https://example.com",
            extraction_type="links"
        )
        
        if links:
            print(f"   Extracted {len(links)} links")
            for i, link in enumerate(links[:3], 1):
                print(f"   Link {i}: {link.get('text')} -> {link.get('url')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 3: Query saved data
    print("\n3. Querying saved data...")
    try:
        results = workflow.query_database("SELECT * FROM countries LIMIT 3")
        print(f"   Found {len(results)} rows")
        for row in results:
            print(f"   {row}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
