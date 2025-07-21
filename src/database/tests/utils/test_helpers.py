import sqlite3
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

def create_test_database(db_path: Path) -> sqlite3.Connection:
    """Create a test database with basic schema"""
    conn = sqlite3.connect(db_path)
    
    # Create basic schema
    conn.executescript("""
        CREATE TABLE lot_master (
            lot_uuid TEXT PRIMARY KEY,
            lot_number TEXT UNIQUE NOT NULL,
            lot_date TEXT NOT NULL,
            product_code TEXT NOT NULL,
            facility_code TEXT NOT NULL,
            batch_size_kg REAL,
            status TEXT DEFAULT 'ACTIVE'
        );
        
        CREATE TABLE suppliers (
            supplier_id TEXT PRIMARY KEY,
            supplier_name TEXT NOT NULL,
            supplier_type TEXT,
            active_flag INTEGER DEFAULT 1
        );
    """)
    
    return conn

def insert_test_data(conn: sqlite3.Connection, table: str, data: List[Dict[str, Any]]):
    """Insert test data into specified table"""
    if not data:
        return
    
    columns = list(data[0].keys())
    placeholders = ', '.join(['?' for _ in columns])
    column_names = ', '.join(columns)
    
    query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
    
    cursor = conn.cursor()
    for row in data:
        values = [row[column] for column in columns]
        cursor.execute(query, values)
    
    conn.commit()

def get_table_row_count(conn: sqlite3.Connection, table: str) -> int:
    """Get row count for specified table"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    return cursor.fetchone()[0]

def validate_date_range(conn: sqlite3.Connection, start_date: str, end_date: str) -> bool:
    """Validate that all dates in lot_master are within specified range"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM lot_master 
        WHERE lot_date < ? OR lot_date > ?
    """, (start_date, end_date))
    
    out_of_range_count = cursor.fetchone()[0]
    return out_of_range_count == 0 