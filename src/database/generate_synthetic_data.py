# DEBUG UTILITY: Standalone test for sensory_evaluations schema and index
if __name__ == "__main__":
    import sqlite3
    from pathlib import Path
    db_path = "/tmp/test_sensory_py.db"
    schema_file = Path("src/database/sqlite/07_sensory_analysis.sqlite.sql")
    conn = sqlite3.connect(db_path)
    with open(schema_file, 'r') as f:
        schema_sql = f.read()
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
    conn.close()

import sqlite3
import os
from pathlib import Path
from typing import Dict, Any
import time
from datetime import datetime, timedelta

# Use absolute imports for direct script execution
from src.database.generators.core_generator import CoreDataGenerator
from src.database.generators.raw_materials_generator import RawMaterialsGenerator
from src.database.generators.preprocessing_generator import PreprocessingGenerator
from src.database.generators.manufacturing_generator import ManufacturingGenerator
from src.database.generators.aging_generator import AgingGenerator
from src.database.generators.quality_generator import QualityGenerator
from src.database.generators.sensory_generator import SensoryGenerator
from src.database.generators.packaging_generator import PackagingGenerator
from src.database.generators.labeling_generator import LabelingGenerator
from src.database.generators.weighing_generator import WeighingGenerator
from src.database.generators.shipping_generator import ShippingGenerator

class CheeseManufacturingDataGenerator:
    def __init__(self, db_path="src/database/data/database/cheese_manufacturing.db"):
        print(f"[DEBUG] CheeseManufacturingDataGenerator using db_path: {db_path}")
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        # Delete the database file before opening the connection
        if self.db_path.exists():
            print(f"[DEBUG] Removing existing database file in __init__: {self.db_path}")
            self.db_path.unlink()
        import sqlite3
        self.conn = sqlite3.connect(self.db_path, isolation_level=None)
        # Initialize generators with shared connection
        self.generators = {
            'core': CoreDataGenerator(self.conn),
            'raw_materials': RawMaterialsGenerator(self.conn),
            'preprocessing': PreprocessingGenerator(self.conn),
            'manufacturing': ManufacturingGenerator(self.conn),
            'aging': AgingGenerator(self.conn),
            'quality': QualityGenerator(self.conn),
            'sensory': SensoryGenerator(self.conn),
            'packaging': PackagingGenerator(self.conn),
            'labeling': LabelingGenerator(self.conn),
            'weighing': WeighingGenerator(self.conn),
            'shipping': ShippingGenerator(self.conn),
        }
        self.start_date = datetime(2024, 1, 1)
        self.end_date = datetime(2024, 1, 31)

    def setup_database(self):
        print("Setting up database schema...")
        schema_dir = Path("src/database/sqlite")
        schema_files = [
            "01_core_architecture.sqlite.sql",
            "02_raw_materials_suppliers.sqlite.sql", 
            "03_preprocessing_operations.sqlite.sql",
            "04_manufacturing_process.sqlite.sql",
            "05_aging_maturation.sqlite.sql",
            "06_quality_control_testing.sqlite.sql",
            "07_sensory_analysis.sqlite.sql",
            "08_packaging_operations.sqlite.sql",
            "09_labeling_regulatory.sqlite.sql",
            "10_weighing_pricing_distribution.sqlite.sql",
            "11_shipping_logistics.sqlite.sql",
            "12_advanced_relationships_views.sqlite.sql"
        ]
        # Phase 1: Load all tables and views
        for schema_file in schema_files:
            schema_path = schema_dir / schema_file
            if schema_path.exists():
                print(f"Loading schema: {schema_file}")
                with open(schema_path, 'r') as f:
                    schema_sql = f.read()
                    print(f"--- Executing SQL from {schema_file} ---\n{schema_sql}\n--- END SQL ---")
                    try:
                        self.conn.executescript(schema_sql)
                        self.conn.commit()
                    except Exception as e:
                        print(f"Error loading {schema_file}: {e}")
                        raise
            else:
                print(f"Warning: Schema file {schema_file} not found")
        self.conn.commit()
        # Diagnostic: print all tables before loading indexes
        print("Tables in database before loading indexes:")
        cur = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for row in cur.fetchall():
            print(row[0])
        # Diagnostic: print columns of sensory_evaluations
        try:
            cur = self.conn.execute("PRAGMA table_info(sensory_evaluations);")
            print("Columns in sensory_evaluations before loading indexes:")
            for row in cur.fetchall():
                print(f"{row[1]} ({row[2]})")
        except Exception as e:
            print(f"Error inspecting sensory_evaluations: {e}")
        # Phase 2: Load indexes
        index_file = schema_dir / "13_performance_optimization.sqlite.sql"
        if index_file.exists():
            print(f"Loading schema: 13_performance_optimization.sqlite.sql (indexes)")
            with open(index_file, 'r') as f:
                index_sql = f.read()
                index_sql = index_sql.replace("CREATE INDEX ", "CREATE INDEX IF NOT EXISTS ")
                try:
                    self.conn.executescript(index_sql)
                except Exception as e:
                    print(f"Error loading 13_performance_optimization.sqlite.sql: {e}")
                    raise
        else:
            print("Warning: Schema file 13_performance_optimization.sqlite.sql not found")
        self.conn.commit()
        print("Database schema loaded successfully!")

    def generate_one_month_data(self):
        print("Generating 1 month of synthetic data...")
        # Removed file deletion logic from here
        self.setup_database()
        current_date = self.start_date
        lot_count = 0
        while current_date <= self.end_date:
            lot_count += 1
            print(f"Generating lot {lot_count} for {current_date.strftime('%Y-%m-%d')}")
            for generator_name, generator in self.generators.items():
                try:
                    generator.populate_data(current_date, lot_count)
                    print(f"   {generator_name}")
                    # Debug: After core and manufacturing, print lot_master count
                    if generator_name == 'core' or generator_name == 'manufacturing':
                        cur = self.conn.execute("SELECT COUNT(*) FROM lot_master")
                        lot_count_db = cur.fetchone()[0]
                        print(f"      [DEBUG] lot_master count after {generator_name}: {lot_count_db}")
                except Exception as e:
                    print(f"   {generator_name}: {e}")
            current_date += timedelta(days=1)
        print(f"Generated {lot_count} lots over {self.end_date - self.start_date + timedelta(days=1)} days")
        # Debug: Print final counts
        cur = self.conn.execute("SELECT COUNT(*) FROM lot_master")
        print(f"[DEBUG] Final lot_master count: {cur.fetchone()[0]}")
        cur = self.conn.execute("SELECT COUNT(*) FROM aging_lots")
        print(f"[DEBUG] Final aging_lots count: {cur.fetchone()[0]}")
        print(f"Database saved to: {self.db_path}")
        self.conn.close() 