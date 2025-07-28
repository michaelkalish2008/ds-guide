# Cheese Manufacturing Database - Data Dictionary

## Overview

This data dictionary provides detailed documentation for all tables, columns, and data relationships in the cheese manufacturing database. The database supports comprehensive traceability from raw materials through production, aging, packaging, and distribution.

## Table Categories

### 1. Core Architecture
### 2. Raw Materials & Suppliers  
### 3. Preprocessing Operations
### 4. Manufacturing Process
### 5. Aging & Maturation
### 6. Quality Control & Testing
### 7. Sensory Analysis
### 8. Packaging Operations
### 9. Labeling & Regulatory
### 10. Weighing & Pricing
### 11. Shipping & Logistics

---

## 1. Core Architecture

### `lot_master` - Master Lot Tracking
**Purpose**: Central table for lot-based traceability system

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `lot_uuid` | TEXT PRIMARY KEY | Unique identifier for the lot | `"uuid-1234-5678-90ab"` |
| `lot_number` | TEXT NOT NULL | Human-readable lot identifier | `"TAL-2024-01-15"` |
| `lot_date` | TEXT NOT NULL | Date when lot was created | `"2024-01-15"` |
| `parent_lot_uuid` | TEXT | Reference to parent lot (if applicable) | `"uuid-parent-123"` |
| `product_code` | TEXT NOT NULL | Product type identifier | `"TALEGGIO"` |
| `facility_code` | TEXT NOT NULL | Manufacturing facility | `"FACILITY-A"` |
| `batch_size_kg` | REAL | Total batch weight in kilograms | `500.0` |
| `production_start_timestamp` | TEXT | When production began | `"2024-01-15 08:00:00"` |
| `production_end_timestamp` | TEXT | When production completed | `"2024-01-15 16:00:00"` |
| `status` | TEXT DEFAULT 'ACTIVE' | Current lot status | `"ACTIVE"`, `"COMPLETED"` |
| `created_at` | TEXT | Record creation timestamp | `"2024-01-15 08:00:00"` |
| `updated_at` | TEXT | Last update timestamp | `"2024-01-15 16:00:00"` |

### `batch_genealogy` - Lot Relationships
**Purpose**: Tracks parent-child relationships between lots

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `genealogy_id` | TEXT PRIMARY KEY | Unique genealogy record | `"gen-1234"` |
| `parent_lot_uuid` | TEXT | Parent lot identifier | `"uuid-parent-123"` |
| `child_lot_uuid` | TEXT | Child lot identifier | `"uuid-child-456"` |
| `quantity_contribution_kg` | REAL | Amount contributed | `100.0` |
| `contribution_percentage` | REAL | Percentage contribution | `20.0` |
| `relationship_type` | TEXT | Type of relationship | `"INGREDIENT"`, `"REWORK"` |
| `created_timestamp` | TEXT | Record creation time | `"2024-01-15 08:00:00"` |

---

## 2. Raw Materials & Suppliers

### `suppliers` - Supplier Master Data
**Purpose**: Manages supplier information and certifications

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `supplier_id` | TEXT PRIMARY KEY | Unique supplier identifier | `"SUP-001"` |
| `supplier_name` | TEXT NOT NULL | Supplier company name | `"Dairy Farmers Co-op"` |
| `supplier_type` | TEXT | Type of supplier | `"MILK"`, `"CULTURES"`, `"EQUIPMENT"` |
| `contact_name` | TEXT | Primary contact person | `"John Smith"` |
| `contact_email` | TEXT | Contact email address | `"john@dairyfarmers.com"` |
| `contact_phone` | TEXT | Contact phone number | `"+1-555-123-4567"` |
| `certification_status` | TEXT | Current certification status | `"CERTIFIED"`, `"PENDING"` |
| `last_audit_date` | TEXT | Date of last audit | `"2024-01-01"` |
| `risk_rating` | TEXT | Supplier risk assessment | `"LOW"`, `"MEDIUM"`, `"HIGH"` |
| `approved_materials` | TEXT | List of approved materials | `"MILK,CULTURES,RENNET"` |
| `active_flag` | INTEGER DEFAULT 1 | Whether supplier is active | `1` (active), `0` (inactive) |
| `address` | TEXT | Street address | `"123 Dairy Lane"` |
| `city` | TEXT | City | `"Cheeseville"` |
| `state` | TEXT | State/province | `"CA"` |
| `zip_code` | TEXT | Postal code | `"90210"` |
| `country` | TEXT | Country | `"USA"` |

