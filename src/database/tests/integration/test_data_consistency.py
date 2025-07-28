import pytest
import sqlite3
from pathlib import Path
import tempfile
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from scripts.generation.generate_synthetic_data import CheeseManufacturingDataGenerator

class TestDataConsistency:
    @pytest.fixture
    def generator(self, temp_db):
        """Create generator with temp database"""
        return CheeseManufacturingDataGenerator(str(temp_db))
    
    def test_lot_number_consistency(self, generator):
        """Test lot number format and uniqueness across all lots"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 5)
        
        generator.generate_one_month_data()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Check lot number format
        cursor.execute("SELECT lot_number FROM lot_master")
        lot_numbers = [row[0] for row in cursor.fetchall()]
        
        for lot_number in lot_numbers:
            # Should start with TAL and contain date
            assert lot_number.startswith("TAL"), f"Lot number {lot_number} should start with TAL"
            assert "2024" in lot_number, f"Lot number {lot_number} should contain year 2024"
        
        # Check uniqueness
        assert len(lot_numbers) == len(set(lot_numbers)), "Lot numbers should be unique"
        
        conn.close()
    
    def test_date_sequence_consistency(self, generator):
        """Test that dates are sequential and match expected range"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 5)
        
        generator.generate_one_month_data()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT lot_date FROM lot_master ORDER BY lot_date")
        dates = [row[0] for row in cursor.fetchall()]
        
        # Check date sequence
        expected_dates = [
            "2024-01-01", "2024-01-02", "2024-01-03", 
            "2024-01-04", "2024-01-05"
        ]
        
        assert dates == expected_dates, f"Date sequence mismatch. Expected {expected_dates}, got {dates}"
        
        conn.close()
    
    def test_data_quality_consistency(self, generator):
        """Test data quality across all tables"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 3)
        
        generator.generate_one_month_data()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Check for null values in critical fields
        critical_fields = [
            ("lot_master", "lot_number"),
            ("lot_master", "lot_date"),
            ("lot_master", "product_code"),
            ("suppliers", "supplier_name"),
            ("manufacturing_batches", "process_step"),
            ("quality_tests", "test_type")
        ]
        
        for table, field in critical_fields:
            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {field} IS NULL")
            null_count = cursor.fetchone()[0]
            assert null_count == 0, f"Critical field {table}.{field} should not be null"
        
        conn.close()
    
    def test_taleggio_specific_consistency(self, generator):
        """Test Taleggio-specific data consistency"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 3)
        
        generator.generate_one_month_data()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Check product code consistency
        cursor.execute("SELECT DISTINCT product_code FROM lot_master")
        product_codes = [row[0] for row in cursor.fetchall()]
        assert "TALEGGIO" in product_codes, "Should have TALEGGIO product code"
        
        # Check manufacturing process consistency
        cursor.execute("SELECT DISTINCT process_step FROM manufacturing_batches")
        process_steps = [row[0] for row in cursor.fetchall()]
        
        expected_steps = ['PASTEURIZATION', 'INOCULATION', 'COAGULATION', 'CUTTING', 'FORMING']
        for step in expected_steps:
            assert step in process_steps, f"Expected Taleggio process step {step}"
        
        # Check quality test consistency
        cursor.execute("SELECT DISTINCT test_type FROM quality_tests")
        test_types = [row[0] for row in cursor.fetchall()]
        
        expected_tests = ['PH_MEASUREMENT', 'MOISTURE_CONTENT', 'FAT_CONTENT']
        for test in expected_tests:
            assert test in test_types, f"Expected quality test {test}"
        
        conn.close()
