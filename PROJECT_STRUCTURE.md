# 📁 Project Structure

This document provides a detailed overview of the Jarvis Voice Assistant project structure and organization.

## 🏗️ **Directory Structure**

```
jarvis-voice-assistant/
├── 📁 .github/                          # GitHub configuration
│   └── 📁 workflows/                    # GitHub Actions workflows
│       └── 📄 ci.yml                    # CI/CD pipeline configuration
├── 📁 audio/                            # Audio processing modules
│   ├── 📄 __init__.py                   # Audio package initialization
│   ├── 📄 input_handler.py              # Voice input handling
│   └── 📄 output_handler.py             # Text-to-speech output
├── 📁 core/                             # Core system components
│   ├── 📄 __init__.py                   # Core package initialization
│   ├── 📄 cache.py                      # Caching system
│   ├── 📄 graph_search.py               # File system graph search
│   ├── 📄 scheduler.py                  # Task scheduling
│   ├── 📄 state_machine.py              # State management
│   └── 📄 trie.py                       # Trie data structure
├── 📁 docs/                             # Documentation
│   ├── 📁 screenshots/                  # UI screenshots
│   ├── 📁 demo/                         # Demo videos and examples
│   ├── 📄 API_REFERENCE.md              # API documentation
│   ├── 📄 CONTRIBUTING.md               # Contribution guidelines
│   ├── 📄 PERFORMANCE.md                # Performance optimization guide
│   ├── 📄 TROUBLESHOOTING.md            # Troubleshooting guide
│   └── 📄 USER_GUIDE.md                 # User manual
├── 📁 examples/                         # Example usage
│   ├── 📄 main_keyboard.py              # Keyboard input example
│   ├── 📄 run_demo.py                   # Demo runner
│   └── 📄 README.md                     # Examples documentation
├── 📁 nlp/                              # Natural language processing
│   ├── 📄 __init__.py                   # NLP package initialization
│   ├── 📄 intent_classifier.py          # Intent recognition
│   ├── 📄 speech_to_text.py             # Speech recognition
│   └── 📄 text_processor.py             # Text processing
├── 📁 skills/                           # Modular skill system
│   ├── 📄 __init__.py                   # Skills package initialization
│   ├── 📄 base_skill.py                 # Base skill class
│   ├── 📄 file_skill.py                 # File operations
│   ├── 📄 app_skill.py                  # Application control
│   ├── 📄 weather_news_skill.py         # Weather & news
│   ├── 📄 todo_notes_skill.py           # Task management
│   ├── 📄 web_browser_skill.py          # Web browsing
│   ├── 📄 music_media_skill.py          # Media control
│   ├── 📄 whatsapp_messaging_skill.py   # WhatsApp integration
│   ├── 📄 calendar_email_skill.py       # Calendar & email
│   ├── 📄 translation_skill.py          # Language translation
│   ├── 📄 conversation_memory_skill.py  # Memory system
│   ├── 📄 info_skill.py                 # System information
│   └── 📄 help_skill.py                 # Help & support
├── 📁 tests/                            # Test suite
│   ├── 📄 __init__.py                   # Tests package initialization
│   ├── 📄 test_basic.py                 # Basic functionality tests
│   ├── 📄 test_speech_recognition.py    # Speech recognition tests
│   ├── 📄 test_voice_assistant_microphone.py # Microphone tests
│   ├── 📄 test_microphone_devices.py    # Microphone device tests
│   ├── 📄 test_microphone_volume.py     # Microphone volume tests
│   ├── 📄 test_simple.py                # Simple functionality tests
│   ├── 📄 test_minimal.py               # Minimal functionality tests
│   ├── 📄 test_ultra_simple.py          # Ultra-simple tests
│   ├── 📄 test_super_simple.py          # Super-simple tests
│   ├── 📄 test_direct_recognition.py    # Direct recognition tests
│   ├── 📄 test_speech_direct.py         # Direct speech tests
│   ├── 📄 test_stereo_mix.py            # Stereo mix tests
│   ├── 📄 test_all_microphones.py       # All microphones tests
│   ├── 📄 test_microphone_volume.py     # Microphone volume tests
│   ├── 📄 test_speech_recognition.py    # Speech recognition tests
│   ├── 📄 test_voice_assistant_microphone.py # Voice assistant microphone tests
│   ├── 📄 train_my_voice.py             # Voice training
│   ├── 📄 train_voice_auto.py           # Automatic voice training
│   ├── 📄 voice_calibration.py          # Voice calibration
│   ├── 📄 check_microphone_volume.py    # Microphone volume check
│   ├── 📄 fix_microphone_windows.py     # Windows microphone fix
│   ├── 📄 select_microphone.py          # Microphone selection
│   └── 📄 README.md                     # Test documentation
├── 📁 ui/                               # User interface components
│   ├── 📄 __init__.py                   # UI package initialization
│   ├── 📄 theme_manager.py              # Theme management
│   ├── 📄 animated_status.py            # Status indicators
│   ├── 📄 progress_widget.py            # Progress bars
│   └── 📄 skill_widget.py               # Skill buttons
├── 📁 venv/                             # Virtual environment
│   ├── 📁 Include/                      # Python includes
│   ├── 📁 Lib/                          # Python libraries
│   ├── 📁 Scripts/                      # Python scripts
│   └── 📄 pyvenv.cfg                    # Virtual environment config
├── 📄 .gitignore                        # Git ignore rules
├── 📄 ARCHITECTURE.md                   # System architecture
├── 📄 CHANGELOG.md                      # Version history
├── 📄 CONTRIBUTING.md                   # Contribution guidelines
├── 📄 LICENSE                           # MIT License
├── 📄 PROJECT_STRUCTURE.md              # This file
├── 📄 PROJECT_SUMMARY.md                # Project overview
├── 📄 README.md                         # Main documentation
├── 📄 RUN_ME.bat                        # Windows batch runner
├── 📄 TEST_COMMANDS.txt                 # Test commands list
├── 📄 main.py                           # Basic entry point
├── 📄 main_hybrid.py                    # Hybrid entry point
├── 📄 main_professional_ui.py           # Professional UI entry point
├── 📄 main_pushtotalk.py                # Push-to-talk entry point
├── 📄 pytest.ini                       # Pytest configuration
├── 📄 requirements.txt                  # Python dependencies
├── 📄 requirements-dev.txt              # Development dependencies
└── 📄 setup.py                          # Package setup
```

