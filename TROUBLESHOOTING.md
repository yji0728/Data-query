# Troubleshooting Guide

Common issues and their solutions for the Data Query Framework.

## Installation Issues

### Problem: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'bs4'
ModuleNotFoundError: No module named 'pandas'
```

**Solution:**
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install specific packages
pip install beautifulsoup4 pandas openpyxl requests lxml
```

### Problem: Permission Denied

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Database Issues

### Problem: Database is Locked

**Error:**
```
sqlite3.OperationalError: database is locked
```

**Solution:**
```python
# Always use context managers
with SQLiteManager("data.db") as manager:
    manager.query("SELECT * FROM table")
# Connection automatically closed

# Or explicitly close connections
manager = SQLiteManager("data.db")
manager.connect()
try:
    # Your operations
    pass
finally:
    manager.close()
```

### Problem: Table Already Exists

**Error:**
```
sqlite3.OperationalError: table already exists
```

**Solution:**
```python
# Check if table exists first
with SQLiteManager("data.db") as manager:
    if not manager.table_exists("my_table"):
        manager.create_table("my_table", schema)
    else:
        print("Table already exists")

# Or use IF NOT EXISTS (default behavior)
manager.create_table("my_table", schema)  # Already uses IF NOT EXISTS
```

### Problem: SQL Syntax Error

**Error:**
```
sqlite3.OperationalError: near "SELECT": syntax error
```

**Solution:**
```python
# Always use parameterized queries
# WRONG:
query = f"SELECT * FROM users WHERE id = {user_id}"

# CORRECT:
query = "SELECT * FROM users WHERE id = ?"
results = manager.query(query, (user_id,))

# For multiple parameters
query = "SELECT * FROM users WHERE age > ? AND city = ?"
results = manager.query(query, (30, "London"))
```

## Web Extraction Issues

### Problem: Connection Timeout

**Error:**
```
requests.exceptions.ConnectTimeout: Connection timeout
```

**Solution:**
```python
# Increase timeout
extractor = WebExtractor()
html = extractor.fetch_url(url, timeout=60)  # 60 seconds

# Add retry logic
import time
for attempt in range(3):
    try:
        html = extractor.fetch_url(url)
        break
    except Exception as e:
        if attempt < 2:
            time.sleep(2 ** attempt)  # Exponential backoff
        else:
            raise
```

### Problem: No Table Found

**Error:**
```
WARNING: No table found on page
```

**Solution:**
```python
# Verify the page has a table
# Option 1: Use specific CSS selector
data = extractor.extract_table(url, table_selector="table.data-table")

# Option 2: Check the HTML structure
html = extractor.fetch_url(url)
soup = extractor.parse_html(html)
tables = soup.find_all('table')
print(f"Found {len(tables)} tables")

# Option 3: Use custom extraction
extraction_config = {
    'data': {'selector': 'div.data-row', 'multiple': True}
}
data = extractor.extract_custom(url, extraction_config)
```

### Problem: 403 Forbidden or 401 Unauthorized

**Error:**
```
requests.exceptions.HTTPError: 403 Forbidden
```

**Solution:**
```python
# Add proper headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9',
}
extractor = WebExtractor(headers=headers)

# Some sites require authentication
session = extractor.session
session.auth = ('username', 'password')

# Or use cookies
session.cookies.set('session_id', 'your_session_id')
```

### Problem: JavaScript-Rendered Content Not Available

**Issue:** Page loads in browser but extractor gets empty content

**Solution:**
```python
# For JavaScript-heavy sites, consider using Selenium or Playwright
# This framework uses static HTML parsing, which works for most sites
# For dynamic content, you may need additional tools:

# Option 1: Check if there's an API endpoint
# Many sites have JSON APIs that are easier to work with

# Option 2: Use Selenium (separate installation required)
# from selenium import webdriver
# driver = webdriver.Chrome()
# driver.get(url)
# html = driver.page_source
# soup = BeautifulSoup(html, 'lxml')
```

## Excel Extraction Issues

### Problem: File Not Found

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data.xlsx'
```

**Solution:**
```python
# Use absolute paths
import os
file_path = os.path.abspath("data.xlsx")
data = extractor.read_excel_pandas(file_path)

# Or use Path from pathlib
from pathlib import Path
file_path = Path(__file__).parent / "data.xlsx"
data = extractor.read_excel_pandas(str(file_path))

# Check if file exists
if Path(file_path).exists():
    data = extractor.read_excel_pandas(file_path)
else:
    print(f"File not found: {file_path}")
```

### Problem: Invalid Sheet Name

**Error:**
```
ValueError: Worksheet named 'Sheet1' not found
```

**Solution:**
```python
# Get available sheet names first
extractor = ExcelExtractor()
sheets = extractor.get_sheet_names("data.xlsx")
print(f"Available sheets: {sheets}")

# Then use correct sheet name
data = extractor.read_excel_pandas("data.xlsx", sheet_name=sheets[0])

# Or read all sheets
all_data = extractor.read_all_sheets("data.xlsx")
for sheet_name, data in all_data.items():
    print(f"Sheet '{sheet_name}': {len(data)} rows")
