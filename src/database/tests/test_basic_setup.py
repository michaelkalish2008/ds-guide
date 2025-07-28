import pytest
from pathlib import Path

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

def test_imports_work():
    """Test that we can import the database modules"""
    try:
        from scripts.generation.generators.core_generator import CoreDataGenerator
        from scripts.generation.generate_synthetic_data import CheeseManufacturingDataGenerator
        assert True, "Imports successful"
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_schema_files_exist():
    """Test that schema files exist"""
    schema_dir = Path(__file__).parent.parent / "scripts" / "schema" / "sqlite"
    assert schema_dir.exists(), f"Schema directory not found: {schema_dir}"
    
    schema_files = list(schema_dir.glob("*.sql"))
    assert len(schema_files) > 0, "No schema files found"

def test_generator_files_exist():
    """Test that generator files exist"""
    generators_dir = Path(__file__).parent.parent / "scripts" / "generation" / "generators"
    assert generators_dir.exists(), f"Generators directory not found: {generators_dir}"
    
    generator_files = list(generators_dir.glob("*_generator.py"))
    assert len(generator_files) > 0, "No generator files found" 