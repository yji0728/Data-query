# Data Query Framework Architecture

## System Overview

The Data Query Framework is designed as a modular, extensible system for data extraction and management.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                           User Application                           │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ imports
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DataQueryWorkflow                               │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  • Unified API for all operations                             │  │
│  │  • Workflow orchestration                                     │  │
│  │  • Logging and error handling                                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
└────────┬──────────────────────────────────────────┬─────────────────┘
         │                                          │
         │                                          │
         ▼                                          ▼
┌──────────────────────────┐           ┌──────────────────────────────┐
│   Extractor Layer        │           │   Database Layer             │
│ ┌────────────────────┐   │           │ ┌────────────────────────┐   │
│ │  WebExtractor      │   │           │ │  SQLiteManager         │   │
│ │  • HTTP requests   │   │           │ │  • CRUD operations     │   │
│ │  • HTML parsing    │   │           │ │  • Query execution     │   │
│ │  • CSS selectors   │   │           │ │  • Transaction mgmt    │   │
│ │  • Table extract   │   │           │ │  • Schema management   │   │
│ └────────────────────┘   │           │ └────────────────────────┘   │
│                          │           └──────────────────────────────┘
│ ┌────────────────────┐   │                        │
│ │  ExcelExtractor    │   │                        │
│ │  • Pandas read     │   │                        ▼
│ │  • Openpyxl read   │   │           ┌──────────────────────────────┐
│ │  • Multi-sheet     │   │           │      SQLite Database         │
│ │  • Filtering       │   │           │  ┌────────┐  ┌────────┐     │
│ │  • Transformation  │   │           │  │ Table1 │  │ Table2 │     │
│ └────────────────────┘   │           │  └────────┘  └────────┘     │
└──────────────────────────┘           └──────────────────────────────┘
         │                                          ▲
         │                                          │
         ▼                                          │
┌──────────────────────────┐                       │
│   Data Sources           │                       │
│ • Web Pages              │───────────────────────┘
│ • Excel Files            │     extracted data
│ • HTML Tables            │
└──────────────────────────┘
```

## Component Layers

### 1. User Application Layer
- End-user scripts and applications
- Imports and uses the framework
- Defines workflows and operations

### 2. Workflow Orchestration Layer
**DataQueryWorkflow**
- Main entry point for all operations
- Coordinates between extractors and database
- Provides high-level API
- Manages logging and error handling

### 3. Extractor Layer

**WebExtractor**
- HTTP/HTTPS request handling
- HTML parsing with BeautifulSoup
- CSS selector-based extraction
- Multiple extraction modes:
  - Table extraction
  - Element extraction
  - Link extraction
  - Custom extraction

**ExcelExtractor**
- Excel file reading (pandas/openpyxl)
- Multi-sheet support
- Data filtering
- Column selection
- Data transformation

### 4. Database Layer

**SQLiteManager**
- Connection management
- Table creation and schema definition
- CRUD operations (Create, Read, Update, Delete)
- Parameterized query execution
- Transaction handling
- Context manager support

### 5. Data Storage Layer
- SQLite database files
- Stores extracted data
- Supports complex queries
- ACID compliance

## Data Flow

### Web Extraction Flow

```
URL → WebExtractor.fetch_url() → HTML content
                                      ↓
                      BeautifulSoup parsing
                                      ↓
                      CSS selector extraction
                                      ↓
                      List[Dict] data structure
                                      ↓
                      SQLiteManager.insert_data()
                                      ↓
                      SQLite database
```

### Excel Extraction Flow

```
Excel File → ExcelExtractor.read_excel_*() → Raw data (DataFrame/List)
                                                    ↓
                                    Optional filtering/transformation
                                                    ↓
                                    List[Dict] data structure
                                                    ↓
                                    SQLiteManager.insert_data()
                                                    ↓
                                    SQLite database
```

### Query Flow

```
SQL Query → DataQueryWorkflow.query_database()
                    ↓
         SQLiteManager.query()
                    ↓
         SQLite engine execution
                    ↓
         Result rows
                    ↓
         List[Dict] results
```

## Design Patterns

### 1. Context Manager Pattern
SQLiteManager uses context managers for automatic resource cleanup:
```python
with SQLiteManager("db.db") as manager:
    # Operations here
    pass  # Automatically closes connection
