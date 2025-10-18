# Contributing to Sigma Voice Assistant

Thank you for your interest in contributing to Sigma Voice Assistant! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs
1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/voice_assistant/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Relevant logs or error messages

### Suggesting Enhancements
1. Open an issue with tag `enhancement`
2. Describe the feature and its benefits
3. Provide examples of how it would work
4. Discuss implementation approach

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add AmazingFeature'`)
6. Push to your fork (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

---

## 🏗️ Development Setup

### 1. Clone and Setup
```bash
git clone https://github.com/yourusername/voice_assistant.git
cd voice_assistant
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### 2. Run Tests
```bash
python tests/test_microphone_volume.py
python tests/test_speech_recognition.py
```

### 3. Run the Assistant
```bash
python main_pushtotalk.py
```

---

## 📝 Code Style

### Python Style Guide
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and under 50 lines when possible
- Use type hints where applicable

### Example
```python
def process_audio(self, audio_data: bytes) -> Optional[str]:
    """
    Process audio data and return recognized text.
    
    Args:
        audio_data: Raw audio bytes from microphone
        
    Returns:
        Recognized text or None if recognition fails
    """
    # Implementation here
    pass
```

---

## 🧪 Testing

### Adding Tests
- All new features should include tests
- Place tests in `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test function names

### Running Tests
```bash
# Test microphone
python tests/test_microphone_volume.py

# Test speech recognition
python tests/test_speech_recognition.py

# Select microphone
python tests/select_microphone.py
```

---

## 🎯 Areas for Contribution

### High Priority
- [ ] Whisper integration for offline speech recognition
- [ ] Multi-language support
- [ ] Voice training system
- [ ] Improved accent handling
- [ ] macOS and Linux support

### Medium Priority
- [ ] Cloud sync for reminders
- [ ] Custom wake word support
- [ ] Voice feedback (TTS) improvements
- [ ] Mobile companion app
- [ ] Web interface

### Low Priority
- [ ] Plugin marketplace
- [ ] Voice analytics
- [ ] Performance optimizations
- [ ] UI themes
- [ ] Easter eggs

---

## 📂 File Organization

### Adding New Skills
1. Create skill file in `skills/` directory
2. Inherit from `BaseSkill` class
3. Implement `can_handle()` and `execute()` methods
4. Register skill in main files

Example:
```python
from skills.base_skill import BaseSkill, SkillContext, SkillResult

class MyNewSkill(BaseSkill):
    def __init__(self):
        super().__init__(
            name="my_skill",
            description="What this skill does",
            priority=SkillPriority.NORMAL
        )
    
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle the request."""
        return "my_keyword" in context.user_input.lower()
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute the skill."""
        # Implementation
        return SkillResult(success=True, message="Done!")
```

### Adding Documentation
- Place in `docs/` directory
- Use Markdown format
- Include examples
- Update README.md links

---

## 🔍 Code Review Process

### What We Look For
- ✅ Code follows style guidelines
- ✅ Changes are well-tested
- ✅ Documentation is updated
- ✅ No breaking changes (or clearly documented)
- ✅ Commits are clean and descriptive

### Review Timeline
- Initial response: Within 48 hours
- Full review: Within 1 week
- Merge decision: Within 2 weeks

---

## 💡 Tips for Contributors

### Best Practices
1. **Start Small** - Begin with bug fixes or documentation
2. **Ask Questions** - Use discussions for clarifications
3. **Test Thoroughly** - Test on different systems if possible
4. **Document Changes** - Update docs with your changes
5. **Be Patient** - Reviews take time

### Communication
- Be respectful and professional
- Provide context for your changes
- Respond to feedback constructively
- Help others when you can

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🌟 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for their contributions
- Special thanks in documentation

---

## 📧 Contact

Questions about contributing?
- Open a [Discussion](https://github.com/yourusername/voice_assistant/discussions)
- Create an [Issue](https://github.com/yourusername/voice_assistant/issues)

---

Thank you for contributing to Sigma Voice Assistant! 🎉

