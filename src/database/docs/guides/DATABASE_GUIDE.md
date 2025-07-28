# Database Guide

This guide provides an overview of the cheese manufacturing database system and references to specialized guides for specific tasks.

## Overview

This database system simulates a complete cheese manufacturing facility, creating realistic synthetic data for every step of the cheese production process. It's designed to provide a synthetic data universe for learning and applying Python and Python-related code.

### What the System Creates

The database tracks the entire cheese manufacturing lifecycle:

**🏭 Production Process**:
- Raw materials and suppliers (milk, cultures, rennet)
- Manufacturing processes (curdling, cutting, cooking, pressing)
- Quality control testing (pH, moisture, fat content)
- Aging and maturation (temperature, humidity, time)

**📦 Distribution Process**:
- Packaging and labeling (weights, labels, containers)
- Shipping and logistics (destinations, delivery times)
- Inventory management (lot tracking, batch numbers)

### How the Files Work Together

**Schema Files** (`src/database/sqlite/`):
- 13 numbered SQL files (00-13) define the database structure
- Each file creates specific tables for different aspects of cheese production
- Files are numbered to ensure proper creation order (dependencies matter)

**Generators** (`src/database/generators/`):
- 11 Python generators create realistic synthetic data
- Each generator matches a specific schema file
- Generators create interconnected data (lots link to batches, batches link to tests, etc.)

**Example Flow**:
1. `01_core_architecture.sqlite.sql` creates the `lot_master` table
2. `CoreDataGenerator` creates lot records that match this table structure
3. `04_manufacturing_process.sqlite.sql` creates `manufacturing_batches` table
4. `ManufacturingGenerator` creates batch records linked to the lots
5. The data is interconnected and realistic for a cheese factory

## Database Architecture

The database is organized into logical modules, each represented by SQL schema files in `src/database/sqlite/`. These files are numbered to ensure they're executed in the correct order, as some tables depend on others.

### Schema Files (Execution Order)

**Foundation Layer**:
- **`00_master_sqlite_schema.sql`** - Master schema with all table definitions (creates the complete database structure)
- **`01_core_architecture.sqlite.sql`** - Core lot and batch tracking (creates `lot_master` table - the foundation for all other data)

**Supply Chain Layer**:
- **`02_raw_materials_suppliers.sqlite.sql`** - Raw materials and supplier management (milk, cultures, rennet suppliers)
- **`03_preprocessing_operations.sqlite.sql`** - Preprocessing operations (milk testing, pasteurization)

**Production Layer**:
- **`04_manufacturing_process.sqlite.sql`** - Manufacturing process tracking (curdling, cutting, cooking, pressing steps)
- **`05_aging_maturation.sqlite.sql`** - Aging and maturation processes (temperature, humidity, time tracking)
- **`06_quality_control_testing.sqlite.sql`** - Quality control and testing (pH, moisture, fat content tests)
- **`07_sensory_analysis.sqlite.sql`** - Sensory analysis and evaluation (taste, texture, appearance)

**Distribution Layer**:
- **`08_packaging_operations.sqlite.sql`** - Packaging operations (weights, containers, sealing)
- **`09_labeling_regulatory.sqlite.sql`** - Labeling and regulatory compliance (nutrition facts, expiration dates)
- **`10_weighing_pricing_distribution.sqlite.sql`** - Weighing, pricing, and distribution (final weights, pricing)
- **`11_shipping_logistics.sqlite.sql`** - Shipping and logistics (destinations, delivery tracking)

**Optimization Layer**:
- **`12_advanced_relationships_views.sqlite.sql`** - Advanced views and relationships (complex queries, data summaries)
- **`13_performance_optimization.sqlite.sql`** - Performance optimization (indexes, query optimization)

### Core Tables

These are the main tables that form the foundation of the cheese manufacturing database:

#### Lot Master (`lot_master`)
- **Purpose**: The central tracking table for every cheese production lot
- **What it contains**: Lot UUID, lot number, production date, cheese type, facility code, batch size
- **Why it's important**: Every other table links back to this table - it's the "parent" of all manufacturing data
- **Example data**: `TAL-2024-01-15` (Taleggio cheese lot from January 15, 2024)
- **Schema file**: `01_core_architecture.sqlite.sql`

