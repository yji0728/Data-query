# Data Query Framework - Detailed Specification

## 1. Overview

The Data Query Framework is a comprehensive Python-based solution for extracting, transforming, and managing data from various sources. It provides a unified interface for working with web data and Excel files, storing results in a lightweight SQLite database.

## 2. Architecture

### 2.1 Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    DataQueryWorkflow                         │
│                  (Main Orchestrator)                         │
└──────────────┬──────────────────────────┬───────────────────┘
               │                          │
       ┌───────▼──────┐          ┌───────▼──────────┐
       │  Extractors   │          │  Database Manager │
       └───────┬───────┘          └──────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐  ┌─────▼────────┐
│WebExtractor │  │ExcelExtractor│
└─────────────┘  └──────────────┘
```

### 2.2 Data Flow

1. **Data Source** → Extractor (Web/Excel)
2. **Extractor** → Raw Data (List[Dict])
3. **Raw Data** → SQLiteManager
4. **SQLiteManager** → Database Storage
5. **Database** → Query Results
6. **Query Results** → Analysis/Transformation

## 3. Module Specifications

### 3.1 SQLiteManager

**Purpose**: Manage all SQLite database operations

**Key Features**:
- Connection management with context manager support
- Table creation with custom schemas
- CRUD operations (Create, Read, Update, Delete)
- Transaction handling
- Parameterized queries for security

**Methods**:
```python
connect() -> None
close() -> None
create_table(table_name: str, schema: Dict[str, str]) -> None
insert_data(table_name: str, data: List[Dict]) -> None
query(query: str, params: Optional[tuple]) -> List[Dict]
update_data(table_name: str, updates: Dict, condition: str, params: Optional[tuple]) -> None
delete_data(table_name: str, condition: str, params: Optional[tuple]) -> None
table_exists(table_name: str) -> bool
get_table_schema(table_name: str) -> List[Dict]
```

**Schema Definition**:
- Tables are created with explicit type definitions
- Supports all SQLite data types: INTEGER, TEXT, REAL, BLOB, NULL
- Primary keys and constraints can be defined
- Auto-increment supported

### 3.2 WebExtractor

**Purpose**: Extract data from web sources

**Key Features**:
- HTTP request handling with custom headers
- HTML parsing with BeautifulSoup
- Multiple extraction modes
- CSS selector support
- Configurable timeout and retry logic

**Extraction Types**:

1. **Table Extraction**:
   - Extracts HTML tables
   - Automatic header detection
   - Supports CSS selectors for specific tables

2. **Element Extraction**:
   - Extract specific HTML elements
   - Support for attributes extraction
   - Multiple elements support

3. **Link Extraction**:
   - Extract all links from a page
   - Optional filtering by pattern
   - Captures link text and title

4. **Custom Extraction**:
   - Configuration-based extraction
   - Support for complex nested structures
   - Multiple field extraction

**Methods**:
```python
fetch_url(url: str, timeout: int) -> Optional[str]
parse_html(html: str, parser: str) -> Optional[BeautifulSoup]
extract_table(url: str, table_selector: Optional[str]) -> List[Dict]
extract_elements(url: str, selector: str, attributes: Optional[List]) -> List[Dict]
extract_links(url: str, filter_pattern: Optional[str]) -> List[Dict]
extract_custom(url: str, extraction_config: Dict) -> Dict
```

### 3.3 ExcelExtractor

**Purpose**: Extract and process data from Excel files

**Key Features**:
- Support for both pandas and openpyxl libraries
- Multiple sheet handling
- Specific range extraction
- Data filtering and transformation
- Column selection

**Methods**:
```python
read_excel_pandas(file_path: str, sheet_name: Optional[Union[str, int]], header: Optional[int], usecols: Optional[List]) -> List[Dict]
read_excel_openpyxl(file_path: str, sheet_name: Optional[str]) -> List[Dict]
get_sheet_names(file_path: str) -> List[str]
read_specific_range(file_path: str, sheet_name: Optional[str], min_row: int, max_row: Optional[int], min_col: int, max_col: Optional[int]) -> List[List]
read_all_sheets(file_path: str) -> Dict[str, List[Dict]]
filter_data(data: List[Dict], filters: Dict) -> List[Dict]
select_columns(data: List[Dict], columns: List[str]) -> List[Dict]
transform_data(data: List[Dict], transformations: Dict[str, callable]) -> List[Dict]
```

### 3.4 DataQueryWorkflow

**Purpose**: Main orchestrator for the entire framework

**Key Features**:
- Unified interface for all operations
- Direct extraction-to-database workflows
- Query execution and result management
- Data transformation pipelines
- Comprehensive logging

**Methods**:
```python
extract_from_web(url: str, extraction_type: str, **kwargs) -> List[Dict]
extract_from_excel(file_path: str, sheet_name: Optional[str], **kwargs) -> List[Dict]
save_to_database(table_name: str, data: List[Dict], schema: Optional[Dict], create_table: bool) -> None
query_database(query: str, params: Optional[tuple]) -> List[Dict]
web_to_database(url: str, table_name: str, extraction_type: str, schema: Optional[Dict], **kwargs) -> None
excel_to_database(file_path: str, table_name: str, sheet_name: Optional[str], schema: Optional[Dict], **kwargs) -> None
get_table_info(table_name: str) -> Dict
transform_and_save(source_table: str, dest_table: str, transformation_query: str, schema: Optional[Dict]) -> None
```

## 4. Data Types and Structures

### 4.1 Data Representation

All extracted data is represented as `List[Dict[str, Any]]`:
```python
[
    {"column1": "value1", "column2": 123, "column3": 45.67},
    {"column1": "value2", "column2": 456, "column3": 89.01},
    ...
]
```

### 4.2 Schema Definition

Schemas are defined as dictionaries:
```python
schema = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "name": "TEXT NOT NULL",
    "age": "INTEGER",
    "salary": "REAL",
    "created_at": "TEXT DEFAULT CURRENT_TIMESTAMP"
}
```

## 5. Use Cases

### 5.1 Web Data Collection

**Scenario**: Collect product information from an e-commerce website

**Workflow**:
1. Extract product table using WebExtractor
2. Store in SQLite database
3. Query for specific products
4. Generate reports

### 5.2 Excel Report Processing

**Scenario**: Process monthly sales reports

**Workflow**:
1. Read Excel file with ExcelExtractor
2. Filter and transform data
3. Save to database
4. Create summary tables with SQL

### 5.3 Data Pipeline

**Scenario**: Regular ETL process

**Workflow**:
1. Extract data from multiple sources
2. Transform and clean data
3. Load into database
4. Execute analytical queries

## 6. Error Handling

### 6.1 Web Extraction Errors
- Connection timeout: Retry with exponential backoff
- Invalid HTML: Log error and skip
- Missing elements: Return empty results

### 6.2 Excel Extraction Errors
- File not found: Raise FileNotFoundError
- Invalid sheet: Raise ValueError
- Corrupted file: Log error and skip

### 6.3 Database Errors
- Connection errors: Retry connection
- SQL syntax errors: Raise with detailed message
- Constraint violations: Log and raise

## 7. Performance Considerations

### 7.1 Database Optimization
- Use transactions for bulk inserts
- Create indexes on frequently queried columns
- Use appropriate data types
- Vacuum database periodically

### 7.2 Web Extraction Optimization
- Implement rate limiting
- Use connection pooling
- Cache parsed HTML when possible
- Implement timeout mechanisms

### 7.3 Excel Processing Optimization
- Use pandas for large files
- Read only necessary columns
- Process data in chunks if needed
- Close file handles properly

## 8. Security Considerations

### 8.1 SQL Injection Prevention
- Always use parameterized queries
- Validate table and column names
- Sanitize user input

### 8.2 Web Scraping Ethics
- Respect robots.txt
- Implement rate limiting
- Use appropriate User-Agent headers
- Handle errors gracefully

### 8.3 Data Privacy
- Don't store sensitive data in plain text
- Implement access controls
- Log access to sensitive data
- Secure database file permissions

## 9. Testing Strategy

### 9.1 Unit Tests
- Test each module independently
- Mock external dependencies
- Test edge cases and error conditions
- Achieve >80% code coverage

### 9.2 Integration Tests
- Test complete workflows
- Test with real data sources
- Verify database integrity
- Test error recovery

### 9.3 Performance Tests
- Benchmark large data extractions
- Test database query performance
- Monitor memory usage
- Test concurrent operations

## 10. Deployment

### 10.1 Requirements
- Python 3.8+
- SQLite3
- Required packages from requirements.txt

### 10.2 Installation
```bash
pip install -r requirements.txt
```

### 10.3 Configuration
- Edit config/config.yaml
- Set database path
- Configure logging level
- Set extraction timeouts

## 11. Maintenance

### 11.1 Database Maintenance
- Regular backups
- Vacuum operation
- Index optimization
- Schema migrations

### 11.2 Code Maintenance
- Regular dependency updates
- Code review process
- Documentation updates
- Performance monitoring

## 12. Future Enhancements

### 12.1 Planned Features
- Support for more data sources (CSV, JSON, APIs)
- Advanced web scraping with JavaScript rendering (Selenium/Playwright)
- Data validation and cleaning utilities
- Export to multiple formats (CSV, JSON, XML)
- GUI interface for non-programmers
- Scheduling and automation features
- Cloud database support (PostgreSQL, MySQL)
- Async operations for better performance
- Plugin system for custom extractors
- Data versioning and history

### 12.2 API Enhancements
- RESTful API wrapper
- GraphQL support
- Webhooks for data updates
- Real-time data streaming

## 13. License

MIT License - Open source and free to use

## 14. References

- Microsoft Power Query: https://powerquery.microsoft.com/
- SQLite Documentation: https://www.sqlite.org/docs.html
- BeautifulSoup Documentation: https://www.crummy.com/software/BeautifulSoup/
- Pandas Documentation: https://pandas.pydata.org/docs/
- Python Best Practices: https://docs.python-guide.org/