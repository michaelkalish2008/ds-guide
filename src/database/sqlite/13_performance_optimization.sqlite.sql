-- SQLite Performance Optimization and Indexing Strategy

-- Essential indexes for high-performance queries 
CREATE INDEX idx_lot_master_product_date ON lot_master (product_code, lot_date DESC);
CREATE INDEX idx_quality_tests_lot_method ON quality_test_results (lot_uuid, method_id);
CREATE INDEX idx_environmental_cave_time ON environmental_monitoring (cave_id, timestamp DESC);
CREATE INDEX idx_packaging_timestamp ON individual_packages (packaging_timestamp DESC);
CREATE INDEX idx_shipment_status ON shipments (shipping_status, estimated_delivery_timestamp);

-- Composite indexes for common query patterns
CREATE INDEX idx_batch_genealogy_parent_child ON batch_genealogy (parent_lot_uuid, child_lot_uuid);
CREATE INDEX idx_traceability_product_date ON traceability_lot_codes (product_covered, created_timestamp DESC);
CREATE INDEX idx_temperature_monitoring_shipment_time ON temperature_monitoring (shipment_id, reading_timestamp DESC);

-- Additional indexes for common lookups
CREATE INDEX idx_suppliers_type ON suppliers (supplier_type, active_flag);
-- CREATE INDEX idx_raw_materials_supplier ON raw_material_lots (supplier_id, received_date);
CREATE INDEX idx_manufacturing_batches_supervisor ON cheese_manufacturing_batches (batch_supervisor, start_timestamp);
CREATE INDEX idx_aging_lots_cave_id ON aging_lots (cave_id);
CREATE INDEX idx_aging_lots_lot_uuid ON aging_lots (lot_uuid); 
CREATE INDEX idx_sensory_evaluations_lot ON sensory_evaluations (lot_uuid, evaluation_timestamp); 