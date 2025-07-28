# Database Querying Guide

This guide covers the database schema, SQLite syntax, and how to query the cheese manufacturing database.

# Browser for SQLite

If you'd like to use a UI for exploring the data, use brew to install and the command below to open.

```bash
# Install
brew install db-browser-for-sqlite

# Open in browser
open -a "DB Browser for SQLite" cheese_manufacturing.db
```

## Database Schema Overview

The cheese manufacturing database is organized into logical modules, each represented by SQL schema files in `src/database/sqlite/`:

### Schema Files

- **`00_master_sqlite_schema.sql`** - Master schema with all table definitions
- **`01_core_architecture.sqlite.sql`** - Core lot and batch tracking
- **`02_raw_materials_suppliers.sqlite.sql`** - Raw materials and supplier management
- **`03_preprocessing_operations.sqlite.sql`** - Preprocessing operations
- **`04_manufacturing_process.sqlite.sql`** - Manufacturing process tracking
- **`05_aging_maturation.sqlite.sql`** - Aging and maturation processes
- **`06_quality_control_testing.sqlite.sql`** - Quality control and testing
- **`07_sensory_analysis.sqlite.sql`** - Sensory analysis and evaluation
- **`08_packaging_operations.sqlite.sql`** - Packaging operations
- **`09_labeling_regulatory.sqlite.sql`** - Labeling and regulatory compliance
- **`10_weighing_pricing_distribution.sqlite.sql`** - Weighing, pricing, and distribution
- **`11_shipping_logistics.sqlite.sql`** - Shipping and logistics
- **`12_advanced_relationships_views.sqlite.sql`** - Advanced views and relationships
- **`13_performance_optimization.sqlite.sql`** - Performance optimization

### Core Tables

#### Lot Master (`lot_master`)
- Primary tracking table for all cheese lots
- Contains lot UUID, number, date, product code, facility code
- See `01_core_architecture.sqlite.sql` for complete table definition

#### Manufacturing Batches (`manufacturing_batches`)
- Tracks individual production batches within lots
- Links to lot_master via lot_number
- See `04_manufacturing_process.sqlite.sql` for complete table definition

#### Quality Tests (`quality_tests`)
- Stores quality control test results
- Links to manufacturing batches
- See `06_quality_control_testing.sqlite.sql` for complete table definition

## SQLite Syntax and Features

### Basic Query Structure

```sql
-- Basic SELECT with WHERE
SELECT column1, column2, column3
FROM table_name
WHERE condition
ORDER BY column1;

-- JOIN example
SELECT lm.lot_number, mb.batch_number, qt.test_result
FROM lot_master lm
JOIN manufacturing_batches mb ON lm.lot_number = mb.lot_number
JOIN quality_tests qt ON mb.batch_id = qt.batch_id
WHERE lm.lot_date >= '2024-01-01';
```

### SQLite-Specific Features

#### 1. Row Factory
```python
import sqlite3

# Enable row factory for dictionary-like access
conn = sqlite3.connect("cheese_manufacturing.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()
cursor.execute("SELECT * FROM lot_master LIMIT 1")
row = cursor.fetchone()

# Access by column name
print(row['lot_number'])
print(row['product_code'])
```

#### 2. Date Functions
```sql
-- SQLite date functions
SELECT 
    lot_date,
    date(lot_date, '+30 days') as aging_date,
    strftime('%Y-%m', lot_date) as month_year
FROM lot_master
WHERE lot_date >= date('now', '-90 days');
```

#### 3. JSON Functions (SQLite 3.38+)
```sql
-- Extract from JSON columns
SELECT 
    lot_number,
    json_extract(metadata, '$.temperature') as temp,
    json_extract(metadata, '$.humidity') as humidity
FROM aging_records
WHERE json_extract(metadata, '$.temperature') > 10;
```

## Query Examples

### Basic Queries

#### 1. Count Total Lots
```python
import sqlite3

conn = sqlite3.connect("cheese_manufacturing.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM lot_master")
total_lots = cursor.fetchone()[0]
print(f"Total lots: {total_lots}")

conn.close()
```

