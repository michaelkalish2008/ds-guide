import pytest
import sqlite3
from pathlib import Path
import tempfile
from datetime import datetime
from src.database.generators.manufacturing_generator import ManufacturingGenerator

class TestManufacturingGenerator:
    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing and load core schema"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = Path(tmp.name)
        # Load core schema
        core_schema = Path(__file__).parent.parent.parent / "sqlite" / "01_core_architecture.sqlite.sql"
        conn = sqlite3.connect(db_path)
        with open(core_schema, 'r') as f:
            conn.executescript(f.read())
        conn.close()
        # Load manufacturing process schema
        manufacturing_schema = Path(__file__).parent.parent.parent / "sqlite" / "04_manufacturing_process.sqlite.sql"
        conn = sqlite3.connect(db_path)
        with open(manufacturing_schema, 'r') as f:
            conn.executescript(f.read())
        conn.close()
        yield db_path
        db_path.unlink(missing_ok=True)
    
    @pytest.fixture
    def generator(self, temp_db):
        """Create generator instance with temp database"""
        return ManufacturingGenerator(temp_db)
    
    def test_manufacturing_batch_creation(self, generator):
        """Test manufacturing batch creation"""
        test_date = datetime(2024, 1, 15)
        lot_count = 1
        
        generator.populate_data(test_date, lot_count)
        
        cursor = generator.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM manufacturing_batches")
        count = cursor.fetchone()[0]
        
        assert count > 0
    
    def test_taleggio_process_steps(self, generator):
        """Test that Taleggio process steps are correctly implemented"""
        test_date = datetime(2024, 1, 15)
        lot_count = 1
        
        generator.populate_data(test_date, lot_count)
        
        cursor = generator.conn.cursor()
        cursor.execute("SELECT process_step FROM manufacturing_batches")
        steps = [row[0] for row in cursor.fetchall()]
        
        # Check for key Taleggio process steps
        expected_steps = ['PASTEURIZATION', 'INOCULATION', 'COAGULATION', 'CUTTING', 'FORMING']
        for step in expected_steps:
            assert step in steps, f"Expected step {step} not found in manufacturing process"
    
    def test_temperature_validation(self, generator):
        """Test temperature values are within realistic ranges"""
        test_date = datetime(2024, 1, 15)
        lot_count = 1
        
        generator.populate_data(test_date, lot_count)
        
        cursor = generator.conn.cursor()
        cursor.execute("SELECT temperature_c FROM manufacturing_batches WHERE temperature_c IS NOT NULL")
        temperatures = [row[0] for row in cursor.fetchall()]
        
        for temp in temperatures:
            assert 0 <= temp <= 100, f"Temperature {temp}°C is outside realistic range"
    
    def test_process_timing(self, generator):
        """Test that process timing follows Taleggio specifications"""
        test_date = datetime(2024, 1, 15)
        lot_count = 1
        
        generator.populate_data(test_date, lot_count)
        
        cursor = generator.conn.cursor()
        cursor.execute("""
            SELECT process_step, duration_minutes 
            FROM manufacturing_batches 
            WHERE duration_minutes IS NOT NULL
        """)
        
        process_times = cursor.fetchall()
        
        # Check that key processes have realistic durations
        for step, duration in process_times:
            if step == "PASTEURIZATION":
                assert 10 <= duration <= 20, f"Pasteurization should take 10-20 minutes, got {duration}"
            elif step == "COAGULATION":
                assert 30 <= duration <= 60, f"Coagulation should take 30-60 minutes, got {duration}" 