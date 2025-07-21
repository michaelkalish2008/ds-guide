import sqlite3
import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path

class QualityGenerator:
    def __init__(self, db):
        import sqlite3
        from pathlib import Path
        if isinstance(db, sqlite3.Connection):
            self.conn = db
            self.db_path = None
        else:
            self.db_path = Path(db)
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._ensure_schema_exists()
        
    def _ensure_schema_exists(self):
        """Ensure basic schema exists for testing"""
        cursor = self.conn.cursor()
        
        # Check if quality_tests table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='quality_tests'
        """)
        
        if not cursor.fetchone():
            # Create basic schema for testing
            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS lot_master (
                    lot_uuid TEXT PRIMARY KEY,
                    lot_number TEXT UNIQUE NOT NULL,
                    lot_date TEXT NOT NULL,
                    product_code TEXT NOT NULL,
                    facility_code TEXT NOT NULL,
                    batch_size_kg REAL,
                    status TEXT DEFAULT 'ACTIVE'
                );
                
                CREATE TABLE quality_tests (
                    test_uuid TEXT PRIMARY KEY,
                    lot_uuid TEXT REFERENCES lot_master(lot_uuid),
                    test_date TEXT NOT NULL,
                    test_type TEXT NOT NULL,
                    test_method TEXT,
                    target_range TEXT,
                    actual_result REAL,
                    ph_level REAL,
                    unit TEXT,
                    frequency TEXT,
                    analyst_id TEXT,
                    test_passed INTEGER,
                    notes TEXT
                );
            """)
            self.conn.commit()
        
    def populate_data(self, current_date, lot_count):
        """Generate quality control data"""
        self._populate_quality_tests(current_date, lot_count)
        
    def _populate_quality_tests(self, current_date, lot_count):
        """Generate quality test data"""
        cursor = self.conn.cursor()
        
        # Get lot UUID for this day
        cursor.execute("""
            SELECT lot_uuid FROM lot_master 
            WHERE lot_date = ? AND lot_number LIKE 'TAL-%'
        """, (current_date.strftime("%Y-%m-%d"),))
        
        lot_result = cursor.fetchone()
        if not lot_result:
            print(f"  ⚠️  No lots found in lot_master table for {current_date.strftime('%Y-%m-%d')}, skipping quality data generation.")
            return
        lot_uuid = lot_result[0]
        
        # Quality test types for Taleggio
        quality_tests = [
            {
                "test_type": "PH_MEASUREMENT",
                "test_method": "pH meter",
                "target_range": (5.0, 6.0),
                "unit": "pH",
                "frequency": "DAILY"
            },
            {
                "test_type": "MOISTURE_CONTENT",
                "test_method": "Gravimetric",
                "target_range": (45.0, 55.0),
                "unit": "%",
                "frequency": "DAILY"
            },
            {
                "test_type": "FAT_CONTENT",
                "test_method": "Gerber method",
                "target_range": (25.0, 35.0),
                "unit": "%",
                "frequency": "DAILY"
            },
            {
                "test_type": "SALT_CONTENT",
                "test_method": "Mohr titration",
                "target_range": (1.5, 2.5),
                "unit": "%",
                "frequency": "DAILY"
            },
            {
                "test_type": "TOTAL_PLATE_COUNT",
                "test_method": "Plate count",
                "target_range": (0, 10000),
                "unit": "CFU/g",
                "frequency": "WEEKLY"
            },
            {
                "test_type": "COLIFORMS",
                "test_method": "MPN method",
                "target_range": (0, 100),
                "unit": "MPN/g",
                "frequency": "WEEKLY"
            },
            {
                "test_type": "YEAST_MOLD",
                "test_method": "Plate count",
                "target_range": (0, 1000),
                "unit": "CFU/g",
                "frequency": "WEEKLY"
            }
        ]
        
        # Generate quality tests for this lot
        for test in quality_tests:
            test_uuid = str(uuid.uuid4())
            
            # Generate test result within target range
            min_val, max_val = test["target_range"]
            if test["test_type"] in ["TOTAL_PLATE_COUNT", "COLIFORMS", "YEAST_MOLD"]:
                # Microbiological tests - most should be low
                if random.random() < 0.8:  # 80% chance of low count
                    test_result = random.uniform(0, min_val * 0.1)
                else:
                    test_result = random.uniform(min_val, max_val)
            else:
                # Chemical tests - within normal range
                test_result = random.uniform(min_val, max_val)
            
            # Determine if test passed
            test_passed = min_val <= test_result <= max_val
            
            cursor.execute("""
                INSERT INTO quality_tests 
                (test_uuid, lot_uuid, test_date, test_type, test_method, 
                 target_range, actual_result, ph_level, unit, frequency, 
                 analyst_id, test_passed, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                test_uuid, lot_uuid, current_date.strftime("%Y-%m-%d"),
                test["test_type"], test["test_method"], str(test["target_range"]),
                test_result, test_result if test["test_type"] == "PH_MEASUREMENT" else None,
                test["unit"], test["frequency"],
                f"QA{random.randint(1, 3):03d}", test_passed,
                f"Quality test for {test['test_type']} - {'PASSED' if test_passed else 'FAILED'}"
            ))
        
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close() 