#### 2. Find Lots by Date Range
```python
import sqlite3
from datetime import datetime

conn = sqlite3.connect("cheese_manufacturing.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()
cursor.execute("""
    SELECT lot_number, lot_date, product_code, batch_size_kg
    FROM lot_master
    WHERE lot_date BETWEEN ? AND ?
    ORDER BY lot_date
""", ('2024-01-01', '2024-01-31'))

for row in cursor.fetchall():
    print(f"Lot: {row['lot_number']}, Date: {row['lot_date']}, Product: {row['product_code']}")

conn.close()
```

#### 3. Quality Test Results
```python
import sqlite3

conn = sqlite3.connect("cheese_manufacturing.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()
cursor.execute("""
    SELECT l.lot_number, q.ph_level, q.moisture_content, q.fat_content
    FROM lot_master l
    JOIN quality_tests q ON l.lot_uuid = q.lot_uuid
    WHERE q.ph_level BETWEEN 5.5 AND 6.5
    ORDER BY q.ph_level
""")

for row in cursor.fetchall():
    print(f"Lot: {row['lot_number']}, pH: {row['ph_level']}, Moisture: {row['moisture_content']}%")

conn.close()
```

### Advanced Queries

#### 4. Manufacturing Process Analysis
```python
import sqlite3

conn = sqlite3.connect("cheese_manufacturing.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()
cursor.execute("""
    SELECT 
        l.lot_number,
        l.product_code,
        COUNT(m.batch_uuid) as batch_count,
        AVG(m.temperature_c) as avg_temp,
        AVG(m.duration_minutes) as avg_duration
    FROM lot_master l
    LEFT JOIN manufacturing_batches m ON l.lot_uuid = m.lot_uuid
    GROUP BY l.lot_uuid
    HAVING batch_count > 0
    ORDER BY avg_temp DESC
""")

for row in cursor.fetchall():
    print(f"Lot: {row['lot_number']}, Batches: {row['batch_count']}, Avg Temp: {row['avg_temp']:.1f}°C")

conn.close()
```

#### 5. Supplier Performance Analysis
```python
import sqlite3

conn = sqlite3.connect("cheese_manufacturing.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()
cursor.execute("""
    SELECT 
        s.supplier_name,
        COUNT(r.raw_lot_uuid) as material_lots,
        AVG(r.quality_score) as avg_quality,
        MIN(r.arrival_date) as first_delivery,
        MAX(r.arrival_date) as last_delivery
    FROM suppliers s
    LEFT JOIN raw_material_lots r ON s.supplier_id = r.supplier_id
    WHERE s.active_flag = 1
    GROUP BY s.supplier_id
    HAVING material_lots > 0
    ORDER BY avg_quality DESC
""")

for row in cursor.fetchall():
    print(f"Supplier: {row['supplier_name']}, Quality: {row['avg_quality']:.2f}")

conn.close()
```

#### 6. Complete Workflow Tracking
```python
import sqlite3

conn = sqlite3.connect("cheese_manufacturing.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()
cursor.execute("""
    SELECT 
        l.lot_number,
        l.lot_date,
        l.product_code,
        COUNT(DISTINCT m.batch_uuid) as manufacturing_steps,
        COUNT(DISTINCT q.test_id) as quality_tests,
        COUNT(DISTINCT p.package_id) as packages,
        COUNT(DISTINCT s.shipment_id) as shipments
    FROM lot_master l
    LEFT JOIN manufacturing_batches m ON l.lot_uuid = m.lot_uuid
    LEFT JOIN quality_tests q ON l.lot_uuid = q.lot_uuid
    LEFT JOIN packaging_operations p ON l.lot_uuid = p.lot_uuid
    LEFT JOIN shipping_logistics s ON l.lot_uuid = s.lot_uuid
    GROUP BY l.lot_uuid
    ORDER BY l.lot_date DESC
    LIMIT 10
""")

for row in cursor.fetchall():
    print(f"Lot: {row['lot_number']}, Steps: {row['manufacturing_steps']}, Tests: {row['quality_tests']}")

conn.close()
```

## Running SQL Queries

### From Python

```python
import sqlite3
from pathlib import Path

# Connect to database
db_path = Path("cheese_manufacturing.db")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

# Execute query
cursor = conn.cursor()
cursor.execute("""
    SELECT lot_number, product_code, batch_size_kg
    FROM lot_master
    WHERE lot_date >= '2024-01-01'
    ORDER BY lot_date DESC
    LIMIT 10
""")

# Fetch results
for row in cursor.fetchall():
    print(f"Lot: {row['lot_number']}, Product: {row['product_code']}, Size: {row['batch_size_kg']}kg")

conn.close()
```

