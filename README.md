# 🎯 SmartMatch - AI-Powered Extracurricular Recommender

SmartMatch is an intelligent, student-centered AI application designed to help high school students discover extracurricular activities that perfectly align with their unique strengths, interests, and personal values. Using advanced AI technology, SmartMatch provides personalized recommendations with detailed reasoning to guide students toward meaningful growth opportunities.

## ✨ Key Features

### 🎓 **Student-Centered Experience**
- **Smart Profile Builder**: Comprehensive interest, strength, and values assessment
- **4-Digit ID System**: Easy-to-remember student identification
- **Load Existing Profiles**: Quick access to saved student data
- **Availability Matching**: Activities that fit your schedule

### 📚 **Enhanced Activity Database**
- **16+ Curated Activities**: Sports, STEM, Arts, Leadership, Community Service
- **Smart Filtering**: Instant category, difficulty, and search filtering
- **Reset Functionality**: Easy return to full activity list
- **Add New Activities**: Expand the database with custom opportunities
- **Activity Management**: Add, edit, and delete activities with cascade cleanup

### 🤖 **AI-Powered Recommendations**
- **Customizable Count**: Choose 1-10 recommendations (slider control)
- **Intelligent Matching**: AI analyzes compatibility across multiple dimensions
- **Detailed Reasoning**: Understand why each activity matches your profile
- **Recommendation Insights**: Deep AI analysis of student-activity alignment
- **Dynamic Updates**: Replace and refresh recommendations easily

### 🎨 **Modern Interface**
- **Clean Design**: Professional blue theme with intuitive navigation
- **Instant Filtering**: No more double-clicking - filters work immediately
- **Student Directory**: Comprehensive management of all students and recommendations
- **Enhanced Confirmations**: Clear deletion confirmations with safety measures
- **Responsive Layout**: Works seamlessly across different screen sizes

## 🚀 Quick Start

### Prerequisites
- Python 3.13+ (tested and optimized for Python 3.13.5)
- Azure OpenAI access (recommended) or OpenAI API key

### Installation

1. **Clone and Setup**:
   ```bash
   git clone https://github.com/yanxu55/ai-smart-match.git
   cd ai-smart-match
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AI Settings** - Create `.env` file:
   
   **Azure OpenAI (Recommended):**
   ```env
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_CHAT_MODEL=gpt-4.1
   AZURE_OPENAI_EMBEDDING_MODEL=adaembed02
   ```
   
   **Regular OpenAI (Alternative):**
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4
   ```

4. **Launch the Application**:
   ```bash
   streamlit run app.py
   ```
   
   🎉 **Access at**: http://localhost:8501

## 💻 Usage Options
## 💻 Usage Options

### 🌐 **1. Web Interface (Recommended)**
```bash
streamlit run app.py
```
**Full-featured interactive experience:**
- 👤 **Student Profile Management**: Create and load student profiles with 4-digit IDs
- 📚 **Activity Database Browser**: Smart filtering, search, and category selection
- 🎯 **Personalized Recommendations**: 1-10 recommendations with detailed AI reasoning
- ➕ **Activity Management**: Add new activities, delete existing ones
- 🏫 **Student Directory**: Manage all students and their recommendations
- 📊 **AI Insights**: Deep analysis of student-activity compatibility

### 🖥️ **2. Command Line Interface**
```bash
python smartmatch_cli.py
```
**Terminal-based interface for:**
- Student profile creation and management
- Activity browsing and addition
- Recommendation generation
- System analytics and reports

### 🔧 **3. API Integration**
```bash
python api_example.py
```
**Programmatic access for:**
- Automated profile creation
- Bulk recommendation processing
- Integration with existing systems
- Custom application development

### 📊 **4. Batch Processing**
```bash
python batch_processor.py sample_students.json
```
**High-volume processing:**
- Multiple student processing from JSON/CSV
- Bulk recommendation generation
- Summary reports and analytics
- Export capabilities

## 🏗️ Architecture Overview
## 🏗️ Architecture Overview

