from openai import OpenAI, AzureOpenAI
from typing import Dict, List, Optional
import json
import os
from dotenv import load_dotenv

load_dotenv()

class AIAgent:
    def __init__(self):
        # Check if Azure OpenAI is configured
        azure_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        
        if azure_key and azure_endpoint:
            # Use Azure OpenAI
            self.client = AzureOpenAI(
                api_key=azure_key,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                azure_endpoint=azure_endpoint
            )
            self.model = os.getenv("AZURE_OPENAI_CHAT_MODEL", "gpt-4")
            self.is_azure = True
        else:
            # Use regular OpenAI
            openai_key = os.getenv("OPENAI_API_KEY")
            if not openai_key:
                raise ValueError("No OpenAI API key found in environment variables")
            self.client = OpenAI(api_key=openai_key)
            self.model = os.getenv("OPENAI_MODEL", "gpt-4")
            self.is_azure = False
        
        # Validate configuration
        self._validate_configuration()
    
    def _validate_configuration(self):
        """Validate the AI configuration."""
        try:
            # Test the connection with a simple request
            test_response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            print(f"✅ AI Agent initialized successfully with {'Azure OpenAI' if self.is_azure else 'OpenAI'}")
            print(f"   Model: {self.model}")
        except Exception as e:
            print(f"❌ AI Agent configuration error: {str(e)}")
            print("   Please check your API keys and endpoints in the .env file")
    
    def get_model_info(self) -> Dict[str, Optional[str]]:
        """Get information about the current model configuration."""
        return {
            "provider": "Azure OpenAI" if self.is_azure else "OpenAI",
            "model": self.model,
            "api_version": os.getenv("AZURE_OPENAI_API_VERSION") if self.is_azure else None,
            "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT") if self.is_azure else None
        }
    
    def generate_response(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Generate a response using OpenAI GPT."""
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            content = response.choices[0].message.content
            return content if content is not None else "No response generated"
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def analyze_student_profile(self, student_profile: Dict) -> Dict:
        """Analyze student profile to extract insights."""
        system_message = """
        You are an expert educational counselor and career advisor. Analyze the student profile
        and provide insights about their potential interests, strengths, and recommended development areas.
        Return your analysis as a JSON object with the following structure:
        {
            "personality_traits": ["list", "of", "traits"],
            "potential_interests": ["list", "of", "potential", "interests"],
            "development_areas": ["list", "of", "areas", "to", "develop"],
            "leadership_potential": "high/medium/low",
            "collaboration_style": "description",
            "recommended_focus": "description"
        }
        """
        
        prompt = f"""
        Student Profile:
        Name: {student_profile.get('name', 'Unknown')}
        Grade: {student_profile.get('grade', 'Unknown')}
        Interests: {', '.join(student_profile.get('interests', []))}
        Strengths: {', '.join(student_profile.get('strengths', []))}
        Values: {', '.join(student_profile.get('values', []))}
        Availability: {student_profile.get('availability', {})}
        
        Please analyze this student profile and provide detailed insights.
        """
        
        response = self.generate_response(prompt, system_message)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "personality_traits": [],
                "potential_interests": [],
                "development_areas": [],
                "leadership_potential": "medium",
                "collaboration_style": "balanced",
                "recommended_focus": response
            }
    
    def generate_activity_reasoning(self, student_profile: Dict, activity: Dict, score: float) -> str:
        """Generate reasoning for why an activity is recommended."""
        system_message = """
        You are an expert educational counselor. Generate a clear, personalized explanation
        for why a specific extracurricular activity is recommended for a student.
        Focus on how the activity aligns with their interests, develops their strengths,
        and supports their values. Be encouraging and specific.
        """
        
        prompt = f"""
        Student Profile:
        Interests: {', '.join(student_profile.get('interests', []))}
        Strengths: {', '.join(student_profile.get('strengths', []))}
        Values: {', '.join(student_profile.get('values', []))}
        
        Recommended Activity:
        Name: {activity.get('name', '')}
        Category: {activity.get('category', '')}
        Description: {activity.get('description', '')}
        Skills Developed: {', '.join(activity.get('skills_developed', []))}
        
        Recommendation Score: {score:.2f}/10
        
        Please explain why this activity is recommended for this student in 2-3 sentences.
        """
        
        return self.generate_response(prompt, system_message)
    
    def plan_development_pathway(self, student_profile: Dict, recommended_activities: List[Dict]) -> Dict:
        """Create a development pathway plan for the student."""
        system_message = """
        You are an expert educational planner. Create a structured development pathway
        for a student based on their profile and recommended activities.
        Return a JSON object with the following structure:
        {
            "short_term_goals": ["goal1", "goal2"],
            "long_term_goals": ["goal1", "goal2"],
            "activity_sequence": [
                {
                    "activity": "activity_name",
                    "timeline": "when to start",
                    "reason": "why this timing"
                }
            ],
            "skill_progression": {
                "beginner": ["skills"],
                "intermediate": ["skills"],
                "advanced": ["skills"]
            },
            "milestones": [
                {
                    "milestone": "description",
                    "timeframe": "when to achieve"
                }
            ]
        }
        """
        
        activities_text = "\n".join([
            f"- {act.get('name', '')}: {act.get('description', '')}"
            for act in recommended_activities[:5]  # Top 5 activities
        ])
        
        prompt = f"""
        Student Profile:
        Grade: {student_profile.get('grade', 'Unknown')}
        Interests: {', '.join(student_profile.get('interests', []))}
        Strengths: {', '.join(student_profile.get('strengths', []))}
        Values: {', '.join(student_profile.get('values', []))}
        
        Recommended Activities:
        {activities_text}
        
        Create a comprehensive development pathway plan for this student.
        """
        
        response = self.generate_response(prompt, system_message)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "short_term_goals": ["Explore recommended activities", "Develop key skills"],
                "long_term_goals": ["Build leadership experience", "Create positive impact"],
                "activity_sequence": [],
                "skill_progression": {
                    "beginner": [],
                    "intermediate": [],
                    "advanced": []
                },
                "milestones": []
            }
    
    def evaluate_activity_fit(self, student_profile: Dict, activity: Dict) -> Dict:
        """Evaluate how well an activity fits a student's profile."""
        system_message = """
        You are an expert in student development and extracurricular activities.
        Evaluate how well an activity fits a student's profile across three dimensions:
        1. Personal Growth (develops their strengths and addresses development areas)
        2. Social Impact (creates value for others and community)
        3. Personal Fulfillment (aligns with interests and values)
        
        Return a JSON object with scores (0-10) and brief explanations:
        {
            "personal_growth": {"score": 8, "explanation": "reasoning"},
            "social_impact": {"score": 7, "explanation": "reasoning"},
            "personal_fulfillment": {"score": 9, "explanation": "reasoning"},
            "overall_score": 8.0,
            "key_benefits": ["benefit1", "benefit2"],
            "potential_challenges": ["challenge1", "challenge2"]
        }
        """
        
        prompt = f"""
        Student Profile:
        Interests: {', '.join(student_profile.get('interests', []))}
        Strengths: {', '.join(student_profile.get('strengths', []))}
        Values: {', '.join(student_profile.get('values', []))}
        Grade: {student_profile.get('grade', 'Unknown')}
        
        Activity:
        Name: {activity.get('name', '')}
        Category: {activity.get('category', '')}
        Description: {activity.get('description', '')}
        Skills Developed: {', '.join(activity.get('skills_developed', []))}
        Time Commitment: {activity.get('time_commitment', '')}
        Difficulty Level: {activity.get('difficulty_level', 1)}
        
        Evaluate this activity fit for the student.
        """
        
        response = self.generate_response(prompt, system_message)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "personal_growth": {"score": 5, "explanation": "Moderate fit"},
                "social_impact": {"score": 5, "explanation": "Moderate impact"},
                "personal_fulfillment": {"score": 5, "explanation": "Moderate alignment"},
                "overall_score": 5.0,
                "key_benefits": [],
                "potential_challenges": []
            }
