# Data Query Framework

A comprehensive Python framework for extracting data from various sources (web pages, Excel files) and managing it in a lightweight SQLite database.

## Features

- **Web Data Extraction**: Extract tables, links, and custom elements from web pages
- **Excel Data Extraction**: Read and process Excel files with multiple sheets
- **SQLite Database Management**: Store, query, and manage extracted data
- **Workflow Orchestration**: Complete data pipeline from extraction to storage
- **Flexible Query System**: Support for complex SQL queries and data transformations
- **Logging and Error Handling**: Comprehensive logging for debugging and monitoring

## Inspiration

This framework is inspired by Microsoft's Power Query and other data extraction tools available on GitHub. It provides a lightweight, Python-based solution for data extraction and management workflows.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Project Structure

```
Data-query/
├── src/
│   └── data_query/
│       ├── __init__.py
│       ├── workflow.py              # Main workflow orchestrator
│       ├── database/
│       │   ├── __init__.py
│       │   └── sqlite_manager.py   # SQLite database manager
│       ├── extractors/
│       │   ├── __init__.py
│       │   ├── web_extractor.py    # Web data extractor
│       │   └── excel_extractor.py  # Excel data extractor
│       └── utils/
│           ├── __init__.py
│           └── logger.py           # Logging utilities
├── tests/                          # Unit tests
├── examples/                       # Example scripts
├── config/                         # Configuration files
└── requirements.txt               # Python dependencies
```

## Quick Start

### Basic Usage

```python
from data_query import DataQueryWorkflow

# Initialize the workflow
workflow = DataQueryWorkflow(db_path="mydata.db")

# Extract data from a web page
data = workflow.extract_from_web(
    url="https://example.com/table",
    extraction_type="table"
)

# Save to database
workflow.save_to_database("mytable", data)

# Query the data
results = workflow.query_database("SELECT * FROM mytable LIMIT 10")
print(results)
```

### Extract from Excel

```python
from data_query import DataQueryWorkflow

workflow = DataQueryWorkflow()

# Extract from Excel file
data = workflow.extract_from_excel(
    file_path="data.xlsx",
    sheet_name="Sheet1"
)

# Save to database with schema
schema = {
    "id": "INTEGER PRIMARY KEY",
    "name": "TEXT",
    "value": "REAL"
}
workflow.save_to_database("excel_data", data, schema=schema)
```

### Complete Workflow

```python
from data_query import DataQueryWorkflow

workflow = DataQueryWorkflow(db_path="workflow.db")

# Direct Excel to Database
workflow.excel_to_database(
    file_path="sales.xlsx",
    table_name="sales",
    sheet_name="Q1_Sales"
)

# Query and analyze
results = workflow.query_database("""
    SELECT product, SUM(quantity) as total_sales
    FROM sales
    GROUP BY product
    ORDER BY total_sales DESC
""")

# Transform and save to new table
workflow.transform_and_save(
    source_table="sales",
    dest_table="sales_summary",
    transformation_query="SELECT product, AVG(price) as avg_price FROM sales GROUP BY product"
)
```

## Examples

The `examples/` directory contains complete working examples:

1. **example_web_extraction.py**: Demonstrates web data extraction
2. **example_excel_extraction.py**: Shows Excel file processing
3. **example_complete_workflow.py**: Complete end-to-end workflow

Run an example:

```bash
python examples/example_complete_workflow.py
```

## Core Components

### SQLiteManager

Manages all SQLite database operations:

- Create tables with custom schemas
- Insert, update, delete data
- Execute complex queries
- Transaction management
- Context manager support

### WebExtractor

Extract data from web sources:

- Extract HTML tables
- Extract specific elements using CSS selectors
- Extract links
- Custom extraction with configuration
- Configurable headers and timeout

### ExcelExtractor

Process Excel files:

- Read single or multiple sheets
- Filter and transform data
- Select specific columns
- Support for both pandas and openpyxl
- Handle multiple data formats

### DataQueryWorkflow

Main orchestrator that combines all components:

- Unified interface for all operations
- Direct extraction-to-database workflows
- Query and analysis capabilities
- Data transformation pipelines
- Comprehensive logging

## API Reference

### DataQueryWorkflow

```python
workflow = DataQueryWorkflow(db_path="data.db", log_level=logging.INFO)

# Extract from web
data = workflow.extract_from_web(url, extraction_type="table", **kwargs)

# Extract from Excel
data = workflow.extract_from_excel(file_path, sheet_name=None, **kwargs)

# Save to database
workflow.save_to_database(table_name, data, schema=None, create_table=True)

# Query database
results = workflow.query_database(query, params=None)

# Direct workflows
workflow.web_to_database(url, table_name, extraction_type="table", **kwargs)
workflow.excel_to_database(file_path, table_name, sheet_name=None, **kwargs)

# Get table information
info = workflow.get_table_info(table_name)

# Transform data
workflow.transform_and_save(source_table, dest_table, transformation_query, schema=None)
```

## Configuration

Create a `config.yaml` file to customize the framework:

```yaml
database:
  path: "data_query.db"
  
logging:
  level: "INFO"
  file: "data_query.log"
  
web_extraction:
  timeout: 30
  headers:
    User-Agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```

## Testing

Run the test suite:

```bash
python -m unittest discover tests
```

Run specific test:

```bash
python -m unittest tests.test_sqlite_manager
```

## Use Cases

1. **Data Collection**: Scrape data from websites and store in a database
2. **Report Automation**: Extract data from Excel reports and transform for analysis
3. **Data Pipeline**: Create ETL pipelines for regular data processing
4. **Data Analysis**: Query and analyze data from multiple sources
5. **Data Migration**: Convert Excel data to SQLite for better querying

## Best Practices

1. **Always use context managers** when working with the database
2. **Define schemas** for better data type management
3. **Use parameterized queries** to prevent SQL injection
4. **Handle exceptions** appropriately in production code
5. **Log important operations** for debugging and monitoring
6. **Clean up temporary files** after processing

## Advanced Features

### Custom Web Extraction

```python
extraction_config = {
    'title': {'selector': 'h1.title', 'attribute': None},
    'price': {'selector': '.price', 'attribute': None},
    'images': {'selector': 'img.product', 'attribute': 'src', 'multiple': True}
}

data = workflow.extract_from_web(
    url="https://example.com/product",
    extraction_type="custom",
    extraction_config=extraction_config
)
```

### Data Transformation

```python
from data_query.extractors import ExcelExtractor

extractor = ExcelExtractor()
data = extractor.read_excel_pandas("data.xlsx")

# Transform data
transformations = {
    'price': lambda x: float(x) * 1.1,  # Add 10% markup
    'date': lambda x: x.strftime('%Y-%m-%d')
}
transformed = extractor.transform_data(data, transformations)
```

## Troubleshooting

### Common Issues

1. **Module not found**: Ensure you've installed dependencies with `pip install -r requirements.txt`
2. **Database locked**: Close all connections before accessing the database
3. **Web extraction fails**: Check URL accessibility and CSS selectors
4. **Excel file not found**: Use absolute paths or verify the file location

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Inspired by Microsoft Power Query
- Built with Python, SQLite, BeautifulSoup, and pandas
- Thanks to the open source community

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Roadmap

Future enhancements:

- [ ] Support for more data sources (CSV, JSON, APIs)
- [ ] Advanced web scraping with JavaScript rendering
- [ ] Data validation and cleaning utilities
- [ ] Export to multiple formats
- [ ] GUI interface for non-programmers
- [ ] Scheduling and automation features
- [ ] Cloud database support