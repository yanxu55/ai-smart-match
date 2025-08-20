# Contributing to SmartMatch

Thank you for your interest in contributing to SmartMatch! We welcome contributions from the community.

## How to Contribute

### 🐛 Reporting Bugs
1. Check if the bug has already been reported in the [Issues](../../issues)
2. Create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)

### 💡 Suggesting Features
1. Check existing [Issues](../../issues) and [Pull Requests](../../pulls)
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Any implementation ideas

### 🔧 Code Contributions

#### Getting Started
1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/ai-smart-match.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Set up development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

#### Development Guidelines
- Follow PEP 8 style guide
- Add comments for complex logic
- Update documentation if needed
- Test your changes thoroughly

#### Adding New Activities
- Use the built-in "Add New Activity" feature
- Ensure activities have proper categorization
- Include comprehensive skill lists
- Add meaningful descriptions

#### Adding New Features
- Maintain compatibility with existing interfaces
- Update all relevant interfaces (Web UI, CLI, API)
- Add appropriate error handling
- Document new features in README

#### Submitting Changes
1. Commit your changes: `git commit -m "Add new feature: description"`
2. Push to your fork: `git push origin feature/your-feature-name`
3. Create a Pull Request with:
   - Clear description of changes
   - Testing performed
   - Screenshots (if UI changes)

## Development Setup

### Prerequisites
- Python 3.8+
- OpenAI or Azure OpenAI API access
- Git

### Local Development
```bash
# Clone and setup
git clone https://github.com/yanxu55/ai-smart-match.git
cd ai-smart-match
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup environment
cp .env.template .env
# Edit .env with your API keys

# Test the system
python api_example.py
```

### Running Tests
```bash
python -m pytest  # If tests are added
python api_example.py  # Manual testing
```

## Code Style

- Use descriptive variable names
- Keep functions focused and small
- Add type hints where helpful
- Use docstrings for functions and classes

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.

Thank you for contributing! 🎯