#### Manufacturing Batches (`manufacturing_batches`)
- **Purpose**: Tracks each step of the cheese manufacturing process within a lot
- **What it contains**: Process steps (curdling, cutting, cooking, pressing), temperatures, timing, equipment used
- **Why it's important**: Shows the complete manufacturing workflow for each lot
- **Example data**: A batch record showing curdling at 35°C for 45 minutes
- **Schema file**: `04_manufacturing_process.sqlite.sql`

#### Quality Tests (`quality_tests`)
- **Purpose**: Stores all quality control measurements and test results
- **What it contains**: pH levels, moisture content, fat content, protein content, test timestamps
- **Why it's important**: Ensures cheese meets quality standards and regulatory requirements
- **Example data**: pH test result of 6.1, moisture content of 48%
- **Schema file**: `06_quality_control_testing.sqlite.sql`

#### Additional Tables
The database also includes tables for:
- **Raw materials** (milk suppliers, ingredient tracking)
- **Aging records** (temperature, humidity during maturation)
- **Packaging records** (weights, container types, labels)
- **Shipping records** (destinations, delivery dates, logistics)
- **And many more** - see the schema files for complete details

## Specialized Guides

### Data Generation
For comprehensive information on generating synthetic data using the built-in generators, see:
**[`DB_GENERATION.md`](DB_GENERATION.md)**

This guide covers:
- Generator architecture and available generators
- Basic and advanced usage patterns
- Batch processing and custom data generation
- Data validation and troubleshooting
- Performance optimization

### Database Querying
For detailed information on SQLite syntax, querying patterns, and business intelligence queries, see:
**[`DB_QUERYING.md`](DB_QUERYING.md)**

This guide covers:
- SQLite-specific features and syntax
- Common query patterns and examples
- Business intelligence and analytics queries
- Performance optimization and troubleshooting
- Creating reusable query functions

## Quick Start

### 1. Set Up Database
Install the necessary Python packages for working with the database system.

**What this does**: Installs Python packages like `pandas`, `sqlite3`, `pytest`, and other tools needed for database operations, data generation, and testing.

**For detailed setup instructions, see**: [DB_GENERATION.md](DB_GENERATION.md)

### 2. Generate Data
Create a complete cheese manufacturing database with realistic synthetic data. The system uses all 11 generators to create data for every aspect of cheese production.

**What this does**: 
- Creates a SQLite database file called `cheese_manufacturing.db`
- Uses the database schema from `src/database/sqlite/` files (13 schema files numbered 00-13)
- Generates realistic data for raw materials, manufacturing processes, quality control tests, aging, packaging, shipping, and all other aspects of cheese production

**How the schema files are used**: The generators read the table structures from the SQLite schema files and create data that matches those specifications.

**For detailed generation instructions, see**: [DB_GENERATION.md](DB_GENERATION.md)

### 3. Query Data
Connect to the database and run queries to explore the generated data.

**What this does**: 
- Connects to the database file created in step 2
- Uses SQLite's `Row` factory to access data by column names
- Allows you to explore all the tables created by the generators

**Available data**: After generation, you'll have tables for lots, manufacturing batches, quality tests, aging records, packaging, shipping, and more - all with realistic, interconnected data.

**For detailed query examples and SQL patterns, see**: [DB_QUERYING.md](DB_QUERYING.md)

### 4. Run Tests
Validate that the database system is working correctly by running automated tests.

**What this does**:
- **Unit tests**: Tests individual generators and functions in isolation
- **Integration tests**: Tests database operations and data relationships
- **End-to-end tests**: Tests complete workflows from data generation to querying
- **Performance tests**: Tests how fast the system can generate large datasets

**Why this matters**: Tests ensure the database schema is correct, data relationships are maintained, and the generators create realistic, consistent data.

**For detailed testing examples and commands, see**: [TESTING_GUIDE.md](TESTING_GUIDE.md)

## Next Steps

1. **Generate Data**: Use the generators described in [DB_GENERATION.md](DB_GENERATION.md)
2. **Query Data**: Learn SQLite syntax and patterns in [DB_QUERYING.md](DB_QUERYING.md)
3. **Test System**: Validate data integrity using [TESTING_GUIDE.md](TESTING_GUIDE.md)
4. **Explore Schema**: Review the SQL schema files in `src/database/sqlite/` 