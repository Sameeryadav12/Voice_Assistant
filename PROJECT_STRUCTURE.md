# 📁 Project Structure

This document provides a detailed overview of the Jarvis Voice Assistant project structure and organization.

## 🏗️ Directory Structure

```
sigma-voice-assistant/
├── 📁 .github/                 # GitHub workflows and templates
│   ├── workflows/             # CI/CD pipelines
│   │   ├── python-app.yml    # Main CI workflow
│   │   └── release.yml       # Release workflow
│   └── ISSUE_TEMPLATE/       # Issue and PR templates
│       ├── bug_report.md     # Bug report template
│       └── feature_request.md # Feature request template
├── 📁 audio/                  # Audio processing components
│   ├── input_handler.py      # Audio capture & VAD
│   └── output_handler.py     # Text-to-speech
├── 📁 core/                   # Core algorithms and data structures
│   ├── trie.py               # Keyword matching (O(m))
│   ├── state_machine.py      # Dialogue management
│   ├── scheduler.py          # Task scheduling (Priority Heap)
│   ├── cache.py              # LRU cache implementation
│   └── graph_search.py       # Graph algorithms for file search
├── 📁 docs/                   # Documentation
│   ├── README.md             # Documentation index
│   ├── USER_GUIDE.md         # Complete user guide
│   ├── API_REFERENCE.md      # Technical documentation
│   ├── TROUBLESHOOTING.md    # Problem solving guide
│   ├── PERFORMANCE.md        # Optimization guide
│   └── CONTRIBUTING.md       # Development guidelines
├── 📁 examples/               # Example scripts and demos
│   ├── README.md             # Examples documentation
│   ├── main_keyboard.py      # Keyboard-only example
│   └── run_demo.py           # Demo script
├── 📁 nlp/                    # Natural language processing
│   ├── speech_to_text.py     # Speech recognition
│   ├── intent_classifier.py  # Intent classification (ML)
│   └── text_processor.py     # Text preprocessing
├── 📁 skills/                 # Skill implementations
│   ├── base_skill.py         # Abstract skill framework
│   ├── reminder_skill.py     # Reminders & scheduling
│   ├── file_skill.py         # File operations
│   ├── app_skill.py          # Application control
│   ├── info_skill.py         # Time, date, system info
│   └── help_skill.py         # Help system
├── 📁 tests/                  # Testing utilities
│   ├── README.md             # Testing documentation
│   ├── test_microphone_volume.py
│   ├── test_speech_recognition.py
│   ├── test_audio_pipeline.py
│   ├── select_microphone.py
│   └── voice_calibration.py
├── 🎮 main_professional_ui.py # Main application (Recommended)
├── 🎮 main_pushtotalk.py     # Push-to-talk mode
├── 🎮 main_hybrid.py         # Keyboard-only mode
├── 🎮 main.py                # Original voice-only mode
├── 📋 requirements.txt       # Production dependencies
├── 📋 requirements-dev.txt   # Development dependencies
├── 📖 README.md              # Project overview
├── 📝 CHANGELOG.md           # Version history
├── 📄 LICENSE                # MIT License
├── 🔧 .gitignore             # Git ignore rules
├── 🏗️ setup.py               # Python package setup
├── 🏗️ ARCHITECTURE.md        # Architecture overview
├── 🤝 CONTRIBUTING.md        # Contribution guidelines
└── 📊 PROJECT_STRUCTURE.md   # This file
```

## 🧩 Component Overview

### Core Application Files

| File | Purpose | Description |
|------|---------|-------------|
| `main_professional_ui.py` | **Main Application** | Modern UI with push-to-talk |
| `main_pushtotalk.py` | **Push-to-Talk Mode** | Precise voice control |
| `main_hybrid.py` | **Keyboard Mode** | Type commands instead of speaking |
| `main.py` | **Original Mode** | Continuous listening mode |

### Core Algorithms (`core/`)

| File | Data Structure | Complexity | Purpose |
|------|----------------|------------|---------|
| `trie.py` | Trie | O(m) | Wake word detection |
| `scheduler.py` | Priority Heap | O(log n) | Task scheduling |
| `cache.py` | LRU Cache | O(1) | Performance optimization |
| `state_machine.py` | FSM | O(1) | Dialogue management |
| `graph_search.py` | Graph | O(V+E) | File system search |

### Audio Processing (`audio/`)

| File | Purpose | Technology |
|------|---------|------------|
| `input_handler.py` | Audio capture | PyAudio + WebRTC VAD |
| `output_handler.py` | Text-to-speech | TTS engines |

### Natural Language Processing (`nlp/`)

