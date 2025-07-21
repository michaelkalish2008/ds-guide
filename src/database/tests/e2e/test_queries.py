# Move from tests/test_queries.py to tests/e2e/test_queries.py
import pytest
import sqlite3
from pathlib import Path
import tempfile
from datetime import datetime
from src.database.generate_synthetic_data import CheeseManufacturingDataGenerator

class TestQueries:
    @pytest.fixture
    def generator(self, temp_db):
        """Create generator with temp database"""
        return CheeseManufacturingDataGenerator(str(temp_db))
    
    @pytest.fixture
    def populated_db(self, generator):
        """Create populated database for query testing"""
        generator.start_date = datetime(2024, 1, 1)
        generator.end_date = datetime(2024, 1, 10)
        generator.generate_one_month_data()
        return generator.db_path
    
    def test_basic_queries(self, populated_db):
        """Test basic SQL queries on generated data"""
        conn = sqlite3.connect(populated_db)
        cursor = conn.cursor()
        
        # Test lot count
        cursor.execute("SELECT COUNT(*) FROM lot_master")
        lot_count = cursor.fetchone()[0]
        assert lot_count == 10, f"Expected 10 lots, got {lot_count}"
        
        # Test date range
        cursor.execute("SELECT MIN(lot_date), MAX(lot_date) FROM lot_master")
        min_date, max_date = cursor.fetchone()
        assert min_date == "2024-01-01"
        assert max_date == "2024-01-10"
        
        conn.close()
    
    def test_complex_queries(self, populated_db):
        """Test complex analytical queries"""
        conn = sqlite3.connect(populated_db)
        cursor = conn.cursor()
        
        # Test manufacturing process analysis
        cursor.execute("""
            SELECT process_step, COUNT(*) as step_count,
                   AVG(temperature_c) as avg_temp
            FROM manufacturing_batches
            GROUP BY process_step
            ORDER BY step_count DESC
        """)
        
        process_analysis = cursor.fetchall()
        assert len(process_analysis) > 0, "Should have manufacturing process data"
        
        # Test quality metrics
        cursor.execute("""
            SELECT AVG(ph_level) as avg_ph,
                   MIN(ph_level) as min_ph,
                   MAX(ph_level) as max_ph
            FROM quality_tests
            WHERE ph_level IS NOT NULL
        """)
        
        quality_metrics = cursor.fetchone()
        assert quality_metrics[0] is not None, "Should have average pH data"
        
        conn.close()
    
    def test_business_intelligence_queries(self, populated_db):
        """Test business intelligence style queries"""
        conn = sqlite3.connect(populated_db)
        cursor = conn.cursor()
        
        # Test daily production summary
        cursor.execute("""
            SELECT lot_date, COUNT(*) as lots_produced,
                   SUM(batch_size_kg) as total_production_kg
            FROM lot_master
            GROUP BY lot_date
            ORDER BY lot_date
        """)
        
        daily_summary = cursor.fetchall()
        assert len(daily_summary) == 10, "Should have 10 days of data"
        
        # Test supplier performance
        cursor.execute("""
            SELECT s.supplier_name, COUNT(r.raw_lot_uuid) as deliveries,
                   AVG(r.quality_score) as avg_quality
            FROM suppliers s
            LEFT JOIN raw_material_lots r ON s.supplier_id = r.supplier_id
            GROUP BY s.supplier_id
            ORDER BY deliveries DESC
        """)
        
        supplier_performance = cursor.fetchall()
        assert len(supplier_performance) > 0, "Should have supplier data"
        
        conn.close() 