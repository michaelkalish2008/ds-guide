import sqlite3
import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path

class SensoryGenerator:
    def __init__(self, db):
        import sqlite3
        from pathlib import Path
        if isinstance(db, sqlite3.Connection):
            self.conn = db
            self.db_path = None
        else:
            self.db_path = Path(db)
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._ensure_schema_exists()
        
    def _ensure_schema_exists(self):
        """Ensure basic schema exists for testing"""
        cursor = self.conn.cursor()
        
        # Check if sensory_evaluations table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='sensory_evaluations'
        """)
        
        # No table creation here; rely on schema files
        
    def populate_data(self, current_date, lot_count):
        """Generate sensory evaluation data"""
        self._populate_sensory_evaluations(current_date, lot_count)
        
    def _populate_sensory_evaluations(self, current_date, lot_count):
        """Generate sensory evaluation data"""
        cursor = self.conn.cursor()
        
        # Get lot UUID for this day
        cursor.execute("""
            SELECT lot_uuid FROM lot_master 
            WHERE lot_date = ? AND lot_number LIKE 'TAL-%'
        """, (current_date.strftime("%Y-%m-%d"),))
        
        lot_result = cursor.fetchone()
        if not lot_result:
            print(f"  ⚠️  No lots found in lot_master table for {current_date.strftime('%Y-%m-%d')}, skipping sensory data generation.")
            return
        lot_uuid = lot_result[0]
        
        # Sensory evaluation parameters for Taleggio
        sensory_attributes = [
            {
                "attribute": "AROMA_INTENSITY",
                "scale": (1, 10),
                "target_range": (6, 8),
                "description": "Intensity of cheese aroma"
            },
            {
                "attribute": "FLAVOR_INTENSITY", 
                "scale": (1, 10),
                "target_range": (6, 8),
                "description": "Intensity of cheese flavor"
            },
            {
                "attribute": "TEXTURE_FIRMNESS",
                "scale": (1, 10),
                "target_range": (4, 6),
                "description": "Firmness of cheese texture"
            },
            {
                "attribute": "MOUTHFEEL",
                "scale": (1, 10),
                "target_range": (6, 8),
                "description": "Smoothness and creaminess"
            },
            {
                "attribute": "SALTINESS",
                "scale": (1, 10),
                "target_range": (5, 7),
                "description": "Salt perception"
            },
            {
                "attribute": "ACIDITY",
                "scale": (1, 10),
                "target_range": (4, 6),
                "description": "Acidic taste perception"
            }
        ]
        
        # Generate sensory evaluation for this lot
        evaluation_id = str(uuid.uuid4())
        panel_id = f"PANEL{random.randint(1, 3):03d}"
        panelist_id = f"EVAL{random.randint(1, 5):03d}"
        evaluation_timestamp = current_date.strftime("%Y-%m-%dT%H:%M:%S")
        sample_code = f"SAMPLE{lot_count:03d}"
        sample_age_days = random.randint(7, 30)
        sample_temperature_celsius = round(random.uniform(4.0, 12.0), 1)
        overall_quality_score = random.randint(6, 10)
        defect_intensity_score = random.choice(["SLIGHT", "DEFINITE", "PRONOUNCED"])
        panel_notes = random.choice([
            "Panel detected mild aroma and creamy texture.",
            "Slight bitterness noted, otherwise typical profile.",
            "Excellent surface flora, no defects detected.",
            "Texture slightly firmer than expected.",
            "Classic Taleggio flavor, well balanced."
        ])
        evaluation_notes = self._generate_evaluation_notes()
        
        # Calculate overall score
        total_score = 0
        attribute_scores = {}
        
        for attr in sensory_attributes:
            min_val, max_val = attr["target_range"]
            score = random.uniform(min_val, max_val)
            attribute_scores[attr["attribute"]] = round(score, 1)
            total_score += score
        
        overall_score = round(total_score / len(sensory_attributes), 1)
        
        cursor.execute("""
            INSERT INTO sensory_evaluations (
                evaluation_id, lot_uuid, panel_id, panelist_id, evaluation_timestamp, sample_code, sample_age_days, sample_temperature_celsius, overall_quality_score, defect_intensity_score, panel_notes, evaluation_notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            evaluation_id, lot_uuid, panel_id, panelist_id, evaluation_timestamp, sample_code, sample_age_days, sample_temperature_celsius, overall_quality_score, defect_intensity_score, panel_notes, evaluation_notes
        ))
        
        self.conn.commit()
        
    def _generate_evaluation_notes(self):
        """Generate realistic evaluation notes for Taleggio"""
        notes_templates = [
            "Taleggio exhibits characteristic creamy texture with subtle mushroom notes. Aroma is well-developed with typical surface flora presence. Flavor profile shows good balance of salt and acidity.",
            "Classic Taleggio characteristics present. Smooth, supple texture with proper moisture content. Surface rind shows appropriate development. Overall quality meets specifications.",
            "Excellent Taleggio profile with rich, buttery notes. Texture is perfectly soft and spreadable. Aroma has pleasant earthy undertones typical of the variety.",
            "Good Taleggio development with proper ripening characteristics. Creamy mouthfeel with balanced salt perception. Surface flora contributes to authentic flavor profile.",
            "Standard Taleggio quality with typical soft texture and mild aroma. Flavor is well-balanced with appropriate salt content. Texture shows proper aging development."
        ]
        
        return random.choice(notes_templates)
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
 