| File | Purpose | Technology |
|------|---------|------------|
| `speech_to_text.py` | Speech recognition | Google API + Sphinx |
| `intent_classifier.py` | Intent detection | scikit-learn + NLTK |
| `text_processor.py` | Text preprocessing | NLTK + regex |

### Skills System (`skills/`)

| File | Skill | Commands |
|------|-------|----------|
| `base_skill.py` | Framework | Abstract base class |
| `info_skill.py` | Time & Date | "what time is it?" |
| `reminder_skill.py` | Reminders | "set a reminder" |
| `file_skill.py` | File Search | "find files" |
| `app_skill.py` | App Launcher | "open calculator" |
| `help_skill.py` | Help System | "what can you do?" |

## 📚 Documentation Structure

### User Documentation
- **README.md** - Project overview and quick start
- **docs/USER_GUIDE.md** - Complete user manual
- **docs/TROUBLESHOOTING.md** - Problem solving guide

### Developer Documentation
- **docs/API_REFERENCE.md** - Technical documentation
- **docs/PERFORMANCE.md** - Optimization guide
- **docs/CONTRIBUTING.md** - Development guidelines
- **ARCHITECTURE.md** - System architecture overview

### Project Documentation
- **CHANGELOG.md** - Version history
- **PROJECT_STRUCTURE.md** - This file
- **LICENSE** - MIT License

## 🧪 Testing Structure

### Test Categories
- **Audio Tests** - Microphone and audio processing
- **Speech Tests** - Speech recognition accuracy
- **UI Tests** - User interface functionality
- **Performance Tests** - System performance
- **Integration Tests** - Component interactions

### Test Files
- `test_microphone_volume.py` - Audio level testing
- `test_speech_recognition.py` - Speech recognition testing
- `test_audio_pipeline.py` - Audio processing pipeline
- `select_microphone.py` - Microphone selection utility
- `voice_calibration.py` - Voice training utility

## 🎯 Examples Structure

### Example Scripts
- `main_keyboard.py` - Keyboard-only mode example
- `run_demo.py` - Feature demonstration script

## 🔧 Configuration Files

### Dependencies
- `requirements.txt` - Production dependencies
- `requirements-dev.txt` - Development dependencies

### Project Setup
- `setup.py` - Python package configuration
- `.gitignore` - Git ignore rules
- `LICENSE` - MIT License

### GitHub Integration
- `.github/workflows/` - CI/CD pipelines
- `.github/ISSUE_TEMPLATE/` - Issue templates
- `.github/pull_request_template.md` - PR template

## 📊 File Statistics

### Code Files
- **Python Files**: 25+ core files
- **Documentation**: 10+ markdown files
- **Tests**: 10+ test files
- **Examples**: 2+ example scripts
- **Configuration**: 5+ config files

### Lines of Code
- **Total**: 6,500+ lines
- **Core Logic**: 3,000+ lines
- **UI Code**: 1,500+ lines
- **Documentation**: 2,000+ lines

## 🎯 Design Principles

### Modularity
- **Separate concerns** - Each module has a specific purpose
- **Loose coupling** - Components interact through well-defined interfaces
- **High cohesion** - Related functionality is grouped together

### Extensibility
- **Plugin architecture** - Easy to add new skills
- **Configuration-driven** - Settings can be modified without code changes
- **API-based** - Clear interfaces for integration

### Performance
- **Efficient algorithms** - O(1), O(log n), O(m) complexities
- **Caching** - LRU cache for frequently accessed data
- **Lazy loading** - Load components only when needed

### Maintainability
- **Clear structure** - Logical organization of files
- **Comprehensive documentation** - Every component is documented
- **Testing** - Comprehensive test coverage
- **Code quality** - Linting, formatting, type hints

## 🚀 Getting Started

### For Users
1. **Read README.md** - Project overview
2. **Follow installation guide** - Setup instructions
3. **Try examples** - Run example scripts
4. **Read user guide** - Complete usage instructions

### For Developers
1. **Read CONTRIBUTING.md** - Development guidelines
2. **Set up development environment** - Install dependencies
3. **Read API reference** - Technical documentation
4. **Run tests** - Verify everything works
5. **Start contributing** - Pick an issue or feature

### For Contributors
1. **Fork repository** - Create your own copy
2. **Create feature branch** - Work on your changes
3. **Follow coding standards** - Use provided guidelines
4. **Write tests** - Ensure your code works
5. **Submit pull request** - Share your changes

---

*This structure is designed to be intuitive, maintainable, and scalable. Each component has a clear purpose and well-defined interfaces.*
