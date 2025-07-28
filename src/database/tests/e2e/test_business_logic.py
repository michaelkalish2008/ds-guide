import pytest
import sqlite3
from pathlib import Path
import tempfile
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from scripts.generation.generate_synthetic_data import CheeseManufacturingDataGenerator

class TestBusinessLogic:
    @pytest.fixture
    def generator(self, temp_db):
        """Create generator with temp database"""
        return CheeseManufacturingDataGenerator(str(temp_db))
    
    def test_taleggio_manufacturing_process(self, generator):
        """Test that Taleggio manufacturing process follows correct sequence"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 3)
        
        generator.generate_one_month_data()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Check manufacturing process sequence for a specific lot
        cursor.execute("""
            SELECT m.process_step, m.temperature_c, m.duration_minutes
            FROM manufacturing_batches m
            JOIN lot_master l ON m.lot_uuid = l.lot_uuid
            WHERE l.lot_date = '2024-01-01'
            ORDER BY m.process_step
        """)
        
        process_steps = cursor.fetchall()
        
        # Verify key Taleggio process steps exist
        step_names = [step[0] for step in process_steps]
        
        expected_steps = ['PASTEURIZATION', 'INOCULATION', 'COAGULATION', 'CUTTING', 'FORMING']
        for expected_step in expected_steps:
            assert expected_step in step_names, f"Expected step {expected_step} not found"
        
        conn.close()
    
    def test_quality_control_workflow(self, generator):
        """Test quality control workflow and data integrity"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 3)
        
        generator.generate_one_month_data()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Check that quality tests are performed for each lot
        cursor.execute("""
            SELECT COUNT(DISTINCT l.lot_uuid) as lots_with_tests
            FROM lot_master l
            JOIN quality_tests q ON l.lot_uuid = q.lot_uuid
        """)
        
        lots_with_tests = cursor.fetchone()[0]
        
        # Check total number of lots
        cursor.execute("SELECT COUNT(*) FROM lot_master")
        total_lots = cursor.fetchone()[0]
        
        assert lots_with_tests == total_lots, "All lots should have quality tests"
        
        conn.close()