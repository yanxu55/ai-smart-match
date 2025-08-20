"""
Configuration settings for SmartMatch AI system
"""

# Database settings
DATABASE_PATH = "data/smartmatch.db"
VECTOR_DB_PATH = "data/chroma_db"

# AI Model settings
OPENAI_MODEL = "gpt-4"
EMBEDDING_MODEL = "text-embedding-ada-002"

# Recommendation engine settings
DEFAULT_RECOMMENDATIONS_COUNT = 8
MAX_RECOMMENDATIONS_COUNT = 15

# Scoring weights for recommendation algorithm
SCORING_WEIGHTS = {
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

# UI settings
STREAMLIT_CONFIG = {
    'page_title': "SmartMatch - AI Extracurricular Recommender",
    'page_icon': "🎯",
    'layout': "wide",
    'initial_sidebar_state': "expanded"
}

# Grade levels supported
SUPPORTED_GRADES = [9, 10, 11, 12]

# Activity difficulty levels
DIFFICULTY_LEVELS = {
    1: "Beginner",
    2: "Easy",
    3: "Moderate",
    4: "Challenging",
    5: "Advanced"
}

# Activity categories
ACTIVITY_CATEGORIES = [
    "Academic",
    "Arts",
    "Community Service",
    "Games & Strategy",
    "Leadership",
    "Media",
    "Sports",
    "STEM",
    "Other"
]
