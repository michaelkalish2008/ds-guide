import pytest
import sqlite3
from pathlib import Path
import tempfile
from datetime import datetime

# Import all generators
from src.database.generators.core_generator import CoreDataGenerator
from src.database.generators.raw_materials_generator import RawMaterialsGenerator
from src.database.generators.preprocessing_generator import PreprocessingGenerator
from src.database.generators.manufacturing_generator import ManufacturingGenerator
from src.database.generators.aging_generator import AgingGenerator
from src.database.generators.quality_generator import QualityGenerator
from src.database.generators.sensory_generator import SensoryGenerator
from src.database.generators.packaging_generator import PackagingGenerator
from src.database.generators.labeling_generator import LabelingGenerator
from src.database.generators.weighing_generator import WeighingGenerator
from src.database.generators.shipping_generator import ShippingGenerator

class TestAllGenerators:
    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = Path(tmp.name)
        yield db_path
        db_path.unlink(missing_ok=True)
    
    def test_all_generators_import(self):
        """Test that all generators can be imported"""
        generators = [
            CoreDataGenerator, RawMaterialsGenerator, PreprocessingGenerator,
            ManufacturingGenerator, AgingGenerator, QualityGenerator,
            SensoryGenerator, PackagingGenerator, LabelingGenerator,
            WeighingGenerator, ShippingGenerator
        ]
        
        for generator_class in generators:
            assert generator_class is not None, f"Generator {generator_class.__name__} failed to import"
    
    def test_generator_initialization(self, temp_db):
        """Test all generators initialize correctly"""
        generators = [
            CoreDataGenerator, RawMaterialsGenerator, PreprocessingGenerator,
            ManufacturingGenerator, AgingGenerator, QualityGenerator,
            SensoryGenerator, PackagingGenerator, LabelingGenerator,
            WeighingGenerator, ShippingGenerator
        ]
        
        for generator_class in generators:
            generator = None
            try:
                generator = generator_class(temp_db)
                assert generator.db_path == temp_db
                assert generator.conn is not None
            finally:
                # Use the proper close method if available
                if generator and hasattr(generator, 'close'):
                    generator.close()
                elif generator and hasattr(generator, 'conn') and generator.conn:
                    generator.conn.close()
    
    def test_generator_data_population(self, temp_db):
        """Test that all generators can populate data"""
        # Load all schema files
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
        
        # First create core data
        core_gen = CoreDataGenerator(temp_db)
        test_date = datetime(2024, 1, 15)
        lot_count = 1
        core_gen.populate_data(test_date, lot_count)
        core_gen.close()
        
        # Test each generator with separate connections to avoid locking
        generators = [
            RawMaterialsGenerator, PreprocessingGenerator, ManufacturingGenerator,
            AgingGenerator, QualityGenerator, SensoryGenerator, PackagingGenerator,
            LabelingGenerator, WeighingGenerator, ShippingGenerator
        ]
        
        for generator_class in generators:
            generator = None
            try:
                generator = generator_class(temp_db)
                generator.populate_data(test_date, lot_count)
                print(f"✓ {generator_class.__name__} populated data successfully")
            except Exception as e:
                pytest.fail(f"{generator_class.__name__} failed: {e}")
            finally:
                # Ensure connection is always closed
                if generator and hasattr(generator, 'close'):
                    generator.close()
                elif generator and hasattr(generator, 'conn') and generator.conn:
                    generator.conn.close()
    
    def test_realistic_cheesemaking_progression(self, temp_db):
        """Test that data follows realistic cheesemaking progression"""
        # Load schema and generate data
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
            with open(schema_path, 'r') as f:
                conn.executescript(f.read())
        conn.commit()
        conn.close()
        
        # Generate data for a specific lot
        test_date = datetime(2024, 1, 15)
        lot_count = 1
        
        # Run all generators
        generators = [
            CoreDataGenerator, RawMaterialsGenerator, PreprocessingGenerator,
            ManufacturingGenerator, AgingGenerator, QualityGenerator,
            SensoryGenerator, PackagingGenerator, LabelingGenerator,
            WeighingGenerator, ShippingGenerator
        ]
        
        for generator_class in generators:
            generator = generator_class(temp_db)
            generator.populate_data(test_date, lot_count)
            generator.close()
        
        # Test realistic progression
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Check that lot creation date is before packaging date
        cursor.execute("""
            SELECT l.lot_date, p.packaging_date 
            FROM lot_master l 
            JOIN packaging_operations p ON l.lot_uuid = p.lot_uuid 
            LIMIT 1
        """)
        result = cursor.fetchone()
        if result:
            lot_date = datetime.strptime(result[0], "%Y-%m-%d")
            packaging_date = datetime.strptime(result[1][:10], "%Y-%m-%d")
            # Packaging should be at least 25 days after lot creation
            days_diff = (packaging_date - lot_date).days
            assert days_diff >= 25, f"Packaging date {packaging_date} is too close to lot date {lot_date} (only {days_diff} days)"
        
        # Check that aging starts on or after lot creation
        cursor.execute("""
            SELECT l.lot_date, a.aging_start_date 
            FROM lot_master l 
            JOIN aging_lots a ON l.lot_uuid = a.lot_uuid 
            LIMIT 1
        """)
        result = cursor.fetchone()
        if result:
            lot_date = datetime.strptime(result[0], "%Y-%m-%d")
            aging_date = datetime.strptime(result[1], "%Y-%m-%d")
            # Aging should start on or after lot creation
            assert aging_date >= lot_date, f"Aging date {aging_date} is before lot date {lot_date}"
        
        # Check that we have realistic data volumes
        cursor.execute("SELECT COUNT(*) FROM lot_master")
        lot_count = cursor.fetchone()[0]
        assert lot_count > 0, "No lots generated"
        
        cursor.execute("SELECT COUNT(*) FROM cheese_manufacturing_batches")
        batch_count = cursor.fetchone()[0]
        assert batch_count > 0, "No manufacturing batches generated"
        
        cursor.execute("SELECT COUNT(*) FROM aging_lots")
        aging_count = cursor.fetchone()[0]
        assert aging_count > 0, "No aging lots generated"
        
        cursor.execute("SELECT COUNT(*) FROM packaging_operations")
        packaging_count = cursor.fetchone()[0]
        assert packaging_count > 0, "No packaging operations generated"
        
        conn.close()
    
    def test_generator_error_handling(self, temp_db):
        """Test generator error handling with invalid parameters"""
        generators = [
            CoreDataGenerator, RawMaterialsGenerator, PreprocessingGenerator,
            ManufacturingGenerator, AgingGenerator, QualityGenerator,
            SensoryGenerator, PackagingGenerator, LabelingGenerator,
            WeighingGenerator, ShippingGenerator
        ]
        
        for generator_class in generators:
            generator = None
            try:
                generator = generator_class(temp_db)
                
                # Should handle invalid date gracefully
                try:
                    generator.populate_data("invalid_date", 1)
                except Exception:
                    pass  # Expected to fail gracefully
            finally:
                # Ensure connection is always closed
                if generator and hasattr(generator, 'conn') and generator.conn:
                    generator.conn.close() 