# SmartMatch Usage Guide

## How to Use SmartMatch for Activity Recommendations

### Step 1: Add Your Own Extracurricular Activities (Optional)

**Via Web Interface:**
1. Run `streamlit run app.py`
2. Navigate to **"Add New Activity"** page
3. Fill out the form with:
   - Activity name and category
   - Description and skills developed
   - Time commitment and difficulty level
   - Scoring (Personal Growth, Social Impact, Fulfillment)
4. Click **"Add Activity"**

**Via Command Line:**
1. Run `python smartmatch_cli.py`
2. Choose option **5** (Add New Activity)
3. Follow the prompts to enter activity details

### Step 2: Create Your Student Profile

**Web Interface:**
1. Go to **"Student Profile"** page
2. Choose **"Create New Profile"**
3. Fill out your information:
   - Basic info (name, grade, availability)
   - **Interests**: Select from checkboxes or add custom ones
   - **Strengths**: Choose your key strengths
   - **Values**: Pick your core values
4. Click **"Create Profile"** and save your Student ID

**Command Line:**
1. Choose option **1** (Create Student Profile)
2. Enter your details when prompted

### Step 3: Get Your Top 3 Recommendations

**Web Interface:**
1. Navigate to **"Get Recommendations"** page
2. Adjust number of recommendations (defaults to 3)
3. Click **"Generate Recommendations"**
4. View your **🏆 Top 3 Recommended Activities** with:
   - Medal rankings (🥇🥈🥉)
   - Compatibility scores
   - Detailed reasoning
   - Skills you'll develop

**Command Line:**
1. Choose option **3** (Generate Recommendations)
2. Enter your Student ID
3. Specify number of recommendations (defaults to 3)
4. Review detailed results with scores and reasoning

## Sample Profile Example

**Student Profile:**
- **Interests**: Technology, Environmental Science, Writing
- **Strengths**: Problem Solving, Communication, Research
- **Values**: Innovation, Social Justice, Environmental Sustainability

**Expected Top 3 Recommendations:**
1. 🥇 **School Newspaper** - Use writing skills to cover tech and environmental topics
2. 🥈 **Environmental Club** - Apply problem-solving to sustainability projects
3. 🥉 **Robotics Club** - Combine technology interest with innovation

## Available Activity Categories

When adding new activities, choose from:
- Academic (Science Olympiad, Debate Team)
- STEM (Robotics, Coding Club)
- Arts (Drama, Photography, Art Club)
- Sports (Various athletic activities)
- Leadership (Student Government, Peer Mentoring)
- Community Service (Environmental Club, Tutoring)
- Media (Newspaper, Yearbook)
- Music (Band, Choir)
- Technology (Coding, Tech Support)
- Business (FBLA, Entrepreneurship)
- Language (Foreign Language Clubs)
- Other (Custom categories)

## Tips for Best Recommendations

1. **Be Specific**: The more detailed your interests and strengths, the better the matches
2. **Add Custom Activities**: Include activities specific to your school or community
3. **Consider All Aspects**: Look at Personal Growth, Social Impact, and Fulfillment scores
4. **Review Reasoning**: Read why each activity was recommended for you
5. **Export Results**: Download your recommendations as CSV for future reference

## Quick Start Commands

```bash
# Start web interface
streamlit run app.py

# Start command line interface  
python smartmatch_cli.py

# Run API example
python api_example.py

# Process batch students
python batch_processor.py students.json
```

## Need Help?

- Check the **Analytics Dashboard** to see all available activities
- Use the **Activity Database** to browse options by category
- The AI provides detailed reasoning for each recommendation
- Export your results for offline review
