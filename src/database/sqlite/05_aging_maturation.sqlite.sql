-- SQLite Aging and Maturation Environmental Controls

CREATE TABLE IF NOT EXISTS aging_lots (
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
    -- legacy columns for backward compatibility, not used by generator:
    -- start_date TEXT,
    -- end_date TEXT,
    -- status TEXT DEFAULT 'AGING',
    -- created_at TEXT DEFAULT (datetime('now')),
    -- updated_at TEXT DEFAULT (datetime('now')),
    -- FOREIGN KEY (lot_uuid) REFERENCES lot_master(lot_uuid),
    -- FOREIGN KEY (cave_id) REFERENCES aging_caves(cave_id)
);

CREATE TABLE IF NOT EXISTS aging_caves (
    cave_id TEXT PRIMARY KEY,
    cave_name TEXT NOT NULL,
    capacity_wheels INTEGER,
    target_temp_celsius REAL,
    target_humidity_percentage REAL,
    air_circulation_cfm REAL,
    cave_type TEXT,
    active_flag INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Environmental monitoring with continuous data collection
CREATE TABLE IF NOT EXISTS environmental_monitoring (
    reading_id TEXT PRIMARY KEY,
    monitor_id TEXT,
    sensor_id TEXT,
    cave_id TEXT NOT NULL,
    reading_timestamp TEXT,
    timestamp TEXT,
    temperature_celsius REAL,
    humidity_percentage REAL,
    airflow_cfm REAL,
    air_velocity_mps REAL,
    co2_concentration_ppm REAL,
    ammonia_concentration_ppm REAL,
    alert_triggered INTEGER DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (cave_id) REFERENCES aging_caves(cave_id)
);

CREATE INDEX idx_aging_lots_cave_id ON aging_lots (cave_id);
CREATE INDEX idx_aging_lots_lot_uuid ON aging_lots (lot_uuid);
CREATE INDEX idx_environmental_monitoring_cave_id ON environmental_monitoring (cave_id);

-- Turning and surface treatment schedules 
CREATE TABLE aging_activities (
    activity_id TEXT PRIMARY KEY,
    aging_lot_uuid TEXT REFERENCES aging_lots(aging_lot_uuid),
    activity_type TEXT, -- 'TURNING', 'WASHING', 'BRUSHING', 'COATING'
    scheduled_date TEXT,
    completed_timestamp TEXT,
    operator_id TEXT,
    notes TEXT,
    surface_condition_score INTEGER, -- 1-10 scale
    mold_development_notes TEXT,
    completed_flag INTEGER DEFAULT 0
);

-- Cave inventory and position tracking
CREATE TABLE wheel_positions (
    position_id TEXT PRIMARY KEY,
    aging_lot_uuid TEXT REFERENCES aging_lots(aging_lot_uuid),
    cave_id TEXT REFERENCES aging_caves(cave_id),
    shelf_number INTEGER,
    position_number INTEGER,
    placement_timestamp TEXT,
    removal_timestamp TEXT,
    wheel_identifier TEXT,
    current_position INTEGER DEFAULT 1
); 