### `raw_material_lots` - Raw Material Tracking
**Purpose**: Tracks individual lots of raw materials

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `raw_lot_uuid` | TEXT PRIMARY KEY | Unique raw material lot ID | `"raw-uuid-123"` |
| `supplier_id` | TEXT | Reference to supplier | `"SUP-001"` |
| `material_type` | TEXT NOT NULL | Type of raw material | `"MILK"`, `"CULTURES"`, `"RENNET"` |
| `lot_number` | TEXT UNIQUE NOT NULL | Supplier lot number | `"MILK-2024-001"` |
| `arrival_date` | TEXT NOT NULL | When material arrived | `"2024-01-15"` |
| `quantity_kg` | REAL | Quantity received | `1000.0` |
| `quality_parameters` | TEXT | Quality specifications | `"FAT:3.5%,PROTEIN:3.2%"` |
| `temperature_c` | REAL | Temperature at arrival | `4.0` |
| `ph_level` | REAL | pH level | `6.7` |
| `fat_content` | REAL | Fat percentage | `3.5` |
| `protein_content` | REAL | Protein percentage | `3.2` |
| `microbiological_results` | TEXT | Micro test results | `"TBC:1000,Coliforms:<10"` |
| `quality_score` | REAL | Overall quality score | `95.0` |
| `status` | TEXT DEFAULT 'PENDING' | Current status | `"PENDING"`, `"APPROVED"`, `"REJECTED"` |

### `milk_quality_tests` - Milk-Specific Testing
**Purpose**: Detailed milk quality testing results

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `test_id` | TEXT PRIMARY KEY | Unique test identifier | `"MILK-TEST-001"` |
| `raw_lot_uuid` | TEXT | Reference to raw material lot | `"raw-uuid-123"` |
| `test_timestamp` | TEXT NOT NULL | When test was performed | `"2024-01-15 09:00:00"` |
| `temperature_celsius` | REAL | Milk temperature | `4.0` |
| `fat_percentage` | REAL | Fat content percentage | `3.5` |
| `protein_percentage` | REAL | Protein content percentage | `3.2` |
| `ph_level` | REAL | pH level | `6.7` |
| `somatic_cell_count` | INTEGER | Somatic cell count | `250000` |
| `total_bacterial_count` | INTEGER | Total bacterial count | `15000` |
| `antibiotic_test_result` | TEXT | Antibiotic test result | `"NEGATIVE"`, `"POSITIVE"` |
| `acidity_titratable` | REAL | Titratable acidity | `0.15` |
| `freezing_point` | REAL | Freezing point depression | `-0.520` |
| `test_operator` | TEXT | Who performed the test | `"LAB-TECH-001"` |
| `pass_fail` | TEXT | Test result | `"PASS"`, `"FAIL"` |

---

## 3. Preprocessing Operations

### `preprocessing_batches` - Preprocessing Operations
**Purpose**: Tracks preprocessing operations like pasteurization and standardization

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `preprocess_uuid` | TEXT PRIMARY KEY | Unique preprocessing batch ID | `"prep-uuid-123"` |
| `input_lot_uuid` | TEXT | Reference to input raw material | `"raw-uuid-123"` |
| `process_type` | TEXT | Type of preprocessing | `"PASTEURIZATION"`, `"STANDARDIZATION"` |
| `equipment_id` | TEXT | Equipment used | `"PASTEURIZER-001"` |
| `start_timestamp` | TEXT | When process started | `"2024-01-15 10:00:00"` |
| `end_timestamp` | TEXT | When process completed | `"2024-01-15 10:30:00"` |
| `target_output_kg` | REAL | Expected output weight | `950.0` |
| `actual_output_kg` | REAL | Actual output weight | `945.0` |
| `yield_percentage` | REAL | Process yield percentage | `94.5` |
| `operator_id` | TEXT | Operator performing process | `"OP-001"` |
| `recipe_id` | TEXT | Recipe used | `"RECIPE-001"` |
| `status` | TEXT | Process status | `"COMPLETED"`, `"IN_PROGRESS"` |

