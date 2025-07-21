import pytest
import sqlite3
from pathlib import Path
import tempfile
from datetime import datetime
from src.database.generators.quality_generator import QualityGenerator

class TestQualityGenerator:
    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = Path(tmp.name)
        yield db_path
        db_path.unlink(missing_ok=True)
    
    @pytest.fixture
    def generator(self, temp_db):
        """Create generator instance with temp database"""
        return QualityGenerator(temp_db)
    
    def test_quality_test_creation(self, generator):
        """Test quality test data creation"""
        test_date = datetime(2024, 1, 15)
        lot_count = 1
        
        generator.populate_data(test_date, lot_count)
        
        cursor = generator.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM quality_tests")
        count = cursor.fetchone()[0]
        
        assert count > 0
    
    def test_ph_range_validation(self, generator):
        """Test pH values are within realistic ranges"""
        test_date = datetime(2024, 1, 15)
        lot_count = 1
        
        generator.populate_data(test_date, lot_count)
        
        cursor = generator.conn.cursor()
        cursor.execute("SELECT ph_level FROM quality_tests WHERE ph_level IS NOT NULL")
        ph_values = [row[0] for row in cursor.fetchall()]
        
        for ph in ph_values:
            assert 4.0 <= ph <= 8.0, f"pH value {ph} is outside realistic range for cheese" 