-- SQLite Labeling Requirements and Regulatory Compliance

CREATE TABLE IF NOT EXISTS labeling_regulatory (
    label_uuid TEXT PRIMARY KEY,
    lot_uuid TEXT NOT NULL,
    label_date TEXT,
    product_name TEXT,
    brand_name TEXT,
    net_weight TEXT,
    ingredients TEXT,
    nutritional_info TEXT,
    storage_conditions TEXT,
    best_before_date TEXT,
    batch_code TEXT,
    dop_registration TEXT,
    organic_certification TEXT,
    allergen_info TEXT,
    country_of_origin TEXT,
    label_approved INTEGER,
    regulatory_compliance TEXT,
    FOREIGN KEY (lot_uuid) REFERENCES lot_master(lot_uuid)
);

CREATE TABLE product_labels (
    label_id TEXT PRIMARY KEY,
    product_code TEXT,
    label_version TEXT,
    brand_name TEXT,
    product_name TEXT,
    net_weight_declaration TEXT,
    ingredient_statement TEXT,
    nutrition_facts_panel TEXT, -- JSON stored as TEXT in SQLite 
    allergen_statement TEXT,
    storage_instructions TEXT,
    use_by_statement TEXT,
    regulatory_approval_date TEXT,
    artwork_file_path TEXT
);

-- FDA Traceability compliance (FSMA 204)
CREATE TABLE IF NOT EXISTS traceability_lot_codes (
    tlc_id TEXT PRIMARY KEY,
    lot_uuid TEXT REFERENCES lot_master(lot_uuid),
    traceability_lot_code TEXT UNIQUE NOT NULL, -- Alphanumeric TLC
    product_covered INTEGER, -- Subject to FSMA 204
    cheese_category TEXT, -- 'SOFT_UNRIPENED', 'SOFT_RIPENED', 'HARD'
    unpasteurized_milk INTEGER DEFAULT 0,
    created_timestamp TEXT,
    data_retention_years INTEGER DEFAULT 2
);

CREATE TABLE critical_tracking_events (
    cte_id TEXT PRIMARY KEY,
    tlc_id TEXT REFERENCES traceability_lot_codes(tlc_id),
    event_type TEXT, -- 'TRANSFORMATION', 'SHIPPING', 'RECEIVING', 'CREATION'
    event_timestamp TEXT,
    location_description TEXT,
    business_name TEXT,
    business_address TEXT,
    contact_info TEXT, -- JSON stored as TEXT in SQLite
    quantity_units REAL,
    unit_of_measure TEXT
);

-- Package labeling with date/lot coding
CREATE TABLE IF NOT EXISTS package_labels (
    label_instance_id TEXT PRIMARY KEY,
    package_uuid TEXT REFERENCES individual_packages(package_uuid),
    label_id TEXT REFERENCES product_labels(label_id),
    production_date TEXT,
    best_by_date TEXT,
    lot_code TEXT,
    establishment_number TEXT, -- USDA plant number
    upc_code TEXT,
    price_per_pound REAL, -- For variable weight products
    print_timestamp TEXT,
    printer_id TEXT,
    label_verification_passed INTEGER
);

CREATE INDEX idx_labeling_regulatory_lot_uuid ON labeling_regulatory (lot_uuid); 