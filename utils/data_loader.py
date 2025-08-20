from database.smart_sqlite_db import SmartDatabaseManager
from database.smart_vector_db import SmartVectorDatabase
import json
import uuid

def initialize_sample_data(db_manager: SmartDatabaseManager, vector_db: SmartVectorDatabase):
    """Initialize the database with sample activities and student data."""
    
    # Sample activities data
    sample_activities = [
        {
            "name": "Student Government",
            "category": "Leadership",
            "description": "Participate in school governance, represent student body, and lead initiatives for school improvement.",
            "skills_developed": ["leadership", "public speaking", "communication", "problem-solving", "teamwork"],
            "time_commitment": "5-8 hours/week",
            "difficulty_level": 3,
            "social_impact_score": 8.5,
            "personal_growth_score": 8.0,
            "fulfillment_score": 7.5,
            "prerequisites": ["good academic standing"]
        },
        {
            "name": "Environmental Club",
            "category": "Community Service",
            "description": "Organize environmental awareness campaigns, clean-up drives, and sustainability projects.",
            "skills_developed": ["environmental awareness", "project management", "community engagement", "research"],
            "time_commitment": "3-5 hours/week",
            "difficulty_level": 2,
            "social_impact_score": 9.0,
            "personal_growth_score": 7.0,
            "fulfillment_score": 8.0,
            "prerequisites": []
        },
        {
            "name": "Debate Team",
            "category": "Academic",
            "description": "Develop critical thinking and public speaking skills through competitive debates on various topics.",
            "skills_developed": ["critical thinking", "public speaking", "research", "argumentation", "confidence"],
            "time_commitment": "6-10 hours/week",
            "difficulty_level": 4,
            "social_impact_score": 6.0,
            "personal_growth_score": 9.0,
            "fulfillment_score": 7.0,
            "prerequisites": ["strong academic performance"]
        },
        {
            "name": "Drama Club",
            "category": "Arts",
            "description": "Perform in school plays, develop acting skills, and explore creative expression through theater.",
            "skills_developed": ["creativity", "public speaking", "teamwork", "confidence", "artistic expression"],
            "time_commitment": "8-12 hours/week during productions",
            "difficulty_level": 3,
            "social_impact_score": 7.0,
            "personal_growth_score": 8.5,
            "fulfillment_score": 9.0,
            "prerequisites": []
        },
        {
            "name": "Varsity Basketball",
            "category": "Sports",
            "description": "Compete at the highest level in basketball, representing the school in tournaments and leagues.",
            "skills_developed": ["teamwork", "physical fitness", "discipline", "leadership", "competitive spirit"],
            "time_commitment": "15-20 hours/week",
            "difficulty_level": 5,
            "social_impact_score": 6.5,
            "personal_growth_score": 8.0,
            "fulfillment_score": 8.5,
            "prerequisites": ["athletic ability", "tryout required"]
        },
        {
            "name": "Volunteer Tutoring",
            "category": "Community Service",
            "description": "Tutor younger students or peers in various subjects, helping them improve academically.",
            "skills_developed": ["teaching", "patience", "communication", "subject expertise", "mentoring"],
            "time_commitment": "2-4 hours/week",
            "difficulty_level": 2,
            "social_impact_score": 9.5,
            "personal_growth_score": 7.5,
            "fulfillment_score": 8.0,
            "prerequisites": ["good grades in subject areas"]
        },
        {
            "name": "Robotics Club",
            "category": "STEM",
            "description": "Design, build, and program robots for competitions while learning engineering principles.",
            "skills_developed": ["engineering", "programming", "problem-solving", "teamwork", "innovation"],
            "time_commitment": "8-15 hours/week",
            "difficulty_level": 4,
            "social_impact_score": 6.0,
            "personal_growth_score": 9.5,
            "fulfillment_score": 8.5,
            "prerequisites": ["interest in technology"]
        },
        {
            "name": "School Newspaper",
            "category": "Media",
            "description": "Write articles, conduct interviews, and produce the school newspaper to inform the community.",
            "skills_developed": ["writing", "journalism", "research", "communication", "creativity"],
            "time_commitment": "4-6 hours/week",
            "difficulty_level": 3,
            "social_impact_score": 7.5,
            "personal_growth_score": 8.0,
            "fulfillment_score": 7.5,
            "prerequisites": ["good writing skills"]
        },
        {
            "name": "Music Band",
            "category": "Arts",
            "description": "Perform in school concerts and competitions as part of the marching or concert band.",
            "skills_developed": ["musical skills", "teamwork", "discipline", "performance", "creativity"],
            "time_commitment": "6-10 hours/week",
            "difficulty_level": 3,
            "social_impact_score": 7.0,
            "personal_growth_score": 8.0,
            "fulfillment_score": 9.0,
            "prerequisites": ["musical instrument proficiency"]
        },
        {
            "name": "Science Olympiad",
            "category": "Academic",
            "description": "Compete in various science events, from biology to engineering, in team-based competitions.",
            "skills_developed": ["scientific knowledge", "problem-solving", "teamwork", "research", "competition"],
            "time_commitment": "5-8 hours/week",
            "difficulty_level": 4,
            "social_impact_score": 6.0,
            "personal_growth_score": 9.0,
            "fulfillment_score": 7.5,
            "prerequisites": ["strong science grades"]
        },
        {
            "name": "Red Cross Club",
            "category": "Community Service",
            "description": "Organize blood drives, disaster relief efforts, and health awareness campaigns.",
            "skills_developed": ["community service", "health awareness", "organization", "empathy", "leadership"],
            "time_commitment": "3-5 hours/week",
            "difficulty_level": 2,
            "social_impact_score": 9.5,
            "personal_growth_score": 7.0,
            "fulfillment_score": 8.5,
            "prerequisites": []
        },
        {
            "name": "Computer Programming Club",
            "category": "STEM",
            "description": "Learn programming languages, develop apps, and participate in coding competitions.",
            "skills_developed": ["programming", "logical thinking", "creativity", "problem-solving", "technology"],
            "time_commitment": "4-7 hours/week",
            "difficulty_level": 3,
            "social_impact_score": 5.5,
            "personal_growth_score": 9.0,
            "fulfillment_score": 8.0,
            "prerequisites": ["basic computer skills"]
        },
        {
            "name": "Art Club",
            "category": "Arts",
            "description": "Explore various art mediums, create artwork for school displays, and participate in art shows.",
            "skills_developed": ["creativity", "artistic skills", "visual communication", "patience", "self-expression"],
            "time_commitment": "3-6 hours/week",
            "difficulty_level": 2,
            "social_impact_score": 6.5,
            "personal_growth_score": 8.0,
            "fulfillment_score": 9.5,
            "prerequisites": []
        },
        {
            "name": "Model United Nations",
            "category": "Academic",
            "description": "Simulate UN conferences, debate global issues, and develop diplomatic and negotiation skills.",
            "skills_developed": ["diplomacy", "research", "public speaking", "global awareness", "negotiation"],
            "time_commitment": "5-8 hours/week",
            "difficulty_level": 4,
            "social_impact_score": 8.0,
            "personal_growth_score": 8.5,
            "fulfillment_score": 7.0,
            "prerequisites": ["strong academic performance"]
        },
        {
            "name": "Chess Club",
            "category": "Games & Strategy",
            "description": "Improve chess skills, participate in tournaments, and develop strategic thinking abilities.",
            "skills_developed": ["strategic thinking", "patience", "concentration", "problem-solving", "competition"],
            "time_commitment": "2-4 hours/week",
            "difficulty_level": 2,
            "social_impact_score": 5.0,
            "personal_growth_score": 7.5,
            "fulfillment_score": 7.0,
            "prerequisites": ["basic chess knowledge"]
        }
    ]
    
    # Create activities in database
    activity_ids = []
    for activity_data in sample_activities:
        activity_id = db_manager.add_activity(activity_data)
        activity_ids.append(activity_id)
        print(f"Created activity: {activity_data['name']}")
    
    # Add activities to vector database
    all_activities = db_manager.get_all_activities()
    vector_db.add_activities(all_activities)
    print(f"Added {len(all_activities)} activities to vector database")
    
    # Sample student profiles for testing
    sample_students = [
        {
            "name": "Alex Johnson",
            "grade": 11,
            "interests": ["technology", "problem-solving", "innovation", "competition"],
            "strengths": ["analytical thinking", "programming", "mathematics", "logical reasoning"],
            "values": ["learning", "innovation", "teamwork", "achievement"],
            "availability": {"weekdays": "3-4 hours", "weekends": "6-8 hours"}
        },
        {
            "name": "Maria Garcia",
            "grade": 10,
            "interests": ["helping others", "community service", "environmental issues", "health"],
            "strengths": ["empathy", "communication", "organization", "leadership"],
            "values": ["helping others", "environmental protection", "social justice", "community"],
            "availability": {"weekdays": "2-3 hours", "weekends": "4-6 hours"}
        },
        {
            "name": "David Chen",
            "grade": 12,
            "interests": ["arts", "creativity", "performance", "music"],
            "strengths": ["creativity", "artistic ability", "public speaking", "collaboration"],
            "values": ["self-expression", "creativity", "beauty", "collaboration"],
            "availability": {"weekdays": "4-5 hours", "weekends": "8-10 hours"}
        }
    ]
    
    # Create sample students
    for student_data in sample_students:
        student_id = db_manager.add_student(student_data)
        student_data['id'] = student_id
        vector_db.add_student_profile(student_data)
        print(f"Created student: {student_data['name']}")
    
    print("Sample data initialization complete!")

