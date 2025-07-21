# Move from tests/test_data_integrity.py to tests/integration/test_data_integrity.py
import pytest
import sqlite3
from pathlib import Path
import tempfile
from datetime import datetime
from src.database.generate_synthetic_data import CheeseManufacturingDataGenerator

class TestDataIntegrity:
    @pytest.fixture
    def generator(self, temp_db):
        """Create generator with temp database"""
        return CheeseManufacturingDataGenerator(str(temp_db))
    
    def test_data_consistency_across_tables(self, generator):
        """Test data consistency across all tables"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 5)
        
        generator.generate_one_month_data()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Check that all lots have corresponding records in related tables
        cursor.execute("""
            SELECT COUNT(*) FROM lot_master l
            LEFT JOIN manufacturing_batches m ON l.lot_uuid = m.lot_uuid
            LEFT JOIN quality_tests q ON l.lot_uuid = q.lot_uuid
            LEFT JOIN sensory_evaluations s ON l.lot_uuid = s.lot_uuid
            WHERE m.lot_uuid IS NULL OR q.lot_uuid IS NULL OR s.lot_uuid IS NULL
        """)
        
        incomplete_lots = cursor.fetchone()[0]
        assert incomplete_lots == 0, "All lots should have complete records"
        
        conn.close()
    
    def test_foreign_key_constraints(self, generator):
        """Test foreign key relationships are maintained"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 3)
        
        generator.generate_one_month_data()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Check for orphaned records
        cursor.execute("""
            SELECT COUNT(*) FROM manufacturing_batches m
            LEFT JOIN lot_master l ON m.lot_uuid = l.lot_uuid
            WHERE l.lot_uuid IS NULL
        """)
        
        orphaned_manufacturing = cursor.fetchone()[0]
        assert orphaned_manufacturing == 0, "No orphaned manufacturing records"
        
        cursor.execute("""
            SELECT COUNT(*) FROM quality_tests q
            LEFT JOIN lot_master l ON q.lot_uuid = l.lot_uuid
            WHERE l.lot_uuid IS NULL
        """)
        
        orphaned_quality = cursor.fetchone()[0]
        assert orphaned_quality == 0, "No orphaned quality test records"
        
        conn.close() 