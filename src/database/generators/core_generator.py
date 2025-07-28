import sqlite3
import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path

class CoreDataGenerator:
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
        
        # Check if lot_master table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='lot_master'
        """)
        
        if not cursor.fetchone():
            # Create basic schema for testing
            cursor.executescript("""
                CREATE TABLE lot_master (
                    lot_uuid TEXT PRIMARY KEY,
                    lot_number TEXT UNIQUE NOT NULL,
                    lot_date TEXT NOT NULL,
                    product_code TEXT NOT NULL,
                    facility_code TEXT NOT NULL,
                    batch_size_kg REAL,
                    status TEXT DEFAULT 'ACTIVE'
                );
            """)
            self.conn.commit()
    
    def populate_data(self, current_date, lot_count):
        """Generate core lot master data"""
        print(f"Generating core data for {lot_count} lots...")
        
        # Generate lot master record for the current date
        lot_uuid = str(uuid.uuid4())
        lot_number = f"TAL-{current_date.strftime('%Y-%m-%d')}"
        lot_date = current_date.strftime("%Y-%m-%d")
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO lot_master (
                lot_uuid, lot_number, lot_date, product_code, facility_code, 
                batch_size_kg, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            lot_uuid, lot_number, lot_date, "TALEGGIO", "FAC001", 
            random.uniform(45.0, 55.0), "ACTIVE"
        ))
        
        self.conn.commit()
        print(f"Generated lot record for {lot_number}")
        
        # Populate batch genealogy
        self._populate_batch_genealogy(lot_uuid, lot_number)

    def _populate_batch_genealogy(self, lot_uuid, lot_number):
        """Populate batch genealogy table"""
        cursor = self.conn.cursor()
        
        genealogy_id = str(uuid.uuid4())
        parent_lot = f"PARENT-{lot_number}" if random.random() < 0.3 else None
        child_lots = [f"CHILD-{lot_number}-{i}" for i in range(1, random.randint(2, 5))] if random.random() < 0.4 else []
        
        cursor.execute("""
            INSERT OR IGNORE INTO batch_genealogy 
            (genealogy_id, parent_lot_uuid, child_lot_uuid, quantity_contribution_kg,
             contribution_percentage, relationship_type, created_timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            genealogy_id, parent_lot, lot_uuid, random.uniform(10, 50),
            random.uniform(20, 100), "INGREDIENT" if parent_lot else "NEW_BATCH",
            "2024-01-15 10:00:00"
        ))
        
        print(f"  ✅ Generated batch genealogy for {lot_number}")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close() 