### `pasteurization_records` - Pasteurization Details
**Purpose**: Detailed pasteurization process parameters

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `record_id` | TEXT PRIMARY KEY | Unique record identifier | `"PASTEUR-001"` |
| `preprocess_uuid` | TEXT | Reference to preprocessing batch | `"prep-uuid-123"` |
| `holding_temp_celsius` | REAL | Target holding temperature | `72.0` |
| `holding_time_seconds` | INTEGER | Target holding time | `15` |
| `actual_temp_celsius` | REAL | Actual temperature achieved | `71.8` |
| `actual_time_seconds` | INTEGER | Actual holding time | `16` |
| `flow_rate_lpm` | REAL | Flow rate in liters per minute | `500.0` |
| `inlet_temp_celsius` | REAL | Inlet temperature | `4.0` |
| `outlet_temp_celsius` | REAL | Outlet temperature | `72.0` |
| `pressure_bar` | REAL | System pressure | `2.5` |
| `deviation_flag` | INTEGER DEFAULT 0 | Whether parameters deviated | `0` (no), `1` (yes) |
| `corrective_action` | TEXT | Corrective action taken | `"Adjusted flow rate"` |
| `timestamp` | TEXT | When record was created | `"2024-01-15 10:15:00"` |
| `chart_recorder_file` | TEXT | Chart recorder file path | `"/charts/pasteur-001.pdf"` |

---

## 4. Manufacturing Process

### `cheese_manufacturing_batches` - Manufacturing Batches
**Purpose**: Tracks individual cheese manufacturing batches

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `batch_uuid` | TEXT PRIMARY KEY | Unique batch identifier | `"batch-uuid-123"` |
| `lot_uuid` | TEXT | Reference to lot master | `"lot-uuid-123"` |
| `standardized_milk_lot` | TEXT | Reference to standardized milk | `"prep-uuid-123"` |
| `recipe_id` | TEXT | Recipe used | `"TALEGGIO-RECIPE"` |
| `cheese_type` | TEXT | Type of cheese | `"TALEGGIO"` |
| `vat_id` | TEXT | Vat used for production | `"VAT-001"` |
| `batch_size_kg` | REAL | Batch size in kilograms | `500.0` |
| `start_timestamp` | TEXT | When batch started | `"2024-01-15 11:00:00"` |
| `expected_end_timestamp` | TEXT | Expected completion time | `"2024-01-15 15:00:00"` |
| `actual_end_timestamp` | TEXT | Actual completion time | `"2024-01-15 14:45:00"` |
| `batch_supervisor` | TEXT | Supervisor overseeing batch | `"SUPERVISOR-001"` |
| `shift_code` | TEXT | Production shift | `"DAY"`, `"NIGHT"` |
| `status` | TEXT | Batch status | `"IN_PROGRESS"`, `"COMPLETED"` |

### `coagulation_records` - Coagulation Process
**Purpose**: Detailed coagulation process parameters

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `coag_id` | TEXT PRIMARY KEY | Unique coagulation record | `"COAG-001"` |
| `batch_uuid` | TEXT | Reference to manufacturing batch | `"batch-uuid-123"` |
| `milk_temp_celsius` | REAL | Milk temperature | `32.0` |
| `culture_type` | TEXT | Type of culture used | `"MESOPHILIC"` |
| `culture_amount_units` | INTEGER | Amount of culture added | `50` |
| `culture_added_timestamp` | TEXT | When culture was added | `"2024-01-15 11:05:00"` |
| `rennet_type` | TEXT | Type of rennet | `"ANIMAL"`, `"MICROBIAL"` |
| `rennet_amount_ml` | REAL | Amount of rennet in ml | `25.0` |
| `rennet_added_timestamp` | TEXT | When rennet was added | `"2024-01-15 11:30:00"` |
| `calcium_chloride_ml` | REAL | Calcium chloride added | `5.0` |
| `coagulation_time_minutes` | INTEGER | Time to coagulation | `45` |
| `curd_firmness_score` | INTEGER | Curd firmness (1-10) | `7` |
| `ph_at_cutting` | REAL | pH at cutting time | `6.2` |
| `temperature_at_cutting` | REAL | Temperature at cutting | `32.0` |
| `cutting_timestamp` | TEXT | When curd was cut | `"2024-01-15 12:15:00"` |

---

## 5. Aging & Maturation

