#!/usr/bin/env python3
"""
Quick Start Script for Cheese Manufacturing Database

This script provides easy access to the cheese manufacturing database
and demonstrates basic usage patterns.
"""

import sqlite3
import pandas as pd
import os
from pathlib import Path

def get_database_path():
    """Get the path to the main database file"""
    script_dir = Path(__file__).parent
    db_path = script_dir / "db" / "cheese_manufacturing.db"
    return db_path

def connect_to_database():
    """Connect to the main database"""
    db_path = get_database_path()
    
    if not db_path.exists():
        print(f"❌ Database not found at: {db_path}")
        print("Please ensure the database file exists in the db/ directory.")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        print(f"✅ Connected to database: {db_path}")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def show_database_info(conn):
    """Show basic database information"""
    cursor = conn.cursor()
    
    # Get table list
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [table[0] for table in cursor.fetchall()]
    
    print(f"\n📊 Database contains {len(tables)} tables:")
    for table in sorted(tables):
        # Get row count for each table
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  • {table}: {count:,} records")
        except:
            print(f"  • {table}: (error getting count)")
    
    return tables

def show_sample_data(conn, table_name, limit=5):
    """Show sample data from a table"""
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}", conn)
        print(f"\n📋 Sample data from '{table_name}':")
        print(df.to_string(index=False))
        return df
    except Exception as e:
        print(f"❌ Error reading from {table_name}: {e}")
        return None

def run_example_queries(conn):
    """Run some example queries to demonstrate usage"""
    print("\n🔍 Example Queries:")
    
    # Example 1: Manufacturing summary
    try:
        df1 = pd.read_sql_query("""
            SELECT 
                cheese_type,
                COUNT(*) as batch_count,
                AVG(batch_size_kg) as avg_batch_size,
                SUM(batch_size_kg) as total_production
            FROM cheese_manufacturing_batches 
            GROUP BY cheese_type
        """, conn)
        print("\n1. Production Summary by Cheese Type:")
        print(df1.to_string(index=False))
    except Exception as e:
        print(f"❌ Error in query 1: {e}")
    
    # Example 2: Quality analysis
    try:
        df2 = pd.read_sql_query("""
            SELECT 
                qt.test_type,
                COUNT(*) as test_count,
                AVG(qt.actual_result) as avg_score,
                SUM(qt.test_passed) as passed_tests
            FROM quality_tests qt
            GROUP BY qt.test_type
        """, conn)
        print("\n2. Quality Test Summary:")
        print(df2.to_string(index=False))
    except Exception as e:
        print(f"❌ Error in query 2: {e}")
    
    # Example 3: Recent activity
    try:
        df3 = pd.read_sql_query("""
            SELECT 
                cmb.cheese_type,
                cmb.start_timestamp,
                cmb.batch_size_kg,
                qt.actual_result
            FROM cheese_manufacturing_batches cmb
            LEFT JOIN quality_tests qt ON cmb.lot_uuid = qt.lot_uuid
            ORDER BY cmb.start_timestamp DESC
            LIMIT 5
        """, conn)
        print("\n3. Recent Manufacturing Activity:")
        print(df3.to_string(index=False))
    except Exception as e:
        print(f"❌ Error in query 3: {e}")

def main():
    """Main function to demonstrate database usage"""
    print("🧀 Cheese Manufacturing Database - Quick Start")
    print("=" * 50)
    
    # Connect to database
    conn = connect_to_database()
    if conn is None:
        return
    
    try:
        # Show database info
        tables = show_database_info(conn)
        
        # Show sample data from a key table
        if 'cheese_manufacturing_batches' in tables:
            show_sample_data(conn, 'cheese_manufacturing_batches')
        
        # Run example queries
        run_example_queries(conn)
        
        print("\n✅ Quick start completed successfully!")
        print("\n💡 Next steps:")
        print("  • Explore the database with DB Browser for SQLite")
        print("  • Check out the guides in docs/guides/")
        print("  • Run your own queries using the connection object")
        
    except Exception as e:
        print(f"❌ Error during quick start: {e}")
    
    finally:
        conn.close()
        print("\n🔌 Database connection closed")

if __name__ == "__main__":
    main() 