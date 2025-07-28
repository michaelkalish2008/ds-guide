# Database Data Generation Guide

This guide covers how to generate synthetic data for the cheese manufacturing database using the built-in generators.

## Quick Start

**The primary way to create the database is by running the main script:**

```bash
cd src/database
python generate_synthetic_data.py
```

This single command creates a complete cheese manufacturing database with realistic data.

## Overview

The data generation system creates realistic synthetic data for a cheese manufacturing facility, including:
- Raw materials and suppliers
- Manufacturing processes
- Quality control testing
- Aging and maturation
- Packaging and labeling
- Shipping and logistics

## Generator Architecture

All generators are located in `src/database/generators/` and follow a consistent pattern:

### Available Generators

- **`CoreDataGenerator`** (`core_generator.py`) - Core lot and batch generation
- **`RawMaterialsGenerator`** (`raw_materials_generator.py`) - Raw materials and suppliers
- **`PreprocessingGenerator`** (`preprocessing_generator.py`) - Preprocessing operations
- **`ManufacturingGenerator`** (`manufacturing_generator.py`) - Manufacturing process data
- **`AgingGenerator`** (`aging_generator.py`) - Aging and maturation records
- **`QualityGenerator`** (`quality_generator.py`) - Quality control test data
- **`SensoryGenerator`** (`sensory_generator.py`) - Sensory analysis
- **`PackagingGenerator`** (`packaging_generator.py`) - Packaging and labeling data
- **`LabelingGenerator`** (`labeling_generator.py`) - Labeling and regulatory
- **`WeighingGenerator`** (`weighing_generator.py`) - Weighing and pricing
- **`ShippingGenerator`** (`shipping_generator.py`) - Shipping and logistics data

## Basic Usage

### 1. Initialize Database Connection

```python
import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect("cheese_manufacturing.db")
```

**Note**: Make sure you're in the database directory when running these examples:
```bash
cd src/database
```

### 2. Import and Initialize Generators

The generators are located in `src/database/generators/` and can be imported individually or used through the main data generator script.

**Available Generators**:
- `CoreDataGenerator` - Creates lot master records (foundation for all data)
- `ManufacturingGenerator` - Creates manufacturing batch records
- `QualityGenerator` - Creates quality test records
- `AgingGenerator` - Creates aging and maturation records
- `PackagingGenerator` - Creates packaging operation records
- `ShippingGenerator` - Creates shipping and logistics records
- `RawMaterialsGenerator` - Creates raw material and supplier records
- `PreprocessingGenerator` - Creates preprocessing operation records
- `SensoryGenerator` - Creates sensory evaluation records
- `LabelingGenerator` - Creates labeling and regulatory records
- `WeighingGenerator` - Creates weighing and pricing records

**Main Script**: `src/database/generate_synthetic_data.py` - Orchestrates all generators

### 3. Generate Data

**Primary Method: Run the Main Script**
```bash
cd src/database
python generate_synthetic_data.py
```

This script:
- Creates the database file (`cheese_manufacturing.db`)
- Loads all schema files from `src/database/sqlite/`
- Runs all 11 generators in the correct dependency order
- Generates one month of realistic cheese manufacturing data
- Saves the complete database to `src/database/data/`

**Alternative: Use Individual Generators**
Each generator can be used independently by importing from `src/database/generators/` and calling their `populate_data()` method.

**Execution Order**: Generators must be run in dependency order:
1. Core data (lots)
2. Raw materials and preprocessing
3. Manufacturing batches
4. Quality tests and aging
5. Packaging and shipping

## Advanced Usage

### Custom Data Generation

**Main Orchestrator**: `src/database/generate_synthetic_data.py`
- Contains `CheeseManufacturingDataGenerator` class
- Orchestrates all 11 generators in correct dependency order
- Handles database setup and schema loading
- Provides methods for different generation scenarios

**Individual Generator Files**:
- `src/database/generators/core_generator.py` - Core lot generation
- `src/database/generators/manufacturing_generator.py` - Manufacturing processes
- `src/database/generators/quality_generator.py` - Quality control tests
- `src/database/generators/aging_generator.py` - Aging and maturation
- `src/database/generators/packaging_generator.py` - Packaging operations
- `src/database/generators/shipping_generator.py` - Shipping and logistics
- `src/database/generators/raw_materials_generator.py` - Raw materials
- `src/database/generators/preprocessing_generator.py` - Preprocessing
- `src/database/generators/sensory_generator.py` - Sensory analysis
- `src/database/generators/labeling_generator.py` - Labeling and compliance
- `src/database/generators/weighing_generator.py` - Weighing and pricing