### `aging_lots` - Aging Lot Management
**Purpose**: Tracks cheese during aging process

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `aging_lot_uuid` | TEXT PRIMARY KEY | Unique aging lot identifier | `"aging-uuid-123"` |
| `lot_uuid` | TEXT NOT NULL | Reference to lot master | `"lot-uuid-123"` |
| `batch_uuid` | TEXT | Reference to manufacturing batch | `"batch-uuid-123"` |
| `cave_id` | TEXT NOT NULL | Aging cave identifier | `"CAVE-001"` |
| `aging_start_date` | TEXT | When aging began | `"2024-01-16"` |
| `planned_aging_days` | INTEGER | Planned aging duration | `60` |
| `actual_aging_days` | INTEGER | Actual aging duration | `58` |
| `initial_weight_kg` | REAL | Weight at start of aging | `450.0` |
| `current_weight_kg` | REAL | Current weight | `420.0` |
| `weight_loss_percentage` | REAL | Percentage weight loss | `6.7` |
| `wheel_count` | INTEGER | Number of cheese wheels | `45` |
| `aging_status` | TEXT | Current aging status | `"AGING"`, `"COMPLETED"` |
| `target_grade` | TEXT | Target quality grade | `"PREMIUM"`, `"STANDARD"` |
| `shelf_location` | TEXT | Physical location in cave | `"SHELF-A-ROW-3"` |

### `aging_caves` - Aging Cave Management
**Purpose**: Manages aging cave environments

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `cave_id` | TEXT PRIMARY KEY | Unique cave identifier | `"CAVE-001"` |
| `cave_name` | TEXT NOT NULL | Cave name | `"Cave A - Premium"` |
| `capacity_wheels` | INTEGER | Maximum wheel capacity | `1000` |
| `target_temp_celsius` | REAL | Target temperature | `12.0` |
| `target_humidity_percentage` | REAL | Target humidity | `85.0` |
| `air_circulation_cfm` | REAL | Air circulation rate | `500.0` |
| `cave_type` | TEXT | Type of cave | `"PREMIUM"`, `"STANDARD"` |
| `active_flag` | INTEGER DEFAULT 1 | Whether cave is active | `1` (active), `0` (inactive) |
| `created_at` | TEXT | When cave was created | `"2024-01-01 00:00:00"` |
| `updated_at` | TEXT | Last update timestamp | `"2024-01-15 16:00:00"` |

### `environmental_monitoring` - Environmental Controls
**Purpose**: Continuous environmental monitoring data

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `reading_id` | TEXT PRIMARY KEY | Unique reading identifier | `"READING-001"` |
| `monitor_id` | TEXT | Monitoring device ID | `"MONITOR-001"` |
| `sensor_id` | TEXT | Sensor identifier | `"SENSOR-TEMP-001"` |
| `cave_id` | TEXT NOT NULL | Reference to aging cave | `"CAVE-001"` |
| `reading_timestamp` | TEXT | When reading was taken | `"2024-01-15 14:30:00"` |
| `timestamp` | TEXT | Alternative timestamp field | `"2024-01-15 14:30:00"` |
| `temperature_celsius` | REAL | Temperature reading | `12.2` |
| `humidity_percentage` | REAL | Humidity reading | `85.5` |
| `airflow_cfm` | REAL | Airflow rate | `500.0` |
| `air_velocity_mps` | REAL | Air velocity in m/s | `0.5` |
| `co2_concentration_ppm` | REAL | CO2 concentration | `800.0` |
| `ammonia_concentration_ppm` | REAL | Ammonia concentration | `5.0` |
| `alert_triggered` | INTEGER DEFAULT 0 | Whether alert was triggered | `0` (no), `1` (yes) |
| `notes` | TEXT | Additional notes | `"Normal operation"` |

---

## 6. Quality Control & Testing

### `quality_tests` - Quality Test Results
**Purpose**: Stores quality test results for lots

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `test_uuid` | TEXT PRIMARY KEY | Unique test identifier | `"TEST-001"` |
| `lot_uuid` | TEXT | Reference to lot master | `"lot-uuid-123"` |
| `test_date` | TEXT NOT NULL | Date test was performed | `"2024-01-15"` |
| `test_type` | TEXT NOT NULL | Type of test | `"COMPOSITION"`, `"MICROBIOLOGY"` |
| `test_method` | TEXT | Testing method used | `"AOAC_920.123"` |
| `target_range` | TEXT | Target range for test | `"6.0-6.8"` |
| `actual_result` | REAL | Actual test result | `6.5` |
| `ph_level` | REAL | pH level (legacy field) | `6.5` |
| `unit` | TEXT | Unit of measurement | `"pH"`, `"%"`, `"CFU/g"` |
| `frequency` | TEXT | Test frequency | `"DAILY"`, `"WEEKLY"` |
| `analyst_id` | TEXT | Analyst performing test | `"ANALYST-001"` |
| `test_passed` | INTEGER | Whether test passed | `1` (pass), `0` (fail) |
| `notes` | TEXT | Additional notes | `"Within specification"` |

