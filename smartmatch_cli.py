#!/usr/bin/env python3
"""
SmartMatch Command Line Interface
Run the AI extracurricular recommendation system without Streamlit UI.
"""

import os
import sys
from pathlib import Path
import json

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from database.smart_sqlite_db import SmartDatabaseManager
from database.smart_vector_db import SmartVectorDatabase
from agents.ai_agent import AIAgent
from agents.recommendation_engine import RecommendationEngine
from utils.data_loader import (
    initialize_sample_data, get_sample_interests, get_sample_strengths,
    get_sample_values, validate_student_data
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SmartMatchCLI:
    """Command line interface for SmartMatch system."""
    
    def __init__(self):
        """Initialize the SmartMatch CLI."""
        print("🎯 SmartMatch - AI Extracurricular Recommender")
        print("=" * 50)
        
        # Initialize system components
        self.initialize_system()
        
    def initialize_system(self):
        """Initialize the SmartMatch system components."""
        print("Initializing system...")
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        try:
            # Initialize components
            self.db_manager = SmartDatabaseManager("data/smartmatch.db")
            self.vector_db = SmartVectorDatabase("data/vector_db")
            self.ai_agent = AIAgent()
            self.recommendation_engine = RecommendationEngine(
                self.db_manager, self.vector_db, self.ai_agent
            )
            
            # Check if we need to initialize sample data
            activities = self.db_manager.get_all_activities()
            if len(activities) == 0:
                print("No activities found. Initializing sample data...")
                initialize_sample_data(self.db_manager, self.vector_db)
                print("✅ Sample data initialized successfully!")
            else:
                print(f"✅ Found {len(activities)} activities in database")
            
            # Show AI configuration
            model_info = self.ai_agent.get_model_info()
            print(f"✅ AI Provider: {model_info['provider']}")
            print(f"   Model: {model_info['model']}")
            
            print("✅ System initialized successfully!")
            print()
            
        except Exception as e:
            print(f"❌ Error initializing system: {str(e)}")
            print("Please check your .env file configuration.")
            sys.exit(1)
    
    def run(self):
        """Run the CLI interface."""
        while True:
            self.show_menu()
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                self.create_student_profile()
            elif choice == '2':
                self.show_students()
            elif choice == '3':
                self.generate_recommendations()
            elif choice == '4':
                self.show_activities()
            elif choice == '5':
                self.add_new_activity()
            elif choice == '6':
                self.show_analytics()
            elif choice == '7':
                print("👋 Thank you for using SmartMatch!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
    
    def show_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 50)
        print("📋 SmartMatch Main Menu")
        print("=" * 50)
        print("1. Create Student Profile")
        print("2. View Students")
        print("3. Generate Recommendations")
        print("4. Browse Activities")
        print("5. Add New Activity")
        print("6. Show Analytics")
        print("7. Exit")
        print()
    
    def create_student_profile(self):
        """Create a new student profile."""
        print("\n📝 Create Student Profile")
        print("-" * 30)
        
        # Basic information
        name = input("Full Name: ").strip()
        if not name:
            print("❌ Name is required!")
            return
        
        try:
            grade = int(input("Grade (9-12): ").strip())
            if grade not in [9, 10, 11, 12]:
                print("❌ Grade must be between 9 and 12!")
                return
        except ValueError:
            print("❌ Invalid grade. Please enter a number between 9 and 12.")
            return
        
        # Interests
        print("\n🎯 Select Interests")
        print("Available interests:", ", ".join(get_sample_interests()))
        interests_input = input("Enter interests (comma-separated): ").strip()
        interests = [interest.strip() for interest in interests_input.split(",") if interest.strip()]
        
        # Strengths
        print("\n💪 Select Strengths")
        print("Available strengths:", ", ".join(get_sample_strengths()))
        strengths_input = input("Enter strengths (comma-separated): ").strip()
        strengths = [strength.strip() for strength in strengths_input.split(",") if strength.strip()]
        
        # Values
        print("\n❤️ Select Values")
        print("Available values:", ", ".join(get_sample_values()))
        values_input = input("Enter values (comma-separated): ").strip()
        values = [value.strip() for value in values_input.split(",") if value.strip()]
        
        # Availability
        try:
            weekday_hours = int(input("\nWeekday availability (hours/day, 0-8): ").strip())
            weekend_hours = int(input("Weekend availability (hours/day, 0-12): ").strip())
        except ValueError:
            weekday_hours, weekend_hours = 2, 4
            print("Using default availability: 2 weekday hours, 4 weekend hours")
        
        # Prepare student data
        student_data = {
            "name": name,
            "grade": grade,
            "interests": interests,
            "strengths": strengths,
            "values": values,
            "availability": {
                "weekdays": f"{weekday_hours} hours/day",
                "weekends": f"{weekend_hours} hours/day"
            }
        }
        
        # Validate data
        errors = validate_student_data(student_data)
        if errors:
            print("\n❌ Validation errors:")
            for error in errors:
                print(f"   • {error}")
            return
        
        try:
            # Create student profile
            student_id = self.db_manager.add_student(student_data)
            student_data['id'] = student_id
            
            # Add to vector database
            self.vector_db.add_student_profile(student_data)
            
            print(f"\n✅ Profile created successfully!")
            print(f"   Student ID: {student_id}")
            print(f"   Name: {name}")
            print(f"   Grade: {grade}")
            print(f"   Interests: {', '.join(interests)}")
            print(f"   Strengths: {', '.join(strengths)}")
            print(f"   Values: {', '.join(values)}")
            
        except Exception as e:
            print(f"❌ Error creating profile: {str(e)}")
    
    def show_students(self):
        """Show all students in the database."""
        print("\n👥 Student Database")
        print("-" * 30)
        
        try:
            students = self.db_manager.get_all_students()
            
            if not students:
                print("No students found in the database.")
                return
            
            for i, student in enumerate(students, 1):
                print(f"\n{i}. {student['name']} (Grade {student['grade']})")
                print(f"   ID: {student['id']}")
                print(f"   Interests: {', '.join(student['interests'][:3])}...")
                print(f"   Created: {student['created_at']}")
            
            print(f"\nTotal students: {len(students)}")
            
        except Exception as e:
            print(f"❌ Error fetching students: {str(e)}")
    
    def generate_recommendations(self):
        """Generate recommendations for a student."""
        print("\n🎯 Generate Recommendations")
        print("-" * 30)
        
        # Get student ID
        student_id = input("Enter student ID: ").strip()
        if not student_id:
            print("❌ Student ID is required!")
            return
        
        try:
            # Check if student exists
            student = self.db_manager.get_student(student_id)
            if not student:
                print("❌ Student not found!")
                return
            
            print(f"\nGenerating recommendations for {student['name']}...")
            
            # Get number of recommendations
            try:
                num_recs = int(input("Number of recommendations (default 3): ").strip() or "3")
            except ValueError:
                num_recs = 3
            
            # Generate recommendations
            recommendations = self.recommendation_engine.generate_recommendations(
                student_id, n_recommendations=num_recs
            )
            
            if recommendations:
                print(f"\n✅ Generated {len(recommendations)} recommendations!")
                print("\n" + "=" * 60)
                
                for i, rec in enumerate(recommendations, 1):
                    activity = rec['activity']
                    score = rec['score']
                    reasoning = rec.get('reasoning', 'No reasoning provided')
                    
                    print(f"\n{i}. {activity['name']} (Score: {score:.1f}/10)")
                    print(f"   Category: {activity['category']}")
                    print(f"   Description: {activity.get('description', 'No description')}")
                    print(f"   Time: {activity.get('time_commitment', 'N/A')}")
                    print(f"   Difficulty: {activity.get('difficulty_level', 1)}/5")
                    print(f"   Why recommended: {reasoning}")
                    
                    # Scores
                    print(f"   Growth: {activity.get('personal_growth_score', 0):.1f} | "
                          f"Impact: {activity.get('social_impact_score', 0):.1f} | "
                          f"Fulfillment: {activity.get('fulfillment_score', 0):.1f}")
                    
                    if i < len(recommendations):
                        print("-" * 60)
                
                # Save to file option
                save = input("\nSave recommendations to file? (y/n): ").strip().lower()
                if save == 'y':
                    filename = f"recommendations_{student['name'].replace(' ', '_')}.txt"
                    self.save_recommendations_to_file(recommendations, student, filename)
                    print(f"✅ Recommendations saved to {filename}")
            
            else:
                print("❌ No recommendations generated.")
                
        except Exception as e:
            print(f"❌ Error generating recommendations: {str(e)}")
    
    def show_activities(self):
        """Show all activities in the database."""
        print("\n📚 Activity Database")
        print("-" * 30)
        
        try:
            activities = self.db_manager.get_all_activities()
            
            if not activities:
                print("No activities found in the database.")
                return
            
            # Group by category
            categories = {}
            for activity in activities:
                cat = activity['category']
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(activity)
            
            for category, acts in categories.items():
                print(f"\n📂 {category} ({len(acts)} activities)")
                print("-" * 40)
                
                for activity in acts:
                    print(f"• {activity['name']}")
                    print(f"  Difficulty: {activity.get('difficulty_level', 1)}/5 | "
                          f"Growth: {activity.get('personal_growth_score', 0):.1f} | "
                          f"Impact: {activity.get('social_impact_score', 0):.1f}")
            
            print(f"\nTotal activities: {len(activities)}")
            
        except Exception as e:
            print(f"❌ Error fetching activities: {str(e)}")
    
    def show_analytics(self):
        """Show system analytics."""
        print("\n📊 System Analytics")
        print("-" * 30)
        
        try:
            activities = self.db_manager.get_all_activities()
            students = self.db_manager.get_all_students()
            
            print(f"📚 Total Activities: {len(activities)}")
            print(f"👥 Total Students: {len(students)}")
            
            if activities:
                # Category distribution
                categories = {}
                for activity in activities:
                    cat = activity['category']
                    categories[cat] = categories.get(cat, 0) + 1
                
                print(f"\n📂 Categories:")
                for cat, count in sorted(categories.items()):
                    print(f"   • {cat}: {count} activities")
                
                # Score averages
                avg_growth = sum(a.get('personal_growth_score', 0) for a in activities) / len(activities)
                avg_impact = sum(a.get('social_impact_score', 0) for a in activities) / len(activities)
                avg_fulfillment = sum(a.get('fulfillment_score', 0) for a in activities) / len(activities)
                
                print(f"\n📈 Average Scores:")
                print(f"   • Personal Growth: {avg_growth:.1f}/10")
                print(f"   • Social Impact: {avg_impact:.1f}/10")
                print(f"   • Fulfillment: {avg_fulfillment:.1f}/10")
                
                # Top activities by score
                top_activities = sorted(activities, 
                                      key=lambda x: (x.get('personal_growth_score', 0) + 
                                                   x.get('social_impact_score', 0) + 
                                                   x.get('fulfillment_score', 0)) / 3, 
                                      reverse=True)[:5]
                
                print(f"\n🏆 Top 5 Activities (by average score):")
                for i, activity in enumerate(top_activities, 1):
                    avg_score = (activity.get('personal_growth_score', 0) + 
                               activity.get('social_impact_score', 0) + 
                               activity.get('fulfillment_score', 0)) / 3
                    print(f"   {i}. {activity['name']} - {avg_score:.1f}/10")
            
            # Vector database stats
            vector_stats = self.vector_db.get_stats()
            print(f"\n🔍 Vector Database:")
            print(f"   • Embedding dimension: {vector_stats['embedding_dimension']}")
            print(f"   • Indexed activities: {vector_stats['total_activities']}")
            print(f"   • Indexed students: {vector_stats['total_student_profiles']}")
            
        except Exception as e:
            print(f"❌ Error generating analytics: {str(e)}")
    
    def add_new_activity(self):
        """Add a new extracurricular activity."""
        print("\n➕ Add New Extracurricular Activity")
        print("-" * 40)
        
        # Basic information
        name = input("Activity Name: ").strip()
        if not name:
            print("❌ Activity name is required!")
            return
        
        print("\nAvailable categories:")
        categories = ["Academic", "STEM", "Arts", "Sports", "Leadership", 
                     "Community Service", "Media", "Music", "Technology", 
                     "Business", "Language", "Other"]
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            cat_choice = int(input(f"\nChoose category (1-{len(categories)}): ").strip())
            if 1 <= cat_choice <= len(categories):
                category = categories[cat_choice - 1]
            else:
                category = "Other"
                print("Invalid choice, using 'Other'")
        except ValueError:
            category = "Other"
            print("Invalid input, using 'Other'")
        
        description = input("\nDescription: ").strip()
        if not description:
            print("❌ Description is required!")
            return
        
        skills_input = input("Skills developed (comma-separated): ").strip()
        if not skills_input:
            print("❌ At least one skill is required!")
            return
        
        skills_list = [skill.strip() for skill in skills_input.split(",") if skill.strip()]
        
        # Optional fields
        time_commitments = ["1-2 hours/week", "3-4 hours/week", "5-6 hours/week", 
                          "7-10 hours/week", "10+ hours/week"]
        print(f"\nTime commitment options:")
        for i, tc in enumerate(time_commitments, 1):
            print(f"   {i}. {tc}")
        
        try:
            tc_choice = int(input(f"Choose time commitment (1-{len(time_commitments)}): ").strip())
            if 1 <= tc_choice <= len(time_commitments):
                time_commitment = time_commitments[tc_choice - 1]
            else:
                time_commitment = "3-4 hours/week"
        except ValueError:
            time_commitment = "3-4 hours/week"
        
        try:
            difficulty = int(input("Difficulty level (1-5): ").strip())
            if not 1 <= difficulty <= 5:
                difficulty = 3
        except ValueError:
            difficulty = 3
        
        try:
            personal_growth = float(input("Personal Growth Score (1-10): ").strip())
            if not 1 <= personal_growth <= 10:
                personal_growth = 7.0
        except ValueError:
            personal_growth = 7.0
        
        try:
            social_impact = float(input("Social Impact Score (1-10): ").strip())
            if not 1 <= social_impact <= 10:
                social_impact = 6.0
        except ValueError:
            social_impact = 6.0
        
        try:
            fulfillment = float(input("Fulfillment Score (1-10): ").strip())
            if not 1 <= fulfillment <= 10:
                fulfillment = 7.0
        except ValueError:
            fulfillment = 7.0
        
        prerequisites_input = input("Prerequisites (comma-separated, press Enter if none): ").strip()
        prerequisites_list = [prereq.strip() for prereq in prerequisites_input.split(",") if prereq.strip()] if prerequisites_input else []
        
        # Prepare activity data
        activity_data = {
            "name": name,
            "category": category,
            "description": description,
            "skills_developed": skills_list,
            "time_commitment": time_commitment,
            "difficulty_level": difficulty,
            "personal_growth_score": personal_growth,
            "social_impact_score": social_impact,
            "fulfillment_score": fulfillment,
            "prerequisites": prerequisites_list
        }
        
        try:
            # Add activity to database
            activity_id = self.db_manager.add_activity(activity_data)
            activity_data['id'] = activity_id
            
            # Add to vector database
            self.vector_db.add_activities([activity_data])
            
            print(f"\n✅ Activity '{name}' added successfully!")
            print(f"   Activity ID: {activity_id}")
            print(f"   Category: {category}")
            print(f"   Skills: {', '.join(skills_list)}")
            print(f"   Scores: Growth={personal_growth:.1f}, Impact={social_impact:.1f}, Fulfillment={fulfillment:.1f}")
            
        except Exception as e:
            print(f"❌ Error adding activity: {str(e)}")
    
    def save_recommendations_to_file(self, recommendations, student, filename):
        """Save recommendations to a text file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"SmartMatch Recommendations for {student['name']}\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Student Profile:\n")
                f.write(f"• Name: {student['name']}\n")
                f.write(f"• Grade: {student['grade']}\n")
                f.write(f"• Interests: {', '.join(student['interests'])}\n")
                f.write(f"• Strengths: {', '.join(student['strengths'])}\n")
                f.write(f"• Values: {', '.join(student['values'])}\n\n")
                
                f.write(f"Recommendations ({len(recommendations)} activities):\n")
                f.write("-" * 50 + "\n\n")
                
                for i, rec in enumerate(recommendations, 1):
                    activity = rec['activity']
                    score = rec['score']
                    reasoning = rec.get('reasoning', 'No reasoning provided')
                    
                    f.write(f"{i}. {activity['name']} (Score: {score:.1f}/10)\n")
                    f.write(f"   Category: {activity['category']}\n")
                    f.write(f"   Description: {activity.get('description', 'No description')}\n")
                    f.write(f"   Time Commitment: {activity.get('time_commitment', 'N/A')}\n")
                    f.write(f"   Difficulty Level: {activity.get('difficulty_level', 1)}/5\n")
                    f.write(f"   Personal Growth: {activity.get('personal_growth_score', 0):.1f}/10\n")
                    f.write(f"   Social Impact: {activity.get('social_impact_score', 0):.1f}/10\n")
                    f.write(f"   Fulfillment: {activity.get('fulfillment_score', 0):.1f}/10\n")
                    f.write(f"   Why Recommended: {reasoning}\n\n")
                    
        except Exception as e:
            print(f"❌ Error saving file: {str(e)}")

def main():
    """Main function to run the CLI."""
    try:
        cli = SmartMatchCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
