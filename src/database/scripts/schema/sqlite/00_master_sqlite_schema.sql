-- Master SQLite Schema for Cheese Manufacturing Database
-- Complete setup for SQLite compatibility

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Import all schema components in dependency order
.read 01_core_architecture.sqlite.sql
.read 02_raw_materials_suppliers.sqlite.sql
.read 03_preprocessing_operations.sqlite.sql
.read 04_manufacturing_process.sqlite.sql
.read 05_aging_maturation.sqlite.sql
.read 06_quality_control_testing.sqlite.sql
.read 07_sensory_analysis.sqlite.sql
.read 08_packaging_operations.sqlite.sql
.read 09_labeling_regulatory.sqlite.sql
.read 10_weighing_pricing_distribution.sqlite.sql
.read 11_shipping_logistics.sqlite.sql
.read 12_advanced_relationships_views.sqlite.sql
.read 13_performance_optimization.sqlite.sql

-- Verify setup
SELECT 'SQLite database setup complete!' as status;
SELECT COUNT(*) as total_tables FROM sqlite_master WHERE type='table';
SELECT COUNT(*) as total_views FROM sqlite_master WHERE type='view';
SELECT COUNT(*) as total_indexes FROM sqlite_master WHERE type='index'; 
