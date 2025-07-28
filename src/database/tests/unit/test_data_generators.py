# Move from tests/test_data_generators.py to tests/unit/test_data_generators.py
import pytest
import sqlite3
from pathlib import Path
import tempfile
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from scripts.generation.generators.core_generator import CoreDataGenerator
from scripts.generation.generators.manufacturing_generator import ManufacturingGenerator
from scripts.generation.generators.quality_generator import QualityGenerator

class TestDataGenerators:
    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = Path(tmp.name)
        yield db_path
        db_path.unlink(missing_ok=True)
    
    def test_core_generator_initialization(self, temp_db):
        """Test core generator initialization"""
        generator = CoreDataGenerator(temp_db)
        assert generator.db_path == temp_db
        assert generator.conn is not None
        generator.close()
    
    def test_manufacturing_generator_initialization(self, temp_db):
        """Test manufacturing generator initialization"""
        generator = ManufacturingGenerator(temp_db)
        assert generator.db_path == temp_db
        assert generator.conn is not None
        generator.close()
    
    def test_quality_generator_initialization(self, temp_db):
        """Test quality generator initialization"""
        generator = QualityGenerator(temp_db)
        assert generator.db_path == temp_db
        assert generator.conn is not None
        generator.close()
    
    def test_generator_data_population(self, temp_db):
        """Test that generators can populate data"""
        # Load schema first
        schema_dir = Path(__file__).parent.parent.parent / "scripts" / "schema" / "sqlite"
        schema_files = [
            "01_core_architecture.sqlite.sql",
            "02_raw_materials_suppliers.sqlite.sql",
            "03_preprocessing_operations.sqlite.sql",
            "04_manufacturing_process.sqlite.sql",
            "05_aging_maturation.sqlite.sql",
            "06_quality_control_testing.sqlite.sql",
            "07_sensory_analysis.sqlite.sql",
            "08_packaging_operations.sqlite.sql",
            "09_labeling_regulatory.sqlite.sql",
            "10_weighing_pricing_distribution.sqlite.sql",
            "11_shipping_logistics.sqlite.sql",
            "12_advanced_relationships_views.sqlite.sql"
        ]
        
        conn = sqlite3.connect(temp_db)
        for schema_file in schema_files:
            schema_path = schema_dir / schema_file
            if schema_path.exists():
                with open(schema_path, 'r') as f:
                    conn.executescript(f.read())
        conn.commit()
        conn.close()
        
        test_date = datetime(2024, 1, 15)
        lot_count = 1
        
        # Test core generator
        core_gen = CoreDataGenerator(temp_db)
        core_gen.populate_data(test_date, lot_count)
        core_gen.close()
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM lot_master")
        count = cursor.fetchone()[0]
        assert count > 0
        conn.close()
    
    def test_generator_error_handling(self, temp_db):
        """Test generator error handling"""
        # Test with invalid parameters
        generator = CoreDataGenerator(temp_db)
        
        # Should handle invalid date gracefully
        try:
            generator.populate_data("invalid_date", 1)
        except Exception:
            pass  # Expected to fail gracefully
        
        generator.close() 