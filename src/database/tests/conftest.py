import pytest
import tempfile
from pathlib import Path
import sys
import os
import sqlite3
from datetime import datetime, timedelta
import getpass

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture(scope="session")
def test_data_dir():
    """Create temporary test data directory"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)

@pytest.fixture(scope="session")
def sample_database():
    """Create sample database for testing"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = Path(tmp.name)
    yield db_path
    db_path.unlink(missing_ok=True)

@pytest.fixture(scope="function")
def temp_db():
    """Create database in a known writable location for each test"""
    db_path = Path("src/database/data/test_database.db")
    if db_path.exists():
        print(f"[DEBUG] Pre-test: {db_path} exists. Permissions: {oct(db_path.stat().st_mode)}, Owner: {getpass.getuser()}")
        db_path.unlink()
    else:
        print(f"[DEBUG] Pre-test: {db_path} does not exist.")
    print(f"[DEBUG] Using test database at: {db_path}")
    yield str(db_path)
    # Do not delete the file after the test to avoid deleting an open database file.

@pytest.fixture(scope="function")
def populated_test_db(temp_db):
    """Create database with minimal test data"""
    conn = sqlite3.connect(temp_db)
    
    # Create basic schema for testing
    conn.executescript("""
        CREATE TABLE lot_master (
            lot_uuid TEXT PRIMARY KEY,
            lot_number TEXT UNIQUE NOT NULL,
            lot_date TEXT NOT NULL,
            product_code TEXT NOT NULL,
            facility_code TEXT NOT NULL,
            batch_size_kg REAL,
            status TEXT DEFAULT 'ACTIVE'
        );
        
        CREATE TABLE suppliers (
            supplier_id TEXT PRIMARY KEY,
            supplier_name TEXT NOT NULL,
            supplier_type TEXT,
            active_flag INTEGER DEFAULT 1
        );
        
        CREATE TABLE manufacturing_batches (
            batch_uuid TEXT PRIMARY KEY,
            lot_uuid TEXT REFERENCES lot_master(lot_uuid),
            batch_date TEXT NOT NULL,
            process_step TEXT NOT NULL,
            temperature_c REAL,
            duration_minutes INTEGER
        );
    """)
    
    # Insert test data
    test_date = datetime(2024, 1, 15)
    
    # Insert test lot
    conn.execute("""
        INSERT INTO lot_master (lot_uuid, lot_number, lot_date, product_code, facility_code, batch_size_kg)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("test-uuid-1", "TAL-2024-001", test_date.strftime("%Y-%m-%d"), "TALEGGIO", "FAC001", 50.0))
    
    # Insert test supplier
    conn.execute("""
        INSERT INTO suppliers (supplier_id, supplier_name, supplier_type)
        VALUES (?, ?, ?)
    """, ("SUP001", "Test Dairy Farm", "DAIRY_FARM"))
    
    # Insert test manufacturing batch
    conn.execute("""
        INSERT INTO manufacturing_batches (batch_uuid, lot_uuid, batch_date, process_step, temperature_c, duration_minutes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("batch-uuid-1", "test-uuid-1", test_date.strftime("%Y-%m-%d"), "PASTEURIZATION", 72.0, 15))
    
    conn.commit()
    conn.close()
    
    yield temp_db

@pytest.fixture(scope="session")
def test_date_range():
    """Provide test date range for data generation"""
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 31)
    return start_date, end_date

@pytest.fixture(scope="function")
def single_test_date():
    """Provide single test date"""
    return datetime(2024, 1, 15)

@pytest.fixture(scope="function")
def test_lot_data():
    """Provide sample lot data for testing"""
    return {
        "lot_uuid": "test-uuid-123",
        "lot_number": "TAL-2024-001",
        "lot_date": "2024-01-15",
        "product_code": "TALEGGIO",
        "facility_code": "FAC001",
        "batch_size_kg": 50.0,
        "status": "ACTIVE"
    }

@pytest.fixture(scope="function")
def test_supplier_data():
    """Provide sample supplier data for testing"""
    return {
        "supplier_id": "SUP001",
        "supplier_name": "Test Dairy Farm",
        "supplier_type": "DAIRY_FARM",
        "contact_info": '{"phone": "+1-555-0123", "email": "test@dairy.com"}',
        "certification_status": "CERTIFIED",
        "active_flag": 1
    }

@pytest.fixture(scope="function")
def test_manufacturing_data():
    """Provide sample manufacturing data for testing"""
    return {
        "batch_uuid": "batch-uuid-123",
        "lot_uuid": "test-uuid-123",
        "batch_date": "2024-01-15",
        "process_step": "PASTEURIZATION",
        "temperature_c": 72.0,
        "duration_minutes": 15,
        "ph_level": 6.8
    }

@pytest.fixture(scope="function")
def mock_anthropic_response():
    """Mock Claude response for testing"""
    return {
        "evaluation_notes": "Sample sensory evaluation notes for testing purposes. The cheese exhibits typical Taleggio characteristics with proper aroma development and texture.",
        "flavor_profile": "Creamy, tangy, with subtle mushroom notes",
        "texture_assessment": "Smooth and supple with proper moisture content"
    }

@pytest.fixture(scope="session")
def schema_files():
    """Get list of schema files for testing"""
    schema_dir = project_root / "schemas" / "database" / "sqlite"
    if schema_dir.exists():
        return sorted([f for f in schema_dir.glob("*.sql")])
    return []

@pytest.fixture(scope="function")
def clean_database(temp_db):
    """Ensure database is clean and ready for testing"""
    conn = sqlite3.connect(temp_db)
    
    # Drop all tables if they exist
    conn.executescript("""
        DROP TABLE IF EXISTS shipping_logistics;
        DROP TABLE IF EXISTS weighing_pricing;
        DROP TABLE IF EXISTS labeling_regulatory;
        DROP TABLE IF EXISTS packaging_operations;
        DROP TABLE IF EXISTS sensory_evaluations;
        DROP TABLE IF EXISTS quality_tests;
        DROP TABLE IF EXISTS manufacturing_batches;
        DROP TABLE IF EXISTS preprocessing_batches;
        DROP TABLE IF EXISTS raw_material_lots;
        DROP TABLE IF EXISTS supplier_certifications;
        DROP TABLE IF EXISTS suppliers;
        DROP TABLE IF EXISTS lot_master;
    """)
    
    conn.commit()
    conn.close()
    
    yield temp_db

@pytest.fixture(scope="function")
def database_connection(temp_db):
    """Provide database connection for testing"""
    conn = sqlite3.connect(temp_db)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()

@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration"""
    return {
        "database_path": "test_cheese_manufacturing.db",
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
        "lots_per_day": 1,
        "batch_size_range": (40.0, 60.0),
        "temperature_range": (2.0, 40.0),
        "ph_range": (5.0, 7.0)
    }

# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end test"
    )
    config.addinivalue_line(
        "markers", "database: mark test as database test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add default markers"""
    for item in items:
        if "unit" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        elif "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "e2e" in item.nodeid:
            item.add_marker(pytest.mark.e2e)
        elif "database" in item.nodeid:
            item.add_marker(pytest.mark.database) 