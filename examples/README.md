# Data Query Framework Examples

This directory contains example scripts demonstrating the capabilities of the Data Query Framework.

## Examples

### 1. example_web_extraction.py

Demonstrates web data extraction capabilities:
- Extracting HTML tables from Wikipedia
- Extracting links from web pages
- Saving extracted data to SQLite database
- Querying saved data

**Run:**
```bash
python examples/example_web_extraction.py
```

### 2. example_excel_extraction.py

Demonstrates Excel file processing:
- Creating sample Excel files
- Extracting data from Excel sheets
- Saving Excel data to database
- Filtering and querying data
- Getting table information

**Run:**
```bash
python examples/example_excel_extraction.py
```

### 3. example_complete_workflow.py

Demonstrates a complete end-to-end data workflow:
- Creating sample data
- Excel to database extraction
- Data analysis with SQL queries
- Creating summary tables
- Data transformation
- Database information retrieval

**Run:**
```bash
python examples/example_complete_workflow.py
```

## Generated Files

When you run these examples, they will generate:
- Excel files (.xlsx) - Sample data files
- SQLite databases (.db) - Database files with extracted data

These generated files are automatically ignored by git (see .gitignore).

## Notes

- All examples use temporary databases that can be safely deleted
- Web extraction examples require internet connectivity
- Examples are self-contained and can run independently
- The framework logs all operations to console for visibility