### `quality_test_methods` - Test Method Definitions
**Purpose**: Defines quality testing methods and specifications

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `method_id` | TEXT PRIMARY KEY | Unique method identifier | `"METHOD-001"` |
| `method_name` | TEXT | Name of test method | `"pH Measurement"` |
| `test_category` | TEXT | Category of test | `"COMPOSITION"`, `"MICROBIOLOGY"` |
| `unit_of_measure` | TEXT | Unit of measurement | `"pH"`, `"%"`, `"CFU/g"` |
| `specification_min` | REAL | Minimum acceptable value | `6.0` |
| `specification_max` | REAL | Maximum acceptable value | `6.8` |
| `test_frequency` | TEXT | How often to test | `"DAILY"`, `"WEEKLY"` |
| `ccp_associated` | INTEGER DEFAULT 0 | Whether associated with CCP | `1` (yes), `0` (no) |
| `regulatory_required` | INTEGER DEFAULT 0 | Whether required by regulation | `1` (yes), `0` (no) |
| `method_reference` | TEXT | Reference standard | `"AOAC_920.123"` |

---

## 7. Sensory Analysis

### `sensory_evaluations` - Sensory Evaluation Results
**Purpose**: Professional sensory evaluation results

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `evaluation_id` | TEXT PRIMARY KEY | Unique evaluation identifier | `"EVAL-001"` |
| `lot_uuid` | TEXT NOT NULL | Reference to lot master | `"lot-uuid-123"` |
| `panel_id` | TEXT NOT NULL | Reference to sensory panel | `"PANEL-001"` |
| `panelist_id` | TEXT NOT NULL | Reference to panelist | `"PANELIST-001"` |
| `evaluation_timestamp` | TEXT | When evaluation was performed | `"2024-01-15 14:00:00"` |
| `sample_code` | TEXT | Sample identifier | `"SAMPLE-001"` |
| `sample_age_days` | INTEGER | Age of cheese sample | `45` |
| `sample_temperature_celsius` | REAL | Temperature of sample | `20.0` |
| `overall_quality_score` | INTEGER | Overall quality (1-10) | `8` |
| `defect_intensity_score` | TEXT | Defect intensity | `"SLIGHT"`, `"DEFINITE"` |
| `panel_notes` | TEXT | Panel notes | `"Excellent aroma development"` |
| `evaluation_notes` | TEXT | Detailed observations | `"Creamy texture, nutty flavor"` |

### `sensory_attributes` - Individual Attribute Scores
**Purpose**: Detailed sensory attribute scoring

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `attribute_id` | TEXT PRIMARY KEY | Unique attribute identifier | `"ATTR-001"` |
| `evaluation_id` | TEXT | Reference to evaluation | `"EVAL-001"` |
| `attribute_category` | TEXT | Category of attribute | `"APPEARANCE"`, `"AROMA"`, `"TEXTURE"` |
| `attribute_name` | TEXT | Name of attribute | `"Creaminess"`, `"Nutty"` |
| `intensity_score` | INTEGER | Intensity score (0-9) | `7` |
| `quality_score` | INTEGER | Quality score (1-10) | `8` |
| `descriptor_notes` | TEXT | Descriptive notes | `"Rich, buttery aroma"` |
| `defect_flag` | INTEGER DEFAULT 0 | Whether defect is present | `0` (no), `1` (yes) |
| `benchmark_comparison` | TEXT | Comparison to benchmark | `"Similar to premium Taleggio"` |

---

## 8. Packaging Operations

