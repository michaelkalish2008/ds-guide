-- SQLite Shipping and Logistics Tracking

CREATE TABLE IF NOT EXISTS shipping_carriers (
    carrier_id TEXT PRIMARY KEY,
    carrier_name TEXT,
    service_types TEXT, -- Array stored as TEXT in SQLite 
    temperature_monitoring_capable INTEGER,
    tracking_system_url TEXT,
    api_endpoint TEXT,
    contact_info TEXT, -- JSON stored as TEXT in SQLite
    insurance_coverage REAL
);

CREATE TABLE IF NOT EXISTS shipments (
    shipment_id TEXT PRIMARY KEY,
    shipment_uuid TEXT UNIQUE,
    carrier_id TEXT REFERENCES shipping_carriers(carrier_id),
    pickup_timestamp TEXT,
    estimated_delivery_timestamp TEXT,
    actual_delivery_timestamp TEXT,
    origin_location TEXT,
    destination_location TEXT,
    total_weight_kg REAL,
    total_value REAL,
    temperature_controlled INTEGER,
    target_temp_celsius REAL,
    tracking_number TEXT,
    bill_of_lading TEXT,
    shipping_status TEXT
);

CREATE TABLE IF NOT EXISTS shipment_contents (
    shipment_line_id TEXT PRIMARY KEY,
    shipment_id TEXT REFERENCES shipments(shipment_id),
    package_uuid TEXT REFERENCES individual_packages(package_uuid),
    quantity_shipped INTEGER,
    unit_weight_kg REAL,
    line_value REAL,
    customer_po_number TEXT,
    customer_item_code TEXT
);

-- Cold chain monitoring integration
CREATE TABLE IF NOT EXISTS temperature_monitoring (
    monitoring_id TEXT PRIMARY KEY,
    shipment_id TEXT REFERENCES shipments(shipment_id),
    sensor_id TEXT,
    reading_timestamp TEXT,
    temperature_celsius REAL,
    humidity_percentage REAL,
    gps_latitude REAL,
    gps_longitude REAL,
    alert_triggered INTEGER DEFAULT 0,
    alert_type TEXT, -- 'TEMPERATURE', 'HUMIDITY', 'SHOCK', 'DOOR_OPEN'
    battery_level_percentage INTEGER
);

CREATE TABLE IF NOT EXISTS delivery_confirmations (
    delivery_id TEXT PRIMARY KEY,
    shipment_id TEXT REFERENCES shipments(shipment_id),
    delivery_timestamp TEXT,
    recipient_name TEXT,
    recipient_signature TEXT, -- BLOB stored as TEXT in SQLite
    delivery_notes TEXT,
    photo_proof_url TEXT,
    delivery_condition TEXT, -- 'GOOD', 'DAMAGED', 'TEMPERATURE_ABUSE'
    driver_id TEXT
); 