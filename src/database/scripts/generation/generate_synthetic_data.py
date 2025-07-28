import sqlite3
import os
import logging
from pathlib import Path
from typing import Dict, Any
import time
from datetime import datetime, timedelta

# Use relative imports for direct script execution
from .generators.core_generator import CoreDataGenerator
from .generators.raw_materials_generator import RawMaterialsGenerator
from .generators.preprocessing_generator import PreprocessingGenerator
from .generators.manufacturing_generator import ManufacturingGenerator
from .generators.aging_generator import AgingGenerator
from .generators.quality_generator import QualityGenerator
from .generators.sensory_generator import SensoryGenerator
from .generators.packaging_generator import PackagingGenerator
from .generators.labeling_generator import LabelingGenerator
from .generators.weighing_generator import WeighingGenerator
from .generators.shipping_generator import ShippingGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CheeseManufacturingDataGenerator:
    def __init__(self, db_path="db/cheese_manufacturing.db"):
        logger.info(f"Initializing CheeseManufacturingDataGenerator with db_path: {db_path}")
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        # Delete the database file before opening the connection
        if self.db_path.exists():
            logger.info(f"Removing existing database file: {self.db_path}")
            self.db_path.unlink()
        import sqlite3
        self.conn = sqlite3.connect(self.db_path, isolation_level=None)
        # Initialize generators with shared connection
        self.generators = {
            'core': CoreDataGenerator(self.conn),
            'raw_materials': RawMaterialsGenerator(self.conn),
            'preprocessing': PreprocessingGenerator(self.conn),
            'manufacturing': ManufacturingGenerator(self.conn),
            'aging': AgingGenerator(self.conn),
            'quality': QualityGenerator(self.conn),
            'sensory': SensoryGenerator(self.conn),
            'packaging': PackagingGenerator(self.conn),
            'labeling': LabelingGenerator(self.conn),
            'weighing': WeighingGenerator(self.conn),
            'shipping': ShippingGenerator(self.conn),
        }
        self.start_date = datetime(2024, 1, 1)
        self.end_date = datetime(2024, 1, 31)

    def setup_database(self):
        logger.info("Setting up database schema...")
        # Use multiple path resolution strategies
        current_dir = Path.cwd()
        
        # Strategy 1: Try relative to script location
        script_dir = Path(__file__).parent
        schema_dir = script_dir / "schema" / "sqlite"
        
        # Strategy 2: Try from project root
        if not schema_dir.exists():
            schema_dir = current_dir.parent.parent / "src" / "database" / "scripts" / "schema" / "sqlite"
        
        # Strategy 3: Try absolute path from project root
        if not schema_dir.exists():
            project_root = Path(__file__).parent.parent.parent.parent
            schema_dir = project_root / "src" / "database" / "scripts" / "schema" / "sqlite"
        
        logger.debug(f"Looking for schema files in: {schema_dir}")
        logger.debug(f"Schema directory exists: {schema_dir.exists()}")
        if schema_dir.exists():
            logger.debug(f"Schema files found: {list(schema_dir.glob('*.sql'))}")
        
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
        
        # Phase 1: Load all tables and views
        for schema_file in schema_files:
            schema_path = schema_dir / schema_file
            if schema_path.exists():
                logger.info(f"Loading schema: {schema_file}")
                with open(schema_path, 'r') as f:
                    schema_sql = f.read()
                    try:
                        self.conn.executescript(schema_sql)
                        self.conn.commit()
                    except Exception as e:
                        logger.error(f"Error loading {schema_file}: {e}")
                        raise
            else:
                logger.warning(f"Schema file {schema_file} not found at {schema_path}")
        self.conn.commit()
        
        # Diagnostic: log all tables before loading indexes
        logger.debug("Tables in database before loading indexes:")
        cur = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for row in cur.fetchall():
            logger.debug(f"  {row[0]}")
            
        # Diagnostic: log columns of sensory_evaluations
        try:
            cur = self.conn.execute("PRAGMA table_info(sensory_evaluations);")
            logger.debug("Columns in sensory_evaluations before loading indexes:")
            for row in cur.fetchall():
                logger.debug(f"  {row[1]} ({row[2]})")
        except Exception as e:
            logger.error(f"Error inspecting sensory_evaluations: {e}")
            
        # Phase 2: Load indexes
        index_file = schema_dir / "13_performance_optimization.sqlite.sql"
        if index_file.exists():
            logger.info(f"Loading schema: 13_performance_optimization.sqlite.sql (indexes)")
            with open(index_file, 'r') as f:
                index_sql = f.read()
                index_sql = index_sql.replace("CREATE INDEX ", "CREATE INDEX IF NOT EXISTS ")
                try:
                    self.conn.executescript(index_sql)
                except Exception as e:
                    logger.error(f"Error loading 13_performance_optimization.sqlite.sql: {e}")
                    raise
        else:
            logger.warning(f"Schema file 13_performance_optimization.sqlite.sql not found at {index_file}")
        self.conn.commit()
        logger.info("Database schema loaded successfully!")

    def generate_one_month_data(self):
        logger.info("Generating 1 month of synthetic data...")
        # Removed file deletion logic from here
        self.setup_database()
        current_date = self.start_date
        lot_count = 0
        while current_date <= self.end_date:
            lot_count += 1
            logger.info(f"Generating lot {lot_count} for {current_date.strftime('%Y-%m-%d')}")
            for generator_name, generator in self.generators.items():
                try:
                    generator.populate_data(current_date, lot_count)
                    logger.debug(f"   {generator_name}")
                    # Debug: After core and manufacturing, log lot_master count
                    if generator_name == 'core' or generator_name == 'manufacturing':
                        cur = self.conn.execute("SELECT COUNT(*) FROM lot_master")
                        lot_count_db = cur.fetchone()[0]
                        logger.debug(f"      lot_master count after {generator_name}: {lot_count_db}")
                except Exception as e:
                    logger.error(f"   {generator_name}: {e}")
            current_date += timedelta(days=1)
        logger.info(f"Generated {lot_count} lots over {self.end_date - self.start_date + timedelta(days=1)} days")
        
        # Log final counts
        cur = self.conn.execute("SELECT COUNT(*) FROM lot_master")
        logger.info(f"Final lot_master count: {cur.fetchone()[0]}")
        cur = self.conn.execute("SELECT COUNT(*) FROM aging_lots")
        logger.info(f"Final aging_lots count: {cur.fetchone()[0]}")
        logger.info(f"Database saved to: {self.db_path}")
        self.conn.close()

if __name__ == "__main__":
    # Create and run the data generator
    generator = CheeseManufacturingDataGenerator()
    generator.generate_one_month_data()
    logger.info("Data generation complete!") 