import chromadb
from chromadb.utils import embedding_functions
import json
from typing import List, Dict, Optional
import numpy as np

class VectorDatabase:
    def __init__(self, persist_directory: str = "data/chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Initialize embedding function (using default sentence transformers)
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        
        # Collections for different types of data
        self.activities_collection = self.client.get_or_create_collection(
            name="activities",
            embedding_function=self.embedding_function
        )
        
        self.student_profiles_collection = self.client.get_or_create_collection(
            name="student_profiles",
            embedding_function=self.embedding_function
        )
    
    def add_activity_embeddings(self, activities: List[Dict]):
        """Add activity embeddings to the vector database."""
        documents = []
        metadatas = []
        ids = []
        
        for activity in activities:
            # Create text representation for embedding
            text = f"""
            Activity: {activity['name']}
            Category: {activity['category']}
            Description: {activity['description']}
            Skills: {', '.join(activity.get('skills_developed', []))}
            Time Commitment: {activity.get('time_commitment', '')}
            Prerequisites: {', '.join(activity.get('prerequisites', []))}
            """
            
            documents.append(text.strip())
            metadatas.append({
                'name': activity['name'],
                'category': activity['category'],
                'difficulty_level': activity.get('difficulty_level', 1),
                'social_impact_score': activity.get('social_impact_score', 0.0),
                'personal_growth_score': activity.get('personal_growth_score', 0.0),
                'fulfillment_score': activity.get('fulfillment_score', 0.0)
            })
            ids.append(activity['id'])
        
        # Add to collection
        self.activities_collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def add_student_profile_embedding(self, student: Dict):
        """Add student profile embedding to the vector database."""
        # Create text representation for embedding
        text = f"""
        Student Profile:
        Interests: {', '.join(student.get('interests', []))}
        Strengths: {', '.join(student.get('strengths', []))}
        Values: {', '.join(student.get('values', []))}
        Grade: {student.get('grade', '')}
        """
        
        metadata = {
            'name': student['name'],
            'grade': student.get('grade', 0),
            'interests_count': len(student.get('interests', [])),
            'strengths_count': len(student.get('strengths', [])),
            'values_count': len(student.get('values', []))
        }
        
        self.student_profiles_collection.add(
            documents=[text.strip()],
            metadatas=[metadata],
            ids=[student['id']]
        )
    
    def find_similar_activities(self, student_profile: Dict, n_results: int = 10) -> List[Dict]:
        """Find activities similar to student profile using vector similarity."""
        # Create query text from student profile
        query_text = f"""
        Looking for activities matching:
        Interests: {', '.join(student_profile.get('interests', []))}
        Strengths: {', '.join(student_profile.get('strengths', []))}
        Values: {', '.join(student_profile.get('values', []))}
        """
        
        # Query the activities collection
        results = self.activities_collection.query(
            query_texts=[query_text.strip()],
            n_results=n_results
        )
        
        # Format results
        similar_activities = []
        if results['ids'] and results['ids'][0]:
            for i, activity_id in enumerate(results['ids'][0]):
                activity_data = {
                    'id': activity_id,
                    'name': results['metadatas'][0][i]['name'],
                    'category': results['metadatas'][0][i]['category'],
                    'similarity_score': 1 - results['distances'][0][i] if results['distances'] else 0.0,
                    'metadata': results['metadatas'][0][i]
                }
                similar_activities.append(activity_data)
        
        return similar_activities
    
    def find_similar_students(self, student_profile: Dict, n_results: int = 5) -> List[Dict]:
        """Find students with similar profiles."""
        # Create query text from student profile
        query_text = f"""
        Student Profile:
        Interests: {', '.join(student_profile.get('interests', []))}
        Strengths: {', '.join(student_profile.get('strengths', []))}
        Values: {', '.join(student_profile.get('values', []))}
        """
        
        # Query the student profiles collection
        results = self.student_profiles_collection.query(
            query_texts=[query_text.strip()],
            n_results=n_results
        )
        
        # Format results (exclude self)
        similar_students = []
        if results['ids'] and results['ids'][0]:
            for i, student_id in enumerate(results['ids'][0]):
                if student_id != student_profile['id']:  # Exclude self
                    student_data = {
                        'id': student_id,
                        'similarity_score': 1 - results['distances'][0][i] if results['distances'] else 0.0,
                        'metadata': results['metadatas'][0][i]
                    }
                    similar_students.append(student_data)
        
        return similar_students
    
    def update_activity_embedding(self, activity: Dict):
        """Update an existing activity embedding."""
        # Delete existing
        try:
            self.activities_collection.delete(ids=[activity['id']])
        except:
            pass  # Activity might not exist yet
        
        # Add updated version
        self.add_activity_embeddings([activity])
    
    def update_student_profile_embedding(self, student: Dict):
        """Update an existing student profile embedding."""
        # Delete existing
        try:
            self.student_profiles_collection.delete(ids=[student['id']])
        except:
            pass  # Student might not exist yet
        
        # Add updated version
        self.add_student_profile_embedding(student)
    
    def get_activity_by_category(self, category: str, n_results: int = 10) -> List[Dict]:
        """Get activities by category using vector search."""
        query_text = f"Activities in category: {category}"
        
        results = self.activities_collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where={"category": category}
        )
        
        activities = []
        if results['ids'] and results['ids'][0]:
            for i, activity_id in enumerate(results['ids'][0]):
                activity_data = {
                    'id': activity_id,
                    'name': results['metadatas'][0][i]['name'],
                    'category': results['metadatas'][0][i]['category'],
                    'metadata': results['metadatas'][0][i]
                }
                activities.append(activity_data)
        
        return activities
