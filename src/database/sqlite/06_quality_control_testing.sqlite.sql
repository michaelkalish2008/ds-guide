-- SQLite Quality Control and Testing Data Model

CREATE TABLE IF NOT EXISTS quality_test_methods (
    method_id TEXT PRIMARY KEY,
    method_name TEXT,
    test_category TEXT, -- 'COMPOSITION', 'MICROBIOLOGY', 'PHYSICAL', 'SENSORY' 
    unit_of_measure TEXT,
    specification_min REAL,
    specification_max REAL,
    test_frequency TEXT,
    ccp_associated INTEGER DEFAULT 0,
    regulatory_required INTEGER DEFAULT 0,
    method_reference TEXT -- AOAC, ISO, etc.
);

CREATE TABLE IF NOT EXISTS quality_test_results (
    test_result_id TEXT PRIMARY KEY,
    lot_uuid TEXT REFERENCES lot_master(lot_uuid),
    sample_stage TEXT, -- 'RAW_MATERIAL', 'IN_PROCESS', 'FINISHED', 'AGED'
    method_id TEXT REFERENCES quality_test_methods(method_id),
    test_value REAL,
    unit_of_measure TEXT,
    test_timestamp TEXT,
    lab_technician TEXT,
    equipment_id TEXT,
    pass_fail_result TEXT,
    deviation_notes TEXT,
    retest_required INTEGER DEFAULT 0,
    sample_id TEXT,
    certificate_number TEXT
);

-- Cheese composition testing
CREATE TABLE IF NOT EXISTS composition_tests (
    comp_test_id TEXT PRIMARY KEY,
    test_result_id TEXT REFERENCES quality_test_results(test_result_id),
    moisture_percentage REAL,
    fat_percentage REAL,
    salt_percentage REAL,
    protein_percentage REAL,
    ph_level REAL,
    water_activity REAL,
    fat_in_dry_matter REAL, -- FDM calculation
    moisture_in_nonfat_solids REAL, -- MNFS calculation
    salt_in_moisture REAL, -- S/M ratio
    ash_percentage REAL
);

-- Microbiology testing
CREATE TABLE IF NOT EXISTS microbiology_tests (
    micro_test_id TEXT PRIMARY KEY,
    test_result_id TEXT REFERENCES quality_test_results(test_result_id),
    test_organism TEXT,
    result_count INTEGER,
    count_unit TEXT, -- 'CFU_PER_G', 'MPN_PER_G', 'PRESENT_ABSENT'
    enrichment_required INTEGER,
    incubation_temp_celsius INTEGER,
    incubation_time_hours INTEGER,
    detection_limit INTEGER,
    pathogen_status TEXT, -- 'DETECTED', 'NOT_DETECTED', 'PRESUMPTIVE'
    confirmation_required INTEGER DEFAULT 0
); 