-- SQLite Raw Materials Receiving and Supplier Management

-- Supplier Master Data
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id TEXT PRIMARY KEY,
    supplier_name TEXT NOT NULL,
    supplier_type TEXT,
    contact_name TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    contact_info TEXT,
    certification_status TEXT,
    last_audit_date TEXT,
    risk_rating TEXT,
    approved_materials TEXT,
    active_flag INTEGER DEFAULT 1,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    country TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS supplier_certifications (
    cert_id TEXT PRIMARY KEY,
    supplier_id TEXT REFERENCES suppliers(supplier_id),
    cert_type TEXT, -- 'ORGANIC', 'HACCP', 'SQF', 'BRC'
    cert_number TEXT,
    issue_date TEXT,
    expiry_date TEXT,
    certifying_body TEXT,
    status TEXT DEFAULT 'ACTIVE'
);

-- Raw Material Lots and Quality Parameters
CREATE TABLE IF NOT EXISTS raw_material_lots (
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

-- Milk-specific quality parameters
CREATE TABLE IF NOT EXISTS milk_quality_tests (
    test_id TEXT PRIMARY KEY,
    raw_lot_uuid TEXT REFERENCES raw_material_lots(raw_lot_uuid),
    test_timestamp TEXT NOT NULL,
    temperature_celsius REAL,
    fat_percentage REAL,
    protein_percentage REAL,
    ph_level REAL,
    somatic_cell_count INTEGER,
    total_bacterial_count INTEGER,
    antibiotic_test_result TEXT, -- 'NEGATIVE', 'POSITIVE'
    acidity_titratable REAL,
    freezing_point REAL,
    test_operator TEXT,
    pass_fail TEXT
);

-- Other ingredients quality tracking
CREATE TABLE IF NOT EXISTS ingredient_quality_tests (
    test_id TEXT PRIMARY KEY,
    raw_lot_uuid TEXT REFERENCES raw_material_lots(raw_lot_uuid),
    test_type TEXT, -- 'CULTURES', 'ENZYMES', 'SALT', 'CALCIUM_CHLORIDE'
    test_parameter TEXT,
    result_value REAL,
    unit_of_measure TEXT,
    specification_min REAL,
    specification_max REAL,
    test_date TEXT,
    lab_technician TEXT,
    compliance_status TEXT
); 