### `packaging_operations` - Packaging Operations
**Purpose**: Tracks packaging operations for lots

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `operation_id` | TEXT PRIMARY KEY | Unique operation identifier | `"OP-001"` |
| `lot_uuid` | TEXT NOT NULL | Reference to lot master | `"lot-uuid-123"` |
| `packaging_date` | TEXT | Date of packaging | `"2024-03-15"` |
| `operation_type` | TEXT | Type of operation | `"VACUUM_PACK"`, `"FLOW_WRAP"` |
| `equipment_id` | TEXT | Equipment used | `"PACKAGER-001"` |
| `target_weight_g` | REAL | Target package weight | `250.0` |
| `actual_weight_g` | REAL | Actual package weight | `248.0` |
| `pieces_packaged` | INTEGER | Number of pieces packaged | `1800` |
| `operator_id` | TEXT | Operator performing work | `"OP-001"` |
| `temperature_c` | REAL | Temperature during packaging | `18.0` |
| `humidity_percent` | REAL | Humidity during packaging | `45.0` |
| `status` | TEXT | Operation status | `"COMPLETED"`, `"IN_PROGRESS"` |
| `notes` | TEXT | Additional notes | `"Normal operation"` |
| `operation_date` | TEXT | Alternative date field | `"2024-03-15"` |
| `package_type` | TEXT | Type of package | `"VACUUM_BAG"`, `"TRAY_WRAP"` |
| `quantity` | INTEGER | Quantity packaged | `1800` |

### `packaging_runs` - Packaging Run Management
**Purpose**: Manages individual packaging runs

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `packaging_run_uuid` | TEXT PRIMARY KEY | Unique run identifier | `"RUN-001"` |
| `aging_lot_id` | TEXT | Reference to aging lot | `"aging-uuid-123"` |
| `line_id` | TEXT | Reference to packaging line | `"LINE-001"` |
| `target_package_size_g` | REAL | Target package size | `250.0` |
| `target_package_count` | INTEGER | Target number of packages | `1800` |
| `actual_package_count` | INTEGER | Actual packages produced | `1785` |
| `packaging_start_timestamp` | TEXT | When run started | `"2024-03-15 08:00:00"` |
| `packaging_end_timestamp` | TEXT | When run completed | `"2024-03-15 12:00:00"` |
| `line_efficiency_percentage` | REAL | Line efficiency | `95.0` |
| `waste_percentage` | REAL | Waste percentage | `2.5` |
| `operator_id` | TEXT | Operator running line | `"OP-001"` |
| `shift_supervisor` | TEXT | Shift supervisor | `"SUPERVISOR-001"` |
| `quality_hold_flag` | INTEGER DEFAULT 0 | Whether on quality hold | `0` (no), `1` (yes) |

### `individual_packages` - Individual Package Tracking
**Purpose**: Tracks individual packages with quality data

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `package_uuid` | TEXT PRIMARY KEY | Unique package identifier | `"PKG-001"` |
| `packaging_run_uuid` | TEXT | Reference to packaging run | `"RUN-001"` |
| `package_sequence_number` | INTEGER | Sequence number in run | `1` |
| `actual_weight_g` | REAL | Actual package weight | `248.0` |
| `target_weight_g` | REAL | Target package weight | `250.0` |
| `weight_variance_percentage` | REAL | Weight variance | `-0.8` |
| `packaging_timestamp` | TEXT | When packaged | `"2024-03-15 08:15:00"` |
| `checkweigher_result` | TEXT | Checkweigher result | `"PASS"`, `"UNDERWEIGHT"` |
| `metal_detector_result` | TEXT | Metal detector result | `"PASS"`, `"FAIL"` |
| `seal_integrity_result` | TEXT | Seal integrity result | `"PASS"`, `"FAIL"` |
| `reject_reason` | TEXT | Reason for rejection | `"Underweight"` |
| `package_barcode` | TEXT | Package barcode | `"1234567890123"` |
| `consumer_unit_flag` | INTEGER DEFAULT 1 | Whether consumer unit | `1` (yes), `0` (no) |

---

## 9. Labeling & Regulatory

### `product_labels` - Product Label Definitions
**Purpose**: Defines product label content and requirements

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `label_id` | TEXT PRIMARY KEY | Unique label identifier | `"LABEL-001"` |
| `product_code` | TEXT | Product code | `"TALEGGIO"` |
| `label_version` | TEXT | Label version | `"V2.1"` |
| `brand_name` | TEXT | Brand name | `"Artisan Cheese Co."` |
| `product_name` | TEXT | Product name | `"Taleggio DOP"` |
| `net_weight_declaration` | TEXT | Net weight declaration | `"250g"` |
| `ingredient_statement` | TEXT | Ingredient statement | `"Milk, salt, cultures, rennet"` |
| `nutrition_facts_panel` | TEXT | Nutrition facts (JSON) | `{"calories": 320, "fat": 25}` |
| `allergen_statement` | TEXT | Allergen information | `"Contains milk"` |
| `storage_instructions` | TEXT | Storage instructions | `"Keep refrigerated"` |
| `use_by_statement` | TEXT | Use by statement | `"Best before date shown"` |
| `regulatory_approval_date` | TEXT | Regulatory approval date | `"2024-01-01"` |
| `artwork_file_path` | TEXT | Path to artwork file | `"/artwork/taleggio-label.pdf"` |

