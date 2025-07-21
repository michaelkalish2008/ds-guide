import sqlite3
import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path

class LabelingGenerator:
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
        
        # Check if labeling_regulatory table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='labeling_regulatory'
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
                
                CREATE TABLE labeling_regulatory (
                    label_uuid TEXT PRIMARY KEY,
                    lot_uuid TEXT REFERENCES lot_master(lot_uuid),
                    label_date TEXT NOT NULL,
                    product_name TEXT,
                    brand_name TEXT,
                    net_weight TEXT,
                    ingredients TEXT,
                    nutritional_info TEXT,
                    storage_conditions TEXT,
                    best_before_date TEXT,
                    batch_code TEXT,
                    dop_registration TEXT,
                    organic_certification TEXT,
                    allergen_info TEXT,
                    country_of_origin TEXT,
                    label_approved INTEGER,
                    regulatory_compliance TEXT
                );
            """)
            self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
        
    def populate_data(self, current_date, lot_count):
        """Generate labeling and regulatory data"""
        self._populate_labeling_regulatory(current_date, lot_count)
        
    def _populate_labeling_regulatory(self, current_date, lot_count):
        """Generate labeling and regulatory data"""
        cursor = self.conn.cursor()
        
        # Get lot UUID for this day
        cursor.execute("""
            SELECT lot_uuid FROM lot_master 
            WHERE lot_date = ? AND lot_number LIKE 'TAL-%'
        """, (current_date.strftime("%Y-%m-%d"),))
        
        lot_result = cursor.fetchone()
        if not lot_result:
            print(f"  ⚠️  No lots found in lot_master table for {current_date.strftime('%Y-%m-%d')}, skipping labeling data generation.")
            return
        lot_uuid = lot_result[0]
        
        # Labeling information for Taleggio
        labeling_data = {
            "product_name": "Taleggio DOP",
            "brand_name": "Alpine Dairy",
            "net_weight": "250g",
            "ingredients": "Raw cow's milk, salt, rennet, starter cultures",
            "nutritional_info": {
                "energy_kcal": 320,
                "fat_g": 28,
                "saturated_fat_g": 18,
                "carbohydrates_g": 0.5,
                "protein_g": 18,
                "salt_g": 2.0
            },
            "storage_conditions": "Keep refrigerated at 2-8°C",
            "best_before": (current_date + timedelta(days=60)).strftime("%Y-%m-%d"),
            "batch_code": f"TAL-{current_date.strftime('%Y%m%d')}",
            "dop_registration": "IT-123456",
            "organic_certification": "BIO-IT-789",
            "allergen_info": "Contains milk",
            "country_of_origin": "Italy"
        }
        
        label_uuid = str(uuid.uuid4())
        
        cursor.execute("""
            INSERT INTO labeling_regulatory 
            (label_uuid, lot_uuid, label_date, product_name, brand_name, 
             net_weight, ingredients, nutritional_info, storage_conditions,
             best_before_date, batch_code, dop_registration, organic_certification,
             allergen_info, country_of_origin, label_approved, regulatory_compliance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            label_uuid, lot_uuid, current_date.strftime("%Y-%m-%d"),
            labeling_data["product_name"], labeling_data["brand_name"],
            labeling_data["net_weight"], labeling_data["ingredients"],
            str(labeling_data["nutritional_info"]), labeling_data["storage_conditions"],
            labeling_data["best_before"], labeling_data["batch_code"],
            labeling_data["dop_registration"], labeling_data["organic_certification"],
            labeling_data["allergen_info"], labeling_data["country_of_origin"],
            1, "COMPLIANT"
        ))
        
        self.conn.commit()
