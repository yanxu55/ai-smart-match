# SmartMatch Setup and Usage Guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key
1. Open the `.env` file
2. Replace `your_openai_api_key_here` with your actual OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

### 3. Initialize the System
```bash
python setup.py
```

### 4. Test the System (Optional)
```bash
python test_system.py
```

### 5. Run the Application
```bash
streamlit run app.py
```

## 📋 System Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for API calls
- Approximately 100MB disk space for databases

## 🏗️ System Architecture

### Core Components

1. **Database Layer**
   - `database/db_manager.py` - SQLite database management
   - `database/vector_db.py` - ChromaDB vector database for similarity search

2. **AI Agents**
   - `agents/ai_agent.py` - OpenAI GPT integration for analysis and reasoning
   - `agents/recommendation_engine.py` - Core recommendation logic

3. **User Interface**
   - `app.py` - Streamlit web application
   - `utils/visualization.py` - Charts and dashboards

4. **Data Management**
   - `utils/data_loader.py` - Sample data initialization
   - `config.py` - System configuration

## 🎯 How to Use SmartMatch

### Creating a Student Profile

1. Go to the **Student Profile** page
2. Choose "Create New Profile"
3. Fill in your information:
   - Name and grade level
   - Select interests from the list or add custom ones
   - Choose your strengths
   - Select your core values
   - Set your availability

4. Click "Create Profile"

### Getting Recommendations

1. Go to the **Get Recommendations** page
2. Adjust the number of recommendations (3-15)
3. Click "Generate Recommendations"

### Understanding Your Results

The system provides three views:

**📋 List View**: Detailed cards for each recommended activity
**📊 Dashboard**: Visual impact analysis across three core goals
**📈 Insights**: AI-generated profile analysis and development pathway

### Exploring Activities

Use the **Activity Database** page to:
- Browse all available activities
- Filter by category or difficulty
- Search for specific activities
- View detailed activity information

## 🧠 How the AI Works

### Recommendation Algorithm

SmartMatch uses a multi-factor scoring system:

1. **Vector Similarity (20%)**: Semantic matching between your profile and activities
2. **Interest Alignment (15%)**: How well activities match your stated interests
3. **Strength Utilization (15%)**: Activities that use your existing strengths
4. **Values Alignment (15%)**: Activities that support your core values
5. **Growth Scores (30%)**: Pre-calculated scores for personal growth, social impact, and fulfillment
6. **Practical Factors (5%)**: Availability and difficulty matching

### AI-Generated Insights

The system uses GPT-4 to provide:
- Personality trait analysis
- Development area identification
- Personalized reasoning for each recommendation
- Long-term development pathway planning

## 📊 Sample Data Included

The system comes with 15 sample activities across categories:
- **Academic**: Debate Team, Science Olympiad, Model UN
- **Arts**: Drama Club, Music Band, Art Club
- **Community Service**: Environmental Club, Volunteer Tutoring, Red Cross Club
- **Leadership**: Student Government
- **Sports**: Varsity Basketball
- **STEM**: Robotics Club, Computer Programming Club
- **Media**: School Newspaper
- **Games & Strategy**: Chess Club

## 🔧 Customization

### Adding New Activities

1. Use the database manager to add activities:
```python
from database.db_manager import DatabaseManager

db = DatabaseManager()
activity_data = {
    "name": "New Activity",
    "category": "Category",
    "description": "Description here",
    "skills_developed": ["skill1", "skill2"],
    "time_commitment": "X hours/week",
    "difficulty_level": 3,
    "social_impact_score": 7.0,
    "personal_growth_score": 8.0,
    "fulfillment_score": 6.0,
    "prerequisites": []
}
db.create_activity(activity_data)
```

### Modifying Scoring Weights

Edit the `SCORING_WEIGHTS` in `config.py` to adjust how different factors influence recommendations.

### Customizing the UI

Modify `app.py` to:
- Change the layout or styling
- Add new pages or features
- Customize the recommendation display

## 🚨 Troubleshooting

### Common Issues

1. **"Error initializing system"**
   - Check your OpenAI API key in `.env`
   - Ensure all dependencies are installed
   - Run `python test_system.py` to diagnose

2. **"No recommendations generated"**
   - Verify your student profile has interests, strengths, and values
   - Check that activities exist in the database
   - Try running `python setup.py` to reload sample data

3. **"Module not found" errors**
   - Ensure you're running from the project root directory
   - Check that all `__init__.py` files exist
   - Verify Python path is set correctly

### Getting Help

1. Run the test script: `python test_system.py`
2. Check the console output for detailed error messages
3. Verify your `.env` file has the correct API key format
4. Ensure all requirements are installed with correct versions

## 🔮 Future Enhancements

Potential improvements for the system:
- User authentication and profile persistence
- Activity feedback and rating system
- Collaborative filtering based on similar students
- Integration with school activity databases
- Mobile-responsive design
- Multi-language support
- Advanced analytics and reporting
