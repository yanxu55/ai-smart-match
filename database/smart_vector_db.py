"""
Smart vector database using FAISS for similarity search
This replaces ChromaDB with a lighter, file-based vector search solution.
"""

import faiss
import numpy as np
import json
import os
import pickle
from typing import List, Dict, Optional, Tuple
from sentence_transformers import SentenceTransformer
import uuid

class SmartVectorDatabase:
    """Smart vector database using FAISS for similarity search."""
    
    def __init__(self, data_dir: str = "data/vectors"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize sentence transformer for embeddings
        # Check if a specific embedding model is configured
        embedding_model = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
        
        try:
            self.model = SentenceTransformer(embedding_model)
            print(f"✅ Embedding model loaded: {embedding_model}")
        except Exception as e:
            print(f"⚠️  Failed to load {embedding_model}, falling back to all-MiniLM-L6-v2")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
        # Get embedding dimension dynamically
        test_embedding = self.model.encode("test")
        self.embedding_dim = len(test_embedding)
        print(f"   Embedding dimension: {self.embedding_dim}")
        
        # Initialize FAISS indices
        self.activities_index = None
        self.student_profiles_index = None
        
        # Metadata storage
        self.activities_metadata = {}
        self.student_profiles_metadata = {}
        
        # Load existing indices if they exist
        self.load_indices()
    
    def _get_activities_index_path(self) -> str:
        return os.path.join(self.data_dir, "activities.index")
    
    def _get_student_profiles_index_path(self) -> str:
        return os.path.join(self.data_dir, "student_profiles.index")
    
    def _get_activities_metadata_path(self) -> str:
        return os.path.join(self.data_dir, "activities_metadata.pkl")
    
    def _get_student_profiles_metadata_path(self) -> str:
        return os.path.join(self.data_dir, "student_profiles_metadata.pkl")
    
    def load_indices(self):
        """Load existing FAISS indices and metadata."""
        try:
            # Load activities index
            if os.path.exists(self._get_activities_index_path()):
                self.activities_index = faiss.read_index(self._get_activities_index_path())
            else:
                self.activities_index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product for cosine similarity
            
            # Load student profiles index
            if os.path.exists(self._get_student_profiles_index_path()):
                self.student_profiles_index = faiss.read_index(self._get_student_profiles_index_path())
            else:
                self.student_profiles_index = faiss.IndexFlatIP(self.embedding_dim)
            
            # Load metadata
            if os.path.exists(self._get_activities_metadata_path()):
                with open(self._get_activities_metadata_path(), 'rb') as f:
                    self.activities_metadata = pickle.load(f)
            
            if os.path.exists(self._get_student_profiles_metadata_path()):
                with open(self._get_student_profiles_metadata_path(), 'rb') as f:
                    self.student_profiles_metadata = pickle.load(f)
        
        except Exception as e:
            print(f"Warning: Could not load existing indices: {e}")
            # Initialize fresh indices
            self.activities_index = faiss.IndexFlatIP(self.embedding_dim)
            self.student_profiles_index = faiss.IndexFlatIP(self.embedding_dim)
            self.activities_metadata = {}
            self.student_profiles_metadata = {}
    
    def save_indices(self):
        """Save FAISS indices and metadata to disk."""
        try:
            # Save indices
            faiss.write_index(self.activities_index, self._get_activities_index_path())
            faiss.write_index(self.student_profiles_index, self._get_student_profiles_index_path())
            
            # Save metadata
            with open(self._get_activities_metadata_path(), 'wb') as f:
                pickle.dump(self.activities_metadata, f)
            
            with open(self._get_student_profiles_metadata_path(), 'wb') as f:
                pickle.dump(self.student_profiles_metadata, f)
        
        except Exception as e:
            print(f"Warning: Could not save indices: {e}")
    
    def _create_activity_text(self, activity: Dict) -> str:
        """Create text representation of an activity for embedding."""
        text_parts = [
            f"Activity: {activity['name']}",
            f"Category: {activity['category']}",
            f"Description: {activity.get('description', '')}",
        ]
        
        if activity.get('skills_developed'):
            text_parts.append(f"Skills: {', '.join(activity['skills_developed'])}")
        
        if activity.get('time_commitment'):
            text_parts.append(f"Time Commitment: {activity['time_commitment']}")
        
        if activity.get('prerequisites'):
            text_parts.append(f"Prerequisites: {', '.join(activity['prerequisites'])}")
        
        return " ".join(text_parts)
    
    def _create_student_text(self, student: Dict) -> str:
        """Create text representation of a student profile for embedding."""
        text_parts = [
            f"Student interests: {', '.join(student.get('interests', []))}",
            f"Strengths: {', '.join(student.get('strengths', []))}",
            f"Values: {', '.join(student.get('values', []))}",
        ]
        
        if student.get('grade'):
            text_parts.append(f"Grade: {student['grade']}")
        
        return " ".join(text_parts)
    
    def add_activities(self, activities: List[Dict]):
        """Add activities to the vector database."""
        if not activities:
            return
        
        # Create embeddings
        texts = [self._create_activity_text(activity) for activity in activities]
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        
        # Add to FAISS index
        self.activities_index.add(embeddings.astype('float32'))
        
        # Update metadata
        current_index = self.activities_index.ntotal - len(activities)
        for i, activity in enumerate(activities):
            index_id = current_index + i
            self.activities_metadata[index_id] = {
                'id': activity['id'],
                'name': activity['name'],
                'category': activity['category'],
                'difficulty_level': activity.get('difficulty_level', 1),
                'social_impact_score': activity.get('social_impact_score', 0.0),
                'personal_growth_score': activity.get('personal_growth_score', 0.0),
                'fulfillment_score': activity.get('fulfillment_score', 0.0),
                'text': texts[i]
            }
        
        # Save to disk
        self.save_indices()
    
    def add_student_profile(self, student: Dict):
        """Add a student profile to the vector database."""
        # Create embedding
        text = self._create_student_text(student)
        embedding = self.model.encode([text], normalize_embeddings=True)
        
        # Add to FAISS index
        self.student_profiles_index.add(embedding.astype('float32'))
        
        # Update metadata
        index_id = self.student_profiles_index.ntotal - 1
        self.student_profiles_metadata[index_id] = {
            'id': student['id'],
            'name': student['name'],
            'grade': student.get('grade', 0),
            'interests': student.get('interests', []),
            'strengths': student.get('strengths', []),
            'values': student.get('values', []),
            'text': text
        }
        
        # Save to disk
        self.save_indices()
    
    def find_similar_activities(self, student_profile: Dict, n_results: int = 10) -> List[Dict]:
        """Find activities similar to student profile using vector similarity."""
        if self.activities_index.ntotal == 0:
            return []
        
        # Create query embedding
        query_text = self._create_student_text(student_profile)
        query_embedding = self.model.encode([query_text], normalize_embeddings=True)
        
        # Search FAISS index
        n_results = min(n_results, self.activities_index.ntotal)
        scores, indices = self.activities_index.search(query_embedding.astype('float32'), n_results)
        
        # Prepare results
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx in self.activities_metadata:
                metadata = self.activities_metadata[idx]
                result = {
                    'activity_id': metadata['id'],
                    'name': metadata['name'],
                    'category': metadata['category'],
                    'similarity_score': float(score),
                    'rank': i + 1,
                    'metadata': metadata
                }
                results.append(result)
        
        return results
    
    def find_similar_students(self, target_student: Dict, n_results: int = 5) -> List[Dict]:
        """Find students similar to the target student."""
        if self.student_profiles_index.ntotal == 0:
            return []
        
        # Create query embedding
        query_text = self._create_student_text(target_student)
        query_embedding = self.model.encode([query_text], normalize_embeddings=True)
        
        # Search FAISS index
        n_results = min(n_results, self.student_profiles_index.ntotal)
        scores, indices = self.student_profiles_index.search(query_embedding.astype('float32'), n_results)
        
        # Prepare results
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx in self.student_profiles_metadata:
                metadata = self.student_profiles_metadata[idx]
                # Skip the same student
                if metadata['id'] != target_student['id']:
                    result = {
                        'student_id': metadata['id'],
                        'name': metadata['name'],
                        'grade': metadata['grade'],
                        'similarity_score': float(score),
                        'rank': i + 1,
                        'interests': metadata['interests'],
                        'strengths': metadata['strengths'],
                        'values': metadata['values']
                    }
                    results.append(result)
        
        return results
    
    def search_activities_by_text(self, query_text: str, n_results: int = 10) -> List[Dict]:
        """Search activities using free text query."""
        if self.activities_index.ntotal == 0:
            return []
        
        # Create query embedding
        query_embedding = self.model.encode([query_text], normalize_embeddings=True)
        
        # Search FAISS index
        n_results = min(n_results, self.activities_index.ntotal)
        scores, indices = self.activities_index.search(query_embedding.astype('float32'), n_results)
        
        # Prepare results
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx in self.activities_metadata:
                metadata = self.activities_metadata[idx]
                result = {
                    'activity_id': metadata['id'],
                    'name': metadata['name'],
                    'category': metadata['category'],
                    'similarity_score': float(score),
                    'rank': i + 1,
                    'metadata': metadata
                }
                results.append(result)
        
        return results
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector database."""
        return {
            'total_activities': self.activities_index.ntotal,
            'total_student_profiles': self.student_profiles_index.ntotal,
            'embedding_dimension': self.embedding_dim,
            'model_name': 'all-MiniLM-L6-v2'
        }
    
    def clear_all_data(self):
        """Clear all data from the vector database."""
        # Reset indices
        self.activities_index = faiss.IndexFlatIP(self.embedding_dim)
        self.student_profiles_index = faiss.IndexFlatIP(self.embedding_dim)
        
        # Clear metadata
        self.activities_metadata = {}
        self.student_profiles_metadata = {}
        
        # Remove files
        for file_path in [
            self._get_activities_index_path(),
            self._get_student_profiles_index_path(),
            self._get_activities_metadata_path(),
            self._get_student_profiles_metadata_path()
        ]:
            if os.path.exists(file_path):
                os.remove(file_path)
