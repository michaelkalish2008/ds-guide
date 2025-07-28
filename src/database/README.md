# Cheese Manufacturing Database

A comprehensive SQLite database system for simulating cheese manufacturing operations with synthetic data generation. This database accurately models the complete Taleggio cheese production process with realistic data relationships and chronological progression.

## Overview

This module provides:
- **Database Schema**: Complete SQLite schema for cheese manufacturing
- **Data Generation**: Python generators for synthetic data with realistic cheesemaking progression
- **Querying Tools**: SQLite querying and analysis capabilities
- **Testing Framework**: Comprehensive test suite
- **Documentation**: Detailed guides for usage

## 🧀 Realistic Cheesemaking Progression

The generated data reflects a **realistic Taleggio cheese production timeline**:

### **Chronological Process Flow**
```
Lot Creation (Day 0) 
    ↓
Manufacturing Process (Day 0-1)
    ↓
Aging & Maturation (Days 1-30)
    ↓
Packaging & Distribution (Days 30-35)
```

### **Key Process Parameters**
- **Aging Period**: 15-30 days (realistic for Taleggio)
- **Temperature Progression**: 4°C → 10°C (standard Taleggio aging)
- **Humidity Control**: 80% throughout aging
- **Washing Frequency**: Every 10 days with salt solution
- **Packaging Timeline**: 25-35 days after lot creation

### **Data Relationships**
- **UUID Consistency**: Same `lot_uuid` flows through all tables
- **Foreign Key Integrity**: Proper relationships between manufacturing → aging → packaging
- **Time Sequence**: Realistic gaps between process stages
- **Process Accuracy**: Follows actual Taleggio production parameters

## Quick Start

### 1. Install Dependencies

```bash
# Navigate to database directory
cd src/database

# Initialize project and add dependencies
uv init
uv add -r requirements.txt

# Or from project root
cd ../..
uv init
uv add -r requirements.txt
```

### 2. Generate Data

```bash
# Generate complete dataset (31 days of production)
python3 generate_synthetic_data.py
```

**Or programmatically:**
```python
from generators.core_generator import CoreDataGenerator
import sqlite3

# Connect and generate data
conn = sqlite3.connect("cheese_manufacturing.db")
generator = CoreDataGenerator(conn)
generator.populate_data(datetime.now(), lot_count=5)
conn.close()

# Alternatively (not requiring conn.close())
with sqlite3.connect('data/cheese_manufacturing.db') as conn:
    df = pd.read_sql_query("SELECT * FROM production_data LIMIT 100", conn)
```

**Note**: Run this from the database directory:
```bash
cd src/database
```

### 3. Query Data

```python
import sqlite3

conn = sqlite3.connect("cheese_manufacturing.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM lot_master")
count = cursor.fetchone()[0]
print(f"Total lots: {count}")

conn.close()
```

**Note**: Run this from the database directory:
```bash
cd src/database
```

### 4. Run Tests

```bash
# Navigate to database directory
cd src/database

# Run all tests
python -m pytest tests/ -v --tb=short

# Run specific test categories
python -m pytest -m unit
python -m pytest -m integration
python -m pytest -m e2e
```

## Database Schema Overview

### **Core Tables (31+ tables total)**
- **`lot_master`** - Primary lot tracking (31 records)
- **`cheese_manufacturing_batches`** - Manufacturing process (496 records)
- **`aging_lots`** - Aging and maturation (5,456 records)
- **`packaging_operations`** - Packaging process (1,984 records)
- **`quality_tests`** - Quality control (155 records)
- **`shipping_logistics`** - Distribution (974 records)

### **Data Volume (Generated)**
- **Total Records**: 200,000+ across all tables
- **Time Span**: 31 days of continuous production
- **Lots Generated**: 31 unique production lots
- **Aging Lots**: 5,456 individual aging records
- **Quality Tests**: 1,240 test results
- **Environmental Monitoring**: 66,960 readings

## Project Structure