**Note**: Run this from the database directory:
```bash
cd src/database
```

### From Terminal

```bash
# Navigate to database directory
cd src/database

# Direct SQLite command line
sqlite3 cheese_manufacturing.db

# In SQLite prompt
.tables                    # List all tables
.schema lot_master        # Show table schema
.headers on               # Enable column headers
.mode csv                 # Set output mode
.output results.csv       # Save to file

# Run query
SELECT lot_number, product_code FROM lot_master LIMIT 5;
.quit
```

### From SQL Files

```python
# Execute SQL from file
def execute_sql_file(conn, sql_file_path):
    with open(sql_file_path, 'r') as file:
        sql_script = file.read()
    
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()

# Usage
execute_sql_file(conn, "src/database/sqlite/01_core_architecture.sqlite.sql")
```

**Note**: Run this from the database directory:
```bash
cd src/database
```

## Creating Reusable Query Functions

### Python Class Approach

```python
class CheeseDatabaseQueries:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
    
    def get_lots_by_date_range(self, start_date, end_date):
        """Get all lots within a date range"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT lot_number, lot_date, product_code, batch_size_kg
            FROM lot_master
            WHERE lot_date BETWEEN ? AND ?
            ORDER BY lot_date
        """, (start_date, end_date))
        return cursor.fetchall()
    
    def get_quality_summary(self, lot_number):
        """Get quality test summary for a specific lot"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                qt.test_type,
                AVG(qt.test_result) as avg_result,
                COUNT(*) as test_count
            FROM quality_tests qt
            JOIN manufacturing_batches mb ON qt.batch_id = mb.batch_id
            WHERE mb.lot_number = ?
            GROUP BY qt.test_type
        """, (lot_number,))
        return cursor.fetchall()
    
    def close(self):
        self.conn.close()

# Usage
db = CheeseDatabaseQueries("cheese_manufacturing.db")
lots = db.get_lots_by_date_range("2024-01-01", "2024-01-31")
quality = db.get_quality_summary("TAL-2024-01-15")
db.close()
```

**Note**: Run this from the database directory:
```bash
cd src/database
```

### SQL Query Files

Create reusable SQL files in a `queries/` directory:

```sql
-- queries/lot_summary.sql
SELECT 
    lm.lot_number,
    lm.lot_date,
    lm.product_code,
    lm.batch_size_kg,
    COUNT(mb.batch_id) as batch_count,
    AVG(qt.test_result) as avg_quality_score
FROM lot_master lm
LEFT JOIN manufacturing_batches mb ON lm.lot_number = mb.lot_number
LEFT JOIN quality_tests qt ON mb.batch_id = qt.batch_id
WHERE lm.lot_date BETWEEN ? AND ?
GROUP BY lm.lot_number
ORDER BY lm.lot_date DESC;
```

```python
# Execute parameterized SQL file
def execute_query_file(conn, sql_file_path, params=None):
    with open(sql_file_path, 'r') as file:
        sql = file.read()
    
    cursor = conn.cursor()
    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)
    
    return cursor.fetchall()

# Usage
results = execute_query_file(
    conn, 
    "queries/lot_summary.sql", 
    ("2024-01-01", "2024-01-31")
)
```

**Note**: Run this from the database directory:
```bash
cd src/database
```

## Common Query Patterns

### 1. Basic Data Retrieval

```sql
-- Get recent lots
SELECT lot_number, lot_date, product_code, batch_size_kg
FROM lot_master
WHERE lot_date >= date('now', '-30 days')
ORDER BY lot_date DESC;

-- Get manufacturing batches with quality data
SELECT 
    mb.lot_number,
    mb.batch_number,
    mb.start_time,
    mb.end_time,
    AVG(qt.test_result) as avg_quality
FROM manufacturing_batches mb
LEFT JOIN quality_tests qt ON mb.batch_id = qt.batch_id
GROUP BY mb.batch_id
ORDER BY mb.start_time DESC;
```

### 2. Aggregation and Grouping

