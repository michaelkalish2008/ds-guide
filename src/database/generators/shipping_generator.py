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
        self._populate_shipping_carriers()
        self._populate_shipments()
        self._populate_shipment_contents()
        self._populate_temperature_monitoring()
        self._populate_delivery_confirmations()
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

    def _populate_shipping_carriers(self):
        """Populate shipping carriers table"""
        cursor = self.conn.cursor()
        
        carriers = [
            ("FEDEX", "FedEx Express", "ACTIVE", "Express shipping service"),
            ("UPS", "UPS Ground", "ACTIVE", "Ground shipping service"),
            ("DHL", "DHL International", "ACTIVE", "International shipping"),
            ("USPS", "US Postal Service", "ACTIVE", "Standard mail service"),
            ("TRUCK", "Local Trucking", "ACTIVE", "Local delivery service"),
            ("AIR", "Air Freight", "ACTIVE", "Air freight service")
        ]
        
        for carrier_id, carrier_name, status, description in carriers:
            cursor.execute("""
                INSERT OR IGNORE INTO shipping_carriers 
                (carrier_id, carrier_name, service_types, temperature_monitoring_capable,
                 tracking_system_url, api_endpoint, contact_info, insurance_coverage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (carrier_id, carrier_name, "EXPRESS,GROUND", 1,
                  f"https://{carrier_id.lower()}.com/track", f"https://api.{carrier_id.lower()}.com",
                  '{"phone": "1-800-CARRIER", "email": "support@carrier.com"}', random.uniform(1000, 5000)))
        
        print(f"  ✅ Generated {len(carriers)} shipping carriers")

    def _populate_shipments(self):
        """Populate shipments table"""
        cursor = self.conn.cursor()
        
        # Get some lots
        cursor.execute("SELECT lot_uuid FROM lot_master LIMIT 10")
        lots = cursor.fetchall()
        
        for lot in lots:
            lot_uuid = lot[0]
            shipment_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO shipments 
                (shipment_id, shipment_uuid, carrier_id, pickup_timestamp,
                 estimated_delivery_timestamp, actual_delivery_timestamp,
                 origin_location, destination_location, total_weight_kg, total_value)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                shipment_id, str(uuid.uuid4()), random.choice(["FEDEX", "UPS", "DHL"]),
                "2024-01-15 08:00:00", "2024-01-18 17:00:00", "2024-01-17 14:30:00",
                "Cheese Factory", random.choice(["Retail Store", "Distribution Center", "Customer"]),
                random.uniform(10, 50), random.uniform(200, 1000)
            ))
        
        print(f"  ✅ Generated {len(lots)} shipments")

    def _populate_shipment_contents(self):
        """Populate shipment contents table"""
        cursor = self.conn.cursor()
        
        # Get some shipments
        cursor.execute("SELECT shipment_id FROM shipments LIMIT 10")
        shipments = cursor.fetchall()
        
        for shipment in shipments:
            shipment_id = shipment[0]
            content_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO shipment_contents 
                (shipment_line_id, shipment_id, package_uuid, quantity_shipped,
                 unit_weight_kg, line_value, customer_po_number, customer_item_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                content_id, shipment_id, str(uuid.uuid4()), random.randint(10, 100),
                random.uniform(0.24, 0.26), random.uniform(50, 200),
                f"PO{random.randint(1000, 9999)}", f"ITEM{random.randint(100, 999)}"
            ))
        
        print(f"  ✅ Generated {len(shipments)} shipment contents")

    def _populate_temperature_monitoring(self):
        """Populate temperature monitoring table"""
        cursor = self.conn.cursor()
        
        # Get some shipments
        cursor.execute("SELECT shipment_id FROM shipments LIMIT 10")
        shipments = cursor.fetchall()
        
        if not shipments:
            # Create some test shipments
            cursor.execute("SELECT lot_uuid FROM lot_master LIMIT 5")
            lots = cursor.fetchall()
            
            for lot in lots:
                shipment_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO shipments 
                    (shipment_id, lot_uuid, destination, carrier, tracking_number,
                     shipping_date, expected_delivery_date, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (shipment_id, lot[0], "Test Destination", "Test Carrier",
                      f"TRK{random.randint(100000, 999999)}", "2024-01-15", "2024-01-20", "IN_TRANSIT"))
            
            self.conn.commit()
            cursor.execute("SELECT shipment_id FROM shipments LIMIT 10")
            shipments = cursor.fetchall()
        
        for shipment in shipments:
            shipment_id = shipment[0]
            
            # Generate temperature readings every 2 hours for 5 days
            for hour in range(0, 120, 2):  # 5 days * 24 hours
                monitoring_id = str(uuid.uuid4())
                timestamp = datetime(2024, 1, 15) + timedelta(hours=hour)
                
                cursor.execute("""
                    INSERT INTO temperature_monitoring 
                    (monitoring_id, shipment_id, sensor_id, reading_timestamp,
                     temperature_celsius, humidity_percentage, gps_latitude, gps_longitude,
                     alert_triggered, alert_type, battery_level_percentage)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    monitoring_id, shipment_id, f"SENSOR{random.randint(1, 5):03d}",
                    timestamp.strftime("%Y-%m-%d %H:%M:%S"), random.uniform(2, 8), random.uniform(60, 80),
                    random.uniform(40.0, 45.0), random.uniform(-75.0, -70.0), 0, "NORMAL",
                    random.randint(80, 100)
                ))
        
        print(f"  ✅ Generated temperature monitoring data for {len(shipments)} shipments")

    def _populate_delivery_confirmations(self):
        """Populate delivery confirmations table"""
        cursor = self.conn.cursor()
        
        # Get some shipments
        cursor.execute("SELECT shipment_id FROM shipments LIMIT 10")
        shipments = cursor.fetchall()
        
        if not shipments:
            # Create some test shipments
            cursor.execute("SELECT lot_uuid FROM lot_master LIMIT 5")
            lots = cursor.fetchall()
            
            for lot in lots:
                shipment_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO shipments 
                    (shipment_id, lot_uuid, destination, carrier, tracking_number,
                     shipping_date, expected_delivery_date, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (shipment_id, lot[0], "Test Destination", "Test Carrier",
                      f"TRK{random.randint(100000, 999999)}", "2024-01-15", "2024-01-20", "IN_TRANSIT"))
            
            self.conn.commit()
            cursor.execute("SELECT shipment_id FROM shipments LIMIT 10")
            shipments = cursor.fetchall()
        
        for shipment in shipments:
            shipment_id = shipment[0]
            delivery_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO delivery_confirmations 
                (delivery_id, shipment_id, delivery_timestamp, recipient_name,
                 recipient_signature, delivery_notes, photo_proof_url, delivery_condition, driver_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                delivery_id, shipment_id, "2024-01-20 14:30:00",
                f"Recipient {random.randint(1, 10)}", "SIGNATURE_BLOB_DATA",
                "Delivered to loading dock", "https://example.com/photo.jpg", "GOOD",
                f"DRIVER{random.randint(1, 5):03d}"
            ))
        
        print(f"  ✅ Generated {len(shipments)} delivery confirmations")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
