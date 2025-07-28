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
        self._populate_packaging_lines()
        self._populate_packaging_materials()
        self._populate_packaging_runs()
        self._populate_individual_packages()
        self._populate_product_labels()
        self._populate_traceability_lot_codes()
        self._populate_critical_tracking_events()
        self._populate_package_labels()
        self._populate_packaging_operations(current_date, lot_count)
        
    def _populate_packaging_operations(self, current_date, lot_count):
        """Populate packaging operations table"""
        print(f"Generating packaging operations data for {lot_count} lots...")
        
        # Get lot UUIDs from lot_master
        cursor = self.conn.cursor()
        cursor.execute("SELECT lot_uuid FROM lot_master LIMIT ?", (lot_count,))
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
            lots = [(lot_uuid,)]
        
        packaging_data = []
        
        for lot in lots:
            lot_uuid = lot[0]
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
                    operation_id, lot_uuid, packaging_date.isoformat(),
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

    def _populate_packaging_lines(self):
        """Populate packaging lines table"""
        cursor = self.conn.cursor()
        
        lines = [
            ("LINE001", "Primary Packaging Line", "ACTIVE", "High-speed vacuum sealing line"),
            ("LINE002", "Secondary Packaging Line", "ACTIVE", "Labeling and boxing line"),
            ("LINE003", "Specialty Packaging Line", "ACTIVE", "Premium packaging line"),
            ("LINE004", "Bulk Packaging Line", "INACTIVE", "Bulk packaging for wholesale"),
            ("LINE005", "Sample Packaging Line", "ACTIVE", "Small batch sample packaging")
        ]
        
        for line_id, line_name, status, description in lines:
            cursor.execute("""
                INSERT OR IGNORE INTO packaging_lines 
                (line_id, line_name, current_status, equipment_type, manufacturer, 
                 capacity_packages_per_minute, max_package_weight_kg)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (line_id, line_name, status, "VACUUM", "MULTIVAC", 
                  random.randint(50, 200), random.uniform(0.5, 2.0)))
        
        print(f"  ✅ Generated {len(lines)} packaging lines")

    def _populate_packaging_materials(self):
        """Populate packaging materials table"""
        cursor = self.conn.cursor()
        
        materials = [
            ("MAT001", "Vacuum Bags", "PLASTIC", "250g capacity", "ACTIVE"),
            ("MAT002", "Labels", "PAPER", "Product information labels", "ACTIVE"),
            ("MAT003", "Boxes", "CARDBOARD", "250g cheese boxes", "ACTIVE"),
            ("MAT004", "Wax Paper", "PAPER", "Cheese wrapping paper", "ACTIVE"),
            ("MAT005", "Plastic Trays", "PLASTIC", "250g cheese trays", "ACTIVE"),
            ("MAT006", "Aluminum Foil", "METAL", "Cheese wrapping foil", "ACTIVE"),
            ("MAT007", "Bulk Containers", "PLASTIC", "5kg bulk containers", "ACTIVE"),
            ("MAT008", "Sample Bags", "PLASTIC", "50g sample bags", "ACTIVE")
        ]
        
        for material_id, material_name, material_type, description, status in materials:
            cursor.execute("""
                INSERT OR IGNORE INTO packaging_materials 
                (material_id, material_name, material_type, supplier_id, lot_number,
                 received_date, expiry_date, quantity_received, unit_of_measure)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (material_id, material_name, material_type, f"SUP{random.randint(1, 4):03d}",
                  f"LOT{random.randint(1000, 9999)}", "2024-01-01", "2025-01-01",
                  random.randint(1000, 10000), "ROLLS"))
        
        print(f"  ✅ Generated {len(materials)} packaging materials")

    def _populate_packaging_runs(self):
        """Populate packaging runs table"""
        cursor = self.conn.cursor()
        
        # Get some lots for packaging runs
        cursor.execute("SELECT lot_uuid FROM lot_master LIMIT 5")
        lots = cursor.fetchall()
        
        for i, lot in enumerate(lots):
            lot_uuid = lot[0]
            run_id = str(uuid.uuid4())
            line_id = f"LINE{(i % 3) + 1:03d}"
            
            cursor.execute("""
                INSERT INTO packaging_runs 
                (packaging_run_uuid, aging_lot_id, line_id, target_package_size_g,
                 target_package_count, actual_package_count, packaging_start_timestamp,
                 packaging_end_timestamp, line_efficiency_percentage, waste_percentage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                run_id, str(uuid.uuid4()), line_id, 
                random.uniform(240, 260), random.randint(100, 500), random.randint(95, 105),
                "2024-01-15 08:00:00", "2024-01-15 12:00:00",
                random.uniform(85, 95), random.uniform(1, 5)
            ))
        
        print(f"  ✅ Generated {len(lots)} packaging runs")

    def _populate_individual_packages(self):
        """Populate individual packages table"""
        cursor = self.conn.cursor()
        
        # Get packaging runs - if none exist, create some
        cursor.execute("SELECT packaging_run_uuid FROM packaging_runs LIMIT 10")
        runs = cursor.fetchall()
        
        if not runs:
            # Create some test packaging runs
            cursor.execute("SELECT lot_uuid FROM lot_master LIMIT 5")
            lots = cursor.fetchall()
            
            for i, lot in enumerate(lots):
                run_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO packaging_runs 
                    (packaging_run_uuid, aging_lot_id, line_id, target_package_size_g,
                     target_package_count, actual_package_count, packaging_start_timestamp,
                     packaging_end_timestamp, line_efficiency_percentage, waste_percentage, operator_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (run_id, lot[0], f"LINE{(i % 3) + 1:03d}", 250,
                      random.randint(50, 200), random.randint(45, 190),
                      "2024-01-15 08:00:00", "2024-01-15 12:00:00",
                      random.uniform(85, 95), random.uniform(2, 8), f"OP{random.randint(1, 10):03d}"))
            
            self.conn.commit()
            cursor.execute("SELECT packaging_run_uuid FROM packaging_runs LIMIT 10")
            runs = cursor.fetchall()
        
        for run in runs:
            run_id = run[0]
            package_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO individual_packages 
                (package_uuid, packaging_run_uuid, package_sequence_number, actual_weight_g, 
                 target_weight_g, weight_variance_percentage, packaging_timestamp, 
                 checkweigher_result, metal_detector_result, seal_integrity_result, 
                 reject_reason, package_barcode, consumer_unit_flag)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                package_id, run_id, random.randint(1, 1000), random.uniform(240, 260), 250,
                random.uniform(-5, 5), "2024-01-15 10:00:00", "PASS", "PASS", "PASS",
                None, f"PKG{random.randint(100000, 999999)}", 1
            ))
        
        print(f"  ✅ Generated {len(runs)} individual packages")

    def _populate_product_labels(self):
        """Populate product labels table"""
        cursor = self.conn.cursor()
        
        labels = [
            ("LABEL001", "TALEGGIO", "v1.0", "Taleggio Artisan", "Taleggio 250g", "250g", "Milk, Salt, Cultures", "{}", "Contains: Milk", "Keep refrigerated", "Best before date on package", "2024-01-01", "/artwork/taleggio_250g.png"),
            ("LABEL002", "TALEGGIO", "v1.0", "Taleggio Artisan", "Taleggio 500g", "500g", "Milk, Salt, Cultures", "{}", "Contains: Milk", "Keep refrigerated", "Best before date on package", "2024-01-01", "/artwork/taleggio_500g.png"),
            ("LABEL003", "TALEGGIO", "v1.0", "Taleggio Artisan", "Taleggio 1kg", "1kg", "Milk, Salt, Cultures", "{}", "Contains: Milk", "Keep refrigerated", "Best before date on package", "2024-01-01", "/artwork/taleggio_1kg.png"),
            ("LABEL004", "TALEGGIO", "v2.0", "Premium Taleggio", "Premium Taleggio 250g", "250g", "Milk, Salt, Cultures", "{}", "Contains: Milk", "Keep refrigerated", "Best before date on package", "2024-01-01", "/artwork/premium_taleggio.png"),
            ("LABEL005", "TALEGGIO", "v1.0", "Organic Taleggio", "Organic Taleggio 250g", "250g", "Organic Milk, Salt, Cultures", "{}", "Contains: Milk", "Keep refrigerated", "Best before date on package", "2024-01-01", "/artwork/organic_taleggio.png")
        ]
        
        for label_id, product_code, label_version, brand_name, product_name, net_weight, ingredients, nutrition, allergens, storage, use_by, approval_date, artwork in labels:
            cursor.execute("""
                INSERT OR IGNORE INTO product_labels 
                (label_id, product_code, label_version, brand_name, product_name,
                 net_weight_declaration, ingredient_statement, nutrition_facts_panel,
                 allergen_statement, storage_instructions, use_by_statement,
                 regulatory_approval_date, artwork_file_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (label_id, product_code, label_version, brand_name, product_name,
                  net_weight, ingredients, nutrition, allergens, storage, use_by,
                  approval_date, artwork))
        
        print(f"  ✅ Generated {len(labels)} product labels")

    def _populate_traceability_lot_codes(self):
        """Populate traceability lot codes table"""
        cursor = self.conn.cursor()
        
        # Get some lots
        cursor.execute("SELECT lot_uuid FROM lot_master LIMIT 10")
        lots = cursor.fetchall()
        
        for lot in lots:
            lot_uuid = lot[0]
            tlc_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO traceability_lot_codes 
                (tlc_id, lot_uuid, traceability_lot_code, product_covered, cheese_category,
                 unpasteurized_milk, created_timestamp, data_retention_years)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                tlc_id, lot_uuid, f"TLC{random.randint(100000, 999999)}", 1,
                random.choice(["SOFT_RIPENED", "HARD", "SOFT_UNRIPENED"]), 0,
                "2024-01-15 10:00:00", 2
            ))
        
        print(f"  ✅ Generated {len(lots)} traceability lot codes")

    def _populate_critical_tracking_events(self):
        """Populate critical tracking events table"""
        cursor = self.conn.cursor()
        
        # Get some lots
        cursor.execute("SELECT lot_uuid FROM lot_master LIMIT 10")
        lots = cursor.fetchall()
        
        events = ["TRANSFORMATION", "SHIPPING", "RECEIVING", "CREATION"]
        
        for lot in lots:
            lot_uuid = lot[0]
            for event in events:
                cte_id = str(uuid.uuid4())
                
                cursor.execute("""
                    INSERT INTO critical_tracking_events 
                    (cte_id, tlc_id, event_type, event_timestamp, 
                     location_description, business_name, business_address, contact_info,
                     quantity_units, unit_of_measure)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    cte_id, str(uuid.uuid4()), event, "2024-01-15 10:00:00",
                    "PACKAGING_AREA", "Taleggio Artisan Cheese", "123 Cheese Lane, Italy",
                    '{"phone": "+39-123-456-789", "email": "info@taleggio.com"}',
                    random.uniform(10, 100), "kg"
                ))
        
        print(f"  ✅ Generated {len(lots) * len(events)} critical tracking events")

    def _populate_package_labels(self):
        """Populate package labels table"""
        cursor = self.conn.cursor()
        
        # Get some packages - if none exist, create some
        cursor.execute("SELECT package_uuid FROM individual_packages LIMIT 10")
        packages = cursor.fetchall()
        
        if not packages:
            # Create some test packages
            cursor.execute("SELECT lot_uuid FROM lot_master LIMIT 5")
            lots = cursor.fetchall()
            
            for lot in lots:
                package_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO individual_packages 
                    (package_uuid, packaging_run_uuid, package_sequence_number, actual_weight_g, 
                     target_weight_g, weight_variance_percentage, packaging_timestamp, 
                     checkweigher_result, metal_detector_result, seal_integrity_result, 
                     reject_reason, package_barcode, consumer_unit_flag)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    package_id, str(uuid.uuid4()), random.randint(1, 1000), random.uniform(240, 260), 250,
                    random.uniform(-5, 5), "2024-01-15 10:00:00", "PASS", "PASS", "PASS",
                    None, f"PKG{random.randint(100000, 999999)}", 1
                ))
            
            self.conn.commit()
            cursor.execute("SELECT package_uuid FROM individual_packages LIMIT 10")
            packages = cursor.fetchall()
        
        # Get some product labels
        cursor.execute("SELECT label_id FROM product_labels LIMIT 5")
        product_labels = cursor.fetchall()
        
        if not product_labels:
            # Create some test product labels
            cursor.execute("""
                INSERT INTO product_labels 
                (label_id, product_code, label_version, brand_name, product_name,
                 net_weight_declaration, ingredient_statement, nutrition_facts_panel,
                 allergen_statement, storage_instructions, use_by_statement,
                 regulatory_approval_date, artwork_file_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, ("TEST_LABEL", "TALEGGIO", "v1.0", "Taleggio Artisan", "Taleggio 250g",
                  "250g", "Milk, Salt, Cultures", "{}", "Contains: Milk", "Keep refrigerated",
                  "Best before date on package", "2024-01-01", "/artwork/taleggio_250g.png"))
            self.conn.commit()
            cursor.execute("SELECT label_id FROM product_labels LIMIT 5")
            product_labels = cursor.fetchall()
        
        for package in packages:
            package_uuid = package[0]
            label_instance_id = str(uuid.uuid4())
            label_id = random.choice(product_labels)[0] if product_labels else "TEST_LABEL"
            
            cursor.execute("""
                INSERT INTO package_labels 
                (label_instance_id, package_uuid, label_id, production_date, best_by_date,
                 lot_code, establishment_number, upc_code, price_per_pound, print_timestamp,
                 printer_id, label_verification_passed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                label_instance_id, package_uuid, label_id, "2024-01-15", "2024-04-15",
                f"LOT{random.randint(1000, 9999)}", f"EST{random.randint(1000, 9999)}",
                f"0{random.randint(100000000000, 999999999999)}", random.uniform(8, 12),
                "2024-01-15 10:00:00", f"PRINTER{random.randint(1, 5):03d}", 1
            ))
        
        print(f"  ✅ Generated {len(packages)} package labels")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
