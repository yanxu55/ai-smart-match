from typing import Dict, List, Tuple
import numpy as np
from database.smart_sqlite_db import SmartDatabaseManager
from database.smart_vector_db import SmartVectorDatabase
from agents.ai_agent import AIAgent

class RecommendationEngine:
    def __init__(self, db_manager: SmartDatabaseManager, vector_db: SmartVectorDatabase, ai_agent: AIAgent):
        self.db_manager = db_manager
        self.vector_db = vector_db
        self.ai_agent = ai_agent
    
    def generate_recommendations(self, student_id: str, n_recommendations: int = 10) -> List[Dict]:
        """Generate personalized activity recommendations for a student."""
        
        # Get student profile
        student = self.db_manager.get_student(student_id)
        if not student:
            return []
        
        # Get all activities
        all_activities = self.db_manager.get_all_activities()
        if not all_activities:
            return []
        
        # Use vector similarity to find relevant activities
        similar_activities = self.vector_db.find_similar_activities(student, n_results=20)
        
        # Create a mapping of activity IDs to full activity data
        activity_map = {act['id']: act for act in all_activities}
        
        # Score each activity
        scored_activities = []
        
        for similar_act in similar_activities:
            activity_id = similar_act['activity_id']
            if activity_id in activity_map:
                activity = activity_map[activity_id]
                
                # Calculate comprehensive score
                score_data = self._calculate_activity_score(student, activity, similar_act['similarity_score'])
                
                # Generate AI reasoning
                reasoning = self.ai_agent.generate_activity_reasoning(student, activity, score_data['overall_score'])
                
                recommendation = {
                    'activity': activity,
                    'score': score_data['overall_score'],
                    'score_breakdown': score_data['breakdown'],
                    'reasoning': reasoning,
                    'similarity_score': similar_act['similarity_score']
                }
                
                scored_activities.append(recommendation)
        
        # Sort by score and return top recommendations
        scored_activities.sort(key=lambda x: x['score'], reverse=True)
        
        # Save recommendations to database
        for rec in scored_activities[:n_recommendations]:
            self.db_manager.save_recommendation(
                student_id=student_id,
                activity_id=rec['activity']['id'],
                compatibility_score=rec['score'],
                reasoning=rec['reasoning']
            )
        
        return scored_activities[:n_recommendations]
    
    def _calculate_activity_score(self, student: Dict, activity: Dict, similarity_score: float) -> Dict:
        """Calculate a comprehensive score for an activity based on student profile."""
        
        # Base scores from activity data
        personal_growth_score = activity.get('personal_growth_score', 5.0)
        social_impact_score = activity.get('social_impact_score', 5.0)
        fulfillment_score = activity.get('fulfillment_score', 5.0)
        
        # Interest alignment score
        interest_score = self._calculate_interest_alignment(student, activity)
        
        # Strength utilization score
        strength_score = self._calculate_strength_utilization(student, activity)
        
        # Values alignment score
        values_score = self._calculate_values_alignment(student, activity)
        
        # Availability and difficulty match
        availability_score = self._calculate_availability_match(student, activity)
        difficulty_score = self._calculate_difficulty_match(student, activity)
        
        # Weighted combination
        weights = {
            'similarity': 0.20,
            'interests': 0.15,
            'strengths': 0.15,
            'values': 0.15,
            'personal_growth': 0.10,
            'social_impact': 0.10,
            'fulfillment': 0.10,
            'availability': 0.03,
            'difficulty': 0.02
        }
        
        overall_score = (
            similarity_score * weights['similarity'] * 10 +  # Convert to 0-10 scale
            interest_score * weights['interests'] +
            strength_score * weights['strengths'] +
            values_score * weights['values'] +
            personal_growth_score * weights['personal_growth'] +
            social_impact_score * weights['social_impact'] +
            fulfillment_score * weights['fulfillment'] +
            availability_score * weights['availability'] +
            difficulty_score * weights['difficulty']
        )
        
        # Ensure score is between 0 and 10
        overall_score = max(0, min(10, overall_score))
        
        return {
            'overall_score': overall_score,
            'breakdown': {
                'similarity': similarity_score * 10,
                'interest_alignment': interest_score,
                'strength_utilization': strength_score,
                'values_alignment': values_score,
                'personal_growth': personal_growth_score,
                'social_impact': social_impact_score,
                'fulfillment': fulfillment_score,
                'availability_match': availability_score,
                'difficulty_match': difficulty_score
            }
        }
    
    def _calculate_interest_alignment(self, student: Dict, activity: Dict) -> float:
        """Calculate how well the activity aligns with student interests."""
        student_interests = set(interest.lower() for interest in student.get('interests', []))
        
        # Check activity name, category, description, and skills
        activity_text = f"{activity.get('name', '')} {activity.get('category', '')} {activity.get('description', '')}".lower()
        activity_skills = [skill.lower() for skill in activity.get('skills_developed', [])]
        
        alignment_score = 0
        total_interests = len(student_interests) if student_interests else 1
        
        for interest in student_interests:
            if interest in activity_text or any(interest in skill for skill in activity_skills):
                alignment_score += 1
        
        # Convert to 0-10 scale
        return min(10, (alignment_score / total_interests) * 10)
    
    def _calculate_strength_utilization(self, student: Dict, activity: Dict) -> float:
        """Calculate how well the activity utilizes student strengths."""
        student_strengths = set(strength.lower() for strength in student.get('strengths', []))
        activity_skills = set(skill.lower() for skill in activity.get('skills_developed', []))
        
        if not student_strengths:
            return 5.0  # Neutral score if no strengths specified
        
        # Calculate overlap
        overlap = len(student_strengths.intersection(activity_skills))
        max_possible = len(student_strengths)
        
        # Convert to 0-10 scale
        return min(10, (overlap / max_possible) * 10) if max_possible > 0 else 5.0
    
    def _calculate_values_alignment(self, student: Dict, activity: Dict) -> float:
        """Calculate how well the activity aligns with student values."""
        student_values = set(value.lower() for value in student.get('values', []))
        
        # Map values to activity characteristics
        value_activity_mapping = {
            'helping others': ['community service', 'volunteer', 'social'],
            'leadership': ['leadership', 'team captain', 'president'],
            'creativity': ['arts', 'creative', 'design', 'music'],
            'competition': ['sports', 'competition', 'tournament'],
            'learning': ['academic', 'research', 'study'],
            'teamwork': ['team', 'group', 'collaborative'],
            'independence': ['individual', 'solo', 'personal'],
            'innovation': ['technology', 'science', 'innovation']
        }
        
        activity_text = f"{activity.get('name', '')} {activity.get('category', '')} {activity.get('description', '')}".lower()
        
        alignment_score = 0
        for value in student_values:
            if value in value_activity_mapping:
                for keyword in value_activity_mapping[value]:
                    if keyword in activity_text:
                        alignment_score += 1
                        break
        
        total_values = len(student_values) if student_values else 1
        return min(10, (alignment_score / total_values) * 10)
    
    def _calculate_availability_match(self, student: Dict, activity: Dict) -> float:
        """Calculate how well the activity matches student availability."""
        # Simplified availability check
        availability = student.get('availability', {})
        time_commitment = activity.get('time_commitment', '').lower()
        
        # Basic scoring based on time commitment
        if 'high' in time_commitment or 'intensive' in time_commitment:
            return 7.0  # Moderate score for high commitment
        elif 'low' in time_commitment or 'minimal' in time_commitment:
            return 9.0  # High score for low commitment
        else:
            return 8.0  # Good score for medium commitment
    
    def _calculate_difficulty_match(self, student: Dict, activity: Dict) -> float:
        """Calculate how well the activity difficulty matches student level."""
        grade = student.get('grade', 10)  # Default to grade 10
        difficulty = activity.get('difficulty_level', 1)
        
        # Simple difficulty matching
        if grade <= 9 and difficulty <= 2:
            return 9.0  # Easy activities for younger students
        elif grade >= 11 and difficulty >= 3:
            return 9.0  # Challenging activities for older students
        elif abs(difficulty - (grade - 8)) <= 1:  # Grade 9 -> difficulty 1, Grade 12 -> difficulty 4
            return 8.0  # Good match
        else:
            return 6.0  # Moderate match
    
    def get_recommendation_insights(self, student_id: str) -> Dict:
        """Get insights about the recommendation process for a student."""
        student = self.db_manager.get_student(student_id)
        if not student:
            return {}
        
        # Analyze student profile
        profile_analysis = self.ai_agent.analyze_student_profile(student)
        
        # Get recommendations
        recommendations = self.generate_recommendations(student_id, n_recommendations=5)
        
        # Create development pathway
        development_pathway = self.ai_agent.plan_development_pathway(student, [rec['activity'] for rec in recommendations])
        
        return {
            'profile_analysis': profile_analysis,
            'development_pathway': development_pathway,
            'top_recommendations': recommendations,
            'recommendation_summary': {
                'total_activities_considered': len(self.db_manager.get_all_activities()),
                'recommendation_count': len(recommendations),
                'avg_score': np.mean([rec['score'] for rec in recommendations]) if recommendations else 0
            }
        }
