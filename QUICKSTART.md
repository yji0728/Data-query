# Quick Start Guide

Get started with the Data Query Framework in 5 minutes!

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yji0728/Data-query.git
cd Data-query
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Your First Data Extraction

### Example 1: Extract from Excel

Create a file `my_first_extraction.py`:

```python
from src.data_query import DataQueryWorkflow
import pandas as pd

# Create sample Excel file
data = {'Name': ['Alice', 'Bob'], 'Score': [95, 87]}
df = pd.DataFrame(data)
df.to_excel('test.xlsx', index=False)

# Initialize workflow
workflow = DataQueryWorkflow(db_path="mydata.db")

# Extract and save
workflow.excel_to_database('test.xlsx', 'students')

# Query the data
results = workflow.query_database("SELECT * FROM students")
print(results)
```

Run it:
```bash
python my_first_extraction.py
```

### Example 2: Web Data Extraction

```python
from src.data_query import DataQueryWorkflow

workflow = DataQueryWorkflow()

# Extract table from a web page
data = workflow.extract_from_web(
    url="https://en.wikipedia.org/wiki/List_of_countries_by_population",
    extraction_type="table"
)

# Save to database
workflow.save_to_database("countries", data[:10])

# Query
results = workflow.query_database("SELECT * FROM countries LIMIT 5")
for row in results:
    print(row)
```

## Run the Examples

The repository includes complete working examples:

```bash
# Complete workflow demonstration
python examples/example_complete_workflow.py

# Excel extraction
python examples/example_excel_extraction.py

# Web extraction (requires internet)
python examples/example_web_extraction.py
```

## Basic Operations

### 1. Initialize Workflow

```python
from src.data_query import DataQueryWorkflow

workflow = DataQueryWorkflow(db_path="mydata.db")
```

### 2. Extract Data

**From Web:**
```python
data = workflow.extract_from_web(
    url="https://example.com",
    extraction_type="table"  # or "links", "elements", "custom"
)
```

**From Excel:**
```python
data = workflow.extract_from_excel(
    file_path="data.xlsx",
    sheet_name="Sheet1"
)
```

### 3. Save to Database

```python
workflow.save_to_database("table_name", data)
```

### 4. Query Data

```python
results = workflow.query_database("SELECT * FROM table_name")
```

### 5. Direct Workflows

**Excel → Database:**
```python
workflow.excel_to_database("file.xlsx", "table_name")
```

**Web → Database:**
```python
workflow.web_to_database("https://example.com", "table_name")
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [SPECIFICATION.md](SPECIFICATION.md) for technical details
- Explore [examples/](examples/) for more use cases
- Run tests: `python -m unittest discover tests`

## Common Issues

**Import errors?**
```bash
# Make sure dependencies are installed
pip install -r requirements.txt
```

**Database locked?**
```python
# Use context managers
with workflow.db_manager:
    # Your operations here
    pass
```

**Web extraction fails?**
- Check internet connection
- Verify the URL is accessible
- Check CSS selectors are correct

## Getting Help

- See full documentation in [README.md](README.md)
- Check examples in [examples/](examples/)
- Review [SPECIFICATION.md](SPECIFICATION.md) for API details

Happy data extracting! 🚀
