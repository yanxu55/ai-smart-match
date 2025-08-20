#!/usr/bin/env python3
"""
SmartMatch Batch Processor
Process multiple student profiles and generate recommendations in batch.
"""

import os
import sys
import json
import csv
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from database.smart_sqlite_db import SmartDatabaseManager
from database.smart_vector_db import SmartVectorDatabase
from agents.ai_agent import AIAgent
from agents.recommendation_engine import RecommendationEngine
from utils.data_loader import initialize_sample_data, validate_student_data
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SmartMatchBatchProcessor:
    """Batch processor for SmartMatch recommendations."""
    
    def __init__(self):
        """Initialize the batch processor."""
        # Initialize system components
        os.makedirs("data", exist_ok=True)
        os.makedirs("output", exist_ok=True)
        
        self.db_manager = SmartDatabaseManager("data/smartmatch.db")
        self.vector_db = SmartVectorDatabase("data/vector_db")
        self.ai_agent = AIAgent()
        self.recommendation_engine = RecommendationEngine(
            self.db_manager, self.vector_db, self.ai_agent
        )
        
        # Initialize sample data if needed
        activities = self.db_manager.get_all_activities()
        if len(activities) == 0:
            print("Initializing sample data...")
            initialize_sample_data(self.db_manager, self.vector_db)
    
    def process_students_from_json(self, json_file):
        """Process students from a JSON file."""
        print(f"Processing students from {json_file}...")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                students_data = json.load(f)
            
            results = []
            
            for i, student_data in enumerate(students_data, 1):
                print(f"\nProcessing student {i}/{len(students_data)}: {student_data.get('name', 'Unknown')}")
                
                # Validate student data
                errors = validate_student_data(student_data)
                if errors:
                    print(f"   ❌ Validation errors: {', '.join(errors)}")
                    continue
                
                try:
                    # Add student to database
                    student_id = self.db_manager.add_student(student_data)
                    student_data['id'] = student_id
                    
                    # Add to vector database
                    self.vector_db.add_student_profile(student_data)
                    
                    # Generate recommendations
                    recommendations = self.recommendation_engine.generate_recommendations(
                        student_id, n_recommendations=5
                    )
                    
                    # Get insights
                    insights = self.recommendation_engine.get_recommendation_insights(student_id)
                    
                    result = {
                        'student': student_data,
                        'recommendations': recommendations,
                        'insights': insights,
                        'processed_at': datetime.now().isoformat()
                    }
                    
                    results.append(result)
                    print(f"   ✅ Generated {len(recommendations)} recommendations")
                    
                except Exception as e:
                    print(f"   ❌ Error processing student: {str(e)}")
                    continue
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"output/batch_results_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Batch processing completed!")
            print(f"   Processed: {len(results)}/{len(students_data)} students")
            print(f"   Results saved to: {output_file}")
            
            # Generate summary report
            self.generate_summary_report(results, f"output/summary_{timestamp}.txt")
            
            return results
            
        except Exception as e:
            print(f"❌ Error processing batch: {str(e)}")
            return []
    
    def process_students_from_csv(self, csv_file):
        """Process students from a CSV file."""
        print(f"Processing students from {csv_file}...")
        
        try:
            students_data = []
            
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # Parse CSV row into student data
                    student_data = {
                        'name': row['name'],
                        'grade': int(row['grade']),
                        'interests': [item.strip() for item in row['interests'].split(',')],
                        'strengths': [item.strip() for item in row['strengths'].split(',')],
                        'values': [item.strip() for item in row['values'].split(',')],
                        'availability': {
                            'weekdays': row.get('weekday_hours', '2') + ' hours/day',
                            'weekends': row.get('weekend_hours', '4') + ' hours/day'
                        }
                    }
                    
                    students_data.append(student_data)
            
            # Process as JSON data
            return self.process_students_list(students_data)
            
        except Exception as e:
            print(f"❌ Error processing CSV: {str(e)}")
            return []
    
    def process_students_list(self, students_data):
        """Process a list of student data."""
        results = []
        
        for i, student_data in enumerate(students_data, 1):
            print(f"\nProcessing student {i}/{len(students_data)}: {student_data.get('name', 'Unknown')}")
            
            # Validate student data
            errors = validate_student_data(student_data)
            if errors:
                print(f"   ❌ Validation errors: {', '.join(errors)}")
                continue
            
            try:
                # Add student to database
                student_id = self.db_manager.add_student(student_data)
                student_data['id'] = student_id
                
                # Add to vector database
                self.vector_db.add_student_profile(student_data)
                
                # Generate recommendations
                recommendations = self.recommendation_engine.generate_recommendations(
                    student_id, n_recommendations=5
                )
                
                # Get insights
                insights = self.recommendation_engine.get_recommendation_insights(student_id)
                
                result = {
                    'student': student_data,
                    'recommendations': recommendations,
                    'insights': insights,
                    'processed_at': datetime.now().isoformat()
                }
                
                results.append(result)
                print(f"   ✅ Generated {len(recommendations)} recommendations")
                
            except Exception as e:
                print(f"   ❌ Error processing student: {str(e)}")
                continue
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output/batch_results_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Batch processing completed!")
        print(f"   Processed: {len(results)}/{len(students_data)} students")
        print(f"   Results saved to: {output_file}")
        
        # Generate summary report
        self.generate_summary_report(results, f"output/summary_{timestamp}.txt")
        
        return results
    
    def generate_summary_report(self, results, output_file):
        """Generate a summary report from batch results."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("SmartMatch Batch Processing Summary\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Processed: {len(results)} students\n")
                f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Overall statistics
                total_recommendations = sum(len(r['recommendations']) for r in results)
                f.write(f"Total recommendations generated: {total_recommendations}\n")
                f.write(f"Average recommendations per student: {total_recommendations/len(results):.1f}\n\n")
                
                # Grade distribution
                grades = {}
                for result in results:
                    grade = result['student']['grade']
                    grades[grade] = grades.get(grade, 0) + 1
                
                f.write("Grade Distribution:\n")
                for grade in sorted(grades.keys()):
                    f.write(f"   Grade {grade}: {grades[grade]} students\n")
                f.write("\n")
                
                # Top recommended activities
                activity_counts = {}
                for result in results:
                    for rec in result['recommendations']:
                        activity_name = rec['activity']['name']
                        activity_counts[activity_name] = activity_counts.get(activity_name, 0) + 1
                
                f.write("Top 10 Recommended Activities:\n")
                top_activities = sorted(activity_counts.items(), key=lambda x: x[1], reverse=True)[:10]
                for i, (activity, count) in enumerate(top_activities, 1):
                    f.write(f"   {i}. {activity}: {count} times\n")
                f.write("\n")
                
                # Individual student summaries
                f.write("Individual Student Summaries:\n")
                f.write("-" * 50 + "\n")
                
                for i, result in enumerate(results, 1):
                    student = result['student']
                    recommendations = result['recommendations']
                    
                    f.write(f"\n{i}. {student['name']} (Grade {student['grade']})\n")
                    f.write(f"   Interests: {', '.join(student['interests'])}\n")
                    f.write(f"   Top Recommendations:\n")
                    
                    for j, rec in enumerate(recommendations[:3], 1):
                        f.write(f"      {j}. {rec['activity']['name']} (Score: {rec['score']:.1f})\n")
            
            print(f"   Summary report saved to: {output_file}")
            
        except Exception as e:
            print(f"❌ Error generating summary report: {str(e)}")
    
    def create_sample_input_files(self):
        """Create sample input files for testing."""
        # Sample JSON file
        sample_students = [
            {
                "name": "Emma Wilson",
                "grade": 11,
                "interests": ["Environmental Science", "Photography", "Writing"],
                "strengths": ["Research", "Creativity", "Communication"],
                "values": ["Environmental Sustainability", "Artistic Expression", "Social Justice"]
            },
            {
                "name": "Marcus Chen",
                "grade": 10,
                "interests": ["Technology", "Mathematics", "Gaming"],
                "strengths": ["Problem Solving", "Logical Thinking", "Programming"],
                "values": ["Innovation", "Learning", "Achievement"]
            },
            {
                "name": "Sofia Rodriguez",
                "grade": 12,
                "interests": ["Community Service", "Languages", "Cultural Exchange"],
                "strengths": ["Leadership", "Empathy", "Communication"],
                "values": ["Social Justice", "Cultural Understanding", "Service to Others"]
            }
        ]
        
        # Save JSON sample
        with open("sample_students.json", 'w', encoding='utf-8') as f:
            json.dump(sample_students, f, indent=2, ensure_ascii=False)
        
        # Save CSV sample
        with open("sample_students.csv", 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'grade', 'interests', 'strengths', 'values', 'weekday_hours', 'weekend_hours'])
            
            for student in sample_students:
                writer.writerow([
                    student['name'],
                    student['grade'],
                    ', '.join(student['interests']),
                    ', '.join(student['strengths']),
                    ', '.join(student['values']),
                    '3',  # weekday_hours
                    '5'   # weekend_hours
                ])
        
        print("✅ Sample input files created:")
        print("   • sample_students.json")
        print("   • sample_students.csv")

def main():
    """Main function to run batch processing."""
    print("🎯 SmartMatch Batch Processor")
    print("=" * 40)
    
    processor = SmartMatchBatchProcessor()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        
        if input_file.endswith('.json'):
            processor.process_students_from_json(input_file)
        elif input_file.endswith('.csv'):
            processor.process_students_from_csv(input_file)
        else:
            print("❌ Unsupported file format. Use .json or .csv files.")
    
    else:
        print("Usage examples:")
        print("  python batch_processor.py sample_students.json")
        print("  python batch_processor.py sample_students.csv")
        print("\nCreating sample input files...")
        processor.create_sample_input_files()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Batch processing interrupted!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
