import sqlite3
import json
from typing import Dict, List, Optional
from datetime import datetime
import uuid

class DatabaseManager:
    def __init__(self, db_path: str = "data/smartmatch.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                grade INTEGER,
                interests TEXT,
                strengths TEXT,
                values TEXT,
                availability TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Activities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                skills_developed TEXT,
                time_commitment TEXT,
                difficulty_level INTEGER,
                social_impact_score REAL,
                personal_growth_score REAL,
                fulfillment_score REAL,
                prerequisites TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id TEXT PRIMARY KEY,
                student_id TEXT,
                activity_id TEXT,
                score REAL,
                reasoning TEXT,
                recommended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (activity_id) REFERENCES activities (id)
            )
        ''')
        
        # Feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id TEXT PRIMARY KEY,
                student_id TEXT,
                activity_id TEXT,
                rating INTEGER,
                feedback_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (activity_id) REFERENCES activities (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_student(self, student_data: Dict) -> str:
        """Create a new student profile."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        student_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO students (id, name, grade, interests, strengths, values, availability)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            student_id,
            student_data['name'],
            student_data['grade'],
            json.dumps(student_data.get('interests', [])),
            json.dumps(student_data.get('strengths', [])),
            json.dumps(student_data.get('values', [])),
            json.dumps(student_data.get('availability', {}))
        ))
        
        conn.commit()
        conn.close()
        return student_id
    
    def get_student(self, student_id: str) -> Optional[Dict]:
        """Get student profile by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        row = cursor.fetchone()
        
        if row:
            student = {
                'id': row[0],
                'name': row[1],
                'grade': row[2],
                'interests': json.loads(row[3]) if row[3] else [],
                'strengths': json.loads(row[4]) if row[4] else [],
                'values': json.loads(row[5]) if row[5] else [],
                'availability': json.loads(row[6]) if row[6] else {},
                'created_at': row[7],
                'updated_at': row[8]
            }
            conn.close()
            return student
        
        conn.close()
        return None
    
    def create_activity(self, activity_data: Dict) -> str:
        """Create a new activity."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        activity_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO activities (id, name, category, description, skills_developed, 
                                  time_commitment, difficulty_level, social_impact_score,
                                  personal_growth_score, fulfillment_score, prerequisites)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            activity_id,
            activity_data['name'],
            activity_data['category'],
            activity_data['description'],
            json.dumps(activity_data.get('skills_developed', [])),
            activity_data.get('time_commitment', ''),
            activity_data.get('difficulty_level', 1),
            activity_data.get('social_impact_score', 0.0),
            activity_data.get('personal_growth_score', 0.0),
            activity_data.get('fulfillment_score', 0.0),
            json.dumps(activity_data.get('prerequisites', []))
        ))
        
        conn.commit()
        conn.close()
        return activity_id
    
    def get_all_activities(self) -> List[Dict]:
        """Get all activities."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM activities')
        rows = cursor.fetchall()
        
        activities = []
        for row in rows:
            activity = {
                'id': row[0],
                'name': row[1],
                'category': row[2],
                'description': row[3],
                'skills_developed': json.loads(row[4]) if row[4] else [],
                'time_commitment': row[5],
                'difficulty_level': row[6],
                'social_impact_score': row[7],
                'personal_growth_score': row[8],
                'fulfillment_score': row[9],
                'prerequisites': json.loads(row[10]) if row[10] else [],
                'created_at': row[11]
            }
            activities.append(activity)
        
        conn.close()
        return activities
    
    def save_recommendation(self, student_id: str, activity_id: str, score: float, reasoning: str) -> str:
        """Save a recommendation."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        rec_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO recommendations (id, student_id, activity_id, score, reasoning)
            VALUES (?, ?, ?, ?, ?)
        ''', (rec_id, student_id, activity_id, score, reasoning))
        
        conn.commit()
        conn.close()
        return rec_id
    
    def get_student_recommendations(self, student_id: str) -> List[Dict]:
        """Get recommendations for a student."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT r.*, a.name, a.category, a.description
            FROM recommendations r
            JOIN activities a ON r.activity_id = a.id
            WHERE r.student_id = ?
            ORDER BY r.score DESC
        ''', (student_id,))
        
        rows = cursor.fetchall()
        recommendations = []
        for row in rows:
            rec = {
                'id': row[0],
                'student_id': row[1],
                'activity_id': row[2],
                'score': row[3],
                'reasoning': row[4],
                'recommended_at': row[5],
                'status': row[6],
                'activity_name': row[7],
                'activity_category': row[8],
                'activity_description': row[9]
            }
            recommendations.append(rec)
        
        conn.close()
        return recommendations
    
    def save_feedback(self, student_id: str, activity_id: str, rating: int, feedback_text: str) -> str:
        """Save student feedback on an activity."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        feedback_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO feedback (id, student_id, activity_id, rating, feedback_text)
            VALUES (?, ?, ?, ?, ?)
        ''', (feedback_id, student_id, activity_id, rating, feedback_text))
        
        conn.commit()
        conn.close()
        return feedback_id
