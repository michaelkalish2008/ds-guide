# Move from tests/test_performance.py to tests/performance/test_performance.py
import pytest
import time
import sqlite3
from pathlib import Path
import tempfile
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from scripts.generation.generate_synthetic_data import CheeseManufacturingDataGenerator

class TestPerformance:
    @pytest.fixture
    def generator(self, temp_db):
        """Create generator with temp database"""
        return CheeseManufacturingDataGenerator(str(temp_db))
    
    @pytest.mark.slow
    def test_data_generation_speed(self, generator):
        """Test data generation speed"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 5)
        
        start_time = time.time()
        generator.generate_one_month_data()
        end_time = time.time()
        
        generation_time = end_time - start_time
        
        # Should complete within reasonable time
        assert generation_time < 30, f"Generation took {generation_time:.2f}s, should be under 30s"
        
        print(f"Generated 5 days of data in {generation_time:.2f} seconds")
    
    @pytest.mark.slow
    def test_database_size_optimization(self, generator):
        """Test database size optimization"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 10)
        
        generator.generate_one_month_data()
        
        # Check database size
        db_size = generator.db_path.stat().st_size / 1024 / 1024  # MB
        
        # Should be reasonable size for 10 days of data
        assert db_size < 50, f"Database size {db_size:.1f}MB is too large"
        
        print(f"Database size: {db_size:.1f}MB")
    
    @pytest.mark.slow
    def test_query_performance(self, generator):
        """Test query performance on generated data"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 5)
        
        generator.generate_one_month_data()
        
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        # Test complex query performance
        start_time = time.time()
        cursor.execute("""
            SELECT l.lot_number, COUNT(m.batch_uuid) as batch_count,
                   AVG(CAST(q.actual_result AS REAL)) as avg_result
            FROM lot_master l
            LEFT JOIN manufacturing_batches m ON l.lot_uuid = m.lot_uuid
            LEFT JOIN quality_tests q ON l.lot_uuid = q.lot_uuid
            WHERE q.actual_result IS NOT NULL 
            AND q.actual_result != 'PASS' 
            AND q.actual_result != 'FAIL'
            AND q.actual_result != ''
            GROUP BY l.lot_uuid
            ORDER BY l.lot_date
        """)
        results = cursor.fetchall()
        end_time = time.time()
        
        query_time = end_time - start_time
        
        # Should complete within 1 second
        assert query_time < 1.0, f"Complex query took {query_time:.3f}s, should be under 1s"
        
        print(f"Complex query completed in {query_time:.3f} seconds")
        conn.close() 