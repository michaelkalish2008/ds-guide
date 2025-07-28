# Database Testing Guide

This guide explains how to run tests for the database module and understand the testing structure.

## Table of Contents
- [Quick Start](#quick-start)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Types](#test-types)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites
```bash
# Activate virtual environment
source .venv/bin/activate

# Option 1: Use database-specific requirements.txt (recommended)
cd src/database
uv init
uv add -r requirements.txt

# Option 2: Use root project dependencies
cd ../..
uv init
uv add -r requirements.txt
```

### Run All Tests
```bash
cd src/database
python -m pytest
```

### Run Specific Test Types
```bash
# Navigate to database directory first
cd src/database

# Unit tests only
python -m pytest tests/unit/

# Integration tests only
python -m pytest tests/integration/

# End-to-end tests only
python -m pytest tests/e2e/

# Performance tests only
python -m pytest tests/performance/
```

### Run by Test Markers
```bash
# Run specific test categories
python -m pytest -m unit
python -m pytest -m integration
python -m pytest -m e2e
python -m pytest -m performance
python -m pytest -m slow
python -m pytest -m database

# Run with verbose output
python -m pytest -v

# Run with short tracebacks
python -m pytest --tb=short

# Run with both
python -m pytest tests/ -v --tb=short

# Run specific test file
python -m pytest tests/unit/test_core_generator.py

# Run specific test function
python -m pytest tests/unit/test_core_generator.py::test_lot_number_uniqueness

# Run tests and show coverage
python -m pytest --cov=src
```

## Test Structure

```
tests/
├── unit/                    # Fast, isolated tests
│   ├── test_core_generator.py
│   ├── test_manufacturing_generator.py
│   ├── test_quality_generator.py
│   └── test_all_generators.py
├── integration/             # Database interaction tests
│   ├── test_database_schema.py
│   ├── test_database_integration.py
│   ├── test_data_consistency.py
│   └── test_data_integrity.py
├── e2e/                    # Full workflow tests
│   ├── test_full_workflow.py
│   ├── test_business_logic.py
│   └── test_queries.py
├── performance/             # Performance and load tests
│   ├── test_performance.py
│   └── test_generation_performance.py
├── utils/                   # Test utilities and helpers
│   ├── test_helpers.py
│   └── schema_debug.py
├── conftest.py             # Shared fixtures and configuration
├── test_basic_setup.py     # Basic setup verification
└── run_tests.py            # Test runner script
```

## Running Tests

### Basic Commands

```bash
# Navigate to database directory first
cd src/database

# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run with coverage
python -m pytest --cov=src/database

# Run specific test file
python -m pytest tests/unit/test_core_generator.py

# Run specific test function
python -m pytest tests/unit/test_core_generator.py::TestCoreGenerator::test_generator_initialization
```

### Using Markers

```bash
# Navigate to database directory first
cd src/database

# Run only unit tests
python -m pytest -m unit

# Run only integration tests
python -m pytest -m integration

# Run only end-to-end tests
python -m pytest -m e2e

# Run only performance tests
python -m pytest -m performance

# Skip slow tests
python -m pytest -m "not slow"

# Run database-specific tests
python -m pytest -m database
```

### Advanced Options

```bash
# Navigate to database directory first
cd src/database

# Run tests in parallel (if pytest-xdist installed)
python -m pytest -n auto

# Stop on first failure
python -m pytest -x

# Show local variables on failures
python -m pytest -l

# Generate HTML coverage report
python -m pytest --cov=src/database --cov-report=html

# Run tests with specific database
python -m pytest --db=sqlite
```

## Test Types

### Unit Tests (`tests/unit/`)
- **Purpose**: Test individual functions and classes in isolation
- **Speed**: Fast (< 1 second each)
- **Scope**: Single function or class
- **Database**: Mocked or in-memory

**Example**:
```python
def test_lot_number_uniqueness(self):
    """Test that lot numbers are unique"""
    generator = CoreDataGenerator(self.conn)
    lots = generator.generate_lots(datetime(2024, 1, 1), 5)
    
    lot_numbers = [lot['lot_number'] for lot in lots]
    assert len(lot_numbers) == len(set(lot_numbers)), "Lot numbers must be unique"
```

### Integration Tests (`tests/integration/`)
- **Purpose**: Test how components work together
- **Speed**: Medium (1-10 seconds each)
- **Scope**: Multiple functions or classes
- **Database**: Real database with test data

**Example**:
```python
def test_data_relationships(self, generator):
    """Test that data relationships are maintained"""
    generator.generate_one_month_data()
    
    conn = sqlite3.connect(generator.db_path)
    cursor = conn.cursor()
    
    # Check lot_master references
    cursor.execute("""
        SELECT COUNT(*) FROM lot_master l
        LEFT JOIN manufacturing_batches m ON l.lot_uuid = m.lot_uuid
        WHERE m.lot_uuid IS NOT NULL
    """)
    related_count = cursor.fetchone()[0]
    assert related_count > 0, "Lots should have manufacturing batches"
```

### End-to-End Tests (`tests/e2e/`)
- **Purpose**: Test complete business workflows
- **Speed**: Slow (10-60 seconds each)
- **Scope**: Complete application workflow
- **Database**: Full database with realistic data

**Example**:
```python
def test_complete_manufacturing_workflow(self, generator):
    """Test complete cheese manufacturing workflow"""
    generator.generate_one_month_data()
    
    conn = sqlite3.connect(generator.db_path)
    cursor = conn.cursor()
    
    # Test complete workflow: lot → manufacturing → quality → packaging → shipping
    cursor.execute("""
        SELECT COUNT(*) FROM lot_master l
        JOIN manufacturing_batches m ON l.lot_uuid = m.lot_uuid
        JOIN quality_tests q ON l.lot_uuid = q.lot_uuid
        JOIN packaging_operations p ON l.lot_uuid = p.lot_uuid
        JOIN shipping_logistics s ON l.lot_uuid = s.lot_uuid
    """)
    complete_workflows = cursor.fetchone()[0]
    assert complete_workflows > 0, "Complete workflows should exist"
```

### Performance Tests (`tests/performance/`)
- **Purpose**: Test system performance and speed
- **Speed**: Variable (depends on test)
- **Scope**: System-level performance
- **Database**: Large datasets

**Example**:
```python
def test_data_generation_speed(self, generator):
    """Test that data generation completes within time limits"""
    import time
    
    start_time = time.time()
    generator.generate_one_month_data()
    end_time = time.time()
    
    generation_time = end_time - start_time
    assert generation_time < 60, f"Generation took {generation_time}s, should be under 60s"
```

### Integration Tests (`tests/integration/`)
- **Purpose**: Test database interactions and data consistency
- **Speed**: Medium (1-10 seconds each)
- **Scope**: Multiple components working together
- **Database**: Real database with test data

**Example**:
```python
def test_data_consistency_across_tables():
    # Test that foreign keys are valid
    # Test that data relationships are maintained
    # Test that constraints are enforced
```

### End-to-End Tests (`tests/e2e/`)
- **Purpose**: Test complete workflows and business logic
- **Speed**: Slow (10-60 seconds each)
- **Scope**: Full application workflow
- **Database**: Complete database with realistic data

**Example**:
```python
def test_full_manufacturing_workflow():
    # Test complete cheese manufacturing process
    # Test data generation, processing, and validation
    # Test business rules and constraints
```

### Performance Tests (`tests/performance/`)
- **Purpose**: Test system performance and scalability
- **Speed**: Very slow (1-10 minutes each)
- **Scope**: Load testing and optimization
- **Database**: Large datasets and stress testing

**Example**:
```python
def test_month_generation_performance():
    # Test generating one month of data
    # Measure time and memory usage
    # Verify performance meets requirements
```

## Configuration

### pytest.ini Settings

```ini
[tool:pytest]
# Test discovery
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Output options
addopts = 
    -v                    # Verbose output
    --tb=short           # Short traceback format
    --strict-markers     # Require marker registration
    --disable-warnings   # Suppress warnings
    --color=yes          # Colored output
    --durations=10       # Show 10 slowest tests
    --maxfail=5          # Stop after 5 failures

# Test markers
markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (database interactions)
    e2e: End-to-end tests (full workflow)
    performance: Performance tests (slow)
    slow: Slow running tests
    database: Database-related tests
```

### Environment Variables

```bash
# Set database type for tests
export TEST_DB_TYPE=sqlite

# Set test data size
export TEST_DATA_SIZE=small

# Enable debug output
export TEST_DEBUG=true
```

## Best Practices

### Writing Tests

1. **Use descriptive names**:
   ```python
   # Good
   def test_lot_number_uniqueness():
   
   # Bad
   def test_lot():
   ```

2. **Follow AAA pattern** (Arrange, Act, Assert):
   ```python
   def test_manufacturing_batch_creation():
       # Arrange
       generator = ManufacturingGenerator()
       
       # Act
       batch = generator.create_batch()
       
       # Assert
       assert batch is not None
       assert batch.temperature > 0
   ```

3. **Use fixtures for common setup**:
   ```python
   @pytest.fixture
   def sample_database():
       # Setup test database
       db = create_test_database()
       yield db
       # Cleanup
       db.close()
   ```

### Test Organization

1. **Group related tests in classes**:
   ```python
   class TestCoreGenerator:
       def test_initialization(self):
           pass
       
       def test_lot_creation(self):
           pass
   ```

2. **Use appropriate markers**:
   ```python
   @pytest.mark.unit
   def test_fast_function():
       pass
   
   @pytest.mark.integration
   def test_database_interaction():
       pass
   ```

3. **Keep tests independent**:
   - Each test should be able to run in isolation
   - Don't rely on test execution order
   - Clean up after each test

## Troubleshooting

### Common Issues

1. **Import errors**:
   ```bash
   # Make sure you're in the right directory
   cd src/database
   
   # Check Python path
   python -c "import sys; print(sys.path)"
   ```

2. **Database connection issues**:
   ```bash
   # Check if database file exists
   ls -la *.db *.sqlite
   
   # Reset test database
   python -m pytest --setup-db
   ```

3. **Slow tests**:
   ```bash
   # Run only fast tests
   python -m pytest -m "not slow"
   
   # Profile slow tests
   python -m pytest --durations=10
   ```

### Debug Commands

```bash
# Run with maximum verbosity
python -m pytest -vvv

# Show local variables on failure
python -m pytest -l

# Run single test with debugger
python -m pytest tests/unit/test_core_generator.py::test_initialization --pdb

# Generate test report
python -m pytest --junitxml=test-results.xml
```

### Performance Optimization

```bash
# Run tests in parallel
python -m pytest -n auto

# Use pytest-xdist for parallel execution
uv pip install pytest-xdist

# Profile memory usage
python -m pytest --memray
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Database Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          uv pip install -r requirements.txt
      - name: Run tests
        run: |
          cd src/database
          python -m pytest --cov=src/database --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Database Testing Best Practices](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [Performance Testing Guide](https://docs.pytest.org/en/stable/how-to/parametrize.html) 