## 📋 **File Descriptions**

### **Root Level Files**

#### **Main Entry Points**
- **`main_professional_ui.py`**: Main application with professional UI
- **`main.py`**: Basic application entry point
- **`main_pushtotalk.py`**: Push-to-talk interface
- **`main_hybrid.py`**: Hybrid interface combining multiple modes

#### **Configuration Files**
- **`requirements.txt`**: Production dependencies
- **`requirements-dev.txt`**: Development dependencies
- **`setup.py`**: Package setup and distribution
- **`pytest.ini`**: Pytest configuration
- **`.gitignore`**: Git ignore rules

#### **Documentation Files**
- **`README.md`**: Main project documentation
- **`LICENSE`**: MIT License
- **`CONTRIBUTING.md`**: Contribution guidelines
- **`CHANGELOG.md`**: Version history
- **`ARCHITECTURE.md`**: System architecture
- **`PROJECT_STRUCTURE.md`**: This file
- **`PROJECT_SUMMARY.md`**: Project overview

#### **Utility Files**
- **`RUN_ME.bat`**: Windows batch file for easy execution
- **`TEST_COMMANDS.txt`**: List of test commands

### **Core Components (`core/`)**

#### **System Core**
- **`cache.py`**: Caching system for performance optimization
- **`graph_search.py`**: File system graph search implementation
- **`scheduler.py`**: Task scheduling and management
- **`state_machine.py`**: State machine for dialogue management
- **`trie.py`**: Trie data structure for efficient text matching

### **Audio Processing (`audio/`)**

#### **Voice Input/Output**
- **`input_handler.py`**: Voice input processing and recognition
- **`output_handler.py`**: Text-to-speech output handling

### **Natural Language Processing (`nlp/`)**

#### **Language Processing**
- **`intent_classifier.py`**: Intent recognition and classification
- **`speech_to_text.py`**: Speech recognition implementation
- **`text_processor.py`**: Text preprocessing and normalization

### **Skills System (`skills/`)**

#### **Base Skill**
- **`base_skill.py`**: Abstract base class for all skills

#### **System Skills**
- **`file_skill.py`**: File operations and management
- **`app_skill.py`**: Application launching and control

#### **Communication Skills**
- **`whatsapp_messaging_skill.py`**: WhatsApp integration
- **`calendar_email_skill.py`**: Calendar and email management

#### **Information Skills**
- **`weather_news_skill.py`**: Weather and news data
- **`translation_skill.py`**: Language translation
- **`info_skill.py`**: System information

#### **Productivity Skills**
- **`todo_notes_skill.py`**: Task and note management
- **`conversation_memory_skill.py`**: Conversation history

#### **Media Skills**
- **`music_media_skill.py`**: Music and media control
- **`web_browser_skill.py`**: Web browsing and search

