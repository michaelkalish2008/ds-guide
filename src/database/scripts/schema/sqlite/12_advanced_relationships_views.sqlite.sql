-- SQLite Advanced Data Relationships and Views

-- Complete lot genealogy view 
CREATE VIEW complete_lot_traceability AS
SELECT 
    lm.lot_uuid,
    lm.lot_number,
    lm.lot_date,
    lm.product_code,
    lm.batch_size_kg,
    -- Raw material inputs
    rml.supplier_id,
    rml.supplier_lot_number,
    rml.material_code,
    -- Manufacturing data
    cmb.vat_id,
    cmb.cheese_type,
    cmb.batch_supervisor,
    -- Quality test results
    qtr.test_value,
    qtm.method_name,
    qtr.pass_fail_result,
    -- Aging information
    al.cave_id,
    al.aging_start_date,
    al.actual_aging_days,
    -- Packaging details
    pr.line_id,
    pr.packaging_start_timestamp,
    -- Shipping information
    s.shipment_id,
    s.carrier_id,
    s.actual_delivery_timestamp
FROM lot_master lm
LEFT JOIN batch_genealogy bg ON lm.lot_uuid = bg.child_lot_uuid
LEFT JOIN raw_material_lots rml ON bg.parent_lot_uuid = rml.raw_lot_uuid
LEFT JOIN cheese_manufacturing_batches cmb ON lm.lot_uuid = cmb.lot_uuid
LEFT JOIN quality_test_results qtr ON lm.lot_uuid = qtr.lot_uuid
LEFT JOIN quality_test_methods qtm ON qtr.method_id = qtm.method_id
LEFT JOIN aging_lots al ON cmb.lot_uuid = al.lot_uuid
LEFT JOIN packaging_runs pr ON al.aging_lot_id = pr.aging_lot_id
LEFT JOIN individual_packages ip ON pr.packaging_run_uuid = ip.packaging_run_uuid
LEFT JOIN shipment_contents sc ON ip.package_uuid = sc.package_uuid
LEFT JOIN shipments s ON sc.shipment_id = s.shipment_id;

-- Batch genealogy for complex parent-child relationships
-- Note: This table is already defined in 01_core_architecture.sqlite.sql
-- CREATE TABLE batch_genealogy (
--     genealogy_id TEXT PRIMARY KEY,
--     parent_lot_uuid TEXT,
--     child_lot_uuid TEXT REFERENCES lot_master(lot_uuid),
--     quantity_contribution_kg REAL,
--     contribution_percentage REAL,
--     relationship_type TEXT, -- 'INGREDIENT', 'REWORK', 'BLEND', 'SPLIT'
--     created_timestamp TEXT DEFAULT (datetime('now')),
--     UNIQUE(parent_lot_uuid, child_lot_uuid)
-- );