# SmartMatch - Agentic AI Extracurricular Recommender

SmartMatch is an intelligent, student-centered AI application designed to help high school students choose extracurricular activities that align with their strengths, interests, and personal values.

## Features

- **Student Profile Builder**: Input interests, strengths, values, and availability
- **Activity Database**: Curated list of extracurricular options
- **Add New Activities**: Expand the database with custom extracurricular activities
- **Agentic Recommendation Engine**: AI-driven recommendations with planning and learning
- **Top 3 Recommendations**: Get your best matches with detailed reasoning
- **Impact Dashboard**: Visualize development across core goals

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your AI configuration in `.env`:
   
   **Option A: Regular OpenAI**
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4
   ```
   
   **Option B: Azure OpenAI (Recommended for enterprise)**
   ```
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_CHAT_MODEL=gpt-4
   ```
   
   **Optional: Configure embedding model**
   ```
   EMBEDDING_MODEL=all-MiniLM-L6-v2
   ```

3. Run the application:
   
   **Web Interface (Streamlit):**
   ```bash
   streamlit run app.py
   ```
   
   **Command Line Interface:**
   ```bash
   python smartmatch_cli.py
   ```
   
   **API Example (Programmatic):**
   ```bash
   python api_example.py
   ```
   
   **Batch Processing:**
   ```bash
   python batch_processor.py sample_students.json
   ```

## Usage Options

### 1. Streamlit Web Interface (app.py)
Interactive web application with full features:
- Student profile creation
- Real-time recommendations (top 3 by default)
- Activity database browsing
- **Add new activities** to expand the database
- Analytics dashboard
- Visualization charts

### 2. Command Line Interface (smartmatch_cli.py)
Terminal-based interface for:
- Creating student profiles
- Generating recommendations (top 3 by default)
- Browsing activities
- **Adding new activities**
- System analytics
- Saving recommendations to files

### 3. API Example (api_example.py)
Demonstrates programmatic usage:
- Initialize system components
- Create student profiles via code
- Generate recommendations
- Access insights programmatically

### 4. Batch Processing (batch_processor.py)
Process multiple students from files:
- JSON input format
- CSV input format
- Bulk recommendation generation
- Summary reports
- Export capabilities

## Project Structure

- `app.py` - Main Streamlit application
- `database/` - Smart database management (SQLite + FAISS)
  - `smart_sqlite_db.py` - SQLite database manager
  - `smart_vector_db.py` - FAISS vector similarity search
- `agents/` - AI agent components with Azure OpenAI support
- `utils/` - Utility functions and data loading
- `data/` - Generated database files and vector indices

## Core Goals

1. **Maximize Personal Growth** - Develop capabilities based on unique strengths
2. **Create Value for Others** - Contribute positively to communities
3. **Foster Personal Fulfillment** - Promote happiness and intrinsic motivation

## Architecture

### Smart Database System
- **SQLite Database**: Lightweight relational database for structured data
- **FAISS Vector Search**: Fast similarity search for activity recommendations
- **Dynamic Embeddings**: Configurable text embedding models

### AI Integration
- **Flexible LLM Support**: Works with both OpenAI and Azure OpenAI
- **Model Configuration**: Environment-based model selection
- **Intelligent Reasoning**: AI-powered recommendation explanations

### Key Features
- **No Heavy Dependencies**: Replaced ChromaDB with lighter FAISS
- **File-Based Storage**: Easy deployment without external database servers
- **Configurable Models**: Support for different embedding and chat models
