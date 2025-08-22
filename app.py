import streamlit as st
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from database.smart_sqlite_db import SmartDatabaseManager

# Try to import vector database, but handle gracefully if dependencies are missing
try:
    from database.smart_vector_db import SmartVectorDatabase
    VECTOR_DB_AVAILABLE = True
except ImportError as e:
    VECTOR_DB_AVAILABLE = False
    VECTOR_DB_ERROR = str(e)

from agents.ai_agent import AIAgent
from agents.recommendation_engine import RecommendationEngine
from utils.visualization import (
    create_impact_dashboard, format_recommendation_card,
    display_student_insights, export_recommendations_to_csv,
    create_score_breakdown_chart, create_development_pathway_chart
)
from utils.data_loader import (
    initialize_sample_data, get_sample_interests, get_sample_strengths,
    get_sample_values, validate_student_data
)
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="SmartMatch - AI Extracurricular Recommender",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .recommendation-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
        background-color: #fafafa;
    }
    
    /* Make primary buttons blue except for Stop App button */
    .stButton > button[kind="primary"] {
        background-color: #0066cc !important;
        border-color: #0066cc !important;
        color: white !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #0052a3 !important;
        border-color: #0052a3 !important;
        color: white !important;
    }
    
    /* Keep Stop App button as secondary/gray */
    div[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        background-color: #f0f2f6 !important;
        border-color: #d0d0d0 !important;
        color: #333 !important;
    }
    
    /* Form submit buttons should also be blue */
    .stFormSubmitButton > button {
        background-color: #0066cc !important;
        border-color: #0066cc !important;
        color: white !important;
    }
    
    .stFormSubmitButton > button:hover {
        background-color: #0052a3 !important;
        border-color: #0052a3 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.current_student_id = None
    st.session_state.students = {}

# Initialize databases and agents
@st.cache_resource
def initialize_system():
    """Initialize the SmartMatch system components."""
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Initialize components
    db_manager = SmartDatabaseManager("data/smartmatch.db")
    vector_db = SmartVectorDatabase("data/vector_db")
    ai_agent = AIAgent()
    recommendation_engine = RecommendationEngine(db_manager, vector_db, ai_agent)
    
    return db_manager, vector_db, ai_agent, recommendation_engine

try:
    db_manager, vector_db, ai_agent, recommendation_engine = initialize_system()
    
    # Check if we need to initialize sample data
    if not st.session_state.initialized:
        activities = db_manager.get_all_activities()
        if len(activities) == 0:
            with st.spinner("Initializing sample data..."):
                initialize_sample_data(db_manager, vector_db)
        else:
            # Ensure vector database is populated even if SQLite has data
            if vector_db.activities_index.ntotal == 0 and len(activities) > 0:
                with st.spinner("Indexing activities for recommendations..."):
                    vector_db.add_activities(activities)
                    st.success(f"Indexed {len(activities)} activities for better recommendations!")
        st.session_state.initialized = True
        
except Exception as e:
    st.error(f"Error initializing system: {str(e)}")
    st.info("Please check your OpenAI API key in the .env file and ensure all dependencies are installed.")
    st.stop()

def main():
    """Main application function."""
    
    # Header
    st.markdown('<div class="main-header">🎯 SmartMatch</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Extracurricular Activity Recommender</div>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Student Profile", "Get Recommendations", "Student Directory", "Activity Database", "Add New Activity", "Analytics Dashboard"]
    )
    
    # Add stop app button
    st.sidebar.markdown("---")
    st.sidebar.markdown("### App Control")
    if st.sidebar.button("🛑 Stop App", type="secondary", help="Click to stop the Streamlit application"):
        st.sidebar.error("Shutting down application...")
        st.sidebar.markdown("Please close this browser tab.")
        # Force exit the entire application
        os._exit(0)
    
    if page == "Student Profile":
        show_student_profile_page()
    elif page == "Get Recommendations":
        show_recommendations_page()
    elif page == "Student Directory":
        show_student_directory_page()
    elif page == "Activity Database":
        show_activity_database_page()
    elif page == "Add New Activity":
        show_add_activity_page()
    elif page == "Analytics Dashboard":
        show_analytics_dashboard_page()

def show_student_profile_page():
    """Show the student profile creation/editing page."""
    st.header("📝 Student Profile")
    
    # Option to load existing student or create new
    profile_option = st.radio(
        "Choose an option:",
        ["Create New Profile", "Load Existing Profile"]
    )
    
    if profile_option == "Create New Profile":
        create_student_profile()
    else:
        load_existing_profile()

def create_student_profile():
    """Create a new student profile."""
    st.subheader("Create Your Profile")
    
    with st.form("student_profile_form"):
        # Basic information
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*", placeholder="Enter your full name")
            grade = st.selectbox("Grade*", [9, 10, 11, 12])
        
        with col2:
            st.write("**Availability**")
            weekday_hours = st.slider("Weekday availability (hours/day)", 0, 8, 2)
            weekend_hours = st.slider("Weekend availability (hours/day)", 0, 12, 4)
        
        # Interests
        st.subheader("Interests")
        st.write("Select your interests (choose multiple):")
        
        sample_interests = sorted(get_sample_interests())
        selected_interests = []
        
        # Create columns for interests
        cols = st.columns(4)
        for i, interest in enumerate(sample_interests):
            with cols[i % 4]:
                if st.checkbox(interest, key=f"interest_{interest}"):
                    selected_interests.append(interest)
        
        # Custom interests
        custom_interests = st.text_input(
            "Additional interests (comma-separated)",
            placeholder="Enter any other interests not listed above"
        )
        
        if custom_interests:
            custom_list = [interest.strip() for interest in custom_interests.split(",")]
            selected_interests.extend(custom_list)
        
        # Strengths
        st.subheader("Strengths")
        st.write("Select your strengths (choose multiple):")
        
        sample_strengths = sorted(get_sample_strengths())
        selected_strengths = []
        
        cols = st.columns(4)
        for i, strength in enumerate(sample_strengths):
            with cols[i % 4]:
                if st.checkbox(strength, key=f"strength_{strength}"):
                    selected_strengths.append(strength)
        
        # Custom strengths
        custom_strengths = st.text_input(
            "Additional strengths (comma-separated)",
            placeholder="Enter any other strengths not listed above"
        )
        
        if custom_strengths:
            custom_list = [strength.strip() for strength in custom_strengths.split(",")]
            selected_strengths.extend(custom_list)
        
        # Values
        st.subheader("Values")
        st.write("Select your core values (choose multiple):")
        
        sample_values = sorted(get_sample_values())
        selected_values = []
        
        cols = st.columns(4)
        for i, value in enumerate(sample_values):
            with cols[i % 4]:
                if st.checkbox(value, key=f"value_{value}"):
                    selected_values.append(value)
        
        # Custom values
        custom_values = st.text_input(
            "Additional values (comma-separated)",
            placeholder="Enter any other values not listed above"
        )
        
        if custom_values:
            custom_list = [value.strip() for value in custom_values.split(",")]
            selected_values.extend(custom_list)
        
        # Submit form
        submitted = st.form_submit_button("Create Profile", type="primary")
        
        if submitted:
            # Prepare student data
            student_data = {
                "name": name,
                "grade": grade,
                "interests": selected_interests,
                "strengths": selected_strengths,
                "values": selected_values,
                "availability": {
                    "weekdays": f"{weekday_hours} hours/day",
                    "weekends": f"{weekend_hours} hours/day"
                }
            }
            
            # Validate data
            errors = validate_student_data(student_data)
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                try:
                    # Create student profile
                    student_id = db_manager.add_student(student_data)
                    student_data['id'] = student_id
                    
                    # Add to vector database
                    vector_db.add_student_profile(student_data)
                    
                    # Update session state
                    st.session_state.current_student_id = student_id
                    st.session_state.students[student_id] = student_data
                    
                    st.success(f"Profile created successfully! Student ID: {student_id}")
                    st.balloons()
                    
                    # Show profile summary
                    st.subheader("Profile Summary")
                    st.write(f"**Name:** {name}")
                    st.write(f"**Grade:** {grade}")
                    st.write(f"**Interests:** {', '.join(selected_interests)}")
                    st.write(f"**Strengths:** {', '.join(selected_strengths)}")
                    st.write(f"**Values:** {', '.join(selected_values)}")
                    
                except Exception as e:
                    st.error(f"Error creating profile: {str(e)}")

def load_existing_profile():
    """Load an existing student profile."""
    st.subheader("Load Existing Profile")
    
    # For demo purposes, we'll create a simple ID input
    # In a real application, you might have a dropdown of students or login system
    student_id = st.text_input("Enter Student ID", placeholder="Enter your 4-digit student ID (e.g., 1234)")
    
    if st.button("Load Profile", type="primary"):
        if student_id:
            try:
                student = db_manager.get_student(student_id)
                if student:
                    st.session_state.current_student_id = student_id
                    st.session_state.students[student_id] = student
                    
                    st.success(f"Profile loaded for {student['name']}")
                    
                    # Display profile
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Name:** {student['name']}")
                        st.write(f"**Grade:** {student['grade']}")
                        st.write(f"**Interests:** {', '.join(student['interests'])}")
                    
                    with col2:
                        st.write(f"**Strengths:** {', '.join(student['strengths'])}")
                        st.write(f"**Values:** {', '.join(student['values'])}")
                        st.write(f"**Created:** {student['created_at']}")
                
                else:
                    st.error("Student not found. Please check the ID.")
                    
            except Exception as e:
                st.error(f"Error loading profile: {str(e)}")
        else:
            st.warning("Please enter a student ID.")

def show_recommendations_page():
    """Show the recommendations page."""
    st.header("🎯 Personalized Recommendations")
    
    # Initialize session state for score breakdowns
    if 'show_breakdowns' not in st.session_state:
        st.session_state.show_breakdowns = set()
    
    if not st.session_state.current_student_id:
        st.warning("Please create or load a student profile first.")
        return
    
    student_id = st.session_state.current_student_id
    student = st.session_state.students.get(student_id) or db_manager.get_student(student_id)
    
    if not student:
        st.error("Student profile not found.")
        return
    
    st.write(f"**Generating recommendations for:** {student['name']}")
    
    # Recommendation parameters
    col1, col2 = st.columns(2)
    
    with col1:
        num_recommendations = st.slider("Number of recommendations", 1, 15, 3)
    
    with col2:
        include_insights = st.checkbox("Include detailed insights", value=True)
    
    if st.button("Generate Recommendations", type="primary"):
        with st.spinner("Analyzing your profile and generating recommendations..."):
            try:
                # Generate recommendations
                recommendations = recommendation_engine.generate_recommendations(
                    student_id, n_recommendations=num_recommendations
                )
                
                # Store recommendations in session state for persistence across button clicks
                st.session_state.current_recommendations = recommendations
                
                if recommendations:
                    st.success(f"Generated {len(recommendations)} recommendations!")
                    
                    # Display all recommendations prominently
                    st.subheader("🏆 Your Recommended Activities")
                    
                    # Display all recommendations
                    for i, rec in enumerate(recommendations, 1):
                        with st.container():
                            # Add medal emoji for top 4, then numbered
                            if i == 1:
                                medal = "🥇"
                                bg_color = "#fff2e6"
                                border_color = "#ff6b35"
                            elif i == 2:
                                medal = "�"
                                bg_color = "#f0f8ff"
                                border_color = "#4da6ff"
                            elif i == 3:
                                medal = "🥉"
                                bg_color = "#f8fff8"
                                border_color = "#66cc66"
                            elif i == 4:
                                medal = "🏅"
                                bg_color = "#faf0ff"
                                border_color = "#9966cc"
                            else:
                                medal = f"{i}."
                                bg_color = "#f9f9f9"
                                border_color = "#cccccc"
                            
                            st.markdown(f"""
                            <div style="background-color: {bg_color}; 
                                       padding: 20px; border-radius: 10px; margin: 15px 0; 
                                       border-left: 5px solid {border_color};">
                                <h3>{medal} #{i}: {rec['activity']['name']} 
                                    <span style="color: #666; font-size: 0.8em;">(Score: {rec['score']:.1f}/10)</span>
                                </h3>
                                <p><strong>Category:</strong> {rec['activity']['category']}</p>
                                <p><strong>Why this is perfect for you:</strong> {rec['reasoning']}</p>
                                <p><strong>Skills you'll develop:</strong> {', '.join(rec['activity'].get('skills_developed', []))}</p>
                                <p><strong>Time commitment:</strong> {rec['activity'].get('time_commitment', 'Not specified')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Create tabs for different views
                    tab1, tab2, tab3 = st.tabs(["📋 List View", "📊 Dashboard", "📈 Insights"])
                    
                    with tab1:
                        # List view with detailed cards
                        for i, rec in enumerate(recommendations):
                            with st.expander(f"{i+1}. {rec['activity']['name']} (Score: {rec['score']:.1f}/10)", expanded=i<4):
                                st.markdown(format_recommendation_card(rec), unsafe_allow_html=True)
                                
                                # Score breakdown
                                if st.button(f"Show Score Breakdown", key=f"breakdown_{i}", type="primary"):
                                    fig = create_score_breakdown_chart(rec)
                                    st.plotly_chart(fig, use_container_width=True)
                    
                    with tab2:
                        # Dashboard view
                        st.subheader("Impact Dashboard")
                        fig = create_impact_dashboard(recommendations)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Summary metrics
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            avg_score = sum(rec['score'] for rec in recommendations) / len(recommendations)
                            st.metric("Average Score", f"{avg_score:.1f}/10")
                        
                        with col2:
                            categories = set(rec['activity']['category'] for rec in recommendations)
                            st.metric("Categories Covered", len(categories))
                        
                        with col3:
                            high_impact = sum(1 for rec in recommendations if rec['activity'].get('social_impact_score', 0) >= 8)
                            st.metric("High Social Impact", high_impact)
                        
                        with col4:
                            high_growth = sum(1 for rec in recommendations if rec['activity'].get('personal_growth_score', 0) >= 8)
                            st.metric("High Personal Growth", high_growth)
                    
                    with tab3:
                        # Detailed insights
                        if include_insights:
                            with st.spinner("Generating detailed insights..."):
                                insights = recommendation_engine.get_recommendation_insights(student_id, num_recommendations)
                                
                                if insights:
                                    display_student_insights(insights)
                                    
                                    # Development pathway
                                    if 'development_pathway' in insights:
                                        st.subheader("🗺️ Development Pathway")
                                        pathway = insights['development_pathway']
                                        
                                        if pathway.get('activity_sequence'):
                                            fig = create_development_pathway_chart(pathway)
                                            st.plotly_chart(fig, use_container_width=True)
                                        
                                        # Goals and milestones
                                        col1, col2 = st.columns(2)
                                        
                                        with col1:
                                            st.write("**Short-term Goals:**")
                                            for goal in pathway.get('short_term_goals', []):
                                                st.write(f"• {goal}")
                                        
                                        with col2:
                                            st.write("**Long-term Goals:**")
                                            for goal in pathway.get('long_term_goals', []):
                                                st.write(f"• {goal}")
                    
                    # Export recommendations
                    st.subheader("📥 Export Recommendations")
                    
                    df = export_recommendations_to_csv(recommendations)
                    csv = df.to_csv(index=False)
                    
                    st.download_button(
                        label="Download as CSV",
                        data=csv,
                        file_name=f"recommendations_{student['name'].replace(' ', '_')}.csv",
                        mime="text/csv"
                    )
                
                else:
                    st.warning("No recommendations generated. Please try again.")
                    
            except Exception as e:
                st.error(f"Error generating recommendations: {str(e)}")
    
    # Also display recommendations if they exist in session state (for persistence across button clicks)
    elif hasattr(st.session_state, 'current_recommendations') and st.session_state.current_recommendations:
        recommendations = st.session_state.current_recommendations
        
        # Display all recommendations prominently
        st.subheader("🏆 Your Recommended Activities")
        
        # Display all recommendations
        for i, rec in enumerate(recommendations, 1):
            with st.container():
                # Add medal emoji for top 4, then numbered
                if i == 1:
                    medal = "🥇"
                    bg_color = "#fff2e6"
                    border_color = "#ff6b35"
                elif i == 2:
                    medal = "🥈"
                    bg_color = "#f0f8ff"
                    border_color = "#4da6ff"
                elif i == 3:
                    medal = "🥉"
                    bg_color = "#f0fff0"
                    border_color = "#32cd32"
                elif i == 4:
                    medal = "🏅"
                    bg_color = "#fdf5e6"
                    border_color = "#daa520"
                else:
                    medal = f"{i}."
                    bg_color = "#f9f9f9"
                    border_color = "#cccccc"
                
                st.markdown(f"""
                <div style="background-color: {bg_color}; 
                           padding: 20px; border-radius: 10px; margin: 15px 0; 
                           border-left: 5px solid {border_color};">
                    <h3>{medal} #{i}: {rec['activity']['name']} 
                        <span style="color: #666; font-size: 0.8em;">(Score: {rec['score']:.1f}/10)</span>
                    </h3>
                    <p><strong>Category:</strong> {rec['activity']['category']}</p>
                    <p><strong>Why this is perfect for you:</strong> {rec['reasoning']}</p>
                    <p><strong>Skills you'll develop:</strong> {', '.join(rec['activity'].get('skills_developed', []))}</p>
                    <p><strong>Time commitment:</strong> {rec['activity'].get('time_commitment', 'Not specified')}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 List View", "📊 Dashboard", "📈 Insights"])
        
        with tab1:
            # List view with detailed cards
            for i, rec in enumerate(recommendations):
                with st.expander(f"{i+1}. {rec['activity']['name']} (Score: {rec['score']:.1f}/10)", expanded=i<4):
                    st.markdown(format_recommendation_card(rec), unsafe_allow_html=True)
                    
                    # Score breakdown button and chart with session state
                    breakdown_key = f"breakdown_{i}"
                    button_text = "Hide Score Breakdown" if breakdown_key in st.session_state.show_breakdowns else "Show Score Breakdown"
                    
                    if st.button(button_text, key=breakdown_key, type="primary"):
                        if breakdown_key in st.session_state.show_breakdowns:
                            st.session_state.show_breakdowns.remove(breakdown_key)
                        else:
                            st.session_state.show_breakdowns.add(breakdown_key)
                    
                    # Show chart if this breakdown is active
                    if breakdown_key in st.session_state.show_breakdowns:
                        fig = create_score_breakdown_chart(rec)
                        st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Dashboard view
            st.subheader("Impact Dashboard")
            fig = create_impact_dashboard(recommendations)
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_score = sum(rec['score'] for rec in recommendations) / len(recommendations)
                st.metric("Average Score", f"{avg_score:.1f}/10")
            
            with col2:
                categories = set(rec['activity']['category'] for rec in recommendations)
                st.metric("Categories Covered", len(categories))
            
            with col3:
                high_impact = sum(1 for rec in recommendations if rec['activity'].get('social_impact_score', 0) >= 8)
                st.metric("High Social Impact", high_impact)
            
            with col4:
                high_growth = sum(1 for rec in recommendations if rec['activity'].get('personal_growth_score', 0) >= 8)
                st.metric("High Personal Growth", high_growth)
        
        with tab3:
            # Always show detailed insights
            with st.spinner("Generating detailed insights..."):
                insights = recommendation_engine.get_recommendation_insights(student_id, len(recommendations))
                
                if insights:
                    display_student_insights(insights)
                    
                    # Development pathway
                    if 'development_pathway' in insights:
                        st.subheader("🗺️ Development Pathway")
                        pathway = insights['development_pathway']
                        
                        if pathway.get('activity_sequence'):
                            fig = create_development_pathway_chart(pathway)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Goals and milestones
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Short-term Goals:**")
                            for goal in pathway.get('short_term_goals', []):
                                st.write(f"• {goal}")
                        
                        with col2:
                            st.write("**Long-term Goals:**")
                            for goal in pathway.get('long_term_goals', []):
                                st.write(f"• {goal}")
        
        # Export recommendations
        st.subheader("📥 Export Recommendations")
        
        df = export_recommendations_to_csv(recommendations)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"recommendations_{student['name'].replace(' ', '_')}.csv",
            mime="text/csv"
        )

def show_student_directory_page():
    """Show the student directory page with all students and their activities."""
    st.header("👥 Student Directory")
    st.markdown("View all students with their IDs and recommended activities")
    
    try:
        # Get all students with activities
        students_with_activities = db_manager.get_all_students_with_activities()
        
        if not students_with_activities:
            st.info("No students found in the database.")
            return
        
        # Statistics summary
        total_students = len(students_with_activities)
        students_with_recommendations = len([s for s in students_with_activities if s['recommendation_count'] > 0])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Students", total_students)
        with col2:
            st.metric("Students with Recommendations", students_with_recommendations)
        with col3:
            st.metric("Students without Recommendations", total_students - students_with_recommendations)
        
        st.markdown("---")
        
        # Display students
        for student in students_with_activities:
            with st.expander(f"🎓 {student['name']} (ID: {student['id']})", expanded=False):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.write(f"**Grade:** {student.get('grade', 'N/A')}")
                    st.write(f"**Student ID:** `{student['id']}`")
                    st.write(f"**Recommendations:** {student['recommendation_count']}")
                
                with col2:
                    if student['activities']:
                        st.write("**Recommended Activities:**")
                        for i, activity in enumerate(student['activities'], 1):
                            st.write(f"{i}. **{activity['name']}** ({activity['category']})")
                            st.write(f"   📊 Compatibility Score: {activity['compatibility_score']}")
                            st.write(f"   📅 Recommended: {activity['recommended_at']}")
                            st.write("")
                    else:
                        st.info("No activities recommended yet. Visit the 'Get Recommendations' page to generate recommendations for this student.")
                
                # Quick action buttons
                st.markdown("**Quick Actions:**")
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                with col_btn1:
                    if st.button(f"View Profile", key=f"profile_{student['id']}", type="primary"):
                        st.session_state.current_student_id = student['id']
                        st.session_state.students[student['id']] = db_manager.get_student(student['id'])
                        st.success(f"Switched to {student['name']}'s profile!")
                        st.rerun()
                
                with col_btn2:
                    if st.button(f"Generate Recommendations", key=f"recs_{student['id']}", type="primary"):
                        st.session_state.current_student_id = student['id']
                        st.session_state.students[student['id']] = db_manager.get_student(student['id'])
                        st.success(f"Ready to generate recommendations for {student['name']}!")
                        st.info("Go to 'Get Recommendations' page to generate new recommendations.")
                
                with col_btn3:
                    # Delete button with confirmation
                    delete_key = f"delete_confirm_{student['id']}"
                    
                    if delete_key not in st.session_state:
                        # Show delete button
                        if st.button(f"🗑️ Delete Student", key=f"delete_{student['id']}", type="primary", help="Delete this student and all their data"):
                            st.session_state[delete_key] = True
                            st.rerun()
                    else:
                        # Show confirmation dialog
                        st.warning(f"⚠️ Are you sure you want to delete **{student['name']}**?")
                        st.write("This action cannot be undone!")
                        
                        col_del1, col_del2 = st.columns(2)
                        with col_del1:
                            if st.button("✅ Yes, Delete", key=f"confirm_yes_{student['id']}", type="primary"):
                                try:
                                    success = db_manager.delete_student(student['id'])
                                    if success:
                                        # Clean up session state
                                        if delete_key in st.session_state:
                                            del st.session_state[delete_key]
                                        if st.session_state.get('current_student_id') == student['id']:
                                            st.session_state.current_student_id = None
                                        if 'students' in st.session_state and student['id'] in st.session_state.students:
                                            del st.session_state.students[student['id']]
                                        
                                        st.success(f"✅ Successfully deleted {student['name']} and all associated data!")
                                        st.rerun()
                                    else:
                                        st.error(f"❌ Failed to delete student {student['name']}. Student not found.")
                                        del st.session_state[delete_key]
                                except Exception as e:
                                    st.error(f"❌ Error deleting student: {str(e)}")
                                    if delete_key in st.session_state:
                                        del st.session_state[delete_key]
                        
                        with col_del2:
                            if st.button("❌ Cancel", key=f"cancel_{student['id']}", type="secondary"):
                                del st.session_state[delete_key]
                                st.info("Delete cancelled.")
                                st.rerun()
    
    except Exception as e:
        st.error(f"Error loading student directory: {str(e)}")

def show_activity_database_page():
    """Show the activity database page."""
    st.header("📚 Activity Database")
    
    # Add info about adding new activities
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Browse all available extracurricular activities in the database.")
    with col2:
        st.info("💡 Want to add a new activity? Check out the 'Add New Activity' page!")
    
    # Get all activities
    activities = db_manager.get_all_activities()
    
    if not activities:
        st.warning("No activities found in the database.")
        return
    
    # Filters with session state management
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        categories = sorted(list(set(activity['category'] for activity in activities)))
        # Use session state for category filter
        if 'activity_category_filter' not in st.session_state:
            st.session_state.activity_category_filter = "All"
        
        selected_category = st.selectbox(
            "Filter by Category", 
            ["All"] + categories,
            index=0 if st.session_state.activity_category_filter == "All" else 
                  (["All"] + categories).index(st.session_state.activity_category_filter)
                  if st.session_state.activity_category_filter in categories else 0,
            key="category_selectbox"
        )
        
        # Check if category changed and trigger rerun
        if selected_category != st.session_state.activity_category_filter:
            st.session_state.activity_category_filter = selected_category
            st.rerun()
    
    with col2:
        # Use session state for difficulty filter
        if 'activity_difficulty_filter' not in st.session_state:
            st.session_state.activity_difficulty_filter = (1, 5)
        
        difficulty_range = st.slider(
            "Difficulty Level", 
            1, 5, 
            st.session_state.activity_difficulty_filter,
            key="difficulty_slider"
        )
        
        # Check if difficulty range changed and trigger rerun
        if difficulty_range != st.session_state.activity_difficulty_filter:
            st.session_state.activity_difficulty_filter = difficulty_range
            st.rerun()
    
    with col3:
        # Use session state for search filter
        if 'activity_search_filter' not in st.session_state:
            st.session_state.activity_search_filter = ""
            
        search_term = st.text_input(
            "Search activities", 
            placeholder="Enter search term",
            value=st.session_state.activity_search_filter,
            key="search_input"
        )
        
        # Check if search term changed and trigger rerun
        if search_term != st.session_state.activity_search_filter:
            st.session_state.activity_search_filter = search_term
            st.rerun()
    
    with col4:
        st.write("") # spacer for alignment
        if st.button("🔄 Reset Filters", type="primary", help="Reset all filters to show all activities"):
            st.session_state.activity_category_filter = "All"
            st.session_state.activity_difficulty_filter = (1, 5)
            st.session_state.activity_search_filter = ""
            st.rerun()
    
    # Filter activities
    filtered_activities = activities
    
    if selected_category != "All":
        filtered_activities = [act for act in filtered_activities if act['category'] == selected_category]
    
    if difficulty_range and difficulty_range != (1, 5):
        filtered_activities = [act for act in filtered_activities 
                             if difficulty_range[0] <= act.get('difficulty_level', 1) <= difficulty_range[1]]
    
    if search_term:
        filtered_activities = [act for act in filtered_activities 
                             if search_term.lower() in act['name'].lower() or 
                             search_term.lower() in act.get('description', '').lower()]
    
    # Display filter status
    total_activities = len(activities)
    filtered_count = len(filtered_activities)
    
    if filtered_count == total_activities:
        st.success(f"📋 Showing all {total_activities} activities")
    else:
        filter_info = []
        if selected_category != "All":
            filter_info.append(f"Category: {selected_category}")
        if difficulty_range != (1, 5):
            filter_info.append(f"Difficulty: {difficulty_range[0]}-{difficulty_range[1]}")
        if search_term:
            filter_info.append(f"Search: '{search_term}'")
        
        st.info(f"📋 Showing {filtered_count} of {total_activities} activities | Filters: {', '.join(filter_info)}")
        
        if filtered_count == 0:
            st.warning("No activities match your current filters. Try adjusting the filters or click 'Reset Filters' to see all activities.")
            return
    
    # Activity grid
    cols = st.columns(2)
    
    for i, activity in enumerate(filtered_activities):
        with cols[i % 2]:
            with st.container():
                st.subheader(activity['name'])
                st.write(f"**Category:** {activity['category']}")
                st.write(f"**Description:** {activity.get('description', 'No description')}")
                st.write(f"**Time Commitment:** {activity.get('time_commitment', 'N/A')}")
                st.write(f"**Difficulty:** {activity.get('difficulty_level', 1)}/5")
                
                # Scores
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Growth", f"{activity.get('personal_growth_score', 0):.1f}")
                with col_b:
                    st.metric("Impact", f"{activity.get('social_impact_score', 0):.1f}")
                with col_c:
                    st.metric("Fulfillment", f"{activity.get('fulfillment_score', 0):.1f}")
                
                # Skills
                skills = activity.get('skills_developed', [])
                if skills:
                    st.write("**Skills:** " + ", ".join(skills[:5]))
                
                # Delete button
                delete_key = f"delete_activity_{activity['id']}"
                confirm_key = f"confirm_delete_activity_{activity['id']}"
                
                if st.button(f"🗑️ Delete Activity", key=delete_key, type="primary", help=f"Delete {activity['name']} and all associated recommendations"):
                    st.session_state[confirm_key] = True
                
                # Show confirmation dialog if delete was clicked
                if st.session_state.get(confirm_key, False):
                    st.warning(f"⚠️ Are you sure you want to delete '{activity['name']}'? This will also delete all recommendations for this activity and cannot be undone!")
                    
                    col_confirm1, col_confirm2 = st.columns(2)
                    with col_confirm1:
                        if st.button("✅ Yes, Delete", key=f"confirm_yes_{activity['id']}", type="primary"):
                            try:
                                success = db_manager.delete_activity(activity['id'])
                                if success:
                                    # Clean up session state
                                    if confirm_key in st.session_state:
                                        del st.session_state[confirm_key]
                                    
                                    st.success(f"✅ Successfully deleted '{activity['name']}' and all associated recommendations!")
                                    st.rerun()
                                else:
                                    st.error(f"❌ Failed to delete activity '{activity['name']}'. Activity not found.")
                                    if confirm_key in st.session_state:
                                        del st.session_state[confirm_key]
                            except Exception as e:
                                st.error(f"❌ Error deleting activity: {str(e)}")
                                if confirm_key in st.session_state:
                                    del st.session_state[confirm_key]
                    
                    with col_confirm2:
                        if st.button("❌ Cancel", key=f"confirm_no_{activity['id']}", type="primary"):
                            if confirm_key in st.session_state:
                                del st.session_state[confirm_key]
                            st.info("Delete cancelled.")
                            st.rerun()
                
                st.divider()

def show_add_activity_page():
    """Show the add new activity page."""
    st.header("➕ Add New Extracurricular Activity")
    
    st.write("Expand the activity database by adding new extracurricular opportunities!")
    
    with st.form("add_activity_form"):
        # Basic information
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Activity Name*", placeholder="e.g., Photography Club")
            category = st.selectbox("Category*", [
                "Academic", "STEM", "Arts", "Sports", "Leadership", 
                "Community Service", "Media", "Music", "Technology", 
                "Business", "Language", "Other"
            ])
        
        with col2:
            time_commitment = st.selectbox("Time Commitment*", [
                "1-2 hours/week", "3-4 hours/week", "5-6 hours/week", 
                "7-10 hours/week", "10+ hours/week"
            ])
            difficulty_level = st.slider("Difficulty Level (1=Easy, 5=Very Challenging)", 1, 5, 3)
        
        # Description
        description = st.text_area(
            "Description*", 
            placeholder="Provide a detailed description of what this activity involves, what students will do, and any key features...",
            height=100
        )
        
        # Skills
        st.subheader("Skills Developed")
        skills_input = st.text_input(
            "Skills (comma-separated)*",
            placeholder="e.g., Photography, Editing, Creativity, Technical Skills, Visual Communication"
        )
        
        # Prerequisites
        prerequisites_input = st.text_input(
            "Prerequisites (comma-separated)",
            placeholder="e.g., Basic camera knowledge, Interest in visual arts (leave blank if none)"
        )
        
        # Scoring
        st.subheader("Activity Scores (1-10)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            personal_growth = st.slider("Personal Growth Score", 1.0, 10.0, 7.0, 0.1,
                                       help="How much will this activity help students develop personally?")
        
        with col2:
            social_impact = st.slider("Social Impact Score", 1.0, 10.0, 6.0, 0.1,
                                     help="How much positive impact will this activity have on others/community?")
        
        with col3:
            fulfillment = st.slider("Fulfillment Score", 1.0, 10.0, 7.0, 0.1,
                                   help="How personally rewarding/enjoyable is this activity?")
        
        # Submit button
        submitted = st.form_submit_button("Add Activity", type="primary")
        
        if submitted:
            # Validate required fields
            if not name or not description or not skills_input:
                st.error("Please fill in all required fields (marked with *).")
                return
            
            # Prepare activity data
            skills_list = [skill.strip() for skill in skills_input.split(",") if skill.strip()]
            prerequisites_list = [prereq.strip() for prereq in prerequisites_input.split(",") if prereq.strip()] if prerequisites_input else []
            
            activity_data = {
                "name": name,
                "category": category,
                "description": description,
                "skills_developed": skills_list,
                "time_commitment": time_commitment,
                "difficulty_level": difficulty_level,
                "personal_growth_score": personal_growth,
                "social_impact_score": social_impact,
                "fulfillment_score": fulfillment,
                "prerequisites": prerequisites_list
            }
            
            try:
                # Add activity to database
                activity_id = db_manager.add_activity(activity_data)
                activity_data['id'] = activity_id
                
                # Add to vector database
                vector_db.add_activities([activity_data])
                
                st.success(f"🎉 Activity '{name}' added successfully!")
                st.balloons()
                
                # Show activity summary
                st.subheader("Activity Summary")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Name:** {name}")
                    st.write(f"**Category:** {category}")
                    st.write(f"**Time Commitment:** {time_commitment}")
                    st.write(f"**Difficulty:** {difficulty_level}/5")
                    st.write(f"**Skills:** {', '.join(skills_list)}")
                
                with col2:
                    st.write(f"**Personal Growth:** {personal_growth:.1f}/10")
                    st.write(f"**Social Impact:** {social_impact:.1f}/10")
                    st.write(f"**Fulfillment:** {fulfillment:.1f}/10")
                    if prerequisites_list:
                        st.write(f"**Prerequisites:** {', '.join(prerequisites_list)}")
                
                st.write(f"**Description:** {description}")
                
                # Suggest viewing the activity database
                st.info("💡 You can view all activities in the 'Activity Database' page!")
                
            except Exception as e:
                st.error(f"Error adding activity: {str(e)}")
    
    # Show quick stats
    st.subheader("📊 Current Database Statistics")
    activities = db_manager.get_all_activities()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Activities", len(activities))
    with col2:
        categories = set(activity['category'] for activity in activities)
        st.metric("Categories", len(categories))
    with col3:
        if activities:
            avg_score = sum((act.get('personal_growth_score', 0) + 
                           act.get('social_impact_score', 0) + 
                           act.get('fulfillment_score', 0)) / 3 
                          for act in activities) / len(activities)
            st.metric("Avg Overall Score", f"{avg_score:.1f}/10")

def show_analytics_dashboard_page():
    """Show the analytics dashboard page."""
    st.header("📊 Analytics Dashboard")
    
    # Get data for analytics
    activities = db_manager.get_all_activities()
    
    if not activities:
        st.warning("No data available for analytics.")
        return
    
    # Overall statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Activities", len(activities))
    
    with col2:
        categories = set(activity['category'] for activity in activities)
        st.metric("Categories", len(categories))
    
    with col3:
        avg_growth = sum(activity.get('personal_growth_score', 0) for activity in activities) / len(activities)
        st.metric("Avg Growth Score", f"{avg_growth:.1f}")
    
    with col4:
        avg_impact = sum(activity.get('social_impact_score', 0) for activity in activities) / len(activities)
        st.metric("Avg Impact Score", f"{avg_impact:.1f}")
    
    # Charts
    st.subheader("Activity Distribution")
    
    # Category distribution
    from utils.visualization import create_category_distribution_chart
    fig = create_category_distribution_chart(activities)
    st.plotly_chart(fig, use_container_width=True)
    
    # Score distribution
    import plotly.express as px
    import pandas as pd
    
    # Create DataFrame for analysis
    df = pd.DataFrame([
        {
            'Name': act['name'][:30] + "..." if len(act['name']) > 30 else act['name'],
            'Category': act['category'],
            'Personal Growth': act.get('personal_growth_score', 0),
            'Social Impact': act.get('social_impact_score', 0),
            'Fulfillment': act.get('fulfillment_score', 0),
            'Difficulty': act.get('difficulty_level', 1)
        }
        for act in activities
    ])
    
    # Scatter plot
    st.subheader("Score Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(df, x='Personal Growth', y='Social Impact', 
                        color='Category', size='Fulfillment',
                        hover_name='Name', title="Growth vs Impact")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(df, x='Category', y='Personal Growth', 
                    title="Growth Scores by Category")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