### `traceability_lot_codes` - FSMA 204 Compliance
**Purpose**: FDA traceability compliance for FSMA 204

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `tlc_id` | TEXT PRIMARY KEY | Unique TLC identifier | `"TLC-001"` |
| `lot_uuid` | TEXT | Reference to lot master | `"lot-uuid-123"` |
| `traceability_lot_code` | TEXT UNIQUE NOT NULL | Alphanumeric TLC | `"TAL20240115001"` |
| `product_covered` | INTEGER | Subject to FSMA 204 | `1` (yes), `0` (no) |
| `cheese_category` | TEXT | Cheese category | `"SOFT_RIPENED"` |
| `unpasteurized_milk` | INTEGER DEFAULT 0 | Contains unpasteurized milk | `0` (no), `1` (yes) |
| `created_timestamp` | TEXT | When TLC was created | `"2024-01-15 08:00:00"` |
| `data_retention_years` | INTEGER DEFAULT 2 | Data retention period | `2` |

---

## 10. Weighing & Pricing

### `weighing_pricing` - Weighing and Pricing Data
**Purpose**: Tracks weighing operations and pricing

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `weighing_uuid` | TEXT PRIMARY KEY | Unique weighing identifier | `"WEIGH-001"` |
| `lot_uuid` | TEXT | Reference to lot master | `"lot-uuid-123"` |
| `weighing_date` | TEXT NOT NULL | Date of weighing | `"2024-03-15"` |
| `total_weight_kg` | REAL | Total weight | `420.0` |
| `yield_percentage` | REAL | Yield percentage | `84.0` |
| `unit_price_eur` | REAL | Unit price in EUR | `15.50` |
| `total_value_eur` | REAL | Total value in EUR | `6510.00` |
| `packaging_weight_g` | REAL | Packaging weight | `5.0` |
| `net_weight_kg` | REAL | Net weight | `415.0` |
| `quality_grade` | TEXT | Quality grade | `"PREMIUM"`, `"STANDARD"` |
| `market_destination` | TEXT | Market destination | `"RETAIL"`, `"WHOLESALE"` |
| `pricing_notes` | TEXT | Pricing notes | `"Premium grade pricing"` |

### `weighing_equipment` - Weighing Equipment
**Purpose**: Manages weighing equipment and calibration

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `scale_id` | TEXT PRIMARY KEY | Unique scale identifier | `"SCALE-001"` |
| `equipment_model` | TEXT | Equipment model | `"MT-5000"` |
| `manufacturer` | TEXT | Equipment manufacturer | `"METTLER_TOLEDO"` |
| `ntep_certification` | TEXT | NTEP certification | `"NTEP-12345"` |
| `max_capacity_kg` | REAL | Maximum capacity | `100.0` |
| `readability_g` | REAL | Readability in grams | `1.0` |
| `location_code` | TEXT | Location code | `"PACKAGING-LINE-1"` |
| `last_calibration_date` | TEXT | Last calibration date | `"2024-01-01"` |
| `next_calibration_due` | TEXT | Next calibration due | `"2024-04-01"` |
| `legal_for_trade` | INTEGER DEFAULT 1 | Legal for trade | `1` (yes), `0` (no) |

---

## 11. Shipping & Logistics

### `shipments` - Shipment Management
**Purpose**: Tracks shipments and delivery

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `shipment_id` | TEXT PRIMARY KEY | Unique shipment identifier | `"SHIP-001"` |
| `shipment_uuid` | TEXT UNIQUE | Alternative UUID | `"ship-uuid-123"` |
| `carrier_id` | TEXT | Reference to carrier | `"CARRIER-001"` |
| `pickup_timestamp` | TEXT | When picked up | `"2024-03-15 14:00:00"` |
| `estimated_delivery_timestamp` | TEXT | Estimated delivery | `"2024-03-17 10:00:00"` |
| `actual_delivery_timestamp` | TEXT | Actual delivery | `"2024-03-17 09:30:00"` |
| `origin_location` | TEXT | Origin location | `"FACILITY-A"` |
| `destination_location` | TEXT | Destination location | `"DISTRIBUTION-CENTER-1"` |
| `total_weight_kg` | REAL | Total shipment weight | `400.0` |
| `total_value` | REAL | Total shipment value | `6200.00` |
| `temperature_controlled` | INTEGER | Temperature controlled | `1` (yes), `0` (no) |
| `target_temp_celsius` | REAL | Target temperature | `4.0` |
| `tracking_number` | TEXT | Carrier tracking number | `"1Z999AA1234567890"` |
| `bill_of_lading` | TEXT | Bill of lading number | `"BOL-001"` |
| `shipping_status` | TEXT | Shipping status | `"IN_TRANSIT"`, `"DELIVERED"` |

