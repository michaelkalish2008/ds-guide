import pytest
import sqlite3
from pathlib import Path
import tempfile
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from scripts.generation.generate_synthetic_data import CheeseManufacturingDataGenerator

class TestFullWorkflow:
    @pytest.fixture
    def generator(self, temp_db):
        """Create generator with temp database"""
        return CheeseManufacturingDataGenerator(str(temp_db))
    
    @pytest.mark.slow
    def test_full_month_generation(self, generator):
        """Test generating full month of data (slow test)"""
        generator.generate_one_month_data()
        
        # Verify database file exists and has content
        assert generator.db_path.exists()
        assert generator.db_path.stat().st_size > 0
        
        # Check all tables have data
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Only check these required tables for data
        required_tables = [
            "lot_master",
            "suppliers",
            "raw_material_lots",
            "pasteurization_batches",
            "aging_caves",
            "aging_lots",
            "quality_tests",
            "packaging_operations",
            "labeling_regulatory",
            "weighing_pricing",
            "shipping_logistics",
            "supplier_certifications",
            "milk_quality_tests",
            "ingredient_quality_tests",
            "cheese_manufacturing_batches",
            "manufacturing_batches",
            "coagulation_records",
            "curd_processing_records",
            "pressing_records",
            "environmental_monitoring",
            "aging_activities",
            "wheel_positions",
            "sensory_evaluations"
        ]
        for table in required_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                assert count > 0, f"Table {table} has no data"
        
        conn.close()
    
    def test_data_quality_checks(self, generator):
        """Test data quality and consistency"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 5)
        
        generator.generate_one_month_data()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Check for null values in critical fields
        cursor.execute("""
            SELECT COUNT(*) FROM lot_master 
            WHERE lot_number IS NULL OR lot_date IS NULL OR product_code IS NULL
        """)
        null_count = cursor.fetchone()[0]
        assert null_count == 0, "Critical fields should not be null"
        
        # Check date range
        cursor.execute("SELECT MIN(lot_date), MAX(lot_date) FROM lot_master")
        min_date, max_date = cursor.fetchone()
        assert min_date >= "2024-01-01"
        assert max_date <= "2024-01-05"
        
        # Check lot number format
        cursor.execute("SELECT lot_number FROM lot_master LIMIT 5")
        lot_numbers = [row[0] for row in cursor.fetchall()]
        
        for lot_number in lot_numbers:
            assert lot_number.startswith("TAL"), "Lot numbers should start with TAL"
            assert len(lot_number) > 10, "Lot numbers should be properly formatted"
        
        conn.close()
    
    def test_performance_benchmark(self, generator):
        """Test generation performance"""
        import time
        
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 10)
        
        start_time = time.time()
        generator.generate_one_month_data()
        end_time = time.time()
        
        generation_time = end_time - start_time
        
        # Should complete within reasonable time (adjust as needed)
        assert generation_time < 60, f"Generation took {generation_time:.2f}s, should be under 60s"
        
        print(f"Generated 10 days of data in {generation_time:.2f} seconds")
    
    def test_complete_manufacturing_workflow(self, generator):
        """Test complete manufacturing workflow data"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 5)
        
        generator.generate_one_month_data()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Check complete workflow for each lot
        cursor.execute("""
            SELECT l.lot_uuid, l.lot_number,
                   COUNT(DISTINCT m.batch_uuid) as manufacturing_steps,
                   COUNT(DISTINCT q.test_uuid) as quality_tests,
                   COUNT(DISTINCT s.evaluation_id) as sensory_evaluations,
                   COUNT(DISTINCT p.operation_id) as packaging_ops
            FROM lot_master l
            LEFT JOIN manufacturing_batches m ON l.lot_uuid = m.lot_uuid
            LEFT JOIN quality_tests q ON l.lot_uuid = q.lot_uuid
            LEFT JOIN sensory_evaluations s ON l.lot_uuid = s.lot_uuid
            LEFT JOIN packaging_operations p ON l.lot_uuid = p.lot_uuid
            GROUP BY l.lot_uuid
        """)
        
        workflow_data = cursor.fetchall()
        
        for lot_uuid, lot_number, mfg_steps, quality_tests, sensory, packaging in workflow_data:
            assert mfg_steps > 0, f"Lot {lot_number} should have manufacturing steps"
            assert quality_tests > 0, f"Lot {lot_number} should have quality tests"
            assert sensory > 0, f"Lot {lot_number} should have sensory evaluations"
            assert packaging > 0, f"Lot {lot_number} should have packaging operations"
        
        conn.close() 