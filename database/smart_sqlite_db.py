"""
Smart database manager using pure SQLite
This is a lightweight alternative to ChromaDB for the AI Smart Match application.
"""

import sqlite3
import json
import os
import random
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
    
    def _generate_unique_student_id(self) -> str:
        """Generate a unique 4-digit student ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Try up to 100 times to find a unique ID
        for _ in range(100):
            # Generate a 4-digit ID (1000-9999)
            student_id = str(random.randint(1000, 9999))
            
            # Check if ID already exists
            cursor.execute('SELECT id FROM students WHERE id = ?', (student_id,))
            if cursor.fetchone() is None:
                conn.close()
                return student_id
        
        conn.close()
        # Fallback to UUID if we can't find a unique 4-digit ID
        raise ValueError("Unable to generate unique 4-digit student ID. Database may be full.")
    
    # Student operations
    def add_student(self, student_data: Dict) -> str:
        """Add a new student to the database."""
        student_id = self._generate_unique_student_id()
        
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
    
    def delete_student(self, student_id: str) -> bool:
        """
        Delete a student and all associated data.
        
        Args:
            student_id (str): The ID of the student to delete
            
        Returns:
            bool: True if student was deleted, False if student not found
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # First check if student exists
            cursor.execute('SELECT id FROM students WHERE id = ?', (student_id,))
            if not cursor.fetchone():
                return False
            
            # Delete associated recommendations first (foreign key constraint)
            cursor.execute('DELETE FROM recommendations WHERE student_id = ?', (student_id,))
            
            # Delete the student
            cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
            
            conn.commit()
            return True
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
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
    
    def delete_activity(self, activity_id: str) -> bool:
        """
        Delete an activity and all associated recommendations.
        
        Args:
            activity_id (str): The ID of the activity to delete
            
        Returns:
            bool: True if activity was deleted, False if activity not found
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # First check if activity exists and get its name for logging
            cursor.execute('SELECT name FROM activities WHERE id = ?', (activity_id,))
            result = cursor.fetchone()
            if not result:
                print(f"DEBUG: Activity with ID {activity_id} not found")
                return False
            
            activity_name = result[0]
            print(f"DEBUG: Deleting activity '{activity_name}' (ID: {activity_id})")
            
            # Delete associated recommendations first (foreign key constraint)
            cursor.execute('DELETE FROM recommendations WHERE activity_id = ?', (activity_id,))
            deleted_recs = cursor.rowcount
            print(f"DEBUG: Deleted {deleted_recs} associated recommendations")
            
            # Delete the activity
            cursor.execute('DELETE FROM activities WHERE id = ?', (activity_id,))
            deleted_activities = cursor.rowcount
            print(f"DEBUG: Deleted {deleted_activities} activity record")
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"DEBUG: Error during deletion: {e}")
            conn.rollback()
            raise e
        finally:
            conn.close()

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
    
    def get_all_students_with_activities(self) -> List[Dict]:
        """Get all students with their names, IDs, and recommended/chosen activities."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get all students with their recommendations
        cursor.execute('''
            SELECT 
                s.id, 
                s.name, 
                s.grade,
                COUNT(r.id) as recommendation_count
            FROM students s
            LEFT JOIN recommendations r ON s.id = r.student_id
            GROUP BY s.id, s.name, s.grade
            ORDER BY s.name
        ''')
        
        student_rows = cursor.fetchall()
        
        students_with_activities = []
        for student_row in student_rows:
            student_id = student_row[0]
            student_name = student_row[1]
            student_grade = student_row[2]
            recommendation_count = student_row[3]
            
            # Get recommended activities for this student
            cursor.execute('''
                SELECT 
                    a.name as activity_name,
                    a.category,
                    r.compatibility_score,
                    r.recommended_at
                FROM recommendations r
                JOIN activities a ON r.activity_id = a.id
                WHERE r.student_id = ?
                ORDER BY r.compatibility_score DESC
            ''', (student_id,))
            
            activity_rows = cursor.fetchall()
            
            activities = []
            for activity_row in activity_rows:
                activities.append({
                    'name': activity_row[0],
                    'category': activity_row[1],
                    'compatibility_score': round(activity_row[2], 1),
                    'recommended_at': activity_row[3]
                })
            
            students_with_activities.append({
                'id': student_id,
                'name': student_name,
                'grade': student_grade,
                'recommendation_count': recommendation_count,
                'activities': activities
            })
        
        conn.close()
        return students_with_activities
