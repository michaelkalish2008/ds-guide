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
        self._populate_sensory_panels()
        self._populate_panelist_qualifications()
        self._populate_sensory_attributes()
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

    def _populate_sensory_panels(self):
        """Populate sensory panels table"""
        cursor = self.conn.cursor()
        
        panels = [
            ("PANEL001", "Primary Quality Panel", "DAILY", "ACTIVE", "Core quality evaluation team"),
            ("PANEL002", "Expert Tasting Panel", "WEEKLY", "ACTIVE", "Expert cheese tasters"),
            ("PANEL003", "Development Panel", "MONTHLY", "ACTIVE", "Product development team"),
            ("PANEL004", "Regulatory Panel", "QUARTERLY", "ACTIVE", "Regulatory compliance team"),
            ("PANEL005", "Customer Panel", "MONTHLY", "INACTIVE", "Customer feedback panel")
        ]
        
        for panel_id, panel_name, frequency, status, description in panels:
            cursor.execute("""
                INSERT OR IGNORE INTO sensory_panels 
                (panel_id, panel_name, panel_type, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (panel_id, panel_name, frequency, "2024-01-01", "2024-01-01"))
        
        print(f"  ✅ Generated {len(panels)} sensory panels")

    def _populate_panelist_qualifications(self):
        """Populate panelist qualifications table"""
        cursor = self.conn.cursor()
        
        qualifications = [
            ("EVAL001", "PANEL001", "CERTIFIED", "2020-01-15", "2025-01-15", "Primary quality evaluator"),
            ("EVAL002", "PANEL001", "CERTIFIED", "2019-03-20", "2024-03-20", "Senior quality specialist"),
            ("EVAL003", "PANEL002", "EXPERT", "2018-06-10", "2026-06-10", "Expert cheese taster"),
            ("EVAL004", "PANEL002", "EXPERT", "2017-09-05", "2025-09-05", "Master cheese evaluator"),
            ("EVAL005", "PANEL003", "TRAINED", "2021-02-28", "2024-02-28", "Development specialist"),
            ("EVAL006", "PANEL004", "CERTIFIED", "2020-11-12", "2025-11-12", "Regulatory specialist"),
            ("EVAL007", "PANEL001", "TRAINED", "2022-04-18", "2024-04-18", "Quality technician"),
            ("EVAL008", "PANEL002", "EXPERT", "2016-12-03", "2026-12-03", "Senior expert evaluator")
        ]
        
        for panelist_id, panel_id, qualification_level, certification_date, expiry_date, notes in qualifications:
            cursor.execute("""
                INSERT OR IGNORE INTO panelist_qualifications 
                (panelist_id, panelist_name, certification_level, specialization,
                 last_calibration_date, active_status, sensory_acuity_scores)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (panelist_id, f"Panelist {panelist_id}", qualification_level, "Cheese Evaluation",
                  certification_date, 1, '{"aroma": 8.5, "taste": 9.0, "texture": 8.0}'))
        
        print(f"  ✅ Generated {len(qualifications)} panelist qualifications")

    def _populate_sensory_attributes(self):
        """Populate sensory attributes table"""
        cursor = self.conn.cursor()
        
        attributes = [
            ("AROMA_INTENSITY", "Aroma Intensity", "OLFACTORY", "1-10 scale", "Intensity of cheese aroma"),
            ("FLAVOR_INTENSITY", "Flavor Intensity", "TASTE", "1-10 scale", "Intensity of cheese flavor"),
            ("TEXTURE_FIRMNESS", "Texture Firmness", "TACTILE", "1-10 scale", "Firmness of cheese texture"),
            ("MOUTHFEEL", "Mouthfeel", "TACTILE", "1-10 scale", "Smoothness and creaminess"),
            ("SALTINESS", "Saltiness", "TASTE", "1-10 scale", "Salt perception"),
            ("ACIDITY", "Acidity", "TASTE", "1-10 scale", "Acidic taste perception"),
            ("BITTERNESS", "Bitterness", "TASTE", "1-10 scale", "Bitter taste perception"),
            ("UMAMI", "Umami", "TASTE", "1-10 scale", "Savory taste perception"),
            ("CREAMINESS", "Creaminess", "TACTILE", "1-10 scale", "Creamy texture perception"),
            ("PUNGENCY", "Pungency", "OLFACTORY", "1-10 scale", "Sharp or strong aroma")
        ]
        
        for attribute_id, attribute_name, attribute_category, measurement_scale, description in attributes:
            cursor.execute("""
                INSERT OR IGNORE INTO sensory_attributes 
                (attribute_id, evaluation_id, attribute_category, attribute_name,
                 intensity_score, quality_score, descriptor_notes, defect_flag, benchmark_comparison)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (attribute_id, str(uuid.uuid4()), attribute_category, attribute_name,
                  random.randint(5, 9), random.randint(6, 10), description, 0, "Standard"))
        
        print(f"  ✅ Generated {len(attributes)} sensory attributes")
        
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
 