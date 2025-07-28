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

class TestGenerationPerformance:
    @pytest.fixture
    def generator(self, temp_db):
        """Create generator with temp database"""
        return CheeseManufacturingDataGenerator(str(temp_db))
    
    @pytest.mark.slow
    def test_single_day_generation_performance(self, generator):
        """Test performance of single day generation"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 1)
        
        start_time = time.time()
        generator.generate_one_month_data()
        end_time = time.time()
        
        generation_time = end_time - start_time
        
        # Should complete within 10 seconds for single day
        assert generation_time < 10, f"Single day generation took {generation_time:.2f}s, should be under 10s"
        
        print(f"Single day generation completed in {generation_time:.2f} seconds")
    
    @pytest.mark.slow
    def test_week_generation_performance(self, generator):
        """Test performance of week generation"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 7)
        
        start_time = time.time()
        generator.generate_one_month_data()
        end_time = time.time()
        
        generation_time = end_time - start_time
        
        # Should complete within 30 seconds for week
        assert generation_time < 30, f"Week generation took {generation_time:.2f}s, should be under 30s"
        
        print(f"Week generation completed in {generation_time:.2f} seconds")
    
    @pytest.mark.slow
    def test_month_generation_performance(self, generator):
        """Test performance of full month generation"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 31)
        
        start_time = time.time()
        generator.generate_one_month_data()
        end_time = time.time()
        
        generation_time = end_time - start_time
        
        # Should complete within 2 minutes for full month
        assert generation_time < 120, f"Month generation took {generation_time:.2f}s, should be under 120s"
        
        print(f"Month generation completed in {generation_time:.2f} seconds")
    
    def test_memory_usage(self, generator):
        """Test memory usage during generation"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 5)
        
        generator.generate_one_month_data()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 500MB)
        assert memory_increase < 500, f"Memory increase {memory_increase:.1f}MB is too high"
        
        print(f"Memory usage increased by {memory_increase:.1f}MB")
    
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
                   AVG(CAST(q.actual_result AS REAL)) as avg_result, AVG(s.overall_quality_score) as avg_sensory
            FROM lot_master l
            LEFT JOIN manufacturing_batches m ON l.lot_uuid = m.lot_uuid
            LEFT JOIN quality_tests q ON l.lot_uuid = q.lot_uuid
            LEFT JOIN sensory_evaluations s ON l.lot_uuid = s.lot_uuid
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