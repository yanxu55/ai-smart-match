#!/usr/bin/env python3
"""
Script to add the new clubs directly to the database
"""

from database.smart_sqlite_db import SmartDatabaseManager
from database.smart_vector_db import SmartVectorDatabase

def add_new_clubs():
    """Add the 14 new clubs to the database"""
    
    # Initialize database connections
    db_manager = SmartDatabaseManager("data/smartmatch.db")
    vector_db = SmartVectorDatabase("data/vector_db")
    
    new_clubs = [
        {
            "name": "Esports Team",
            "category": "Technology",
            "description": "Compete in video game tournaments, develop teamwork in gaming, and explore careers in esports.",
            "skills_developed": ["strategic thinking", "hand-eye coordination", "teamwork", "communication", "competition"],
            "time_commitment": "6-10 hours/week",
            "difficulty_level": 3,
            "social_impact_score": 4.0,
            "personal_growth_score": 6.5,
            "fulfillment_score": 9.0,
            "prerequisites": ["gaming experience"]
        },
        {
            "name": "Culinary Arts Club",
            "category": "Life Skills",
            "description": "Learn cooking techniques, explore world cuisines, and cater school events.",
            "skills_developed": ["cooking", "creativity", "time management", "cultural awareness", "nutrition knowledge"],
            "time_commitment": "4-6 hours/week",
            "difficulty_level": 2,
            "social_impact_score": 6.5,
            "personal_growth_score": 7.5,
            "fulfillment_score": 8.5,
            "prerequisites": []
        },
        {
            "name": "Robotics Team",
            "category": "STEM",
            "description": "Design, build, and program robots for competitions like FIRST Robotics.",
            "skills_developed": ["engineering", "programming", "teamwork", "problem-solving", "innovation"],
            "time_commitment": "8-12 hours/week",
            "difficulty_level": 4,
            "social_impact_score": 6.0,
            "personal_growth_score": 9.0,
            "fulfillment_score": 8.0,
            "prerequisites": ["interest in STEM"]
        },
        {
            "name": "Photography Club",
            "category": "Arts",
            "description": "Develop photography skills, document school events, and create visual stories.",
            "skills_developed": ["photography", "visual storytelling", "creativity", "technical skills", "editing"],
            "time_commitment": "3-5 hours/week",
            "difficulty_level": 2,
            "social_impact_score": 6.0,
            "personal_growth_score": 7.5,
            "fulfillment_score": 8.5,
            "prerequisites": []
        },
        {
            "name": "Volunteer Corps",
            "category": "Community Service",
            "description": "Organize community service projects, help local charities, and make a difference in the community.",
            "skills_developed": ["community service", "empathy", "organization", "leadership", "social awareness"],
            "time_commitment": "4-8 hours/week",
            "difficulty_level": 2,
            "social_impact_score": 9.5,
            "personal_growth_score": 8.0,
            "fulfillment_score": 8.5,
            "prerequisites": []
        },
        {
            "name": "Book Club",
            "category": "Academic",
            "description": "Read and discuss literature, explore different genres, and improve critical analysis skills.",
            "skills_developed": ["reading comprehension", "critical thinking", "discussion", "cultural literacy", "communication"],
            "time_commitment": "2-4 hours/week",
            "difficulty_level": 2,
            "social_impact_score": 5.0,
            "personal_growth_score": 7.5,
            "fulfillment_score": 7.5,
            "prerequisites": ["love of reading"]
        },
        {
            "name": "Anime & Manga Club",
            "category": "Cultural",
            "description": "Explore Japanese culture through anime and manga, host viewing parties, and create fan art.",
            "skills_developed": ["cultural awareness", "creativity", "discussion", "artistic skills", "event planning"],
            "time_commitment": "2-4 hours/week",
            "difficulty_level": 1,
            "social_impact_score": 4.5,
            "personal_growth_score": 6.0,
            "fulfillment_score": 8.5,
            "prerequisites": []
        },
        {
            "name": "Peer Tutoring Program",
            "category": "Academic",
            "description": "Help fellow students with academics, develop teaching skills, and build leadership through education.",
            "skills_developed": ["teaching", "patience", "communication", "leadership", "subject mastery"],
            "time_commitment": "3-6 hours/week",
            "difficulty_level": 3,
            "social_impact_score": 8.5,
            "personal_growth_score": 8.0,
            "fulfillment_score": 7.5,
            "prerequisites": ["strong academic performance"]
        },
        {
            "name": "Mental Health Awareness Club",
            "category": "Health & Wellness",
            "description": "Promote mental health awareness, organize wellness activities, and support student wellbeing.",
            "skills_developed": ["empathy", "communication", "health awareness", "event planning", "advocacy"],
            "time_commitment": "3-5 hours/week",
            "difficulty_level": 2,
            "social_impact_score": 9.0,
            "personal_growth_score": 7.5,
            "fulfillment_score": 8.0,
            "prerequisites": ["maturity and empathy"]
        },
        {
            "name": "Entrepreneurship Club",
            "category": "Business",
            "description": "Develop business ideas, learn entrepreneurship skills, and participate in business plan competitions.",
            "skills_developed": ["business planning", "innovation", "presentation", "financial literacy", "leadership"],
            "time_commitment": "4-7 hours/week",
            "difficulty_level": 3,
            "social_impact_score": 6.5,
            "personal_growth_score": 8.5,
            "fulfillment_score": 8.0,
            "prerequisites": ["interest in business"]
        },
        {
            "name": "Film & Video Production",
            "category": "Media",
            "description": "Create films, learn video editing, and produce content for school and community.",
            "skills_developed": ["video production", "storytelling", "technical skills", "creativity", "collaboration"],
            "time_commitment": "5-8 hours/week",
            "difficulty_level": 3,
            "social_impact_score": 6.5,
            "personal_growth_score": 8.0,
            "fulfillment_score": 9.0,
            "prerequisites": ["interest in media"]
        },
        {
            "name": "Outdoor Adventure Club",
            "category": "Sports",
            "description": "Organize hiking, camping, and outdoor activities while learning environmental stewardship.",
            "skills_developed": ["outdoor skills", "leadership", "environmental awareness", "physical fitness", "teamwork"],
            "time_commitment": "6-10 hours/week",
            "difficulty_level": 3,
            "social_impact_score": 7.0,
            "personal_growth_score": 8.5,
            "fulfillment_score": 9.0,
            "prerequisites": ["physical fitness"]
        },
        {
            "name": "Language Exchange Club",
            "category": "Language",
            "description": "Practice foreign languages, explore different cultures, and help international students.",
            "skills_developed": ["language skills", "cultural awareness", "communication", "empathy", "global perspective"],
            "time_commitment": "2-4 hours/week",
            "difficulty_level": 2,
            "social_impact_score": 7.5,
            "personal_growth_score": 8.0,
            "fulfillment_score": 7.5,
            "prerequisites": ["interest in languages"]
        },
        {
            "name": "3D Printing & Maker Club",
            "category": "STEM",
            "description": "Learn 3D design and printing, create prototypes, and explore digital fabrication technologies.",
            "skills_developed": ["3D modeling", "design thinking", "technology", "problem-solving", "innovation"],
            "time_commitment": "4-6 hours/week",
            "difficulty_level": 3,
            "social_impact_score": 5.5,
            "personal_growth_score": 8.0,
            "fulfillment_score": 8.5,
            "prerequisites": ["interest in technology"]
        }
    ]
    
    print(f"Adding {len(new_clubs)} new clubs to the database...")
    
    added_count = 0
    for club in new_clubs:
        try:
            # Check if club already exists
            existing_activities = db_manager.get_all_activities()
            if any(act['name'] == club['name'] for act in existing_activities):
                print(f"⚠️  Skipping '{club['name']}' - already exists")
                continue
                
            # Add to SQLite database
            activity_id = db_manager.add_activity(club)
            
            # Add to vector database
            activity_with_id = club.copy()
            activity_with_id['id'] = activity_id
            vector_db.add_activities([activity_with_id])
            
            print(f"✅ Added '{club['name']}' (ID: {activity_id})")
            added_count += 1
            
        except Exception as e:
            print(f"❌ Error adding '{club['name']}': {str(e)}")
    
    print(f"\n🎉 Successfully added {added_count} new clubs!")
    
    # Show final count
    final_activities = db_manager.get_all_activities()
    print(f"📊 Total activities in database: {len(final_activities)}")

if __name__ == "__main__":
    add_new_clubs()