```

### 2. Strategy Pattern
Different extraction strategies for different data sources:
- WebExtractor for web sources
- ExcelExtractor for Excel files
- Unified interface through DataQueryWorkflow

### 3. Facade Pattern
DataQueryWorkflow provides a simplified interface to complex subsystems:
- Hides complexity of extractors and database manager
- Provides unified API
- Simplifies common operations

### 4. Dependency Injection
Components are loosely coupled and can be easily replaced:
- Extractors can be swapped
- Database manager can be replaced with other implementations
- Easy to extend with new extractors

## Extensibility Points

### Adding New Extractors

```python
class CustomExtractor:
    def extract(self, source, **kwargs):
        # Implement extraction logic
        return List[Dict]

# Use with workflow
workflow.custom_extractor = CustomExtractor()
```

### Custom Database Backends

```python
class PostgresManager:
    def __init__(self, connection_string):
        # Implement postgres connection
        pass
    
    # Implement same interface as SQLiteManager

# Use with workflow
workflow.db_manager = PostgresManager("connection_string")
```

### Custom Transformations

```python
def custom_transform(data):
    # Transform data
    return transformed_data

# Use in workflow
data = workflow.extract_from_excel("file.xlsx")
transformed = custom_transform(data)
workflow.save_to_database("table", transformed)
```

## Security Considerations

### SQL Injection Prevention
- Always use parameterized queries
- No string concatenation in SQL
- Validation of table/column names

### Web Scraping Ethics
- Respect robots.txt
- Implement rate limiting
- Use appropriate User-Agent
- Handle errors gracefully

### Data Security
- Secure database file permissions
- Don't log sensitive data
- Validate input data
- Sanitize before storage

## Performance Optimization

### Database
- Use transactions for bulk operations
- Create indexes on frequently queried columns
- Use appropriate data types
- Regular VACUUM operations

### Extractors
- Connection pooling for web requests
- Caching of parsed HTML
- Batch processing for large files
- Memory-efficient streaming for large Excel files

### General
- Lazy loading where possible
- Efficient data structures
- Minimal copying of data
- Resource cleanup with context managers

## Testing Strategy

### Unit Tests
- Test each component independently
- Mock external dependencies
- Test edge cases
- Achieve high code coverage

### Integration Tests
- Test complete workflows
- Test with real data sources
- Verify database integrity
- Test error recovery

### Example Tests
```python
# Unit test
def test_create_table():
    manager = SQLiteManager(":memory:")
    manager.connect()
    schema = {"id": "INTEGER", "name": "TEXT"}
    manager.create_table("test", schema)
    assert manager.table_exists("test")

# Integration test
def test_complete_workflow():
    workflow = DataQueryWorkflow()
    workflow.excel_to_database("test.xlsx", "data")
    results = workflow.query_database("SELECT * FROM data")
    assert len(results) > 0
```

## Deployment Considerations

### Requirements
- Python 3.8+
- SQLite3 (usually included with Python)
- Required packages from requirements.txt

### Installation
```bash
pip install -r requirements.txt
# or
python setup.py install
```

### Configuration
- Edit config/config.yaml for custom settings
- Set environment variables for sensitive data
- Configure logging levels

## Future Architecture Enhancements

### Planned Improvements
1. **Async Operations**
   - Async web requests
   - Concurrent Excel processing
   - Non-blocking database operations

2. **Plugin System**
   - Dynamic extractor loading
   - Custom database backends
   - Transformation plugins

3. **Distributed Processing**
   - Task queue integration (Celery)
   - Distributed caching (Redis)
   - Load balancing

4. **Cloud Support**
   - S3 integration for file storage
   - Cloud database support (RDS, Cloud SQL)
   - Serverless deployment options

5. **Advanced Features**
   - Data validation layer
   - Schema evolution
   - Version control for data
   - Real-time data streaming

## Conclusion

The Data Query Framework is designed to be:
- **Modular**: Easy to extend and maintain
- **Flexible**: Supports multiple data sources
- **Secure**: Built-in security best practices
- **Performant**: Optimized for common operations
- **Testable**: Comprehensive test coverage
- **Production-ready**: Used in real-world applications