### 📁 **Project Structure**
```
ai-smart-match/
├── app.py                 # 🌐 Main Streamlit web application
├── smartmatch_cli.py      # 🖥️ Command-line interface
├── api_example.py         # 🔧 API usage demonstration
├── batch_processor.py     # 📊 Batch processing utilities
├── config.py             # ⚙️ Configuration management
├── database/             # 💾 Smart database management
│   ├── smart_sqlite_db.py    # SQLite with cascade deletion
│   ├── smart_vector_db.py    # FAISS vector similarity search
│   └── simple_*.py          # Fallback database implementations
├── agents/               # 🤖 AI agent components
│   ├── ai_agent.py          # Azure OpenAI integration
│   └── recommendation_engine.py  # AI recommendation logic
├── utils/                # 🛠️ Utility functions
│   ├── data_loader.py       # Data loading utilities
│   └── visualization.py    # Chart and graph generation
└── data/                 # 📂 Generated database files
    ├── activities.db        # SQLite database
    └── vectors/            # FAISS vector indices
```

### 🗄️ **Database Architecture**
- **SQLite Database**: Lightweight, reliable student and activity data storage
- **FAISS Vector Search**: Lightning-fast similarity matching for recommendations
- **Cascade Deletion**: Safe removal of related data when deleting students/activities
- **4-Digit ID System**: User-friendly identification system
- **JSON Field Storage**: Flexible data structure for complex attributes

### 🤖 **AI Integration**
- **Azure OpenAI**: GPT-4.1 for intelligent reasoning and insights
- **Embedding Models**: adaembed02 (1536 dimensions) for semantic similarity
- **Fallback Support**: OpenAI API compatibility for flexibility
- **Smart Caching**: Efficient vector storage and retrieval
- **Error Handling**: Robust fallbacks and error recovery

## 🎯 Core Educational Goals

SmartMatch is built around three fundamental principles:

### 1. 🌱 **Maximize Personal Growth**
- Activities that build on existing strengths
- Opportunities to develop new capabilities
- Challenges appropriate to skill level
- Progressive skill development paths

### 2. 🤝 **Create Value for Others**
- Community service and leadership opportunities
- Collaborative projects and team activities
- Social impact and contribution focus
- Building empathy and social awareness

### 3. 💫 **Foster Personal Fulfillment**
- Activities aligned with personal interests
- Intrinsic motivation and enjoyment
- Work-life balance considerations
- Long-term satisfaction and engagement

## 🔧 Recent Updates & Bug Fixes

### ✅ **Latest Improvements** (Current Version)
- **Instant Filtering**: Category selection now works immediately (fixed double-click bug)
- **Clean Interface**: Removed technical warning messages for cleaner startup
- **Enhanced Recommendations**: Fixed hardcoded recommendation count bug
- **Database Expansion**: Added Soccer and Chess Club activities
- **Better UI**: Blue button theme, improved confirmations, reset functionality
- **Cascade Deletion**: Safe activity and student removal with relationship cleanup

### 🛡️ **Stability Enhancements**
- Robust error handling for AI API failures
- Fallback mechanisms for vector database issues
- Session state management for filter persistence
- Input validation and sanitization
- Comprehensive logging for debugging

## 🚀 Demo & Training

Check out our comprehensive [DEMO.md](DEMO.md) for:
- 15-minute interactive demo script for high school students
- Audience participation ideas and engagement strategies
- Sample student profiles and scenarios
- Technical presentation tips
- Success metrics and impact stories

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Code standards and best practices
- Testing requirements
- Documentation updates
- Feature requests and bug reports

## 📚 Additional Resources

- **[USAGE_GUIDE.md](USAGE_GUIDE.md)**: Detailed usage instructions
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)**: Comprehensive setup documentation
- **[SECURITY.md](SECURITY.md)**: Security policies and reporting
- **[LICENSE](LICENSE)**: MIT License details

---

## 🎓 Perfect for High Schools

SmartMatch is designed specifically for high school environments:
- **College Preparation**: Build well-rounded application portfolios
- **Skill Development**: Strategic capability building aligned with interests
- **Time Management**: Activities that fit student schedules and commitments
- **Personal Growth**: Opportunities for meaningful development and impact
- **Counselor Support**: Tools to facilitate guidance conversations
- **Data-Driven Decisions**: AI insights to support activity selection

**Ready to help your students discover their perfect extracurricular match?** 🎯

*SmartMatch: Where AI meets student success.*