```sql
-- Monthly production summary
SELECT 
    strftime('%Y-%m', lot_date) as month,
    COUNT(*) as lot_count,
    SUM(batch_size_kg) as total_production_kg,
    AVG(batch_size_kg) as avg_batch_size_kg
FROM lot_master
WHERE lot_date >= date('now', '-12 months')
GROUP BY strftime('%Y-%m', lot_date)
ORDER BY month DESC;

-- Quality metrics by product
SELECT 
    lm.product_code,
    COUNT(DISTINCT lm.lot_number) as lot_count,
    AVG(qt.test_result) as avg_quality_score,
    MIN(qt.test_result) as min_quality_score,
    MAX(qt.test_result) as max_quality_score
FROM lot_master lm
JOIN manufacturing_batches mb ON lm.lot_number = mb.lot_number
JOIN quality_tests qt ON mb.batch_id = qt.batch_id
GROUP BY lm.product_code
ORDER BY avg_quality_score DESC;
```

### 3. Complex Joins

```sql
-- Complete lot lifecycle
SELECT 
    lm.lot_number,
    lm.lot_date,
    lm.product_code,
    mb.batch_number,
    mb.start_time as manufacturing_start,
    mb.end_time as manufacturing_end,
    ar.aging_start_date,
    ar.aging_end_date,
    ar.final_quality_score,
    pkg.packaging_date,
    sh.shipping_date
FROM lot_master lm
LEFT JOIN manufacturing_batches mb ON lm.lot_number = mb.lot_number
LEFT JOIN aging_records ar ON mb.batch_id = ar.batch_id
LEFT JOIN packaging_records pkg ON ar.aging_id = pkg.aging_id
LEFT JOIN shipping_records sh ON pkg.packaging_id = sh.packaging_id
WHERE lm.lot_date >= '2024-01-01'
ORDER BY lm.lot_date DESC;
```

### 4. Subqueries and CTEs

```sql
-- Using Common Table Expressions (CTEs)
WITH quality_summary AS (
    SELECT 
        mb.lot_number,
        AVG(qt.test_result) as avg_quality,
        COUNT(qt.test_id) as test_count
    FROM manufacturing_batches mb
    JOIN quality_tests qt ON mb.batch_id = qt.batch_id
    GROUP BY mb.lot_number
),
production_summary AS (
    SELECT 
        lot_number,
        SUM(batch_size_kg) as total_production
    FROM manufacturing_batches
    GROUP BY lot_number
)
SELECT 
    lm.lot_number,
    lm.lot_date,
    lm.product_code,
    ps.total_production,
    qs.avg_quality,
    qs.test_count
FROM lot_master lm
LEFT JOIN production_summary ps ON lm.lot_number = ps.lot_number
LEFT JOIN quality_summary qs ON lm.lot_number = qs.lot_number
WHERE lm.lot_date >= '2024-01-01'
ORDER BY lm.lot_date DESC;
```

## Business Intelligence Queries

### 1. Production Analytics

```sql
-- Daily production trends
SELECT 
    lot_date,
    COUNT(*) as lots_produced,
    SUM(batch_size_kg) as total_kg,
    AVG(batch_size_kg) as avg_batch_size
FROM lot_master
WHERE lot_date >= date('now', '-90 days')
GROUP BY lot_date
ORDER BY lot_date;

-- Product performance comparison
SELECT 
    product_code,
    COUNT(*) as total_lots,
    AVG(batch_size_kg) as avg_batch_size,
    AVG(quality_score) as avg_quality
FROM (
    SELECT 
        lm.product_code,
        lm.batch_size_kg,
        AVG(qt.test_result) as quality_score
    FROM lot_master lm
    JOIN manufacturing_batches mb ON lm.lot_number = mb.lot_number
    JOIN quality_tests qt ON mb.batch_id = qt.batch_id
    GROUP BY lm.lot_number
)
GROUP BY product_code
ORDER BY avg_quality DESC;
```

### 2. Quality Control Analytics

