-- SQLite Packaging Operations and Material Tracking

CREATE TABLE IF NOT EXISTS packaging_operations (
    operation_id TEXT PRIMARY KEY,
    lot_uuid TEXT NOT NULL,
    packaging_date TEXT,
    operation_type TEXT,
    equipment_id TEXT,
    target_weight_g REAL,
    actual_weight_g REAL,
    pieces_packaged INTEGER,
    operator_id TEXT,
    temperature_c REAL,
    humidity_percent REAL,
    status TEXT,
    notes TEXT,
    operation_date TEXT,
    package_type TEXT,
    quantity INTEGER,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (lot_uuid) REFERENCES lot_master(lot_uuid)
);

CREATE TABLE packaging_lines (
    line_id TEXT PRIMARY KEY,
    line_name TEXT,
    equipment_type TEXT, -- 'THERMOFORM', 'FLOW_WRAP', 'VACUUM', 'MAP' 
    manufacturer TEXT, -- 'MULTIVAC', 'HART_DESIGN', 'SEALED_AIR'
    capacity_packages_per_minute INTEGER,
    max_package_weight_kg REAL,
    current_status TEXT,
    last_maintenance_date TEXT,
    next_maintenance_due TEXT
);

CREATE TABLE packaging_materials (
    material_id TEXT PRIMARY KEY,
    material_name TEXT,
    material_type TEXT, -- 'FILM', 'TRAY', 'LABEL', 'SEAL', 'GAS'
    supplier_id TEXT REFERENCES suppliers(supplier_id),
    lot_number TEXT,
    received_date TEXT,
    expiry_date TEXT,
    quantity_received INTEGER,
    unit_of_measure TEXT,
    specifications TEXT, -- JSON stored as TEXT in SQLite
    food_contact_approved INTEGER DEFAULT 1
);

CREATE TABLE packaging_runs (
    packaging_run_uuid TEXT PRIMARY KEY,
    aging_lot_id TEXT REFERENCES aging_lots(aging_lot_id),
    line_id TEXT REFERENCES packaging_lines(line_id),
    target_package_size_g REAL,
    target_package_count INTEGER,
    actual_package_count INTEGER,
    packaging_start_timestamp TEXT,
    packaging_end_timestamp TEXT,
    line_efficiency_percentage REAL,
    waste_percentage REAL,
    operator_id TEXT,
    shift_supervisor TEXT,
    quality_hold_flag INTEGER DEFAULT 0
);

-- Individual package tracking with weighing integration
CREATE TABLE individual_packages (
    package_uuid TEXT PRIMARY KEY,
    packaging_run_uuid TEXT REFERENCES packaging_runs(packaging_run_uuid),
    package_sequence_number INTEGER,
    actual_weight_g REAL,
    target_weight_g REAL,
    weight_variance_percentage REAL,
    packaging_timestamp TEXT,
    checkweigher_result TEXT, -- 'PASS', 'UNDERWEIGHT', 'OVERWEIGHT'
    metal_detector_result TEXT, -- 'PASS', 'FAIL'
    seal_integrity_result TEXT,
    reject_reason TEXT,
    package_barcode TEXT,
    consumer_unit_flag INTEGER DEFAULT 1
);

CREATE INDEX idx_packaging_operations_lot_uuid ON packaging_operations (lot_uuid); 