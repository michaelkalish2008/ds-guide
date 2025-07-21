-- SQLite Core Architecture: Lot-Based Traceability System
-- Adapted from PostgreSQL for SQLite compatibility

-- Master lot tracking table with UUID primary key (using TEXT for SQLite)
CREATE TABLE IF NOT EXISTS lot_master (
    lot_uuid TEXT PRIMARY KEY,
    lot_number TEXT NOT NULL,
    lot_date TEXT NOT NULL, -- SQLite doesn't have DATE type
    parent_lot_uuid TEXT,
    product_code TEXT NOT NULL,
    facility_code TEXT NOT NULL,
    batch_size_kg REAL,
    production_start_timestamp TEXT, -- SQLite doesn't have TIMESTAMP type
    production_end_timestamp TEXT,
    status TEXT DEFAULT 'ACTIVE',
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Create indexes for optimal query performance
CREATE INDEX idx_lot_date_uuid ON lot_master (lot_date, lot_uuid);
CREATE INDEX idx_lot_number ON lot_master (lot_number);
CREATE INDEX idx_product_code ON lot_master (product_code, lot_date); 
