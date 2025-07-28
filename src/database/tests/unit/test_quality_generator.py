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
        """Create generator instance with shared test database and load schema"""
        # Load schema first
        schema_dir = Path(__file__).parent.parent.parent / "sqlite"
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
        
        return QualityGenerator(temp_db)
    
    def test_quality_test_creation(self, generator):
        """Test quality test data creation"""
        test_date = datetime(2024, 1, 15)
        lot_count = 1
        # Create a lot in lot_master for the test date
        cursor = generator.conn.cursor()
        lot_uuid = "test-lot-uuid"
        cursor.execute("""
            INSERT INTO lot_master (lot_uuid, lot_number, lot_date, product_code, facility_code, batch_size_kg, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (lot_uuid, f"TAL-{test_date.strftime('%Y-%m-%d')}", test_date.strftime('%Y-%m-%d'), "TALEGGIO", "FAC001", 50.0, "ACTIVE"))
        generator.conn.commit()
        # Now run the quality generator
        generator.populate_data(test_date, lot_count)
        cursor.execute("SELECT COUNT(*) FROM quality_tests")
        count = cursor.fetchone()[0]
        assert count > 0
    
    def test_quality_test_results_validation(self, generator):
        """Test quality test results are within realistic ranges"""
        test_date = datetime(2024, 1, 15)
        lot_count = 1
        
        # Create a lot in lot_master for the test date
        cursor = generator.conn.cursor()
        lot_uuid = "test-lot-uuid"
        cursor.execute("""
            INSERT INTO lot_master (lot_uuid, lot_number, lot_date, product_code, facility_code, batch_size_kg, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (lot_uuid, f"TAL-{test_date.strftime('%Y-%m-%d')}", test_date.strftime('%Y-%m-%d'), "TALEGGIO", "FAC001", 50.0, "ACTIVE"))
        generator.conn.commit()
        
        generator.populate_data(test_date, lot_count)
        
        cursor = generator.conn.cursor()
        # Check quality test results for realistic values
        cursor.execute("SELECT actual_result FROM quality_tests WHERE actual_result IS NOT NULL")
        results = [row[0] for row in cursor.fetchall()]
        
        for result in results:
            # Convert to float if possible, otherwise skip
            try:
                result_float = float(result)
                # Check if it's a reasonable value for cheese quality tests
                assert 0 <= result_float <= 100, f"Quality test result {result_float} is outside realistic range"
            except (ValueError, TypeError):
                # Non-numeric results are acceptable (e.g., "PASS", "FAIL")
                pass 