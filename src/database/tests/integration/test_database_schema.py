# Move from tests/test_database_schema.py to tests/integration/test_database_schema.py
import pytest
import sqlite3
from pathlib import Path
import tempfile
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from scripts.generation.generate_synthetic_data import CheeseManufacturingDataGenerator

class TestDatabaseSchema:
    @pytest.fixture
    def generator(self, temp_db):
        """Create generator with temp database"""
        return CheeseManufacturingDataGenerator(str(temp_db))
    
    def test_schema_creation(self, generator):
        """Test that all schema tables are created correctly"""
        generator.setup_database()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Expected tables from all schema files
        expected_tables = [
            'lot_master', 'suppliers', 'supplier_certifications',
            'raw_material_lots', 'pasteurization_batches', 'manufacturing_batches',
            'quality_tests', 'sensory_evaluations',
            'packaging_operations', 'labeling_regulatory', 'weighing_pricing',
            'shipping_logistics'
        ]
        
        for table in expected_tables:
            assert table in tables, f"Expected table {table} not found"
        
        conn.close()
    
    def test_table_structure(self, generator):
        """Test table structure and constraints"""
        generator.setup_database()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Check lot_master table structure
        cursor.execute("PRAGMA table_info(lot_master)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        assert 'lot_uuid' in columns, "lot_uuid column should exist"
        assert 'lot_number' in columns, "lot_number column should exist"
        assert 'lot_date' in columns, "lot_date column should exist"
        
        # Check that lot_uuid is TEXT (SQLite equivalent of UUID)
        assert columns['lot_uuid'] == 'TEXT', "lot_uuid should be TEXT type"
        
        conn.close()
    
    def test_indexes_creation(self, generator):
        """Test that indexes are created correctly"""
        generator.setup_database()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Check for indexes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cursor.fetchall()]
        
        # Should have indexes for performance
        assert len(indexes) > 0, "Database should have indexes for performance"
        
        conn.close() 