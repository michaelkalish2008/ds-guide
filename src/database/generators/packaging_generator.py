import sqlite3
import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path

class PackagingGenerator:
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
        
        # Check if packaging_operations table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='packaging_operations'
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
                
                CREATE TABLE packaging_operations (
                    operation_id TEXT PRIMARY KEY,
                    lot_uuid TEXT REFERENCES lot_master(lot_uuid),
                    packaging_date TEXT NOT NULL,
                    operation_type TEXT NOT NULL,
                    equipment_id TEXT,
                    target_weight_g REAL,
                    actual_weight_g REAL,
                    pieces_packaged INTEGER,
                    operator_id TEXT,
                    temperature_c REAL,
                    humidity_percent REAL,
                    status TEXT,
                    notes TEXT
                );
            """)
            self.conn.commit()
        
    def populate_data(self, current_date, lot_count):
        """Generate packaging operations data"""
        self._populate_packaging_operations(current_date, lot_count)
        
    def _populate_packaging_operations(self, current_date, lot_count):
        """Populate packaging operations table"""
        print(f"Generating packaging operations data for {lot_count} lots...")
        
        # Get lot UUIDs from lot_master
        cursor = self.conn.cursor()
        cursor.execute("SELECT lot_uuid, lot_number FROM lot_master LIMIT ?", (lot_count,))
        lots = cursor.fetchall()
        
        if not lots:
            print("  ⚠️  No lots found in lot_master table, creating test lot...")
            # Create test lot for testing
            lot_uuid = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO lot_master (lot_uuid, lot_number, lot_date, product_code, facility_code, batch_size_kg, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (lot_uuid, "TEST-001", current_date.strftime("%Y-%m-%d"), "TALEGGIO", "FAC001", 50.0, "ACTIVE"))
            self.conn.commit()
            lots = [{'lot_uuid': lot_uuid, 'lot_number': 'TEST-001'}]
        
        packaging_data = []
        
        for lot in lots:
            # Generate packaging operations
            packaging_date = current_date + timedelta(days=random.randint(25, 35))  # After aging
            
            # Multiple packaging steps
            packaging_steps = [
                {"operation_type": "CUTTING", "equipment_id": "CUT001", "target_weight_g": 250},
                {"operation_type": "VACUUM_SEALING", "equipment_id": "VAC001", "target_weight_g": 250},
                {"operation_type": "LABELING", "equipment_id": "LAB001", "target_weight_g": 250},
                {"operation_type": "BOXING", "equipment_id": "BOX001", "target_weight_g": 1000}
            ]
            
            for step in packaging_steps:
                operation_id = str(uuid.uuid4())
                actual_weight = step["target_weight_g"] * random.uniform(0.95, 1.05)
                pieces_packaged = int(actual_weight / step["target_weight_g"])
                
                packaging_data.append((
                    operation_id, lot["lot_uuid"], packaging_date.isoformat(),
                    step["operation_type"], step["equipment_id"], step["target_weight_g"],
                    actual_weight, pieces_packaged, f"OP{random.randint(1, 5):03d}",
                    random.uniform(15, 20), random.uniform(60, 70), "COMPLETED",
                    f"Packaging operation: {step['operation_type']}"
                ))
        
        # Insert packaging data
        cursor.executemany("""
            INSERT INTO packaging_operations (
                operation_id, lot_uuid, packaging_date, operation_type, equipment_id,
                target_weight_g, actual_weight_g, pieces_packaged, operator_id,
                temperature_c, humidity_percent, status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, packaging_data)
        
        self.conn.commit()
        print(f"Generated {len(packaging_data)} packaging operations")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