```
src/database/
├── README.md                    # This file
├── requirements.txt             # Database-specific dependencies
├── config.yaml                 # Configuration settings
├── pytest.ini                 # Test configuration
├── generate_synthetic_data.py  # Main data generation script
├── guides/                     # Documentation
│   ├── DATABASE_GUIDE.md      # Overview guide
│   ├── DB_GENERATION.md       # Data generation guide
│   ├── DB_QUERYING.md         # Querying guide
│   └── TESTING_GUIDE.md       # Testing guide
├── generators/                 # Data generators (11 total)
│   ├── core_generator.py      # Lot master & genealogy
│   ├── raw_materials_generator.py
│   ├── preprocessing_generator.py
│   ├── manufacturing_generator.py  # Manufacturing process
│   ├── aging_generator.py     # Aging & maturation
│   ├── quality_generator.py   # Quality control
│   ├── sensory_generator.py   # Sensory analysis
│   ├── packaging_generator.py # Packaging operations
│   ├── labeling_generator.py  # Labeling & regulatory
│   ├── weighing_generator.py  # Weighing & pricing
│   └── shipping_generator.py  # Shipping & logistics
├── sqlite/                    # Database schema files
│   ├── 00_master_sqlite_schema.sql
│   ├── 01_core_architecture.sqlite.sql
│   └── ... (13 total schema files)
├── tests/                     # Test suite
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── performance/
└── data/                      # Generated data and artifacts
```

## Data Quality Features

### **✅ Realistic Process Modeling**
- **Taleggio-Specific Parameters**: Temperature, humidity, aging times
- **Manufacturing Steps**: Pasteurization, coagulation, curd processing
- **Quality Control**: pH, moisture, microbiology testing
- **Environmental Monitoring**: Continuous temperature/humidity tracking

### **✅ Data Integrity**
- **Foreign Key Relationships**: Proper table relationships maintained
- **UUID Consistency**: Same identifiers flow through process stages
- **Date Progression**: Realistic time gaps between operations
- **No Empty Tables**: All 50+ tables populated with realistic data

### **✅ Comprehensive Coverage**
- **Raw Materials**: Supplier tracking, ingredient quality
- **Manufacturing**: Batch processing, equipment monitoring
- **Aging**: Cave management, environmental control
- **Quality**: Testing protocols, results tracking
- **Packaging**: Operations, labeling, traceability
- **Distribution**: Shipping, temperature monitoring, delivery

## Dependencies

### Core Dependencies
- `pandas>=2.2.0` - Data manipulation
- `numpy>=1.26.0` - Numerical computing
- `sqlalchemy>=2.0.0` - Database ORM
- `faker>=22.6.0` - Synthetic data generation

### Development Dependencies
- `pytest>=7.4.0` - Testing framework
- `black>=24.1.0` - Code formatting
- `flake8>=7.0.0` - Linting
- `mypy>=1.8.0` - Type checking

### Optional Dependencies
- `matplotlib>=3.8.0` - Plotting
- `seaborn>=0.13.0` - Statistical visualization
- `plotly>=5.18.0` - Interactive plots

## Usage from Other Modules

You can import and use the database module from other parts of the project:

```python
# From src/langgraph/
from src.database.generators.core_generator import CoreDataGenerator

# From src/file-types/
from src.database.generators.quality_generator import QualityGenerator

# From root directory
from src.database.generate_synthetic_data import generate_complete_dataset
```

## Configuration

The database module uses `config.yaml` for configuration:

```yaml
database:
  path: "cheese_manufacturing.db"
  create_if_missing: true

generators:
  lot_count: 31
  date_range_days: 31
  quality_standards:
    ph_min: 5.8
    ph_max: 6.2
    moisture_min: 45.0
    moisture_max: 55.0
```

## Testing

The module includes comprehensive tests:

- **Unit Tests**: Test individual generators and functions
- **Integration Tests**: Test database operations and data integrity
- **End-to-End Tests**: Test complete workflows
- **Performance Tests**: Test data generation performance

Run tests with:
```bash
cd src/database
pytest
```

## Use Cases

This database is ideal for:

### **🧪 Process Simulation**
- Manufacturing workflow analysis
- Quality control process modeling
- Environmental monitoring simulation

### **📊 Data Analysis**
- Production efficiency studies
- Quality trend analysis
- Supply chain optimization

### **🎓 Educational Purposes**
- Cheesemaking process demonstration
- Database design examples
- Data science project datasets

### **🔍 Traceability Studies**
- Lot-to-lot tracking
- Quality correlation analysis
- Regulatory compliance modeling

## Documentation

- **[DATABASE_GUIDE.md](guides/DATABASE_GUIDE.md)** - Overview and navigation
- **[DB_GENERATION.md](guides/DB_GENERATION.md)** - Data generation guide
- **[DB_QUERYING.md](guides/DB_QUERYING.md)** - Database querying guide
- **[TESTING_GUIDE.md](guides/TESTING_GUIDE.md)** - Testing guide

## Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Use the database-specific `requirements.txt` for dependency management

## License

This module is part of the ds-guide project and follows the same license terms. 