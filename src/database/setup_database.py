import sqlite3
import os
from pathlib import Path
from .data_generators import (
    CoreDataGenerator, RawMaterialsGenerator, PreprocessingGenerator,
    ManufacturingGenerator, AgingGenerator, QualityGenerator,
    SensoryGenerator, PackagingGenerator, LabelingGenerator,
    WeighingGenerator, ShippingGenerator
)

def setup_database(db_path="cheese_manufacturing.db"):
    """Complete database setup with all schemas and synthetic data"""
    
    # Create database and load schema
    print("Creating database and loading schema...")
    conn = sqlite3.connect(db_path)
    
    # Load the master schema
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "database" / "sqlite" / "00_master_sqlite_schema.sql"
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    
    conn.close()
    
    # Generate data for all schemas in order
    print("Generating core architecture data...")
    core_gen = CoreDataGenerator(db_path)
    core_gen.populate_data()
    core_gen.close()
    
    print("Generating raw materials and suppliers data...")
    raw_gen = RawMaterialsGenerator(db_path)
    raw_gen.populate_data()
    raw_gen.close()
    
    print("Generating preprocessing operations data...")
    preprocess_gen = PreprocessingGenerator(db_path)
    preprocess_gen.populate_data()
    preprocess_gen.close()
    
    print("Generating manufacturing process data...")
    mfg_gen = ManufacturingGenerator(db_path)
    mfg_gen.populate_data()
    mfg_gen.close()
    
    print("Generating aging and maturation data...")
    aging_gen = AgingGenerator(db_path)
    aging_gen.populate_data()
    aging_gen.close()
    
    print("Generating quality control data...")
    quality_gen = QualityGenerator(db_path)
    quality_gen.populate_data()
    quality_gen.close()
    
    print("Generating sensory analysis data...")
    sensory_gen = SensoryGenerator(db_path)
    sensory_gen.populate_data()
    sensory_gen.close()
    
    print("Generating packaging operations data...")
    packaging_gen = PackagingGenerator(db_path)
    packaging_gen.populate_data()
    packaging_gen.close()
    
    print("Generating labeling and regulatory data...")
    labeling_gen = LabelingGenerator(db_path)
    labeling_gen.populate_data()
    labeling_gen.close()
    
    print("Generating weighing and pricing data...")
    weighing_gen = WeighingGenerator(db_path)
    weighing_gen.populate_data()
    weighing_gen.close()
    
    print("Generating shipping and logistics data...")
    shipping_gen = ShippingGenerator(db_path)
    shipping_gen.populate_data()
    shipping_gen.close()
    
    print("Database setup complete!")
    
    # Verify the setup
    verify_database(db_path)

def verify_database(db_path):
    """Verify all tables have been populated"""
    conn = sqlite3.connect(db_path)
    
    tables = [
        'lot_master', 'suppliers', 'supplier_certifications', 'raw_material_lots',
        'milk_quality_tests', 'ingredient_quality_tests', 'preprocessing_batches',
        'pasteurization_records', 'standardization_records', 'cheese_manufacturing_batches',
        'coagulation_records', 'curd_processing_records', 'pressing_records',
        'aging_caves', 'aging_lots', 'environmental_monitoring', 'aging_activities',
        'wheel_positions', 'quality_test_methods', 'quality_test_results',
        'composition_tests', 'microbiology_tests', 'sensory_panels',
        'panelist_qualifications', 'sensory_evaluations', 'sensory_attributes',
        'packaging_lines', 'packaging_materials', 'packaging_runs', 'individual_packages',
        'product_labels', 'traceability_lot_codes', 'critical_tracking_events',
        'package_labels', 'weighing_equipment', 'catch_weight_transactions',
        'pricing_rules', 'inventory_transactions', 'shipping_carriers', 'shipments',
        'shipment_contents', 'temperature_monitoring', 'delivery_confirmations',
        'batch_genealogy'
    ]
    
    print("\nDatabase Verification:")
    print("=" * 50)
    
    for table in tables:
        try:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"{table:35} : {count:5} records")
        except sqlite3.OperationalError:
            print(f"{table:35} : Table not found")
    
    conn.close()

if __name__ == "__main__":
    setup_database() 