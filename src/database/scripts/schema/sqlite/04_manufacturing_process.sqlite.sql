-- SQLite Manufacturing Process Data Structures

CREATE TABLE IF NOT EXISTS cheese_manufacturing_batches (
    batch_uuid TEXT PRIMARY KEY,
    lot_uuid TEXT REFERENCES lot_master(lot_uuid),
    standardized_milk_lot TEXT REFERENCES preprocessing_batches(preprocess_uuid),
    recipe_id TEXT,
    cheese_type TEXT,
    vat_id TEXT,
    batch_size_kg REAL,
    start_timestamp TEXT,
    expected_end_timestamp TEXT,
    actual_end_timestamp TEXT,
    batch_supervisor TEXT,
    shift_code TEXT,
    status TEXT
);

-- Coagulation process parameters 
CREATE TABLE IF NOT EXISTS coagulation_records (
    coag_id TEXT PRIMARY KEY,
    batch_uuid TEXT REFERENCES cheese_manufacturing_batches(batch_uuid),
    milk_temp_celsius REAL, -- Typically 30-32°C
    culture_type TEXT,
    culture_amount_units INTEGER,
    culture_added_timestamp TEXT,
    rennet_type TEXT, -- 'ANIMAL', 'MICROBIAL', 'VEGETABLE'
    rennet_amount_ml REAL, -- Typically 20-30ml per 100kg milk
    rennet_added_timestamp TEXT,
    calcium_chloride_ml REAL,
    coagulation_time_minutes INTEGER,
    curd_firmness_score INTEGER, -- 1-10 scale
    ph_at_cutting REAL,
    temperature_at_cutting REAL,
    cutting_timestamp TEXT
);

-- Cutting and draining operations
CREATE TABLE IF NOT EXISTS curd_processing_records (
    processing_id TEXT PRIMARY KEY,
    batch_uuid TEXT REFERENCES cheese_manufacturing_batches(batch_uuid),
    cutting_size_mm INTEGER, -- Curd grain size
    cutting_duration_minutes INTEGER,
    healing_time_minutes INTEGER,
    stirring_speed_rpm INTEGER,
    cooking_start_temp_celsius REAL,
    cooking_end_temp_celsius REAL,
    cooking_time_minutes INTEGER,
    whey_drainage_start_timestamp TEXT,
    whey_volume_liters REAL,
    curd_moisture_percentage REAL,
    ph_at_drainage REAL,
    syneresis_rate REAL, -- ml whey/g curd/hour
    operator_id TEXT
);

-- Pressing operations tracking
CREATE TABLE IF NOT EXISTS pressing_records (
    pressing_id TEXT PRIMARY KEY,
    batch_uuid TEXT REFERENCES cheese_manufacturing_batches(batch_uuid),
    press_id TEXT,
    initial_weight_kg REAL,
    press_sequence TEXT, -- JSON stored as TEXT in SQLite
    total_pressing_time_hours INTEGER,
    final_weight_kg REAL,
    moisture_loss_percentage REAL,
    final_ph REAL,
    pressing_start_timestamp TEXT,
    pressing_end_timestamp TEXT,
    press_operator TEXT
); 

CREATE TABLE IF NOT EXISTS manufacturing_batches (
    batch_uuid TEXT PRIMARY KEY,
    lot_uuid TEXT REFERENCES lot_master(lot_uuid),
    batch_date TEXT NOT NULL,
    process_step TEXT NOT NULL,
    temperature_c REAL,
    duration_minutes INTEGER
); 