### `temperature_monitoring` - Cold Chain Monitoring
**Purpose**: Monitors temperature during shipping

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `monitoring_id` | TEXT PRIMARY KEY | Unique monitoring record | `"MON-001"` |
| `shipment_id` | TEXT | Reference to shipment | `"SHIP-001"` |
| `sensor_id` | TEXT | Sensor identifier | `"SENSOR-001"` |
| `reading_timestamp` | TEXT | When reading taken | `"2024-03-16 12:00:00"` |
| `temperature_celsius` | REAL | Temperature reading | `4.2` |
| `humidity_percentage` | REAL | Humidity reading | `85.0` |
| `gps_latitude` | REAL | GPS latitude | `40.7128` |
| `gps_longitude` | REAL | GPS longitude | `-74.0060` |
| `alert_triggered` | INTEGER DEFAULT 0 | Whether alert triggered | `0` (no), `1` (yes) |
| `alert_type` | TEXT | Type of alert | `"TEMPERATURE"`, `"HUMIDITY"` |
| `battery_level_percentage` | INTEGER | Battery level | `85` |

---

## Data Relationships

### Primary Relationships
- **`lot_master`** is the central table linking all operations
- **`batch_genealogy`** tracks parent-child lot relationships
- **`aging_lots`** links manufacturing to aging operations
- **`packaging_operations`** links aging to packaging
- **`shipments`** links packaging to distribution

### Key Foreign Keys
- `lot_uuid` appears in most tables as the primary linking field
- `batch_uuid` links manufacturing operations
- `aging_lot_uuid` links aging operations
- `packaging_run_uuid` links packaging operations
- `shipment_id` links shipping operations

### Data Flow
1. **Raw Materials** → `raw_material_lots` → `lot_master`
2. **Manufacturing** → `cheese_manufacturing_batches` → `lot_master`
3. **Aging** → `aging_lots` → `lot_master`
4. **Packaging** → `packaging_operations` → `lot_master`
5. **Shipping** → `shipments` → `lot_master`

---

## Data Types Summary

### SQLite Data Types Used
- **TEXT**: Strings, dates, timestamps, UUIDs
- **REAL**: Decimal numbers (weights, temperatures, percentages)
- **INTEGER**: Whole numbers, flags, counts
- **PRIMARY KEY**: Unique identifiers
- **FOREIGN KEY**: References to other tables

### Common Patterns
- **UUIDs**: Used for unique identifiers (e.g., `lot_uuid`, `batch_uuid`)
- **Timestamps**: Stored as TEXT in ISO format
- **Flags**: INTEGER with 0/1 values for boolean fields
- **Percentages**: REAL values (e.g., 85.0 for 85%)
- **Weights**: REAL values in kilograms or grams

---

## Usage Examples

### Query Examples
```sql
-- Find all lots with quality issues
SELECT l.lot_number, q.test_type, q.actual_result, q.test_passed
FROM lot_master l
JOIN quality_tests q ON l.lot_uuid = q.lot_uuid
WHERE q.test_passed = 0;

-- Track aging progress
SELECT l.lot_number, a.aging_start_date, a.current_weight_kg, a.weight_loss_percentage
FROM lot_master l
JOIN aging_lots a ON l.lot_uuid = a.lot_uuid
WHERE a.aging_status = 'AGING';

-- Monitor environmental conditions
SELECT c.cave_name, e.temperature_celsius, e.humidity_percentage
FROM aging_caves c
JOIN environmental_monitoring e ON c.cave_id = e.cave_id
WHERE e.reading_timestamp >= datetime('now', '-1 hour');
```

This data dictionary provides comprehensive documentation for all tables and columns in the cheese manufacturing database, enabling effective data analysis, reporting, and system integration. 