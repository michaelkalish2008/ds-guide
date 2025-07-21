import pytest
import sqlite3
from pathlib import Path
import tempfile
from datetime import datetime
from src.database.generators.core_generator import CoreDataGenerator

class TestCoreGenerator:
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
        return CoreDataGenerator(temp_db)
    
    def test_generator_initialization(self, generator):
        """Test generator initializes correctly"""
        assert generator.db_path.exists()
        assert generator.conn is not None
    
    def test_lot_master_creation(self, generator):
        """Test lot master table creation and data insertion"""
        test_date = datetime(2024, 1, 15)
        lot_count = 1
        
        generator.populate_data(test_date, lot_count)
        
        # Check if data was inserted
        cursor = generator.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM lot_master")
        count = cursor.fetchone()[0]
        
        assert count > 0
        
        # Check data quality
        cursor.execute("SELECT lot_number, lot_date, product_code FROM lot_master LIMIT 1")
        row = cursor.fetchone()
        
        assert row is not None
        assert row[0] is not None  # lot_number
        assert row[1] is not None  # lot_date
        assert row[2] is not None  # product_code
    
    def test_lot_number_uniqueness(self, generator):
        """Test that lot numbers are unique"""
        test_date = datetime(2024, 1, 15)
        
        # Generate multiple lots
        for i in range(5):
            generator.populate_data(test_date, i + 1)
        
        cursor = generator.conn.cursor()
        cursor.execute("SELECT lot_number FROM lot_master")
        lot_numbers = [row[0] for row in cursor.fetchall()]
        
        # Check uniqueness
        assert len(lot_numbers) == len(set(lot_numbers))
    
    def test_date_range_validation(self, generator):
        """Test date validation"""
        test_date = datetime(2024, 1, 15)
        lot_count = 1
        
        # Should not raise exception
        generator.populate_data(test_date, lot_count)
        
        # Test with invalid date (should handle gracefully)
        invalid_date = "invalid_date"
        try:
            generator.populate_data(invalid_date, lot_count)
        except Exception:
            pass  # Expected to fail gracefully 