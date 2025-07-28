import sqlite3
from pathlib import Path

def test_sensory_schema():
    db_path = "/tmp/test_sensory_debug.db"
    schema_file = Path("scripts/schema/sqlite/07_sensory_analysis.sqlite.sql")
    index_stmt = "CREATE INDEX idx_sensory_evaluations_lot ON sensory_evaluations (lot_uuid, evaluation_timestamp);"
    conn = sqlite3.connect(db_path)
    try:
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
            print(f"--- Executing SQL from {schema_file} ---\n{schema_sql}\n--- END SQL ---")
            try:
                conn.executescript(schema_sql)
                print("Loaded 07_sensory_analysis.sqlite.sql successfully.")
            except Exception as e:
                print(f"Error loading schema: {e}")
        # Print schema
        try:
            cur = conn.execute("PRAGMA table_info(sensory_evaluations);")
            print("sensory_evaluations columns:")
            for row in cur.fetchall():
                print(row)
        except Exception as e:
            print(f"Error inspecting table: {e}")
        # Try to create the index
        try:
            conn.execute(index_stmt)
            print("Index created successfully.")
        except Exception as e:
            print(f"Error creating index: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_sensory_schema() 