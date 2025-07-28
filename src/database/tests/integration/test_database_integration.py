import pytest
import sqlite3
from pathlib import Path
import tempfile
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from scripts.generation.generate_synthetic_data import CheeseManufacturingDataGenerator

class TestDatabaseIntegration:
    @pytest.fixture
    def generator(self, temp_db):
        """Create generator with temp database"""
        return CheeseManufacturingDataGenerator(str(temp_db))
    
    def test_full_database_setup(self, generator):
        """Test complete database setup with all schemas"""
        generator.setup_database()
        
        # Check if all tables exist
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Check for key tables from all generators
        expected_tables = [
            'lot_master', 'suppliers', 'supplier_certifications', 'raw_material_lots',
            'pasteurization_batches', 'manufacturing_batches',
            'quality_tests', 'sensory_evaluations', 'packaging_operations',
            'labeling_regulatory', 'weighing_pricing', 'shipping_logistics'
        ]
        
        for table in expected_tables:
            assert table in tables, f"Table {table} not found"
        
        conn.close()
    
    def test_one_week_data_generation(self, generator):
        """Test generating 1 week of data"""
        # Modify date range for faster testing
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 7)
        
        generator.generate_one_month_data()
        
        # Check data was generated
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Check lot_master has 7 entries
        cursor.execute("SELECT COUNT(*) FROM lot_master")
        lot_count = cursor.fetchone()[0]
        assert lot_count == 7
        
        # Check related tables have data
        cursor.execute("SELECT COUNT(*) FROM suppliers")
        supplier_count = cursor.fetchone()[0]
        assert supplier_count > 0
        
        cursor.execute("SELECT COUNT(*) FROM manufacturing_batches")
        manufacturing_count = cursor.fetchone()[0]
        assert manufacturing_count > 0
        
        cursor.execute("SELECT COUNT(*) FROM quality_tests")
        quality_count = cursor.fetchone()[0]
        assert quality_count > 0
        
        cursor.execute("SELECT COUNT(*) FROM sensory_evaluations")
        sensory_count = cursor.fetchone()[0]
        assert sensory_count > 0
        
        conn.close()
    
    def test_data_relationships(self, generator):
        """Test that data relationships are maintained"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 3)
        
        generator.generate_one_month_data()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Check lot_master references
        cursor.execute("""
            SELECT COUNT(*) FROM lot_master l
            LEFT JOIN manufacturing_batches m ON l.lot_uuid = m.lot_uuid
            WHERE m.lot_uuid IS NOT NULL
        """)
        related_count = cursor.fetchone()[0]
        assert related_count > 0
        
        # Check supplier relationships
        cursor.execute("""
            SELECT COUNT(*) FROM raw_material_lots r
            LEFT JOIN suppliers s ON r.supplier_id = s.supplier_id
            WHERE s.supplier_id IS NOT NULL
        """)
        supplier_related = cursor.fetchone()[0]
        assert supplier_related > 0
        
        # Check quality test relationships
        cursor.execute("""
            SELECT COUNT(*) FROM quality_tests q
            LEFT JOIN lot_master l ON q.lot_uuid = l.lot_uuid
            WHERE l.lot_uuid IS NOT NULL
        """)
        quality_related = cursor.fetchone()[0]
        assert quality_related > 0
        
        conn.close()
    
    def test_all_generators_integration(self, generator):
        """Test that all generators work together"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 5)
        
        generator.generate_one_month_data()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Check all generator tables have data
        generator_tables = [
            'lot_master', 'suppliers', 'raw_material_lots', 'pasteurization_batches',
            'manufacturing_batches', 'quality_tests',
            'sensory_evaluations', 'packaging_operations', 'labeling_regulatory',
            'weighing_pricing', 'shipping_logistics'
        ]
        
        for table in generator_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            assert count > 0, f"Table {table} has no data"
        
        conn.close() 