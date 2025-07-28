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
        self._populate_quality_test_methods()
        self._populate_quality_tests(current_date, lot_count)
        self._populate_quality_test_results(current_date, lot_count)
        self._populate_composition_tests(current_date, lot_count)
        self._populate_microbiology_tests(current_date, lot_count)
        self._populate_preprocessing_batches(current_date, lot_count)
        self._populate_pasteurization_records(current_date, lot_count)
        self._populate_standardization_records(current_date, lot_count)
        
    def _populate_quality_tests(self, current_date, lot_count):
        """Generate quality test data"""
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
            print(f"  ⚠️  No lots found in lot_master table, creating test lot...")
            # Create test lot for testing
            lot_uuid = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO lot_master (lot_uuid, lot_number, lot_date, product_code, facility_code, batch_size_kg, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (lot_uuid, f"TAL-{current_date.strftime('%Y-%m-%d')}", current_date.strftime("%Y-%m-%d"), "TALEGGIO", "FAC001", 50.0, "ACTIVE"))
            self.conn.commit()
        else:
            lot_uuid = lot_result[0]
        
        # Quality test types for Taleggio
        quality_tests = [
            {
                "test_type": "PH_MEASUREMENT",
                "test_method": "pH meter",
                "target_range": "5.0-6.0",
                "unit": "pH",
                "frequency": "DAILY"
            },
            {
                "test_type": "MOISTURE_CONTENT",
                "test_method": "Gravimetric",
                "target_range": "45-55%",
                "unit": "%",
                "frequency": "WEEKLY"
            },
            {
                "test_type": "FAT_CONTENT",
                "test_method": "Soxhlet extraction",
                "target_range": "25-35%",
                "unit": "%",
                "frequency": "WEEKLY"
            },
            {
                "test_type": "SALT_CONTENT",
                "test_method": "Titration",
                "target_range": "1.5-2.5%",
                "unit": "%",
                "frequency": "DAILY"
            },
            {
                "test_type": "PROTEIN_CONTENT",
                "test_method": "Kjeldahl",
                "target_range": "20-30%",
                "unit": "%",
                "frequency": "WEEKLY"
            }
        ]
        
        for test in quality_tests:
            test_uuid = str(uuid.uuid4())
            
            # Generate realistic test results
            if test["test_type"] == "PH_MEASUREMENT":
                actual_result = random.uniform(5.0, 6.0)
            elif test["test_type"] == "MOISTURE_CONTENT":
                actual_result = random.uniform(45, 55)
            elif test["test_type"] == "FAT_CONTENT":
                actual_result = random.uniform(25, 35)
            elif test["test_type"] == "SALT_CONTENT":
                actual_result = random.uniform(1.5, 2.5)
            else:  # PROTEIN_CONTENT
                actual_result = random.uniform(20, 30)
            
            cursor.execute("""
                INSERT INTO quality_tests 
                (test_uuid, lot_uuid, test_date, test_type, test_method,
                 target_range, actual_result, unit, frequency, analyst_id, test_passed, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                test_uuid, lot_uuid, current_date.strftime("%Y-%m-%d"),
                test["test_type"], test["test_method"], test["target_range"],
                round(actual_result, 2), test["unit"], test["frequency"],
                f"ANALYST{random.randint(1, 5):03d}", 1,
                f"Quality test for {test['test_type']} on lot {lot_count}"
            ))
        
        self.conn.commit()
        print(f"  ✅ Generated {len(quality_tests)} quality tests for lot {lot_count}")

    def _populate_quality_test_methods(self):
        """Populate quality test methods table"""
        cursor = self.conn.cursor()
        
        methods = [
            ("PH_METER", "pH Measurement", "PHYSICAL", "pH", 5.0, 6.0, "DAILY", 1, 1, "AOAC 981.12"),
            ("MOISTURE_GRAV", "Moisture Content", "COMPOSITION", "%", 45.0, 55.0, "DAILY", 1, 1, "AOAC 926.08"),
            ("FAT_GERBER", "Fat Content", "COMPOSITION", "%", 25.0, 35.0, "DAILY", 1, 1, "AOAC 905.02"),
            ("SALT_MOHR", "Salt Content", "COMPOSITION", "%", 1.5, 2.5, "DAILY", 1, 1, "AOAC 935.43"),
            ("TOTAL_PLATE", "Total Plate Count", "MICROBIOLOGY", "CFU/g", 0, 10000, "WEEKLY", 0, 1, "ISO 4833"),
            ("COLIFORMS", "Coliform Count", "MICROBIOLOGY", "MPN/g", 0, 100, "WEEKLY", 0, 1, "ISO 4832"),
            ("YEAST_MOLD", "Yeast and Mold", "MICROBIOLOGY", "CFU/g", 0, 1000, "WEEKLY", 0, 1, "ISO 21527"),
            ("STAPH_AUREUS", "Staphylococcus aureus", "MICROBIOLOGY", "CFU/g", 0, 100, "WEEKLY", 1, 1, "ISO 6888"),
            ("LISTERIA", "Listeria monocytogenes", "MICROBIOLOGY", "PRESENT_ABSENT", 0, 0, "WEEKLY", 1, 1, "ISO 11290"),
            ("SALMONELLA", "Salmonella spp.", "MICROBIOLOGY", "PRESENT_ABSENT", 0, 0, "WEEKLY", 1, 1, "ISO 6579")
        ]
        
        for method_id, method_name, category, unit, spec_min, spec_max, frequency, ccp, regulatory, reference in methods:
            cursor.execute("""
                INSERT OR IGNORE INTO quality_test_methods 
                (method_id, method_name, test_category, unit_of_measure, 
                 specification_min, specification_max, test_frequency, 
                 ccp_associated, regulatory_required, method_reference)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (method_id, method_name, category, unit, spec_min, spec_max, frequency, ccp, regulatory, reference))
        
        print(f"  ✅ Generated {len(methods)} quality test methods")

    def _populate_quality_test_results(self, current_date, lot_count):
        """Generate quality test results using proper schema"""
        cursor = self.conn.cursor()
        
        # Get lot UUID for this day
        cursor.execute("""
            SELECT lot_uuid FROM lot_master 
            WHERE lot_date = ? AND lot_number LIKE 'TAL-%'
        """, (current_date.strftime("%Y-%m-%d"),))
        
        lot_result = cursor.fetchone()
        if not lot_result:
            return
        lot_uuid = lot_result[0]
        
        # Get available methods
        cursor.execute("SELECT method_id FROM quality_test_methods")
        methods = [row[0] for row in cursor.fetchall()]
        
        if not methods:
            return
        
        # Generate test results for different stages
        stages = ["RAW_MATERIAL", "IN_PROCESS", "FINISHED", "AGED"]
        
        for stage in stages:
            for method_id in methods:
                test_result_id = str(uuid.uuid4())
                
                # Generate realistic test values based on method
                cursor.execute("""
                    SELECT specification_min, specification_max, unit_of_measure 
                    FROM quality_test_methods WHERE method_id = ?
                """, (method_id,))
                spec_min, spec_max, unit = cursor.fetchone()
                
                if "MICROBIOLOGY" in method_id:
                    # Microbiology tests - most should be low/negative
                    if random.random() < 0.8:
                        test_value = random.uniform(0, spec_max * 0.1)
                    else:
                        test_value = random.uniform(spec_min, spec_max)
                else:
                    # Chemical tests - within normal range
                    test_value = random.uniform(spec_min, spec_max)
                
                pass_fail = "PASS" if spec_min <= test_value <= spec_max else "FAIL"
                
                cursor.execute("""
                    INSERT INTO quality_test_results 
                    (test_result_id, lot_uuid, sample_stage, method_id, test_value,
                     unit_of_measure, test_timestamp, lab_technician, equipment_id,
                     pass_fail_result, deviation_notes, retest_required, sample_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    test_result_id, lot_uuid, stage, method_id, test_value,
                    unit, current_date.strftime("%Y-%m-%d %H:%M:%S"),
                    f"TECH_{random.randint(1, 10)}", f"EQ_{random.randint(1, 5)}",
                    pass_fail, f"Test completed for {method_id}", 0, f"SAMPLE_{random.randint(1000, 9999)}"
                ))
        
        print(f"  ✅ Generated quality test results for {len(stages)} stages")

    def _populate_composition_tests(self, current_date, lot_count):
        """Generate composition test data"""
        cursor = self.conn.cursor()
        
        # Get quality test results for composition tests
        cursor.execute("""
            SELECT test_result_id FROM quality_test_results 
            WHERE method_id IN ('MOISTURE_GRAV', 'FAT_GERBER', 'SALT_MOHR')
            LIMIT 10
        """)
        test_results = cursor.fetchall()
        
        for test_result in test_results:
            test_result_id = test_result[0]
            comp_test_id = str(uuid.uuid4())
            
            # Generate realistic composition values for Taleggio
            moisture = random.uniform(48.0, 52.0)
            fat = random.uniform(27.0, 33.0)
            salt = random.uniform(1.8, 2.2)
            protein = random.uniform(18.0, 22.0)
            ph = random.uniform(5.5, 6.0)
            water_activity = random.uniform(0.95, 0.98)
            fat_in_dry_matter = (fat / (100 - moisture)) * 100
            moisture_in_nonfat_solids = (moisture / (100 - fat)) * 100
            salt_in_moisture = (salt / moisture) * 100
            ash = random.uniform(3.0, 4.0)
            
            cursor.execute("""
                INSERT INTO composition_tests 
                (comp_test_id, test_result_id, moisture_percentage, fat_percentage,
                 salt_percentage, protein_percentage, ph_level, water_activity,
                 fat_in_dry_matter, moisture_in_nonfat_solids, salt_in_moisture, ash_percentage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                comp_test_id, test_result_id, moisture, fat, salt, protein, ph,
                water_activity, fat_in_dry_matter, moisture_in_nonfat_solids,
                salt_in_moisture, ash
            ))
        
        print(f"  ✅ Generated {len(test_results)} composition tests")

    def _populate_microbiology_tests(self, current_date, lot_count):
        """Generate microbiology test data"""
        cursor = self.conn.cursor()
        
        # Get quality test results for microbiology tests
        cursor.execute("""
            SELECT test_result_id FROM quality_test_results 
            WHERE method_id IN ('TOTAL_PLATE', 'COLIFORMS', 'YEAST_MOLD', 'STAPH_AUREUS', 'LISTERIA', 'SALMONELLA')
            LIMIT 15
        """)
        test_results = cursor.fetchall()
        
        organisms = {
            'TOTAL_PLATE': 'Total Aerobic Bacteria',
            'COLIFORMS': 'Coliform Bacteria',
            'YEAST_MOLD': 'Yeast and Mold',
            'STAPH_AUREUS': 'Staphylococcus aureus',
            'LISTERIA': 'Listeria monocytogenes',
            'SALMONELLA': 'Salmonella spp.'
        }
        
        for test_result in test_results:
            test_result_id = test_result[0]
            micro_test_id = str(uuid.uuid4())
            
            # Get the method for this test result
            cursor.execute("""
                SELECT method_id FROM quality_test_results WHERE test_result_id = ?
            """, (test_result_id,))
            method_id = cursor.fetchone()[0]
            
            organism = organisms.get(method_id, 'Unknown Organism')
            
            # Generate realistic microbiology results
            if method_id in ['LISTERIA', 'SALMONELLA']:
                # Pathogen tests - mostly negative
                result_count = 0 if random.random() < 0.95 else random.randint(1, 10)
                count_unit = 'PRESENT_ABSENT'
                pathogen_status = 'NOT_DETECTED' if result_count == 0 else 'DETECTED'
            else:
                # Regular microbiology tests
                result_count = random.randint(0, 1000) if random.random() < 0.8 else random.randint(1000, 10000)
                count_unit = 'CFU_PER_G' if method_id != 'COLIFORMS' else 'MPN_PER_G'
                pathogen_status = 'NOT_DETECTED'
            
            enrichment_required = 1 if method_id in ['LISTERIA', 'SALMONELLA'] else 0
            incubation_temp = 35 if method_id in ['TOTAL_PLATE', 'COLIFORMS'] else 25
            incubation_time = 48 if method_id in ['LISTERIA', 'SALMONELLA'] else 24
            detection_limit = 10 if method_id in ['LISTERIA', 'SALMONELLA'] else 1
            confirmation_required = 1 if method_id in ['LISTERIA', 'SALMONELLA'] else 0
            
            cursor.execute("""
                INSERT INTO microbiology_tests 
                (micro_test_id, test_result_id, test_organism, result_count, count_unit,
                 enrichment_required, incubation_temp_celsius, incubation_time_hours,
                 detection_limit, pathogen_status, confirmation_required)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                micro_test_id, test_result_id, organism, result_count, count_unit,
                enrichment_required, incubation_temp, incubation_time, detection_limit,
                pathogen_status, confirmation_required
            ))
        
        print(f"  ✅ Generated {len(test_results)} microbiology tests")

    def _populate_preprocessing_batches(self, current_date, lot_count):
        """Generate preprocessing batch data"""
        cursor = self.conn.cursor()
        
        # Get lot UUID for this day
        cursor.execute("""
            SELECT lot_uuid FROM lot_master 
            WHERE lot_date = ? AND lot_number LIKE 'TAL-%'
        """, (current_date.strftime("%Y-%m-%d"),))
        
        lot_result = cursor.fetchone()
        if not lot_result:
            return
        lot_uuid = lot_result[0]
        
        # Generate preprocessing batches
        for i in range(random.randint(2, 5)):
            batch_id = str(uuid.uuid4())
            batch_size = random.uniform(1000, 5000)
            temperature = random.uniform(60, 75)
            duration = random.randint(15, 30)
            
            cursor.execute("""
                INSERT INTO preprocessing_batches 
                (preprocess_uuid, input_lot_uuid, process_type, equipment_id,
                 start_timestamp, end_timestamp, target_output_kg, actual_output_kg,
                 yield_percentage, operator_id, recipe_id, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                batch_id, lot_uuid, "PASTEURIZATION", f"EQ_{random.randint(1, 5)}",
                current_date.strftime("%Y-%m-%d 08:00:00"),
                current_date.strftime("%Y-%m-%d 08:30:00"),
                batch_size, batch_size * 0.98, 98.0,
                f"OP_{random.randint(1, 10)}", f"RECIPE_{random.randint(1, 5)}", "COMPLETED"
            ))
        
        print(f"  ✅ Generated preprocessing batches")

    def _populate_pasteurization_records(self, current_date, lot_count):
        """Generate pasteurization record data"""
        cursor = self.conn.cursor()
        
        # Get preprocessing batches - if none exist, create some
        cursor.execute("SELECT preprocess_uuid FROM preprocessing_batches LIMIT 5")
        batches = cursor.fetchall()
        
        if not batches:
            # Create some test preprocessing batches
            cursor.execute("SELECT lot_uuid FROM lot_master LIMIT 3")
            lots = cursor.fetchall()
            
            for lot in lots:
                batch_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO preprocessing_batches 
                    (preprocess_uuid, input_lot_uuid, process_type, equipment_id,
                     start_timestamp, end_timestamp, target_output_kg, actual_output_kg,
                     yield_percentage, operator_id, recipe_id, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (batch_id, lot[0], "PASTEURIZATION", f"EQ_{random.randint(1, 5)}",
                      current_date.strftime("%Y-%m-%d 08:00:00"),
                      current_date.strftime("%Y-%m-%d 08:30:00"),
                      random.uniform(1000, 5000), random.uniform(980, 4900), 98.0,
                      f"OP_{random.randint(1, 10)}", f"RECIPE_{random.randint(1, 5)}", "COMPLETED"))
            
            self.conn.commit()
            cursor.execute("SELECT preprocess_uuid FROM preprocessing_batches LIMIT 5")
            batches = cursor.fetchall()
        
        for batch in batches:
            batch_id = batch[0]
            record_id = str(uuid.uuid4())
            
            # Generate pasteurization parameters
            temp_1 = random.uniform(72, 75)
            temp_2 = random.uniform(72, 75)
            hold_time = random.randint(15, 20)
            flow_rate = random.uniform(1000, 2000)
            
            cursor.execute("""
                INSERT INTO pasteurization_records 
                (record_id, preprocess_uuid, holding_temp_celsius, holding_time_seconds,
                 actual_temp_celsius, actual_time_seconds, flow_rate_lpm,
                 inlet_temp_celsius, outlet_temp_celsius, pressure_bar,
                 deviation_flag, corrective_action, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record_id, batch_id, temp_1, hold_time, temp_2, hold_time,
                flow_rate / 60, temp_1 - 2, temp_2 + 2, random.uniform(1.5, 2.5),
                0, "No deviation", current_date.strftime("%Y-%m-%d 08:30:00")
            ))
        
        print(f"  ✅ Generated {len(batches)} pasteurization records")

    def _populate_standardization_records(self, current_date, lot_count):
        """Generate standardization record data"""
        cursor = self.conn.cursor()
        
        # Get preprocessing batches - if none exist, create some
        cursor.execute("SELECT preprocess_uuid FROM preprocessing_batches LIMIT 3")
        batches = cursor.fetchall()
        
        if not batches:
            # Create some test preprocessing batches
            cursor.execute("SELECT lot_uuid FROM lot_master LIMIT 3")
            lots = cursor.fetchall()
            
            for lot in lots:
                batch_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO preprocessing_batches 
                    (preprocess_uuid, input_lot_uuid, process_type, equipment_id,
                     start_timestamp, end_timestamp, target_output_kg, actual_output_kg,
                     yield_percentage, operator_id, recipe_id, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (batch_id, lot[0], "STANDARDIZATION", f"EQ_{random.randint(1, 5)}",
                      current_date.strftime("%Y-%m-%d 09:00:00"),
                      current_date.strftime("%Y-%m-%d 09:30:00"),
                      random.uniform(1000, 5000), random.uniform(980, 4900), 98.0,
                      f"OP_{random.randint(1, 10)}", f"RECIPE_{random.randint(1, 5)}", "COMPLETED"))
            
            self.conn.commit()
            cursor.execute("SELECT preprocess_uuid FROM preprocessing_batches LIMIT 3")
            batches = cursor.fetchall()
        
        for batch in batches:
            batch_id = batch[0]
            record_id = str(uuid.uuid4())
            
            # Generate standardization parameters
            fat_target = random.uniform(3.0, 3.5)
            fat_actual = random.uniform(fat_target - 0.1, fat_target + 0.1)
            protein_target = random.uniform(3.0, 3.3)
            protein_actual = random.uniform(protein_target - 0.05, protein_target + 0.05)
            
            cursor.execute("""
                INSERT INTO standardization_records 
                (record_id, preprocess_uuid, target_fat_percentage, target_protein_percentage,
                 actual_fat_percentage, actual_protein_percentage, cream_added_kg,
                 skim_milk_added_kg, mixing_time_minutes, mixing_temperature_celsius,
                 homogenization_pressure_bar, final_composition_verified, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record_id, batch_id, fat_target, protein_target, fat_actual, protein_actual,
                random.uniform(0, 5), random.uniform(0, 10), random.randint(10, 30),
                random.uniform(40, 60), random.uniform(150, 200), 1,
                current_date.strftime("%Y-%m-%d 09:00:00")
            ))
        
        print(f"  ✅ Generated {len(batches)} standardization records")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close() 