def get_sample_interests():
    """Get list of sample interests for the UI."""
    return [
        "technology", "arts", "sports", "music", "science", "mathematics",
        "writing", "reading", "community service", "environment", "politics",
        "business", "entrepreneurship", "health", "fitness", "cooking",
        "travel", "languages", "history", "psychology", "philosophy",
        "photography", "gaming", "fashion", "dance", "theater"
    ]

def get_sample_strengths():
    """Get list of sample strengths for the UI."""
    return [
        "leadership", "communication", "creativity", "analytical thinking",
        "problem-solving", "teamwork", "organization", "public speaking",
        "empathy", "patience", "discipline", "perseverance", "adaptability",
        "critical thinking", "artistic ability", "athletic ability",
        "mathematical skills", "writing skills", "research skills",
        "technical skills", "social skills", "time management"
    ]

def get_sample_values():
    """Get list of sample values for the UI."""
    return [
        "helping others", "learning", "creativity", "achievement", "independence",
        "teamwork", "leadership", "innovation", "tradition", "adventure",
        "security", "freedom", "justice", "beauty", "truth", "family",
        "friendship", "respect", "honesty", "responsibility", "excellence",
        "diversity", "sustainability", "community", "personal growth"
    ]

def validate_student_data(student_data):
    """Validate student data before saving."""
    errors = []
    
    if not student_data.get('name', '').strip():
        errors.append("Name is required")
    
    if not student_data.get('grade') or student_data['grade'] < 9 or student_data['grade'] > 12:
        errors.append("Grade must be between 9 and 12")
    
    if not student_data.get('interests'):
        errors.append("At least one interest is required")
    
    if not student_data.get('strengths'):
        errors.append("At least one strength is required")
    
    if not student_data.get('values'):
        errors.append("At least one value is required")
    
    return errors
