-- SQLite Weighing, Pricing, and Distribution Systems

CREATE TABLE IF NOT EXISTS weighing_equipment (
    scale_id TEXT PRIMARY KEY,
    equipment_model TEXT,
    manufacturer TEXT, -- 'MORRISON', 'METTLER_TOLEDO', 'AVERY_WEIGH_TRONIX' 
    ntep_certification TEXT,
    max_capacity_kg REAL,
    readability_g REAL,
    location_code TEXT,
    last_calibration_date TEXT,
    next_calibration_due TEXT,
    legal_for_trade INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS catch_weight_transactions (
    transaction_id TEXT PRIMARY KEY,
    package_uuid TEXT REFERENCES individual_packages(package_uuid),
    scale_id TEXT REFERENCES weighing_equipment(scale_id),
    gross_weight_g REAL,
    tare_weight_g REAL,
    net_weight_g REAL,
    price_per_kg REAL,
    total_price REAL,
    currency TEXT DEFAULT 'USD',
    weigh_timestamp TEXT,
    operator_id TEXT,
    customer_order_number TEXT
);

CREATE TABLE IF NOT EXISTS pricing_rules (
    pricing_rule_id TEXT PRIMARY KEY,
    product_code TEXT,
    customer_category TEXT, -- 'RETAIL', 'WHOLESALE', 'FOODSERVICE'
    price_per_unit REAL,
    unit_of_measure TEXT,
    minimum_quantity REAL,
    volume_discount_percentage REAL,
    effective_start_date TEXT,
    effective_end_date TEXT,
    currency TEXT,
    active_flag INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS inventory_transactions (
    inventory_trans_id TEXT PRIMARY KEY,
    lot_uuid TEXT REFERENCES lot_master(lot_uuid),
    transaction_type TEXT, -- 'PRODUCTION', 'CONSUMPTION', 'SALE', 'ADJUSTMENT'
    quantity_change_kg REAL,
    unit_cost REAL,
    total_value REAL,
    location_code TEXT,
    transaction_timestamp TEXT,
    reason_code TEXT,
    reference_document TEXT,
    operator_id TEXT
);

CREATE TABLE IF NOT EXISTS weighing_pricing (
    weighing_uuid TEXT PRIMARY KEY,
    lot_uuid TEXT REFERENCES lot_master(lot_uuid),
    weighing_date TEXT NOT NULL,
    total_weight_kg REAL,
    yield_percentage REAL,
    unit_price_eur REAL,
    total_value_eur REAL,
    packaging_weight_g REAL,
    net_weight_kg REAL,
    quality_grade TEXT,
    market_destination TEXT,
    pricing_notes TEXT
);

CREATE INDEX idx_weighing_pricing_lot_uuid ON weighing_pricing (lot_uuid); 