"""
Setup script for SmartMatch AI system
Run this script to initialize the system with sample data
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from database.db_manager import DatabaseManager
from database.vector_db import VectorDatabase
from utils.data_loader import initialize_sample_data

def setup_system():
    """Setup the SmartMatch system with initial data."""
    print("🎯 Setting up SmartMatch AI System...")
    
    # Create data directory
    os.makedirs("data", exist_ok=True)
    print("✅ Created data directory")
    
    # Initialize databases
    print("📦 Initializing databases...")
    db_manager = DatabaseManager("data/smartmatch.db")
    vector_db = VectorDatabase("data/chroma_db")
    print("✅ Databases initialized")
    
    # Check if sample data already exists
    activities = db_manager.get_all_activities()
    
    if len(activities) > 0:
        print(f"📚 Found {len(activities)} existing activities in database")
        choice = input("Do you want to reset and reload sample data? (y/N): ")
        if choice.lower() != 'y':
            print("✅ Setup complete - using existing data")
            return
    
    # Initialize sample data
    print("🔄 Loading sample data...")
    initialize_sample_data(db_manager, vector_db)
    print("✅ Sample data loaded successfully")
    
    # Verify setup
    activities = db_manager.get_all_activities()
    print(f"📊 Setup complete! Loaded {len(activities)} activities")
    
    print("\n🎉 SmartMatch is ready to use!")
    print("Run 'streamlit run app.py' to start the application")

if __name__ == "__main__":
    setup_system()
