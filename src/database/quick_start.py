#!/usr/bin/env python3
"""
Quick Start Script for Cheese Manufacturing Database
Run this to generate a complete synthetic database for educational use.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent.parent))

from database.generate_synthetic_data import SyntheticDataGenerator

def quick_start():
    """Quick start function for database generation"""
    print("🧀 Cheese Manufacturing Database Generator")
    print("=" * 50)
    
    # Initialize generator (database will be in src/database/data/database/)
    generator = SyntheticDataGenerator("cheese_manufacturing.db")
    
    # Check if database already exists
    if generator.db_path.exists():
        response = input(f"Database {generator.db_path} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return
    
    # Setup and generate
    print("\n🚀 Starting generation...")
    generator.setup_database()
    generator.generate_all_data()
    
    print(f"\n✅ Database created successfully: {generator.db_path}")
    print("\n📊 Sample queries available in: src/database/sample_queries.sql")
    print("\n🎓 Ready for educational use!")

if __name__ == "__main__":
    quick_start() 