```

### Problem: Memory Error with Large Files

**Error:**
```
MemoryError: Unable to allocate array
```

**Solution:**
```python
# For large files, read in chunks or specific columns only
# Read specific columns
data = extractor.read_excel_pandas(
    "large_file.xlsx",
    usecols=['Column1', 'Column2', 'Column3']
)

# Read specific range with openpyxl
data = extractor.read_specific_range(
    "large_file.xlsx",
    min_row=1,
    max_row=10000  # First 10000 rows only
)

# Process in batches
import pandas as pd
chunk_size = 1000
for chunk in pd.read_excel("large_file.xlsx", chunksize=chunk_size):
    # Process each chunk
    workflow.save_to_database("data", chunk.to_dict('records'))
```

### Problem: Corrupted Excel File

**Error:**
```
BadZipFile: File is not a zip file
```

**Solution:**
```python
# Try opening with different engines
try:
    data = extractor.read_excel_pandas("file.xlsx", engine='openpyxl')
except Exception as e:
    print(f"openpyxl failed: {e}")
    try:
        data = extractor.read_excel_pandas("file.xlsx", engine='xlrd')
    except Exception as e:
        print(f"xlrd also failed: {e}")

# Or try repairing the file with Excel/LibreOffice first
```

## Workflow Issues

### Problem: Import Error

**Error:**
```
ImportError: cannot import name 'DataQueryWorkflow'
```

**Solution:**
```python
# Check your Python path
import sys
sys.path.insert(0, '/path/to/Data-query/src')

# Or install the package
# pip install -e .  # In development mode

# Correct import
from data_query import DataQueryWorkflow
# NOT: from src.data_query import DataQueryWorkflow (unless running examples)
```

### Problem: Logging Not Working

**Issue:** No log messages appear

**Solution:**
```python
import logging

# Set logging level explicitly
workflow = DataQueryWorkflow(db_path="data.db", log_level=logging.DEBUG)

# Or configure logging globally
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Performance Issues

### Problem: Slow Database Operations

**Issue:** Large inserts take too long

**Solution:**
```python
# Use transactions for bulk inserts
with SQLiteManager("data.db") as manager:
    # All operations in a single transaction
    manager.create_table("large_table", schema)
    manager.insert_data("large_table", large_data_list)
    # Commit happens automatically when context exits

# Create indexes for frequently queried columns
with SQLiteManager("data.db") as manager:
    manager.cursor.execute("CREATE INDEX idx_name ON users(name)")
    manager.connection.commit()
```

### Problem: High Memory Usage

**Issue:** Script uses too much memory

**Solution:**
```python
# Process data in chunks
chunk_size = 1000
for i in range(0, len(large_data), chunk_size):
    chunk = large_data[i:i+chunk_size]
    workflow.save_to_database("table", chunk, create_table=(i==0))

# Don't load all data at once
# Use generators when possible
def data_generator(file_path):
    # Yield data in chunks
    pass

for chunk in data_generator("large_file.xlsx"):
    workflow.save_to_database("table", chunk)
```

## Testing Issues

### Problem: Tests Fail on Clean Database

**Issue:** Tests expect data that doesn't exist

**Solution:**
```python
import unittest
import os

class TestMyCode(unittest.TestCase):
    def setUp(self):
        """Create fresh database for each test"""
        self.db_path = "/tmp/test_db.db"
        self.workflow = DataQueryWorkflow(db_path=self.db_path)
        # Setup test data
        
    def tearDown(self):
        """Clean up after each test"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
```

## Getting More Help

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
workflow = DataQueryWorkflow(log_level=logging.DEBUG)
```

### Check Version Information

```python
import sys
import pandas
import requests
import bs4

print(f"Python: {sys.version}")
print(f"Pandas: {pandas.__version__}")
print(f"Requests: {requests.__version__}")
print(f"BeautifulSoup: {bs4.__version__}")
```

### Report Issues

If you encounter a bug or have questions:

1. Check this troubleshooting guide
2. Review the [README.md](README.md) and [SPECIFICATION.md](SPECIFICATION.md)
3. Look at [examples/](examples/) for working code
4. Search existing issues on GitHub
5. Create a new issue with:
   - Error message
   - Minimal code to reproduce
   - Environment details (Python version, OS)
   - What you've already tried

## Best Practices to Avoid Issues

1. **Always close database connections**
   - Use context managers (`with` statement)
   - Or explicitly call `.close()`

2. **Use parameterized queries**
   - Prevents SQL injection
   - Handles special characters correctly

3. **Handle exceptions**
   - Wrap operations in try-except blocks
   - Log errors for debugging

4. **Validate inputs**
   - Check file existence
   - Verify URLs are accessible
   - Validate data before insertion

5. **Test with small datasets first**
   - Verify logic works
   - Then scale to full dataset

6. **Use virtual environments**
   - Isolate dependencies
   - Avoid version conflicts

7. **Keep dependencies updated**
   - Regularly update packages
   - Test after updates

8. **Read documentation**
   - Check README for usage examples
   - Review API documentation
   - Look at example scripts
