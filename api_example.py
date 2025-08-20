#!/usr/bin/env python3
"""
SmartMatch API Example
Demonstrates how to use the SmartMatch system programmatically.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from database.smart_sqlite_db import SmartDatabaseManager
from database.smart_vector_db import SmartVectorDatabase
from agents.ai_agent import AIAgent
from agents.recommendation_engine import RecommendationEngine
from utils.data_loader import initialize_sample_data
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Demonstrate the SmartMatch API usage."""
    print("🎯 SmartMatch API Example")
    print("=" * 40)
    
    # Initialize system components
    print("1. Initializing system...")
    os.makedirs("data", exist_ok=True)
    
    db_manager = SmartDatabaseManager("data/smartmatch.db")
    vector_db = SmartVectorDatabase("data/vector_db")
    ai_agent = AIAgent()
    recommendation_engine = RecommendationEngine(db_manager, vector_db, ai_agent)
    
    # Initialize sample data if needed
    activities = db_manager.get_all_activities()
    if len(activities) == 0:
        print("2. Initializing sample data...")
        initialize_sample_data(db_manager, vector_db)
    else:
        print(f"2. Found {len(activities)} existing activities")
    
    # Create a sample student
    print("3. Creating sample student...")
    student_data = {
        "name": "Alex Johnson",
        "grade": 11,
        "interests": ["Technology", "Environmental Science", "Writing"],
        "strengths": ["Problem Solving", "Communication", "Research"],
        "values": ["Innovation", "Environmental Sustainability", "Social Justice"],
        "availability": {
            "weekdays": "3 hours/day",
            "weekends": "6 hours/day"
        }
    }
    
    # Add student to database
    student_id = db_manager.add_student(student_data)
    student_data['id'] = student_id
    
    # Add to vector database
    vector_db.add_student_profile(student_data)
    
    print(f"   Created student: {student_data['name']} (ID: {student_id})")
    
    # Generate recommendations
    print("4. Generating recommendations...")
    recommendations = recommendation_engine.generate_recommendations(
        student_id, n_recommendations=5
    )
    
    if recommendations:
        print(f"   Generated {len(recommendations)} recommendations!")
        
        print("\n📋 Top Recommendations:")
        print("-" * 40)
        
        for i, rec in enumerate(recommendations, 1):
            activity = rec['activity']
            score = rec['score']
            print(f"{i}. {activity['name']} (Score: {score:.1f}/10)")
            print(f"   Category: {activity['category']}")
            print(f"   Why: {rec.get('reasoning', 'Match based on profile')}")
            print()
    
    # Get insights
    print("5. Getting detailed insights...")
    insights = recommendation_engine.get_recommendation_insights(student_id)
    
    if insights:
        print("📊 Student Insights:")
        print(f"   Strength Areas: {', '.join(insights.get('strength_areas', []))}")
        print(f"   Growth Opportunities: {', '.join(insights.get('growth_opportunities', []))}")
        
        if 'recommended_categories' in insights:
            print(f"   Best Categories: {', '.join(insights['recommended_categories'][:3])}")
    
    # Show database stats
    print("\n6. Database Statistics:")
    activities = db_manager.get_all_activities()
    students = db_manager.get_all_students()
    vector_stats = vector_db.get_stats()
    
    print(f"   Activities: {len(activities)}")
    print(f"   Students: {len(students)}")
    print(f"   Vector DB dimension: {vector_stats['embedding_dimension']}")
    
    # AI agent info
    model_info = ai_agent.get_model_info()
    print(f"   AI Provider: {model_info['provider']}")
    print(f"   AI Model: {model_info['model']}")
    
    print("\n✅ Example completed successfully!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
