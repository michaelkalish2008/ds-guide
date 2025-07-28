# Cheese Manufacturing Database

This directory contains the main database files for the cheese manufacturing dataset.

## Database Files

- **`cheese_manufacturing.db`** - Main SQLite database containing the complete cheese manufacturing dataset
- **`test.db`** - Test database for development and testing purposes
- **`test_database.db`** - Additional test database for development and testing

## Quick Start

### Access the Database

```python
import sqlite3
import pandas as pd

# Connect to the main database
conn = sqlite3.connect('src/database/db/cheese_manufacturing.db')

# Or connect to test databases
# conn = sqlite3.connect('src/database/db/test.db')
# conn = sqlite3.connect('src/database/db/test_database.db')

# Example: Load manufacturing data
manufacturing_data = pd.read_sql_query("""
    SELECT * FROM cheese_manufacturing_batches 
    LIMIT 10
""", conn)

print(f"Loaded {len(manufacturing_data)} records")
conn.close()
```

### Database Overview

The cheese manufacturing database contains comprehensive data across the entire manufacturing pipeline:

- **Manufacturing Batches**: 496 records
- **Aging Lots**: 5,456 records  
- **Quality Tests**: 155 records
- **Packaging Operations**: 1,984 records
- **Shipments**: 265 records
- **Weighing & Pricing**: 31 records

### Key Tables

- `cheese_manufacturing_batches` - Core manufacturing data
- `aging_lots` - Aging and maturation process data
- `quality_tests` - Quality control and testing results
- `packaging_operations` - Packaging efficiency and costs
- `shipments` - Shipping and logistics data
- `weighing_pricing` - Pricing and yield management

## Documentation

For detailed information about the database schema, queries, and usage examples, see:
- `../docs/guides/DATABASE_GUIDE.md` - Complete database guide
- `../docs/guides/DATA_DICTIONARY.md` - Detailed data dictionary
- `../docs/guides/DB_QUERYING.md` - Query examples and patterns
- `../docs/ORGANIZATION_SUMMARY.md` - Database directory organization

## Development

For database development, testing, and maintenance scripts, see the `../scripts/` directory. 