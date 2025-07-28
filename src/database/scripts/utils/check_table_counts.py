#!/usr/bin/env python3
import sqlite3
import os

def check_table_counts():
    # Check if database exists
    db_path = 'db/cheese_manufacturing.db'
    if not os.path.exists(db_path):
        print('Database not found. Please run generate_synthetic_data.py first.')
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = cursor.fetchall()

    print('Table row counts:')
    print('=' * 50)
    empty_tables = []

    for table in tables:
        table_name = table[0]
        cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        count = cursor.fetchone()[0]
        print(f'{table_name:<30} {count:>8} rows')
        if count == 0:
            empty_tables.append(table_name)

    conn.close()

    print('\n' + '=' * 50)
    if empty_tables:
        print(f'Empty tables ({len(empty_tables)}):')
        for table in empty_tables:
            print(f'  - {table}')
    else:
        print('No empty tables found.')

if __name__ == "__main__":
    check_table_counts() 