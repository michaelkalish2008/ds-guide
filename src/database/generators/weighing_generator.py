import sqlite3
import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path

class WeighingGenerator:
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
        
        # Check if weighing_pricing table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='weighing_pricing'
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
                
                CREATE TABLE weighing_pricing (
                    weighing_uuid TEXT PRIMARY KEY,
                    lot_uuid TEXT REFERENCES lot_master(lot_uuid),
                    weighing_date TEXT NOT NULL,
                    total_weight_kg REAL,
                    yield_percentage REAL,
                    unit_price_eur REAL,
                    total_value_eur REAL,
                    packaging_weight_g REAL,
                    net_weight_kg REAL,
                    quality_grade TEXT,
                    market_destination TEXT,
                    pricing_notes TEXT
                );
            """)
            self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
        
    def populate_data(self, current_date, lot_count):
        """Generate weighing and pricing data"""
        self._populate_weighing_pricing(current_date, lot_count)
        
    def _populate_weighing_pricing(self, current_date, lot_count):
        """Generate weighing and pricing data"""
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
        
        # Weighing and pricing data
        weighing_uuid = str(uuid.uuid4())
        
        # Generate realistic weights and prices
        total_weight_kg = random.uniform(45, 55)  # Typical Taleggio batch
        yield_percentage = random.uniform(85, 95)  # Typical cheese yield
        unit_price_eur = random.uniform(12, 18)  # Price per kg
        total_value_eur = total_weight_kg * unit_price_eur
        
        cursor.execute("""
            INSERT INTO weighing_pricing 
            (weighing_uuid, lot_uuid, weighing_date, total_weight_kg, 
             yield_percentage, unit_price_eur, total_value_eur, 
             packaging_weight_g, net_weight_kg, quality_grade, 
             market_destination, pricing_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            weighing_uuid, lot_uuid, current_date.strftime("%Y-%m-%d"),
            round(total_weight_kg, 2), round(yield_percentage, 1),
            round(unit_price_eur, 2), round(total_value_eur, 2),
            random.uniform(5, 15), round(total_weight_kg - 0.01, 2),
            random.choice(["A", "B", "C"]), random.choice(["RETAIL", "WHOLESALE", "EXPORT"]),
            f"Standard pricing for Taleggio lot {lot_count}"
        ))
        
        self.conn.commit()
