import sqlite3
import uuid
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path

class ManufacturingGenerator:
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
        
        # Taleggio manufacturing constants based on the provided data
        self.taleggio_process = {
            'milk_quantity_liters': 50,
            'target_temp_celsius': 40,
            'acidification_time_minutes': 40,
            'rennet_amount_cc': 10,
            'rennet_titer': '1:20,000',
            'first_cut_rest_minutes': 10,
            'second_cut_rest_minutes': 17,
            'target_curd_size': 'hazelnut',
            'stufatura_temp_celsius': 35,
            'target_ph_stufatura': 5.3,
            'aging_days': 15,
            'aging_temp_celsius': [4, 10],  # First 15 days at 4-5°C, then 10°C
            'aging_humidity_percent': 80,
            'washing_frequency': 3,
            'washing_period_days': 10
        }
        
    def _ensure_schema_exists(self):
        """Ensure basic schema exists for testing"""
        cursor = self.conn.cursor()
        # Only check if table exists, do not create it
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='manufacturing_batches'
        """)
        # No table creation here; rely on schema files
        
    def populate_data(self, current_date=None, lot_count=None):
        """Generate manufacturing process data"""
        print("  Generating manufacturing batches...")
        
        # Get existing lots
        lots = self.conn.execute("SELECT lot_uuid, lot_date FROM lot_master").fetchall()
        
        if not lots:
            print("  ⚠️  No lots found in lot_master table, creating test lots...")
            # Create test lots for testing
            test_lots = []
            for i in range(lot_count or 1):
                lot_uuid = str(uuid.uuid4())
                lot_date = current_date or datetime.now()
                test_lots.append({
                    'lot_uuid': lot_uuid,
                    'lot_date': lot_date.strftime("%Y-%m-%d")
                })
                # Insert test lot
                self.conn.execute("""
                    INSERT INTO lot_master (lot_uuid, lot_number, lot_date, product_code, facility_code, batch_size_kg, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (lot_uuid, f"TEST-{i+1:03d}", lot_date.strftime("%Y-%m-%d"), "TALEGGIO", "FAC001", 50.0, "ACTIVE"))
            self.conn.commit()
            lots = test_lots
        
        # Generate and insert cheese_manufacturing_batches records
        manufacturing_batches = self.generate_manufacturing_batches(lots)
        self.insert_manufacturing_batches(manufacturing_batches)
        
        # NEW: Generate and insert coagulation records
        coagulation_records = self.generate_coagulation_records(manufacturing_batches)
        self.insert_coagulation_records(coagulation_records)
        
        # NEW: Generate and insert curd processing records
        curd_processing_records = self.generate_curd_processing_records(manufacturing_batches)
        self.insert_curd_processing_records(curd_processing_records)
        
        # NEW: Generate and insert pressing records
        pressing_records = self.generate_pressing_records(manufacturing_batches)
        self.insert_pressing_records(pressing_records)
        
        # Generate simple manufacturing batches for testing
        batches_data = []
        for lot in lots:
            lot_date = datetime.fromisoformat(lot['lot_date'])
            # Create basic manufacturing records with expected Taleggio steps
            process_steps = [
                ('PASTEURIZATION', 15),  # 10-20 minutes
                ('INOCULATION', 5),      # 5-10 minutes  
                ('COAGULATION', 45),     # 30-60 minutes
                ('CUTTING', 10),         # 10-15 minutes
                ('FORMING', 20)          # 15-30 minutes
            ]
            for step, duration in process_steps:
                batch_uuid = str(uuid.uuid4())  # Unique UUID for each record
                # Add some variation to duration
                actual_duration = duration + random.randint(-2, 2)
                batches_data.append((
                    batch_uuid, lot['lot_uuid'], lot_date.strftime("%Y-%m-%d"),
                    step, random.uniform(20.0, 80.0), actual_duration
                ))
        # Insert manufacturing_batches (legacy/simple)
        cursor = self.conn.cursor()
        cursor.executemany("""
            INSERT INTO manufacturing_batches (
                batch_uuid, lot_uuid, batch_date, process_step, temperature_c, duration_minutes
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, batches_data)
        self.conn.commit()
        print(f"  ✅ Generated {len(batches_data)} manufacturing batch records")
    
    def generate_manufacturing_batches(self, lots: List[sqlite3.Row]) -> List[Dict]:
        """Generate manufacturing batch data with realistic Taleggio parameters"""
        batches = []
        supervisors = ['Maria Rodriguez', 'Carlos Mendez', 'Ana Silva', 'David Chen', 'Giuseppe Rossi']
        vats = ['VAT-01', 'VAT-02', 'VAT-03']
        
        for lot in lots:
            batch_uuid = str(uuid.uuid4())
            lot_date = datetime.fromisoformat(lot['lot_date'])
            
            # Taleggio process timing based on the provided data
            start_time = lot_date.replace(hour=10, minute=0, second=0)  # Process starts at 10:00
            end_time = start_time + timedelta(hours=6)  # Process ends around 16:00
            
            batch = {
                'batch_uuid': batch_uuid,
                'lot_uuid': lot['lot_uuid'],
                'standardized_milk_lot': None,  # Will be linked to preprocessing
                'recipe_id': 'TALEGGIO-RECIPE-001',
                'cheese_type': 'TALEGGIO',
                'vat_id': random.choice(vats),
                'batch_size_kg': self.taleggio_process['milk_quantity_liters'] * 1.03,  # Milk density
                'start_timestamp': start_time.isoformat(),
                'expected_end_timestamp': end_time.isoformat(),
                'actual_end_timestamp': end_time.isoformat(),
                'batch_supervisor': random.choice(supervisors),
                'shift_code': 'DAY',
                'status': 'COMPLETED'
            }
            batches.append(batch)
        
        return batches
    
    def generate_coagulation_records(self, batches: List[Dict]) -> List[Dict]:
        """Generate coagulation records based on Taleggio process"""
        records = []
        
        for batch in batches:
            start_time = datetime.fromisoformat(batch['start_timestamp'])
            
            # Based on the provided Taleggio process
            coagulation_record = {
                'coag_id': str(uuid.uuid4()),
                'batch_uuid': batch['batch_uuid'],
                'milk_temp_celsius': self.taleggio_process['target_temp_celsius'],
                'culture_type': 'TERMOFILI',  # As specified in the process
                'culture_amount_units': 1,  # One packet for 50L (usually for 100L)
                'culture_added_timestamp': start_time.isoformat(),
                'rennet_type': 'ANIMAL',  # Traditional for Taleggio
                'rennet_amount_ml': self.taleggio_process['rennet_amount_cc'],
                'rennet_added_timestamp': (start_time + timedelta(minutes=52)).isoformat(),  # 10:52
                'calcium_chloride_ml': 0,  # Not mentioned in Taleggio process
                'coagulation_time_minutes': self.taleggio_process['acidification_time_minutes'],
                'curd_firmness_score': random.randint(7, 9),  # Good firmness for Taleggio
                'ph_at_cutting': random.uniform(6.2, 6.3),  # Based on process data
                'temperature_at_cutting': self.taleggio_process['target_temp_celsius'],
                'cutting_timestamp': (start_time + timedelta(minutes=52)).isoformat()
            }
            records.append(coagulation_record)
        
        return records
    
    def generate_curd_processing_records(self, batches: List[Dict]) -> List[Dict]:
        """Generate curd processing records based on Taleggio process"""
        records = []
        
        for batch in batches:
            start_time = datetime.fromisoformat(batch['start_timestamp'])
            
            # Based on the provided Taleggio process timing
            first_cut_time = start_time + timedelta(minutes=52)  # 10:52
            second_cut_time = first_cut_time + timedelta(minutes=34)  # 11:26
            agitation_time = second_cut_time + timedelta(minutes=17)  # 11:43
            extraction_time = agitation_time + timedelta(minutes=12)  # 11:55
            
            curd_record = {
                'processing_id': str(uuid.uuid4()),
                'batch_uuid': batch['batch_uuid'],
                'cutting_size_mm': 30,  # 3x3x3 cm as specified
                'cutting_duration_minutes': 5,  # Estimated cutting time
                'healing_time_minutes': self.taleggio_process['first_cut_rest_minutes'],
                'stirring_speed_rpm': random.randint(15, 25),  # Gentle stirring
                'cooking_start_temp_celsius': self.taleggio_process['target_temp_celsius'],
                'cooking_end_temp_celsius': 38,  # As specified in process
                'cooking_time_minutes': 12,  # 11:43 to 11:55
                'whey_drainage_start_timestamp': extraction_time.isoformat(),
                'whey_volume_liters': self.taleggio_process['milk_quantity_liters'] * 0.6,  # ~60% whey
                'curd_moisture_percentage': random.uniform(45, 52),  # Taleggio moisture range
                'ph_at_drainage': random.uniform(6.2, 6.3),
                'syneresis_rate': random.uniform(0.8, 1.2),  # ml whey/g curd/hour
                'operator_id': batch['batch_supervisor']
            }
            records.append(curd_record)
        
        return records
    
    def generate_pressing_records(self, batches: List[Dict]) -> List[Dict]:
        """Generate pressing records based on Taleggio process"""
        records = []
        
        for batch in batches:
            start_time = datetime.fromisoformat(batch['start_timestamp'])
            
            # Taleggio pressing sequence based on process
            press_sequence = [
                {
                    "step": 1,
                    "pressure_bar": 0.5,
                    "duration_hours": 2,
                    "description": "Initial gentle pressing"
                },
                {
                    "step": 2,
                    "pressure_bar": 1.0,
                    "duration_hours": 4,
                    "description": "Medium pressure pressing"
                },
                {
                    "step": 3,
                    "pressure_bar": 2.0,
                    "duration_hours": 12,
                    "description": "Final pressing"
                }
            ]
            
            pressing_start = start_time + timedelta(hours=2)  # After stufatura
            pressing_end = pressing_start + timedelta(hours=18)  # Total pressing time
            
            pressing_record = {
                'pressing_id': str(uuid.uuid4()),
                'batch_uuid': batch['batch_uuid'],
                'press_id': f'PRESS-{random.randint(1, 3):02d}',
                'initial_weight_kg': batch['batch_size_kg'] * 0.15,  # ~15% yield
                'press_sequence': json.dumps(press_sequence),
                'total_pressing_time_hours': 18,
                'final_weight_kg': batch['batch_size_kg'] * 0.12,  # ~12% final yield
                'moisture_loss_percentage': random.uniform(3, 5),
                'final_ph': self.taleggio_process['target_ph_stufatura'],
                'pressing_start_timestamp': pressing_start.isoformat(),
                'pressing_end_timestamp': pressing_end.isoformat(),
                'press_operator': batch['batch_supervisor']
            }
            records.append(pressing_record)
        
        return records
    
    def insert_manufacturing_batches(self, batches: List[Dict]):
        """Insert manufacturing batches into database"""
        for batch in batches:
            self.conn.execute("""
                INSERT INTO cheese_manufacturing_batches (batch_uuid, lot_uuid, standardized_milk_lot,
                                                        recipe_id, cheese_type, vat_id, batch_size_kg,
                                                        start_timestamp, expected_end_timestamp,
                                                        actual_end_timestamp, batch_supervisor, shift_code, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (batch['batch_uuid'], batch['lot_uuid'], batch['standardized_milk_lot'],
                  batch['recipe_id'], batch['cheese_type'], batch['vat_id'], batch['batch_size_kg'],
                  batch['start_timestamp'], batch['expected_end_timestamp'],
                  batch['actual_end_timestamp'], batch['batch_supervisor'], batch['shift_code'], batch['status']))
        self.conn.commit()
    
    def insert_coagulation_records(self, records: List[Dict]):
        """Insert coagulation records into database"""
        for record in records:
            self.conn.execute("""
                INSERT INTO coagulation_records (coag_id, batch_uuid, milk_temp_celsius, culture_type,
                                               culture_amount_units, culture_added_timestamp, rennet_type,
                                               rennet_amount_ml, rennet_added_timestamp, calcium_chloride_ml,
                                               coagulation_time_minutes, curd_firmness_score, ph_at_cutting,
                                               temperature_at_cutting, cutting_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (record['coag_id'], record['batch_uuid'], record['milk_temp_celsius'], record['culture_type'],
                  record['culture_amount_units'], record['culture_added_timestamp'], record['rennet_type'],
                  record['rennet_amount_ml'], record['rennet_added_timestamp'], record['calcium_chloride_ml'],
                  record['coagulation_time_minutes'], record['curd_firmness_score'], record['ph_at_cutting'],
                  record['temperature_at_cutting'], record['cutting_timestamp']))
        self.conn.commit()
    
    def insert_curd_processing_records(self, records: List[Dict]):
        """Insert curd processing records into database"""
        for record in records:
            self.conn.execute("""
                INSERT INTO curd_processing_records (processing_id, batch_uuid, cutting_size_mm,
                                                   cutting_duration_minutes, healing_time_minutes,
                                                   stirring_speed_rpm, cooking_start_temp_celsius,
                                                   cooking_end_temp_celsius, cooking_time_minutes,
                                                   whey_drainage_start_timestamp, whey_volume_liters,
                                                   curd_moisture_percentage, ph_at_drainage, syneresis_rate, operator_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (record['processing_id'], record['batch_uuid'], record['cutting_size_mm'],
                  record['cutting_duration_minutes'], record['healing_time_minutes'],
                  record['stirring_speed_rpm'], record['cooking_start_temp_celsius'],
                  record['cooking_end_temp_celsius'], record['cooking_time_minutes'],
                  record['whey_drainage_start_timestamp'], record['whey_volume_liters'],
                  record['curd_moisture_percentage'], record['ph_at_drainage'], record['syneresis_rate'], record['operator_id']))
        self.conn.commit()
    
    def insert_pressing_records(self, records: List[Dict]):
        """Insert pressing records into database"""
        for record in records:
            self.conn.execute("""
                INSERT INTO pressing_records (pressing_id, batch_uuid, press_id, initial_weight_kg,
                                            press_sequence, total_pressing_time_hours, final_weight_kg,
                                            moisture_loss_percentage, final_ph, pressing_start_timestamp,
                                            pressing_end_timestamp, press_operator)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (record['pressing_id'], record['batch_uuid'], record['press_id'], record['initial_weight_kg'],
                  record['press_sequence'], record['total_pressing_time_hours'], record['final_weight_kg'],
                  record['moisture_loss_percentage'], record['final_ph'], record['pressing_start_timestamp'],
                  record['pressing_end_timestamp'], record['press_operator']))
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        self.conn.close() 