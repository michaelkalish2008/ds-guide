import sqlite3
import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path

class RawMaterialsGenerator:
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
        
        # Check if suppliers table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='suppliers'
        """)
        
        if not cursor.fetchone():
            # Create basic schema for testing
            cursor.executescript("""
                CREATE TABLE suppliers (
                    supplier_id TEXT PRIMARY KEY,
                    supplier_name TEXT NOT NULL,
                    supplier_type TEXT,
                    contact_info TEXT,
                    certification_status TEXT,
                    last_audit_date TEXT,
                    risk_rating TEXT,
                    approved_materials TEXT,
                    active_flag INTEGER DEFAULT 1
                );
                
                CREATE TABLE raw_material_lots (
                    raw_lot_uuid TEXT PRIMARY KEY,
                    supplier_id TEXT REFERENCES suppliers(supplier_id),
                    material_type TEXT NOT NULL,
                    lot_number TEXT UNIQUE NOT NULL,
                    arrival_date TEXT NOT NULL,
                    quantity_kg REAL,
                    quality_parameters TEXT,
                    temperature_c REAL,
                    ph_level REAL,
                    fat_content REAL,
                    protein_content REAL,
                    microbiological_results TEXT,
                    quality_score REAL,
                    status TEXT DEFAULT 'PENDING'
                );
            """)
            self.conn.commit()
        
    def populate_data(self, current_date, lot_count):
        """Generate raw materials and supplier data"""
        self._populate_suppliers()
        self._populate_raw_material_lots(current_date, lot_count)
        
    def _populate_suppliers(self):
        """Generate supplier data"""
        suppliers_data = [
            {
                "supplier_id": "SUP001",
                "supplier_name": "Alpine Dairy Farm",
                "supplier_type": "DAIRY_FARM",
                "contact_info": '{"phone": "+39-02-1234567", "email": "info@alpinedairy.it", "address": "Via delle Alpi 123, Milano"}',
                "certification_status": "CERTIFIED",
                "last_audit_date": "2024-01-15",
                "risk_rating": "LOW",
                "approved_materials": ["raw_milk", "cream"],
                "active_flag": 1
            },
            {
                "supplier_id": "SUP002", 
                "supplier_name": "Lombardy Creamery",
                "supplier_type": "DAIRY_FARM",
                "contact_info": '{"phone": "+39-02-2345678", "email": "contact@lombardycreamery.it", "address": "Strada del Latte 456, Bergamo"}',
                "certification_status": "CERTIFIED",
                "last_audit_date": "2024-01-10",
                "risk_rating": "LOW",
                "approved_materials": ["raw_milk", "cream"],
                "active_flag": 1
            },
            {
                "supplier_id": "SUP003",
                "supplier_name": "Italian Cultures Co.",
                "supplier_type": "INGREDIENT",
                "contact_info": '{"phone": "+39-02-3456789", "email": "sales@italiancultures.it", "address": "Via dei Fermenti 789, Roma"}',
                "certification_status": "CERTIFIED",
                "last_audit_date": "2024-01-20",
                "risk_rating": "MEDIUM",
                "approved_materials": ["starter_cultures", "rennet"],
                "active_flag": 1
            },
            {
                "supplier_id": "SUP004",
                "supplier_name": "Packaging Solutions Ltd",
                "supplier_type": "PACKAGING",
                "contact_info": '{"phone": "+39-02-4567890", "email": "info@packagingsolutions.it", "address": "Via del Packaging 321, Torino"}',
                "certification_status": "CERTIFIED",
                "last_audit_date": "2024-01-05",
                "risk_rating": "LOW",
                "approved_materials": ["wax_paper", "labels", "boxes"],
                "active_flag": 1
            }
        ]
        
        cursor = self.conn.cursor()
        
        for supplier in suppliers_data:
            cursor.execute("""
                INSERT OR IGNORE INTO suppliers 
                (supplier_id, supplier_name, supplier_type, contact_info, certification_status, 
                 last_audit_date, risk_rating, approved_materials, active_flag)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                supplier["supplier_id"], supplier["supplier_name"], supplier["supplier_type"],
                supplier["contact_info"], supplier["certification_status"], supplier["last_audit_date"],
                supplier["risk_rating"], str(supplier["approved_materials"]), supplier["active_flag"]
            ))
            # Add at least one certification per supplier
            cert_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT OR IGNORE INTO supplier_certifications 
                (cert_id, supplier_id, cert_type, cert_number, issue_date, expiry_date, certifying_body, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cert_id, supplier["supplier_id"], "HACCP", f"CERT-{random.randint(1000,9999)}", "2024-01-01", "2025-01-01", "CertBody", "ACTIVE"
            ))
        
        self.conn.commit()
        
    def _populate_raw_material_lots(self, current_date, lot_count):
        """Generate raw material lot data"""
        # Get existing suppliers
        cursor = self.conn.cursor()
        cursor.execute("SELECT supplier_id, supplier_type FROM suppliers WHERE active_flag = 1")
        suppliers = cursor.fetchall()
        
        if not suppliers:
            return
        
        # Generate raw material lots for this day
        raw_materials = [
            {
                "material_type": "raw_milk",
                "supplier_type": "DAIRY_FARM",
                "quality_params": {
                    "fat_content": (3.2, 4.0),
                    "protein_content": (3.0, 3.5),
                    "ph_level": (6.6, 6.8),
                    "temperature_c": (2.0, 8.0)
                }
            },
            {
                "material_type": "cream",
                "supplier_type": "DAIRY_FARM", 
                "quality_params": {
                    "fat_content": (35.0, 40.0),
                    "protein_content": (2.0, 2.5),
                    "ph_level": (6.4, 6.6),
                    "temperature_c": (2.0, 8.0)
                }
            },
            {
                "material_type": "starter_cultures",
                "supplier_type": "INGREDIENT",
                "quality_params": {
                    "cfu_count": (1e9, 1e10),
                    "viability": (85.0, 95.0),
                    "temperature_c": (-20.0, -18.0)
                }
            },
            {
                "material_type": "rennet",
                "supplier_type": "INGREDIENT",
                "quality_params": {
                    "strength": (1, 20),
                    "activity": (80.0, 95.0),
                    "temperature_c": (2.0, 8.0)
                }
            }
        ]
        
        # Generate 2-4 raw material lots per day
        num_lots = random.randint(2, 4)
        
        for i in range(num_lots):
            material = random.choice(raw_materials)
            supplier = random.choice([s for s in suppliers if s[1] == material["supplier_type"]])
            
            raw_lot_uuid = str(uuid.uuid4())
            lot_number = f"RM-{current_date.strftime('%Y%m%d')}-{i+1:03d}"
            
            # Generate quality parameters
            quality_data = {}
            for param, (min_val, max_val) in material["quality_params"].items():
                if param == "cfu_count":
                    quality_data[param] = random.uniform(min_val, max_val)
                else:
                    quality_data[param] = random.uniform(min_val, max_val)
            
            cursor.execute("""
                INSERT INTO raw_material_lots 
                (raw_lot_uuid, supplier_id, material_type, lot_number, arrival_date, 
                 quantity_kg, quality_parameters, temperature_c, ph_level, 
                 fat_content, protein_content, microbiological_results, quality_score, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                raw_lot_uuid, supplier[0], material["material_type"], lot_number,
                current_date.strftime("%Y-%m-%d"), random.uniform(100, 500),
                str(quality_data), quality_data.get("temperature_c", random.uniform(2, 8)),
                quality_data.get("ph_level", random.uniform(6.4, 6.8)),
                quality_data.get("fat_content", random.uniform(3.0, 4.0)),
                quality_data.get("protein_content", random.uniform(2.5, 3.5)),
                '{"total_plate_count": "1000", "coliforms": "<10", "yeast_mold": "<10"}',
                random.uniform(7.0, 10.0),
                "APPROVED"
            ))
            # Add at least one milk quality test per raw milk lot
            if material["material_type"] == "raw_milk":
                test_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT OR IGNORE INTO milk_quality_tests 
                    (test_id, raw_lot_uuid, test_timestamp, temperature_celsius, fat_percentage, protein_percentage, ph_level, somatic_cell_count, total_bacterial_count, antibiotic_test_result, acidity_titratable, freezing_point, test_operator, pass_fail)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    test_id, raw_lot_uuid, current_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    quality_data.get("temperature_c", random.uniform(2, 8)),
                    quality_data.get("fat_content", random.uniform(3.0, 4.0)),
                    quality_data.get("protein_content", random.uniform(2.5, 3.5)),
                    quality_data.get("ph_level", random.uniform(6.4, 6.8)),
                    random.randint(100000, 400000),
                    random.randint(1000, 10000),
                    random.choice(["NEGATIVE", "POSITIVE"]),
                    random.uniform(0.12, 0.18),
                    random.uniform(-0.55, -0.51),
                    f"OP{random.randint(1, 3):03d}",
                    random.choice(["PASS", "FAIL"])
                ))
            # Add at least one ingredient quality test per ingredient lot
            if material["material_type"] in ["starter_cultures", "rennet"]:
                test_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT OR IGNORE INTO ingredient_quality_tests 
                    (test_id, raw_lot_uuid, test_type, test_parameter, result_value, unit_of_measure, specification_min, specification_max, test_date, lab_technician, compliance_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    test_id, raw_lot_uuid, material["material_type"].upper(),
                    "activity" if material["material_type"] == "rennet" else "viability",
                    random.uniform(80.0, 100.0),
                    "%" if material["material_type"] == "starter_cultures" else "IMCU/ml",
                    80.0, 100.0,
                    current_date.strftime("%Y-%m-%d"),
                    f"LAB{random.randint(1, 3):03d}",
                    random.choice(["PASS", "FAIL"])
                ))
        
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close() 