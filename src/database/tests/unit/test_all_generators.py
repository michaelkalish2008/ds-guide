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
            with open(schema_path, 'r') as f:
                conn.executescript(f.read())
        conn.commit()
        conn.close()
        # First create core data
        core_gen = CoreDataGenerator(temp_db)
        test_date = datetime(2024, 1, 15)
        lot_count = 1
        core_gen.populate_data(test_date, lot_count)
        
        # Test each generator
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