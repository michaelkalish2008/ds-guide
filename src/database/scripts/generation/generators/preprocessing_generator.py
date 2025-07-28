import sqlite3
import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path

class PreprocessingGenerator:
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
        
        # Check if pasteurization_batches table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='pasteurization_batches'
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
                
                CREATE TABLE pasteurization_batches (
                    batch_uuid TEXT PRIMARY KEY,
                    lot_uuid TEXT REFERENCES lot_master(lot_uuid),
                    batch_date TEXT NOT NULL,
                    process_step TEXT NOT NULL,
                    temperature_c REAL,
                    duration_minutes INTEGER,
                    target_ph REAL,
                    actual_ph REAL,
                    flow_rate_lpm REAL,
                    pressure_bar REAL,
                    operator_id TEXT,
                    status TEXT,
                    notes TEXT
                );
            """)
            self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
        
    def populate_data(self, current_date, lot_count):
        """Generate preprocessing data"""
        self._populate_pasteurization_batches(current_date, lot_count)
        self.ensure_preprocessing_per_lot()
        
    def _populate_pasteurization_batches(self, current_date, lot_count):
        """Generate pasteurization batch data"""
        cursor = self.conn.cursor()
        
        # Get lot UUID for this day
        cursor.execute("""
            SELECT lot_uuid FROM lot_master 
            WHERE lot_date = ? AND lot_number LIKE 'TAL-%'
        """, (current_date.strftime("%Y-%m-%d"),))
        
        lot_result = cursor.fetchone()
        if not lot_result:
            print("  ⚠️  No lots found in lot_master table, creating test lot...")
            # Create test lot for testing
            lot_uuid = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO lot_master (lot_uuid, lot_number, lot_date, product_code, facility_code, batch_size_kg, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (lot_uuid, "TEST-001", current_date.strftime("%Y-%m-%d"), "TALEGGIO", "FAC001", 50.0, "ACTIVE"))
            self.conn.commit()
        else:
            lot_uuid = lot_result[0]
        
        # Taleggio pasteurization process parameters
        pasteurization_steps = [
            {
                "process_step": "HEATING",
                "temperature_c": 72.0,
                "duration_minutes": 15,
                "target_ph": 6.8,
                "description": "Pasteurization at 72°C for 15 minutes"
            },
            {
                "process_step": "COOLING", 
                "temperature_c": 40.0,
                "duration_minutes": 10,
                "target_ph": 6.8,
                "description": "Cooling to 40°C for inoculation"
            }
        ]
        
        for i, step in enumerate(pasteurization_steps):
            batch_uuid = str(uuid.uuid4())
            
            # Add some variation to the process parameters
            actual_temp = step["temperature_c"] + random.uniform(-1.0, 1.0)
            actual_duration = step["duration_minutes"] + random.randint(-1, 1)
            actual_ph = step["target_ph"] + random.uniform(-0.1, 0.1)
            
            cursor.execute("""
                INSERT INTO pasteurization_batches 
                (batch_uuid, lot_uuid, batch_date, process_step, temperature_c, 
                 duration_minutes, target_ph, actual_ph, flow_rate_lpm, 
                 pressure_bar, operator_id, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                batch_uuid, lot_uuid, current_date.strftime("%Y-%m-%d"),
                step["process_step"], actual_temp, actual_duration,
                step["target_ph"], actual_ph, random.uniform(50, 100),
                random.uniform(1.5, 2.5), f"OP{random.randint(1, 5):03d}",
                "COMPLETED", step["description"]
            ))
        
        self.conn.commit() 

    def ensure_preprocessing_per_lot(self):
        """Ensure at least one preprocessing batch per lot in lot_master"""
        cursor = self.conn.cursor()
        lots = cursor.execute("SELECT lot_uuid, lot_date FROM lot_master").fetchall()
        for lot in lots:
            exists = cursor.execute(
                "SELECT 1 FROM pasteurization_batches WHERE lot_uuid = ? LIMIT 1", (lot["lot_uuid"],)
            ).fetchone()
            if not exists:
                batch_uuid = str(uuid.uuid4())
                cursor.execute(
                    """
                    INSERT INTO pasteurization_batches (
                        batch_uuid, lot_uuid, batch_date, process_step, temperature_c, duration_minutes, target_ph, actual_ph, flow_rate_lpm, pressure_bar, operator_id, status, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        batch_uuid, lot["lot_uuid"], lot["lot_date"], "HEATING", 72.0, 15, 6.8, 6.8, 75.0, 2.0, "OP001", "COMPLETED", "Auto-generated batch"
                    )
                )
        self.conn.commit() 