-- SQLite Sensory Analysis Protocols and Scoring Systems
-- Professional sensory evaluation following American Cheese Society (ACS) protocols

CREATE TABLE IF NOT EXISTS sensory_panels (
    panel_id TEXT PRIMARY KEY,
    panel_name TEXT NOT NULL,
    panel_type TEXT, 
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS panelist_qualifications (
    panelist_id TEXT PRIMARY KEY,
    panelist_name TEXT,
    certification_level TEXT, -- 'CERTIFIED', 'EXPERT', 'TRAINED'
    specialization TEXT,
    last_calibration_date TEXT,
    active_status INTEGER DEFAULT 1,
    sensory_acuity_scores TEXT -- JSON stored as TEXT in SQLite 
);

CREATE TABLE IF NOT EXISTS sensory_evaluations (
    evaluation_id TEXT PRIMARY KEY,
    lot_uuid TEXT NOT NULL,
    panel_id TEXT NOT NULL,
    panelist_id TEXT NOT NULL,
    evaluation_timestamp TEXT,
    sample_code TEXT,
    sample_age_days INTEGER,
    sample_temperature_celsius REAL,
    overall_quality_score INTEGER, -- 1-10 scale
    defect_intensity_score TEXT, -- 'SLIGHT', 'DEFINITE', 'PRONOUNCED'
    panel_notes TEXT,
    evaluation_notes TEXT -- Unstructured content for detailed observations
);

-- ACS T.A.S.T.E. Test attributes
CREATE TABLE IF NOT EXISTS sensory_attributes (
    attribute_id TEXT PRIMARY KEY,
    evaluation_id TEXT REFERENCES sensory_evaluations(evaluation_id),
    attribute_category TEXT, -- 'APPEARANCE', 'AROMA', 'TEXTURE', 'FLAVOR'
    attribute_name TEXT,
    intensity_score INTEGER, -- 0-9 scale
    quality_score INTEGER, -- 1-10 scale  
    descriptor_notes TEXT,
    defect_flag INTEGER DEFAULT 0,
    benchmark_comparison TEXT
); 