```sql
-- Quality trends over time
SELECT 
    strftime('%Y-%m', lm.lot_date) as month,
    qt.test_type,
    AVG(qt.test_result) as avg_result,
    COUNT(*) as test_count,
    MIN(qt.test_result) as min_result,
    MAX(qt.test_result) as max_result
FROM lot_master lm
JOIN manufacturing_batches mb ON lm.lot_number = mb.lot_number
JOIN quality_tests qt ON mb.batch_id = qt.batch_id
WHERE lm.lot_date >= date('now', '-12 months')
GROUP BY strftime('%Y-%m', lm.lot_date), qt.test_type
ORDER BY month DESC, qt.test_type;

-- Quality issues by facility
SELECT 
    lm.facility_code,
    COUNT(CASE WHEN qt.test_result < 7.0 THEN 1 END) as failed_tests,
    COUNT(*) as total_tests,
    ROUND(100.0 * COUNT(CASE WHEN qt.test_result < 7.0 THEN 1 END) / COUNT(*), 2) as failure_rate
FROM lot_master lm
JOIN manufacturing_batches mb ON lm.lot_number = mb.lot_number
JOIN quality_tests qt ON mb.batch_id = qt.batch_id
WHERE lm.lot_date >= date('now', '-6 months')
GROUP BY lm.facility_code
ORDER BY failure_rate DESC;
```

### 3. Supply Chain Analytics

```sql
-- Supplier performance
SELECT 
    rm.supplier_name,
    COUNT(DISTINCT rm.lot_number) as lots_supplied,
    AVG(rm.quality_score) as avg_supplier_quality,
    AVG(rm.delivery_time_days) as avg_delivery_time
FROM raw_materials rm
WHERE rm.delivery_date >= date('now', '-12 months')
GROUP BY rm.supplier_name
ORDER BY avg_supplier_quality DESC;

-- Inventory tracking
SELECT 
    strftime('%Y-%m', lot_date) as month,
    SUM(CASE WHEN status = 'ACTIVE' THEN batch_size_kg ELSE 0 END) as active_inventory,
    SUM(CASE WHEN status = 'SHIPPED' THEN batch_size_kg ELSE 0 END) as shipped_inventory,
    SUM(CASE WHEN status = 'AGING' THEN batch_size_kg ELSE 0 END) as aging_inventory
FROM lot_master
WHERE lot_date >= date('now', '-12 months')
GROUP BY strftime('%Y-%m', lot_date)
ORDER BY month DESC;
```

## Performance Optimization

### 1. Indexing Strategy

```sql
-- Create indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_lot_master_date ON lot_master(lot_date);
CREATE INDEX IF NOT EXISTS idx_lot_master_product ON lot_master(product_code);
CREATE INDEX IF NOT EXISTS idx_manufacturing_lot ON manufacturing_batches(lot_number);
CREATE INDEX IF NOT EXISTS idx_quality_batch ON quality_tests(batch_id);
CREATE INDEX IF NOT EXISTS idx_quality_date ON quality_tests(test_date);
```

**Note**: Run this from the database directory:
```bash
cd src/database
```

### 2. Query Optimization

```sql
-- Use EXPLAIN QUERY PLAN to analyze query performance
EXPLAIN QUERY PLAN
SELECT lot_number, product_code, batch_size_kg
FROM lot_master
WHERE lot_date >= '2024-01-01'
ORDER BY lot_date DESC;

-- Use LIMIT for large result sets
SELECT lot_number, lot_date, product_code
FROM lot_master
WHERE lot_date >= date('now', '-30 days')
ORDER BY lot_date DESC
LIMIT 100;
```

### 3. Connection Management

```python
# Use connection pooling for multiple queries
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Usage
with get_db_connection("cheese_manufacturing.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM lot_master")
    count = cursor.fetchone()[0]
    print(f"Total lots: {count}")
```

**Note**: Run this from the database directory:
```bash
cd src/database
```

## Troubleshooting

### Common Issues

1. **Database Locked**:
   ```python
   # Ensure connections are properly closed
   conn.close()
   
   # Or use with statement
   with sqlite3.connect("cheese_manufacturing.db") as conn:
       # Your queries here
       pass
   ```

2. **Missing Tables**:
   ```python
   # Check if tables exist
   cursor = conn.cursor()
   cursor.execute("""
       SELECT name FROM sqlite_master 
       WHERE type='table' AND name='lot_master'
   """)
   if not cursor.fetchone():
       print("Table lot_master does not exist")
   ```

3. **Performance Issues**:
   ```sql
   -- Check query plan
   EXPLAIN QUERY PLAN
   SELECT * FROM lot_master WHERE lot_date >= '2024-01-01';
   
   -- Check table statistics
   ANALYZE;
   ```

## Next Steps

- Generate data using the generators described in `DB_GENERATION.md`
- Run tests to validate data integrity using `TESTING_GUIDE.md`
- Explore advanced SQL features in the schema files
- Create custom views for frequently used queries 