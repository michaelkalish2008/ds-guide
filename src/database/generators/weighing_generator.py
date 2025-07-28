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

    def _populate_weighing_equipment(self):
        """Populate weighing equipment table"""
        cursor = self.conn.cursor()
        
        equipment = [
            ("SCALE001", "Industrial Scale", "ACTIVE", "High-capacity weighing scale"),
            ("SCALE002", "Precision Scale", "ACTIVE", "High-precision laboratory scale"),
            ("SCALE003", "Belt Scale", "ACTIVE", "Conveyor belt weighing system"),
            ("SCALE004", "Checkweigher", "ACTIVE", "Automatic checkweigher"),
            ("SCALE005", "Portable Scale", "ACTIVE", "Mobile weighing equipment"),
            ("SCALE006", "Bulk Scale", "INACTIVE", "Bulk material weighing scale")
        ]
        
        for equipment_id, equipment_name, status, description in equipment:
            cursor.execute("""
                INSERT OR IGNORE INTO weighing_equipment 
                (scale_id, equipment_model, manufacturer, ntep_certification,
                 max_capacity_kg, readability_g, location_code, last_calibration_date,
                 next_calibration_due, legal_for_trade)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (equipment_id, equipment_name, "METTLER_TOLEDO", "NTEP-12345",
                  random.uniform(100, 500), random.uniform(0.1, 1.0), f"LOC{random.randint(1, 5)}",
                  "2024-01-01", "2024-07-01", 1))
        
        print(f"  ✅ Generated {len(equipment)} weighing equipment")

    def _populate_catch_weight_transactions(self):
        """Populate catch weight transactions table"""
        cursor = self.conn.cursor()
        
        # Get some lots
        cursor.execute("SELECT lot_uuid FROM lot_master LIMIT 10")
        lots = cursor.fetchall()
        
        for lot in lots:
            lot_uuid = lot[0]
            transaction_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO catch_weight_transactions 
                (transaction_id, package_uuid, scale_id, gross_weight_g,
                 tare_weight_g, net_weight_g, price_per_kg, total_price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                transaction_id, str(uuid.uuid4()), f"SCALE{random.randint(1, 5):03d}",
                random.uniform(250, 300), random.uniform(5, 15), random.uniform(240, 285),
                random.uniform(15, 25), random.uniform(3.6, 7.1)
            ))
        
        print(f"  ✅ Generated {len(lots)} catch weight transactions")

    def _populate_pricing_rules(self):
        """Populate pricing rules table"""
        cursor = self.conn.cursor()
        
        rules = [
            ("RULE001", "Premium Grade", "A", 18.0, "Premium quality pricing"),
            ("RULE002", "Standard Grade", "B", 15.0, "Standard quality pricing"),
            ("RULE003", "Economy Grade", "C", 12.0, "Economy quality pricing"),
            ("RULE004", "Bulk Discount", "BULK", 13.0, "Bulk order discount"),
            ("RULE005", "Export Pricing", "EXPORT", 16.0, "Export market pricing"),
            ("RULE006", "Retail Premium", "RETAIL", 20.0, "Retail premium pricing")
        ]
        
        for rule_id, rule_name, grade, base_price, description in rules:
            cursor.execute("""
                INSERT OR IGNORE INTO pricing_rules 
                (pricing_rule_id, product_code, customer_category, price_per_unit,
                 unit_of_measure, minimum_quantity, volume_discount_percentage,
                 effective_start_date, effective_end_date, currency)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (rule_id, "TALEGGIO", grade, base_price, "kg", random.uniform(10, 100),
                  random.uniform(5, 15), "2024-01-01", "2024-12-31", "EUR"))
        
        print(f"  ✅ Generated {len(rules)} pricing rules")

    def _populate_inventory_transactions(self):
        """Populate inventory transactions table"""
        cursor = self.conn.cursor()
        
        # Get some lots
        cursor.execute("SELECT lot_uuid FROM lot_master LIMIT 10")
        lots = cursor.fetchall()
        
        transaction_types = ["PRODUCTION", "CONSUMPTION", "SALE", "ADJUSTMENT"]
        
        for lot in lots:
            lot_uuid = lot[0]
            transaction_id = str(uuid.uuid4())
            transaction_type = random.choice(transaction_types)
            
            cursor.execute("""
                INSERT INTO inventory_transactions 
                (inventory_trans_id, lot_uuid, transaction_type, quantity_change_kg,
                 unit_cost, total_value, location_code, transaction_timestamp, reason_code, reference_document, operator_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                transaction_id, lot_uuid, transaction_type,
                random.uniform(10, 50), random.uniform(10, 20), random.uniform(100, 1000),
                f"LOC{random.randint(1, 5)}", "2024-01-15 10:00:00", f"REASON_{random.randint(1, 5)}",
                f"DOC_{random.randint(1000, 9999)}", f"OP{random.randint(1, 10):03d}"
            ))
        
        print(f"  ✅ Generated {len(lots)} inventory transactions")

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
        
    def populate_data(self, current_date, lot_count):
        """Generate weighing and pricing data"""
        self._populate_weighing_equipment()
        self._populate_catch_weight_transactions()
        self._populate_pricing_rules()
        self._populate_inventory_transactions()
        self._populate_weighing_pricing(current_date, lot_count)
        
    def _populate_weighing_pricing(self, current_date, lot_count):
        """Generate weighing and pricing data"""
        cursor = self.conn.cursor()
        
        # Get lot UUID for this day - try multiple patterns
        cursor.execute("""
            SELECT lot_uuid FROM lot_master 
            WHERE lot_date = ? AND lot_number LIKE 'TAL-%'
        """, (current_date.strftime("%Y-%m-%d"),))
        
        lot_result = cursor.fetchone()
        if not lot_result:
            # Try to get any lot from lot_master
            cursor.execute("SELECT lot_uuid FROM lot_master LIMIT 1")
            lot_result = cursor.fetchone()
            
        if not lot_result:
            print("  ⚠️  No lots found in lot_master table, creating test lot...")
            # Create test lot for testing
            lot_uuid = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO lot_master (lot_uuid, lot_number, lot_date, product_code, facility_code, batch_size_kg, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (lot_uuid, f"TAL-{current_date.strftime('%Y-%m-%d')}", current_date.strftime("%Y-%m-%d"), "TALEGGIO", "FAC001", 50.0, "ACTIVE"))
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
        print(f"  ✅ Generated weighing_pricing record for lot {lot_count}")
