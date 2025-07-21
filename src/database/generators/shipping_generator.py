import uuid
import random
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path

class ShippingGenerator:
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
        
        # Check if shipping_logistics table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='shipping_logistics'
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
                
                CREATE TABLE shipping_logistics (
                    shipping_id TEXT PRIMARY KEY,
                    lot_uuid TEXT REFERENCES lot_master(lot_uuid),
                    destination TEXT NOT NULL,
                    carrier TEXT,
                    tracking_number TEXT,
                    shipping_date TEXT NOT NULL,
                    shipping_cost REAL,
                    distance_km REAL,
                    transit_time_hours REAL,
                    status TEXT,
                    notes TEXT
                );
            """)
            self.conn.commit()
        
    def populate_data(self, current_date, lot_count):
        """Generate shipping logistics data"""
        self._populate_shipping_logistics(current_date, lot_count)
        
    def _populate_shipping_logistics(self, current_date, lot_count):
        """Populate shipping logistics table"""
        print(f"Generating shipping logistics data for {lot_count} lots...")
        
        # Get lot UUIDs from lot_master
        cursor = self.conn.cursor()
        cursor.execute("SELECT lot_uuid, lot_number FROM lot_master LIMIT ?", (lot_count,))
        lots = cursor.fetchall()
        
        shipping_data = []
        
        for lot in lots:
            # Generate shipping records
            shipping_date = current_date + timedelta(days=random.randint(30, 60))  # After aging
            
            # Multiple shipping destinations
            destinations = [
                "Whole Foods Market - Northeast",
                "Trader Joe's - California",
                "Kroger - Midwest",
                "Safeway - West Coast",
                "Wegmans - East Coast"
            ]
            
            for dest in random.sample(destinations, random.randint(1, 3)):
                shipping_id = str(uuid.uuid4())
                carrier = random.choice(["FedEx", "UPS", "DHL", "USPS"])
                tracking_number = f"{carrier[:2].upper()}{random.randint(100000000, 999999999)}"
                
                shipping_data.append((
                    shipping_id, lot["lot_uuid"], dest, carrier, tracking_number,
                    shipping_date.isoformat(), random.uniform(5.0, 15.0),
                    random.uniform(100, 500), random.uniform(50, 200),
                    random.choice(["IN_TRANSIT", "DELIVERED", "OUT_FOR_DELIVERY"]),
                    f"Shipped to {dest} via {carrier}"
                ))
        
        # Insert shipping data
        cursor.executemany("""
            INSERT INTO shipping_logistics (
                shipping_id, lot_uuid, destination, carrier, tracking_number,
                shipping_date, shipping_cost, distance_km, transit_time_hours,
                status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, shipping_data)
        
        self.conn.commit()
        print(f"Generated {len(shipping_data)} shipping records")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
