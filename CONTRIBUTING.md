# 🤝 Contributing to Jarvis Voice Assistant

Thank you for your interest in contributing to Jarvis Voice Assistant! We welcome contributions from the community and appreciate your help in making this project better.

## 📋 **Table of Contents**

- [Code of Conduct](#-code-of-conduct)
- [Getting Started](#-getting-started)
- [How to Contribute](#-how-to-contribute)
- [Development Setup](#-development-setup)
- [Coding Standards](#-coding-standards)
- [Pull Request Process](#-pull-request-process)
- [Issue Reporting](#-issue-reporting)
- [Feature Requests](#-feature-requests)

---

## 📜 **Code of Conduct**

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [conduct@jarvis-assistant.com](mailto:conduct@jarvis-assistant.com).

### **Our Pledge**
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what's best for the community
- Show empathy towards other community members

---

## 🚀 **Getting Started**

### **Prerequisites**
- Python 3.8 or higher
- Git
- A GitHub account
- Basic understanding of Python and voice assistant concepts

### **Fork and Clone**
1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/yourusername/jarvis-voice-assistant.git
   cd jarvis-voice-assistant
   ```
3. **Add upstream** remote:
   ```bash
   git remote add upstream https://github.com/originalusername/jarvis-voice-assistant.git
   ```

---

## 🔧 **How to Contribute**

### **Types of Contributions**
- **Bug Fixes** - Fix existing issues
- **New Features** - Add new skills or capabilities
- **Documentation** - Improve docs, comments, or README
- **Testing** - Add or improve tests
- **UI/UX** - Enhance the user interface
- **Performance** - Optimize code and improve speed

### **Contribution Process**
1. **Check Issues** - Look for existing issues or create new ones
2. **Create Branch** - Create a feature branch from `main`
3. **Make Changes** - Implement your changes
4. **Test** - Ensure all tests pass
5. **Commit** - Write clear commit messages
6. **Push** - Push to your fork
7. **Pull Request** - Create a PR with detailed description

---

## 🛠️ **Development Setup**

### **Environment Setup**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### **Running Tests**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_basic.py

# Run with coverage
pytest --cov=.

# Run linting
flake8 .
black --check .
```

### **Running the Application**
```bash
# Main application
python main_professional_ui.py

# Alternative entry points
python main.py
python main_pushtotalk.py
python main_hybrid.py
```

---

## 📝 **Coding Standards**

### **Python Style Guide**
- Follow **PEP 8** style guidelines
- Use **Black** for code formatting
- Use **flake8** for linting
- Maximum line length: **88 characters**
- Use **type hints** where appropriate

### **Code Structure**
- **Functions** - Keep functions small and focused
- **Classes** - Use clear, descriptive names
- **Comments** - Write clear, helpful comments
- **Docstrings** - Use Google-style docstrings

### **Example Code Style**
```python
def process_voice_input(self, audio_data: bytes) -> str:
    """
    Process voice input and return transcribed text.
    
    Args:
        audio_data: Raw audio data from microphone
        
    Returns:
        Transcribed text string
        
    Raises:
        SpeechRecognitionError: If audio cannot be processed
    """
    try:
        # Process audio data
        text = self.speech_recognizer.recognize_google(audio_data)
        return text.strip()
    except Exception as e:
        raise SpeechRecognitionError(f"Failed to process audio: {e}")
```

### **Commit Message Format**
```
type(scope): brief description

Detailed description of changes

Fixes #123
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes
- `refactor` - Code refactoring
- `test` - Test additions/changes
- `chore` - Maintenance tasks

**Examples:**
```
feat(voice): add noise cancellation for better recognition
fix(ui): resolve theme switching crash issue
docs(readme): update installation instructions
```

---

## 🔄 **Pull Request Process**

### **Before Submitting**
- [ ] **Tests Pass** - All tests must pass
- [ ] **Code Style** - Follows project style guidelines
- [ ] **Documentation** - Updated relevant documentation
- [ ] **No Conflicts** - Resolved merge conflicts
- [ ] **Single Focus** - PR addresses one issue/feature

### **PR Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings introduced
```

### **Review Process**
1. **Automated Checks** - CI/CD pipeline runs
2. **Code Review** - Maintainers review code
3. **Testing** - Manual testing if needed
4. **Approval** - At least one approval required
5. **Merge** - Squash and merge to main

---

## 🐛 **Issue Reporting**

### **Bug Reports**
When reporting bugs, please include:

1. **Clear Title** - Brief description of the issue
2. **Steps to Reproduce** - Detailed steps to reproduce
3. **Expected Behavior** - What should happen
4. **Actual Behavior** - What actually happens
5. **Environment** - OS, Python version, etc.
6. **Screenshots** - If applicable
7. **Logs** - Error messages or logs

### **Issue Template**
```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g. Windows 10]
- Python Version: [e.g. 3.9.0]
- Jarvis Version: [e.g. 1.0.0]

**Additional Context**
Any other context about the problem.
```

---

## 💡 **Feature Requests**

### **Feature Request Guidelines**
- **Check Existing Issues** - Search for similar requests
- **Clear Description** - Explain the feature clearly
- **Use Cases** - Provide real-world use cases
- **Mockups** - Include UI mockups if applicable
- **Implementation Ideas** - Suggest implementation approach

### **Feature Request Template**
```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Use Case**
Describe the problem this feature would solve.

**Proposed Solution**
Describe your proposed solution.

**Alternatives**
Describe any alternative solutions you've considered.

**Additional Context**
Any other context or screenshots about the feature request.
```

---

## 🧪 **Testing Guidelines**

### **Test Types**
- **Unit Tests** - Test individual functions/classes
- **Integration Tests** - Test skill interactions
- **UI Tests** - Test user interface components
- **Voice Tests** - Test voice recognition functionality

### **Writing Tests**
```python
import pytest
from skills.weather_news_skill import WeatherNewsSkill

class TestWeatherNewsSkill:
    def test_weather_keywords_detection(self):
        """Test that weather keywords are properly detected."""
        skill = WeatherNewsSkill()
        context = SkillContext("what's the weather today")
        
        assert skill.can_handle(context) == True
    
    def test_weather_api_call(self):
        """Test weather API call functionality."""
        skill = WeatherNewsSkill()
        result = skill._get_weather("New York")
        
        assert result.success == True
        assert "temperature" in result.data
```

---

## 📚 **Documentation Guidelines**

### **Code Documentation**
- **Docstrings** - Use Google-style docstrings
- **Comments** - Explain complex logic
- **Type Hints** - Use type annotations
- **Examples** - Include usage examples

### **README Updates**
- **Installation** - Keep installation steps current
- **Usage** - Update usage examples
- **Features** - Add new features to feature list
- **Screenshots** - Update screenshots for UI changes

---

## 🏷️ **Release Process**

### **Version Numbering**
We use [Semantic Versioning](https://semver.org/):
- **MAJOR** - Breaking changes
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes (backward compatible)

### **Release Checklist**
- [ ] **Tests Pass** - All tests must pass
- [ ] **Documentation Updated** - README and docs updated
- [ ] **Version Bumped** - Version number updated
- [ ] **Changelog Updated** - CHANGELOG.md updated
- [ ] **Tag Created** - Git tag created for release

---

## 🤔 **Questions?**

If you have questions about contributing:

- **GitHub Discussions** - Use GitHub Discussions for general questions
- **Issues** - Create an issue for specific problems
- **Email** - Contact us at [contributors@jarvis-assistant.com](mailto:contributors@jarvis-assistant.com)

---

## 🙏 **Thank You**

Thank you for contributing to Jarvis Voice Assistant! Your contributions help make this project better for everyone.

---

<div align="center">

**Happy Contributing! 🚀**

</div>