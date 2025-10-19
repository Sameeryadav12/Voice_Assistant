# 🤝 Contributing to Jarvis Voice Assistant

Thank you for your interest in contributing to Jarvis Voice Assistant! This guide will help you get started with development and understand our contribution process.

---

## 📋 Table of Contents

- [Getting Started](#-getting-started)
- [Development Setup](#-development-setup)
- [Code Style](#-code-style)
- [Testing](#-testing)
- [Pull Request Process](#-pull-request-process)
- [Issue Guidelines](#-issue-guidelines)
- [Feature Requests](#-feature-requests)
- [Documentation](#-documentation)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of Python, audio processing, and UI development
- Familiarity with voice assistants and NLP concepts

### Development Environment

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/sigma-voice-assistant.git
   cd sigma-voice-assistant
   ```

2. **Create development branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\Activate.ps1  # Windows
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

---

## 🛠️ Development Setup

### Project Structure

```
sigma-voice-assistant/
├── 📁 audio/                  # Audio processing
├── 📁 core/                   # Core algorithms
├── 📁 nlp/                    # Natural language processing
├── 📁 skills/                 # Skill implementations
├── 📁 docs/                   # Documentation
├── 📁 tests/                  # Test files
├── 📁 examples/               # Example scripts
├── 🎮 main_professional_ui.py # Main application
├── 📋 requirements.txt        # Dependencies
├── 📋 requirements-dev.txt    # Dev dependencies
└── 📖 README.md              # Project overview
```

### Development Dependencies

Create `requirements-dev.txt`:

```txt
# Testing
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0

# Code Quality
black>=22.0.0
flake8>=5.0.0
mypy>=1.0.0
isort>=5.10.0

# Documentation
sphinx>=5.0.0
sphinx-rtd-theme>=1.0.0

# Development Tools
pre-commit>=2.20.0
jupyter>=1.0.0
```

### Pre-commit Hooks

Set up pre-commit hooks for code quality:

```bash
pip install pre-commit
pre-commit install
```

This will automatically run:
- Black (code formatting)
- Flake8 (linting)
- isort (import sorting)
- MyPy (type checking)

---

## 📝 Code Style

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# Use type hints
def process_audio(audio_data: bytes, sample_rate: int) -> str:
    """Process audio data and return text.
    
    Args:
        audio_data: Raw audio bytes
        sample_rate: Sample rate in Hz
        
    Returns:
        Recognized text
        
    Raises:
        AudioError: If audio processing fails
    """
    # Implementation here
    pass

# Use descriptive variable names
user_input = "Hey Jarvis, what time is it?"
current_time = datetime.now()

# Use constants for magic numbers
DEFAULT_SAMPLE_RATE = 16000
MAX_AUDIO_LENGTH = 10  # seconds
```

### Naming Conventions

- **Classes**: PascalCase (`VoiceAssistant`, `AudioProcessor`)
- **Functions/Methods**: snake_case (`process_audio`, `get_current_time`)
- **Variables**: snake_case (`user_input`, `audio_data`)
- **Constants**: UPPER_SNAKE_CASE (`DEFAULT_SAMPLE_RATE`, `MAX_RETRIES`)
- **Private methods**: Leading underscore (`_internal_method`)

### Documentation

Use Google-style docstrings:

```python
def recognize_speech(audio_data: bytes, language: str = "en-US") -> str:
    """Recognize speech from audio data.
    
    Args:
        audio_data: Raw audio bytes from microphone
        language: Language code for recognition (default: "en-US")
        
    Returns:
        Recognized text string
        
    Raises:
        RecognitionError: If speech recognition fails
        AudioError: If audio data is invalid
        
    Example:
        >>> audio = get_audio_from_mic()
        >>> text = recognize_speech(audio)
        >>> print(text)
        "Hello world"
    """
    pass
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sigma_voice_assistant

# Run specific test file
pytest tests/test_audio_processing.py

# Run with verbose output
pytest -v
```

### Writing Tests

Create test files in the `tests/` directory:

```python
# tests/test_audio_processing.py
import pytest
from audio.input_handler import AudioProcessor

class TestAudioProcessor:
    def test_resample_audio(self):
        """Test audio resampling functionality."""
        processor = AudioProcessor()
        # Test implementation
        
    def test_voice_activity_detection(self):
        """Test voice activity detection."""
        processor = AudioProcessor()
        # Test implementation
        
    @pytest.mark.parametrize("sample_rate,expected", [
        (44100, 16000),
        (48000, 16000),
        (16000, 16000),
    ])
    def test_resample_rates(self, sample_rate, expected):
        """Test resampling with different input rates."""
        processor = AudioProcessor()
        result = processor.resample_audio(b"test", sample_rate, 16000)
        assert result is not None
```

### Test Categories

- **Unit Tests** - Test individual functions and methods
- **Integration Tests** - Test component interactions
- **UI Tests** - Test user interface functionality
- **Performance Tests** - Test system performance
- **Audio Tests** - Test audio processing pipeline

---

## 🔄 Pull Request Process

### Before Submitting

1. **Update documentation** for any new features
2. **Add tests** for new functionality
3. **Run all tests** to ensure nothing is broken
4. **Update CHANGELOG.md** with your changes
5. **Check code style** with pre-commit hooks

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] UI tested on different screen sizes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** on different platforms
4. **Documentation** review
5. **Approval** and merge

---

## 🐛 Issue Guidelines

### Bug Reports

Use the bug report template:

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10, macOS 12]
- Python: [e.g., 3.9.7]
- Version: [e.g., 1.0.0]

## Additional Context
Any other relevant information
```

### Feature Requests

Use the feature request template:

```markdown
## Feature Description
Clear description of the feature

## Use Case
Why is this feature needed?

## Proposed Solution
How should this work?

## Alternatives
Other solutions considered

## Additional Context
Any other relevant information
```

---

## 🎯 Feature Requests

### Areas for Contribution

- **New Skills** - Add new voice commands
- **UI Improvements** - Enhance user interface
- **Audio Processing** - Improve speech recognition
- **Performance** - Optimize system performance
- **Documentation** - Improve guides and references
- **Testing** - Add more test coverage
- **Platform Support** - Add support for new platforms

### Skill Development

To add a new skill:

1. **Create skill file** in `skills/` directory
2. **Inherit from BaseSkill**
3. **Implement required methods**
4. **Add tests**
5. **Update documentation**

```python
# skills/weather_skill.py
from skills.base_skill import BaseSkill

class WeatherSkill(BaseSkill):
    def __init__(self):
        super().__init__("weather")
        self.keywords = ["weather", "temperature", "forecast"]
        self.description = "Get weather information"
    
    def execute(self, intent: str, entities: dict) -> str:
        # Implementation here
        return "Weather information here"
```

---

## 📚 Documentation

### Documentation Standards

- **User-facing docs** - Clear, simple language
- **Technical docs** - Detailed, accurate
- **Code comments** - Explain complex logic
- **Examples** - Show how to use features

### Documentation Types

- **User Guide** - How to use the application
- **API Reference** - Technical documentation
- **Developer Guide** - How to contribute
- **Troubleshooting** - Common problems and solutions

### Updating Documentation

1. **Identify** what needs updating
2. **Write** clear, accurate content
3. **Test** examples and code snippets
4. **Review** for clarity and completeness
5. **Update** related documentation

---

## 🏷️ Release Process

### Version Numbering

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR** - Breaking changes
- **MINOR** - New features, backward compatible
- **PATCH** - Bug fixes, backward compatible

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers updated
- [ ] Release notes prepared
- [ ] Tag created
- [ ] Release published

---

## 🤔 Questions?

### Getting Help

- **GitHub Discussions** - Ask questions and share ideas
- **GitHub Issues** - Report bugs and request features
- **Discord** - Real-time chat (if available)
- **Email** - Contact maintainers directly

### Resources

- [Python Style Guide](https://pep8.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Semantic Versioning](https://semver.org/)
- [Contributing to Open Source](https://opensource.guide/how-to-contribute/)

---

## 🙏 Recognition

### Contributors

We recognize all contributors in:
- **README.md** - Contributor list
- **CHANGELOG.md** - Release notes
- **GitHub** - Contributor graphs

### Types of Contributions

- **Code** - Bug fixes, features, improvements
- **Documentation** - Guides, references, examples
- **Testing** - Test cases, bug reports
- **Design** - UI/UX improvements
- **Community** - Helping other users

---

## 📄 License

By contributing to Jarvis Voice Assistant, you agree that your contributions will be licensed under the MIT License.

---

## 🎉 Thank You!

Thank you for contributing to Jarvis Voice Assistant! Your contributions help make this project better for everyone.

**Happy coding!** 🚀

---

*For questions about contributing, please open a GitHub issue or start a discussion.*