#### **Support Skills**
- **`help_skill.py`**: Help and support system

### **User Interface (`ui/`)**

#### **UI Components**
- **`theme_manager.py`**: Theme management and switching
- **`animated_status.py`**: Animated status indicators
- **`progress_widget.py`**: Progress bar widgets
- **`skill_widget.py`**: Interactive skill buttons

### **Testing (`tests/`)**

#### **Core Tests**
- **`test_basic.py`**: Basic functionality tests
- **`test_speech_recognition.py`**: Speech recognition tests
- **`test_voice_assistant_microphone.py`**: Microphone tests

#### **Microphone Tests**
- **`test_microphone_devices.py`**: Microphone device tests
- **`test_microphone_volume.py`**: Microphone volume tests
- **`test_all_microphones.py`**: All microphones tests
- **`check_microphone_volume.py`**: Microphone volume check
- **`fix_microphone_windows.py`**: Windows microphone fix
- **`select_microphone.py`**: Microphone selection

#### **Voice Training**
- **`train_my_voice.py`**: Voice training implementation
- **`train_voice_auto.py`**: Automatic voice training
- **`voice_calibration.py`**: Voice calibration

#### **Simple Tests**
- **`test_simple.py`**: Simple functionality tests
- **`test_minimal.py`**: Minimal functionality tests
- **`test_ultra_simple.py`**: Ultra-simple tests
- **`test_super_simple.py`**: Super-simple tests

#### **Direct Tests**
- **`test_direct_recognition.py`**: Direct recognition tests
- **`test_speech_direct.py`**: Direct speech tests
- **`test_stereo_mix.py`**: Stereo mix tests

### **Documentation (`docs/`)**

#### **User Documentation**
- **`USER_GUIDE.md`**: Comprehensive user manual
- **`TROUBLESHOOTING.md`**: Common issues and solutions
- **`PERFORMANCE.md`**: Performance optimization guide

#### **Developer Documentation**
- **`API_REFERENCE.md`**: Technical API documentation
- **`CONTRIBUTING.md`**: Contribution guidelines

#### **Media**
- **`screenshots/`**: UI screenshots
- **`demo/`**: Demo videos and examples

### **Examples (`examples/`)**

#### **Usage Examples**
- **`main_keyboard.py`**: Keyboard input example
- **`run_demo.py`**: Demo runner
- **`README.md`**: Examples documentation

### **GitHub Configuration (`.github/`)**

#### **Workflows**
- **`workflows/ci.yml`**: CI/CD pipeline configuration

## 🔧 **Development Structure**

### **Package Organization**
- **`__init__.py`**: Package initialization files
- **`__pycache__/`**: Python bytecode cache
- **`venv/`**: Virtual environment

### **Dependencies**
- **`requirements.txt`**: Production dependencies
- **`requirements-dev.txt`**: Development dependencies
- **`setup.py`**: Package setup and distribution

### **Configuration**
- **`pytest.ini`**: Pytest configuration
- **`.gitignore`**: Git ignore rules
- **`pyvenv.cfg`**: Virtual environment configuration

## 📊 **File Statistics**

### **Code Distribution**
- **Python Files**: 50+ files
- **Documentation**: 10+ markdown files
- **Configuration**: 5+ config files
- **Tests**: 20+ test files

### **Size Distribution**
- **Core Components**: ~2,000 lines
- **Skills**: ~3,000 lines
- **UI Components**: ~1,000 lines
- **Tests**: ~2,000 lines
- **Documentation**: ~5,000 lines

## 🎯 **Best Practices**

### **File Naming**
- **Snake Case**: Use snake_case for Python files
- **Descriptive Names**: Use descriptive file names
- **Consistent Naming**: Maintain consistent naming conventions

### **Directory Organization**
- **Logical Grouping**: Group related files together
- **Clear Structure**: Maintain clear directory structure
- **Separation of Concerns**: Separate different concerns

### **Documentation**
- **README Files**: Include README files in each directory
- **Inline Comments**: Add inline comments for complex code
- **Docstrings**: Use docstrings for functions and classes

## 🔄 **Maintenance**

### **Regular Updates**
- **Dependencies**: Keep dependencies updated
- **Documentation**: Update documentation regularly
- **Tests**: Maintain test coverage
- **Code Quality**: Ensure code quality standards

### **File Management**
- **Cleanup**: Remove unused files
- **Organization**: Keep files organized
- **Backup**: Regular backup of important files

---

<div align="center">

**For more information, see the [README](README.md) and [Architecture](ARCHITECTURE.md)**

</div>