-- SQLite Preprocessing Operations Data Model

CREATE TABLE IF NOT EXISTS preprocessing_batches (
    preprocess_uuid TEXT PRIMARY KEY,
    input_lot_uuid TEXT REFERENCES raw_material_lots(raw_lot_uuid),
    process_type TEXT, -- 'PASTEURIZATION', 'STANDARDIZATION', 'SEPARATION'
    equipment_id TEXT,
    start_timestamp TEXT,
    end_timestamp TEXT,
    target_output_kg REAL,
    actual_output_kg REAL,
    yield_percentage REAL,
    operator_id TEXT,
    recipe_id TEXT,
    status TEXT
);

-- Pasteurization process parameters
CREATE TABLE IF NOT EXISTS pasteurization_records (
    record_id TEXT PRIMARY KEY,
    preprocess_uuid TEXT REFERENCES preprocessing_batches(preprocess_uuid),
    holding_temp_celsius REAL, -- Target: 70-72°C
    holding_time_seconds INTEGER, -- Target: 15-20 seconds
    actual_temp_celsius REAL,
    actual_time_seconds INTEGER,
    flow_rate_lpm REAL,
    inlet_temp_celsius REAL,
    outlet_temp_celsius REAL,
    pressure_bar REAL,
    deviation_flag INTEGER DEFAULT 0,
    corrective_action TEXT,
    timestamp TEXT,
    chart_recorder_file TEXT
);

-- Standardization process tracking
CREATE TABLE IF NOT EXISTS standardization_records (
    record_id TEXT PRIMARY KEY,
    preprocess_uuid TEXT REFERENCES preprocessing_batches(preprocess_uuid),
    target_fat_percentage REAL,
    target_protein_percentage REAL,
    actual_fat_percentage REAL,
    actual_protein_percentage REAL,
    cream_added_kg REAL,
    skim_milk_added_kg REAL,
    mixing_time_minutes INTEGER,
    mixing_temperature_celsius REAL,
    homogenization_pressure_bar REAL,
    final_composition_verified INTEGER,
    timestamp TEXT
); 