"""
Smart database manager using pure SQLite
This is a lightweight alternative to ChromaDB for the AI Smart Match application.
"""

import sqlite3
import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import uuid

class SmartDatabaseManager:
    """Smart database manager using SQLite."""
    
    def __init__(self, db_path: str = "data/smartmatch.db"):
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else "data", exist_ok=True)
        
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
                interests TEXT,  -- JSON string
                strengths TEXT,  -- JSON string
                student_values TEXT,     -- JSON string (renamed from values to avoid SQL keyword)
                availability TEXT,  -- JSON string
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
                skills_developed TEXT,  -- JSON string
                time_commitment TEXT,
                difficulty_level INTEGER DEFAULT 1,
                social_impact_score REAL DEFAULT 0.0,
                personal_growth_score REAL DEFAULT 0.0,
                fulfillment_score REAL DEFAULT 0.0,
                prerequisites TEXT,  -- JSON string
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                activity_id TEXT NOT NULL,
                compatibility_score REAL NOT NULL,
                reasoning TEXT,
                recommended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (activity_id) REFERENCES activities (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get a database connection."""
        return sqlite3.connect(self.db_path)
    
    # Student operations
    def add_student(self, student_data: Dict) -> str:
        """Add a new student to the database."""
        student_id = str(uuid.uuid4())
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO students (id, name, grade, interests, strengths, student_values, availability)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            student_id,
            student_data['name'],
            student_data.get('grade'),
            json.dumps(student_data.get('interests', [])),
            json.dumps(student_data.get('strengths', [])),
            json.dumps(student_data.get('values', [])),
            json.dumps(student_data.get('availability', []))
        ))
        
        conn.commit()
        conn.close()
        return student_id
    
    def get_student(self, student_id: str) -> Optional[Dict]:
        """Get a student by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'grade': row[2],
                'interests': json.loads(row[3] or '[]'),
                'strengths': json.loads(row[4] or '[]'),
                'values': json.loads(row[5] or '[]'),  # student_values column
                'availability': json.loads(row[6] or '[]'),
                'created_at': row[7],
                'updated_at': row[8]
            }
        return None
    
    def get_all_students(self) -> List[Dict]:
        """Get all students."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM students ORDER BY name')
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'name': row[1],
                'grade': row[2],
                'interests': json.loads(row[3] or '[]'),
                'strengths': json.loads(row[4] or '[]'),
                'values': json.loads(row[5] or '[]'),  # student_values column
                'availability': json.loads(row[6] or '[]'),
                'created_at': row[7],
                'updated_at': row[8]
            }
            for row in rows
        ]
    
    def update_student(self, student_id: str, student_data: Dict):
        """Update a student's information."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE students 
            SET name = ?, grade = ?, interests = ?, strengths = ?, 
                student_values = ?, availability = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            student_data['name'],
            student_data.get('grade'),
            json.dumps(student_data.get('interests', [])),
            json.dumps(student_data.get('strengths', [])),
            json.dumps(student_data.get('values', [])),
            json.dumps(student_data.get('availability', [])),
            student_id
        ))
        
        conn.commit()
        conn.close()
    
    # Activity operations
    def add_activity(self, activity_data: Dict) -> str:
        """Add a new activity to the database."""
        activity_id = str(uuid.uuid4())
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO activities (
                id, name, category, description, skills_developed, 
                time_commitment, difficulty_level, social_impact_score,
                personal_growth_score, fulfillment_score, prerequisites
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            activity_id,
            activity_data['name'],
            activity_data['category'],
            activity_data.get('description', ''),
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
    
    def get_activity(self, activity_id: str) -> Optional[Dict]:
        """Get an activity by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM activities WHERE id = ?', (activity_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'category': row[2],
                'description': row[3],
                'skills_developed': json.loads(row[4] or '[]'),
                'time_commitment': row[5],
                'difficulty_level': row[6],
                'social_impact_score': row[7],
                'personal_growth_score': row[8],
                'fulfillment_score': row[9],
                'prerequisites': json.loads(row[10] or '[]'),
                'created_at': row[11]
            }
        return None
    
    def get_all_activities(self) -> List[Dict]:
        """Get all activities."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM activities ORDER BY name')
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'name': row[1],
                'category': row[2],
                'description': row[3],
                'skills_developed': json.loads(row[4] or '[]'),
                'time_commitment': row[5],
                'difficulty_level': row[6],
                'social_impact_score': row[7],
                'personal_growth_score': row[8],
                'fulfillment_score': row[9],
                'prerequisites': json.loads(row[10] or '[]'),
                'created_at': row[11]
            }
            for row in rows
        ]
    
    def get_activities_by_category(self, category: str) -> List[Dict]:
        """Get activities by category."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM activities WHERE category = ? ORDER BY name', (category,))
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'name': row[1],
                'category': row[2],
                'description': row[3],
                'skills_developed': json.loads(row[4] or '[]'),
                'time_commitment': row[5],
                'difficulty_level': row[6],
                'social_impact_score': row[7],
                'personal_growth_score': row[8],
                'fulfillment_score': row[9],
                'prerequisites': json.loads(row[10] or '[]'),
                'created_at': row[11]
            }
            for row in rows
        ]
    
    # Recommendation operations
    def save_recommendation(self, student_id: str, activity_id: str, 
                          compatibility_score: float, reasoning: str) -> str:
        """Save a recommendation."""
        recommendation_id = str(uuid.uuid4())
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO recommendations (id, student_id, activity_id, compatibility_score, reasoning)
            VALUES (?, ?, ?, ?, ?)
        ''', (recommendation_id, student_id, activity_id, compatibility_score, reasoning))
        
        conn.commit()
        conn.close()
        return recommendation_id
    
    def get_student_recommendations(self, student_id: str) -> List[Dict]:
        """Get all recommendations for a student."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT r.*, a.name as activity_name, a.category, a.description
            FROM recommendations r
            JOIN activities a ON r.activity_id = a.id
            WHERE r.student_id = ?
            ORDER BY r.compatibility_score DESC
        ''', (student_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        recommendations = []
        for row in rows:
            recommendation = {
                'id': row[0],
                'student_id': row[1],
                'activity_id': row[2],
                'compatibility_score': row[3],
                'reasoning': row[4],
                'recommended_at': row[5],
                'activity': self.get_activity(row[2])
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def clear_student_recommendations(self, student_id: str):
        """Clear all recommendations for a student."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM recommendations WHERE student_id = ?', (student_id,))
        
        conn.commit()
        conn.close()
    
    def get_recommendation_stats(self) -> Dict:
        """Get recommendation statistics."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total recommendations
        cursor.execute('SELECT COUNT(*) FROM recommendations')
        total_recommendations = cursor.fetchone()[0]
        
        # Average compatibility score
        cursor.execute('SELECT AVG(compatibility_score) FROM recommendations')
        avg_score = cursor.fetchone()[0] or 0.0
        
        # Most recommended activities
        cursor.execute('''
            SELECT a.name, COUNT(*) as recommendation_count
            FROM recommendations r
            JOIN activities a ON r.activity_id = a.id
            GROUP BY a.id, a.name
            ORDER BY recommendation_count DESC
            LIMIT 5
        ''')
        top_activities = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_recommendations': total_recommendations,
            'average_compatibility_score': round(avg_score, 2),
            'top_activities': [{'name': row[0], 'count': row[1]} for row in top_activities]
        }