### Batch Processing

**Script**: `src/database/generate_synthetic_data.py`
- Supports date range generation via `generate_one_month_data()`
- Configurable start and end dates
- Automatic lot counting and progression
- Progress reporting and logging

**Usage Patterns**:
1. **Single Day**: Generate data for one specific date
2. **Date Range**: Generate data for multiple days/weeks/months
3. **Custom Lots**: Generate specific number of lots per day
4. **Incremental**: Add data to existing database

## Generator-Specific Features

### Core Data Generator (`core_generator.py`)
- Creates lot master records (foundation for all data)
- Establishes basic batch tracking and lot numbering
- Sets up facility and product codes
- Generates lot UUIDs and tracking information

### Manufacturing Generator (`manufacturing_generator.py`)
- Generates production batches for each lot
- Creates process parameters (temperature, timing, equipment)
- Tracks manufacturing steps (curdling, cutting, cooking, pressing)
- Links batches to lots and maintains process flow

### Quality Generator (`quality_generator.py`)
- Creates quality test schedules and records
- Generates test results (pH, moisture, fat content)
- Tracks quality metrics and compliance
- Links tests to manufacturing batches

### Aging Generator (`aging_generator.py`)
- Manages maturation schedules and aging caves
- Tracks environmental conditions (temperature, humidity)
- Records aging progress and time tracking
- Creates aging activities and wheel positions

### Packaging Generator (`packaging_generator.py`)
- Creates packaging records and operations
- Tracks packaging materials and containers
- Manages inventory and packaging lines
- Links packages to lots and batches

### Shipping Generator (`shipping_generator.py`)
- Generates shipping records and logistics
- Tracks delivery schedules and carriers
- Manages shipment contents and tracking
- Links shipments to packaged products

### Raw Materials Generator (`raw_materials_generator.py`)
- Creates supplier records and certifications
- Generates raw material lots and quality tests
- Tracks ingredient quality and specifications
- Links materials to manufacturing processes

### Preprocessing Generator (`preprocessing_generator.py`)
- Creates preprocessing operations (pasteurization, standardization)
- Tracks milk quality and processing parameters
- Generates preprocessing batches and records
- Links preprocessing to manufacturing

### Sensory Generator (`sensory_generator.py`)
- Creates sensory evaluation panels and tests
- Generates sensory analysis records
- Tracks taste, texture, and appearance evaluations
- Links sensory data to quality control

### Labeling Generator (`labeling_generator.py`)
- Creates labeling and regulatory compliance records
- Generates product labels and traceability codes
- Tracks regulatory requirements and certifications
- Links labels to packaged products

### Weighing Generator (`weighing_generator.py`)
- Creates weighing and pricing records
- Tracks catch weight transactions and pricing rules
- Generates inventory transactions and pricing
- Links weighing to packaging and shipping

## Data Validation

**Data validation should be performed through the testing framework, not manually.**

**For comprehensive data validation, see**: [TESTING_GUIDE.md](TESTING_GUIDE.md)

The testing framework includes:
- **Unit tests**: Validate individual generator output
- **Integration tests**: Verify data relationships and consistency
- **End-to-end tests**: Ensure complete workflow integrity
- **Performance tests**: Validate generation speed and efficiency

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Check that database file exists and is writable
   - Verify database path in `src/database/generate_synthetic_data.py`
   - Ensure proper permissions on database directory

2. **Generator Initialization Issues**:
   - Check that all generator files exist in `src/database/generators/`
   - Verify database schema is loaded before running generators
   - Check for import errors in generator files

3. **Schema Issues**:
   - Verify schema files exist in `src/database/sqlite/`
   - Check that schema files are loaded in correct order
   - Ensure all required tables are created

### Performance Optimization

1. **Batch Processing**:
   - Use the main script `src/database/generate_synthetic_data.py` for large datasets
   - The script handles transactions and memory management automatically
   - Configure date ranges and lot counts for optimal performance

2. **Memory Management**:
   - The main script properly closes database connections
   - Use incremental generation for very large datasets
   - Monitor database file size during generation

### Debugging

**For detailed debugging and validation, see**: [TESTING_GUIDE.md](TESTING_GUIDE.md)

The testing framework provides comprehensive validation and debugging tools.

## Next Steps

- Review the database schema in `src/database/sqlite/` files
- Learn about querying the generated data in [DB_QUERYING.md](DB_QUERYING.md)
- Explore advanced data generation patterns in the generator source files
- Validate data generation using [TESTING_GUIDE.md](TESTING_GUIDE.md) 