import sqlite3
import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path

class AgingGenerator:
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
        
        # Taleggio aging parameters based on the provided process
        self.taleggio_aging = {
            'initial_aging_days': 15,
            'initial_temp_celsius': 4,
            'final_temp_celsius': 10,
            'humidity_percentage': 80,
            'washing_frequency': 3,
            'washing_period_days': 10,
            'washing_solution': 'Salt solution with Brevibacterium linens'
        }
        
    def _ensure_schema_exists(self):
        """Ensure basic schema exists for testing"""
        cursor = self.conn.cursor()
        
        # Check if aging_lots table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='aging_lots'
        """)
        
        if not cursor.fetchone():
            # Create schema matching the real schema
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
                
                CREATE TABLE aging_caves (
                    cave_id TEXT PRIMARY KEY,
                    cave_name TEXT NOT NULL,
                    capacity_wheels INTEGER,
                    target_temp_celsius REAL,
                    target_humidity_percentage REAL,
                    air_circulation_cfm REAL,
                    cave_type TEXT,
                    active_flag INTEGER DEFAULT 1
                );
                
                CREATE TABLE aging_lots (
                    aging_lot_uuid TEXT PRIMARY KEY,
                    lot_uuid TEXT NOT NULL,
                    batch_uuid TEXT,
                    cave_id TEXT NOT NULL,
                    aging_start_date TEXT,
                    planned_aging_days INTEGER,
                    actual_aging_days INTEGER,
                    initial_weight_kg REAL,
                    current_weight_kg REAL,
                    weight_loss_percentage REAL,
                    wheel_count INTEGER,
                    aging_status TEXT,
                    target_grade TEXT,
                    shelf_location TEXT
                );
            """)
            self.conn.commit()
        
    def populate_data(self, current_date=None, lot_count=None):
        """Generate aging and maturation data"""
        print("  Generating aging caves...")
        caves = self.generate_aging_caves()
        self.insert_aging_caves(caves)
        
        print("  Generating aging lots...")
        try:
            batches = self.conn.execute("SELECT batch_uuid, lot_uuid FROM cheese_manufacturing_batches").fetchall()
            print(f"[DEBUG] Found {len(batches)} batches in cheese_manufacturing_batches")
        except sqlite3.OperationalError as e:
            print(f"[DEBUG] Exception fetching batches: {e}")
            # If manufacturing table doesn't exist, create simple aging lots from lot_master
            lots = self.conn.execute("SELECT lot_uuid FROM lot_master").fetchall()
            if not lots:
                print("  ⚠️  No lots found, creating test aging data...")
                return
            # Create simple aging lots for testing
            aging_lots = []
            for lot in lots:
                aging_lot_uuid = str(uuid.uuid4())
                aging_lots.append({
                    'aging_lot_uuid': aging_lot_uuid,
                    'lot_uuid': lot['lot_uuid'],
                    'cave_id': 'CAVE-01',
                    'aging_start_date': current_date.strftime("%Y-%m-%d") if current_date else datetime.now().strftime("%Y-%m-%d"),
                    'expected_aging_days': 60,
                    'current_aging_day': random.randint(1, 60),
                    'status': 'AGING'
                })
            print(f"[DEBUG] Generated {len(aging_lots)} simple aging lots to insert")
            try:
                self.insert_aging_lots(aging_lots)
                print(f"[DEBUG] Inserted {len(aging_lots)} simple aging lots")
            except Exception as e:
                print(f"[DEBUG] Exception inserting simple aging lots: {e}")
            print(f"  ✅ Generated {len(aging_lots)} simple aging lots")
            return
        try:
            aging_lots = self.generate_aging_lots(batches, caves)
            print(f"[DEBUG] Generated {len(aging_lots)} aging lots to insert")
            # Ensure every lot gets an aging lot if not already present
            all_lots = self.conn.execute("SELECT lot_uuid FROM lot_master").fetchall()
            batch_lot_uuids = set([batch['lot_uuid'] for batch in batches])
            for lot in all_lots:
                if lot['lot_uuid'] not in batch_lot_uuids:
                    # Create a simple aging lot for lots without a batch
                    aging_lot_uuid = str(uuid.uuid4())
                    aging_lots.append({
                        'aging_lot_uuid': aging_lot_uuid,
                        'lot_uuid': lot['lot_uuid'],
                        'cave_id': 'CAVE-01',
                        'aging_start_date': datetime.now().strftime('%Y-%m-%d'),
                        'expected_aging_days': 60,
                        'current_aging_day': random.randint(1, 60),
                        'status': 'AGING'
                    })
            print(f"[DEBUG] Total aging lots to insert (after filling missing): {len(aging_lots)}")
            self.insert_aging_lots(aging_lots)
            print(f"[DEBUG] Inserted {len(aging_lots)} aging lots")
        except Exception as e:
            print(f"[DEBUG] Exception generating or inserting aging lots: {e}")
        
        print("  Generating environmental monitoring...")
        env_monitoring = self.generate_environmental_monitoring(caves)
        self.insert_environmental_monitoring(env_monitoring)
        
        print("  Generating aging activities...")
        aging_activities = self.generate_aging_activities(aging_lots)
        self.insert_aging_activities(aging_activities)
        
        print("  Generating wheel positions...")
        wheel_positions = self.generate_wheel_positions(aging_lots, caves)
        self.insert_wheel_positions(wheel_positions)
        
        print(f"  ✅ Generated {len(caves)} caves, {len(aging_lots)} aging lots, {len(env_monitoring)} env readings, {len(aging_activities)} activities, {len(wheel_positions)} wheel positions")
    
    def generate_aging_caves(self) -> List[Dict]:
        """Generate aging cave data"""
        caves = [
            {
                'cave_id': 'CAVE-01',
                'cave_name': 'Taleggio Primary Cave',
                'capacity_wheels': 500,
                'target_temp_celsius': self.taleggio_aging['final_temp_celsius'],
                'target_humidity_percentage': self.taleggio_aging['humidity_percentage'],
                'air_circulation_cfm': 200,
                'cave_type': 'CONTROLLED',
                'active_flag': 1
            },
            {
                'cave_id': 'CAVE-02',
                'cave_name': 'Taleggio Secondary Cave',
                'capacity_wheels': 300,
                'target_temp_celsius': self.taleggio_aging['final_temp_celsius'],
                'target_humidity_percentage': self.taleggio_aging['humidity_percentage'],
                'air_circulation_cfm': 150,
                'cave_type': 'CONTROLLED',
                'active_flag': 1
            },
            {
                'cave_id': 'CAVE-03',
                'cave_name': 'Initial Aging Cave',
                'capacity_wheels': 200,
                'target_temp_celsius': self.taleggio_aging['initial_temp_celsius'],
                'target_humidity_percentage': 70,
                'air_circulation_cfm': 100,
                'cave_type': 'CONTROLLED',
                'active_flag': 1
            }
        ]
        return caves
    
    def generate_aging_lots(self, batches: List[sqlite3.Row], caves: List[Dict]) -> List[Dict]:
        """Generate aging lot data based on Taleggio process"""
        aging_lots = []
        
        for batch in batches:
            aging_lot_uuid = str(uuid.uuid4())
            batch_info = self.conn.execute("SELECT start_timestamp FROM cheese_manufacturing_batches WHERE batch_uuid = ?", (batch['batch_uuid'],)).fetchone()
            start_date = datetime.fromisoformat(batch_info['start_timestamp']).date()
            
            # Taleggio aging schedule
            initial_aging_days = self.taleggio_aging['initial_aging_days']
            total_aging_days = random.randint(40, 60)  # Total aging period
            current_aging_days = random.randint(initial_aging_days, total_aging_days)
            
            # Weight calculations
            batch_size = self.conn.execute("SELECT batch_size_kg FROM cheese_manufacturing_batches WHERE batch_uuid = ?", (batch['batch_uuid'],)).fetchone()['batch_size_kg']
            initial_weight = batch_size * 0.12  # ~12% yield from pressing
            current_weight = initial_weight * (1 - random.uniform(0.05, 0.15))  # 5-15% weight loss
            
            aging_lot = {
                'aging_lot_uuid': aging_lot_uuid,
                'lot_uuid': batch['lot_uuid'],
                'batch_uuid': batch['batch_uuid'],
                'cave_id': random.choice([cave['cave_id'] for cave in caves]),
                'aging_start_date': start_date.strftime('%Y-%m-%d'),
                'planned_aging_days': total_aging_days,
                'actual_aging_days': current_aging_days,
                'initial_weight_kg': initial_weight,
                'current_weight_kg': current_weight,
                'weight_loss_percentage': ((initial_weight - current_weight) / initial_weight) * 100,
                'wheel_count': random.randint(8, 12),  # Number of wheels per batch
                'aging_status': 'AGING' if current_aging_days < total_aging_days else 'READY',
                'target_grade': 'PREMIUM',
                'shelf_location': f"SHELF-{random.randint(1, 10):02d}"
            }
            aging_lots.append(aging_lot)
        
        return aging_lots
    
    def generate_environmental_monitoring(self, caves: List[Dict]) -> List[Dict]:
        """Generate environmental monitoring data"""
        monitoring = []
        
        for cave in caves:
            # Generate hourly readings for the past 30 days
            start_date = datetime.now() - timedelta(days=30)
            
            for i in range(30 * 24):  # 30 days * 24 hours
                reading_time = start_date + timedelta(hours=i)
                
                # Add some realistic variation around target values
                temp_variation = random.uniform(-1, 1)
                humidity_variation = random.uniform(-5, 5)
                
                reading = {
                    'reading_id': str(uuid.uuid4()),
                    'cave_id': cave['cave_id'],
                    'reading_timestamp': reading_time.isoformat(),
                    'temperature_celsius': cave['target_temp_celsius'] + temp_variation,
                    'humidity_percentage': cave['target_humidity_percentage'] + humidity_variation,
                    'air_velocity_mps': random.uniform(0.1, 0.3),
                    'co2_concentration_ppm': random.randint(400, 800),
                    'ammonia_concentration_ppm': random.randint(0, 10),
                    'sensor_id': f"SENSOR-{cave['cave_id']}-{random.randint(1, 3):02d}",
                    'alert_triggered': 0
                }
                monitoring.append(reading)
        
        return monitoring
    
    def generate_aging_activities(self, aging_lots: List[Dict]) -> List[Dict]:
        """Generate aging activities based on Taleggio washing schedule"""
        activities = []
        
        for aging_lot in aging_lots:
            aging_start = datetime.fromisoformat(aging_lot['aging_start_date'])
            
            # Generate washing activities based on Taleggio process
            washing_days = [5, 10, 15]  # 3 washings in 10 days as specified
            
            for i, wash_day in enumerate(washing_days):
                if wash_day <= aging_lot['actual_aging_days']:
                    activity = {
                        'activity_id': str(uuid.uuid4()),
                        'aging_lot_uuid': aging_lot['aging_lot_uuid'],
                        'activity_type': 'WASHING',
                        'scheduled_date': (aging_start + timedelta(days=wash_day)).strftime('%Y-%m-%d'),
                        'completed_timestamp': (aging_start + timedelta(days=wash_day, hours=random.randint(8, 16))).isoformat(),
                        'operator_id': f'OPERATOR-{random.randint(1, 5):02d}',
                        'notes': f"Washing {i+1}/3 with {self.taleggio_aging['washing_solution']}",
                        'surface_condition_score': random.randint(7, 9),
                        'mold_development_notes': "Normal surface development observed",
                        'completed_flag': 1
                    }
                    activities.append(activity)
            
            # Generate turning activities
            turning_days = [3, 7, 12, 18, 25, 35, 45]
            for turn_day in turning_days:
                if turn_day <= aging_lot['actual_aging_days']:
                    activity = {
                        'activity_id': str(uuid.uuid4()),
                        'aging_lot_uuid': aging_lot['aging_lot_uuid'],
                        'activity_type': 'TURNING',
                        'scheduled_date': (aging_start + timedelta(days=turn_day)).strftime('%Y-%m-%d'),
                        'completed_timestamp': (aging_start + timedelta(days=turn_day, hours=random.randint(8, 16))).isoformat(),
                        'operator_id': f'OPERATOR-{random.randint(1, 5):02d}',
                        'notes': f"Regular turning - day {turn_day}",
                        'surface_condition_score': random.randint(6, 9),
                        'mold_development_notes': "Even mold development",
                        'completed_flag': 1
                    }
                    activities.append(activity)
        
        return activities
    
    def generate_wheel_positions(self, aging_lots: List[Dict], caves: List[Dict]) -> List[Dict]:
        """Generate wheel position tracking"""
        positions = []
        
        for aging_lot in aging_lots:
            wheel_count = aging_lot['wheel_count']
            cave_id = aging_lot['cave_id']
            aging_start = datetime.fromisoformat(aging_lot['aging_start_date'])
            
            for wheel_num in range(wheel_count):
                position = {
                    'position_id': str(uuid.uuid4()),
                    'aging_lot_uuid': aging_lot['aging_lot_uuid'],
                    'cave_id': cave_id,
                    'shelf_number': random.randint(1, 10),
                    'position_number': random.randint(1, 20),
                    'placement_timestamp': (aging_start + timedelta(hours=random.randint(1, 24))).isoformat(),
                    'removal_timestamp': None,  # Still in position
                    'wheel_identifier': f"{aging_lot['aging_lot_uuid'][:8]}-W{wheel_num+1:02d}",
                    'current_position': 1
                }
                positions.append(position)
        
        return positions
    
    def insert_aging_caves(self, caves: List[Dict]):
        """Insert aging caves into database"""
        for cave in caves:
            self.conn.execute("""
                INSERT OR IGNORE INTO aging_caves (cave_id, cave_name, capacity_wheels, target_temp_celsius,
                                       target_humidity_percentage, air_circulation_cfm, cave_type, active_flag)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (cave['cave_id'], cave['cave_name'], cave['capacity_wheels'], cave['target_temp_celsius'],
                  cave['target_humidity_percentage'], cave['air_circulation_cfm'], cave['cave_type'], cave['active_flag']))
        self.conn.commit()
    
    def insert_aging_lots(self, aging_lots: List[Dict]):
        """Insert aging lots into database"""
        for lot in aging_lots:
            # Always insert lot_uuid for both full and simple aging lots
            if 'batch_uuid' in lot:
                # Full aging lot with all fields
                self.conn.execute("""
                    INSERT INTO aging_lots (aging_lot_uuid, lot_uuid, batch_uuid, cave_id, aging_start_date,
                                          planned_aging_days, actual_aging_days, initial_weight_kg,
                                          current_weight_kg, weight_loss_percentage, wheel_count,
                                          aging_status, target_grade, shelf_location)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (lot['aging_lot_uuid'], lot['lot_uuid'], lot['batch_uuid'], lot['cave_id'], lot['aging_start_date'],
                      lot['planned_aging_days'], lot['actual_aging_days'], lot['initial_weight_kg'],
                      lot['current_weight_kg'], lot['weight_loss_percentage'], lot['wheel_count'],
                      lot['aging_status'], lot['target_grade'], lot['shelf_location']))
            else:
                # Simple aging lot for testing
                self.conn.execute("""
                    INSERT INTO aging_lots (aging_lot_uuid, lot_uuid, cave_id, aging_start_date,
                                          expected_aging_days, current_aging_day, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (lot['aging_lot_uuid'], lot['lot_uuid'], lot['cave_id'], lot['aging_start_date'],
                      lot['expected_aging_days'], lot['current_aging_day'], lot['status']))
        self.conn.commit()
    
    def insert_environmental_monitoring(self, monitoring: List[Dict]):
        """Insert environmental monitoring into database"""
        for reading in monitoring:
            self.conn.execute("""
                INSERT INTO environmental_monitoring (reading_id, cave_id, reading_timestamp,
                                                    temperature_celsius, humidity_percentage,
                                                    air_velocity_mps, co2_concentration_ppm,
                                                    ammonia_concentration_ppm, sensor_id, alert_triggered)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (reading['reading_id'], reading['cave_id'], reading['reading_timestamp'],
                  reading['temperature_celsius'], reading['humidity_percentage'],
                  reading['air_velocity_mps'], reading['co2_concentration_ppm'],
                  reading['ammonia_concentration_ppm'], reading['sensor_id'], reading['alert_triggered']))
        self.conn.commit()
    
    def insert_aging_activities(self, activities: List[Dict]):
        """Insert aging activities into database"""
        for activity in activities:
            self.conn.execute("""
                INSERT INTO aging_activities (activity_id, aging_lot_uuid, activity_type,
                                            scheduled_date, completed_timestamp, operator_id,
                                            notes, surface_condition_score, mold_development_notes, completed_flag)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (activity['activity_id'], activity['aging_lot_uuid'], activity['activity_type'],
                  activity['scheduled_date'], activity['completed_timestamp'], activity['operator_id'],
                  activity['notes'], activity['surface_condition_score'], activity['mold_development_notes'], activity['completed_flag']))
        self.conn.commit()
    
    def insert_wheel_positions(self, positions: List[Dict]):
        """Insert wheel positions into database"""
        for position in positions:
            self.conn.execute("""
                INSERT INTO wheel_positions (position_id, aging_lot_uuid, cave_id, shelf_number,
                                           position_number, placement_timestamp, removal_timestamp,
                                           wheel_identifier, current_position)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (position['position_id'], position['aging_lot_uuid'], position['cave_id'], position['shelf_number'],
                  position['position_number'], position['placement_timestamp'], position['removal_timestamp'],
                  position['wheel_identifier'], position['current_position']))
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        self.conn.close() 