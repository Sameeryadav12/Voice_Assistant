# Project Structure

Complete overview of all files and directories in Sigma Voice Assistant.

---

## 📁 Directory Structure

```
voice_assistant/
│
├── 📁 audio/                    # Audio processing components
│   ├── input_handler.py         # Microphone input, VAD, audio capture
│   └── output_handler.py        # Text-to-speech, audio playback
│
├── 📁 core/                     # Core algorithms and data structures
│   ├── trie.py                  # Trie-based keyword matching
│   ├── state_machine.py         # Dialogue state management
│   ├── scheduler.py             # Priority-based task scheduling
│   ├── cache.py                 # LRU cache implementation
│   └── graph_search.py          # Graph-based file/app search
│
├── 📁 nlp/                      # Natural language processing
│   ├── speech_to_text.py        # Speech recognition engines
│   ├── intent_classifier.py    # Intent classification (ML)
│   └── text_processor.py       # Text preprocessing
│
├── 📁 skills/                   # Skill implementations
│   ├── base_skill.py            # Skill framework and manager
│   ├── reminder_skill.py        # Reminder and scheduling
│   ├── file_skill.py            # File search and management
│   ├── app_skill.py             # Application launching and control
│   ├── info_skill.py            # Time, date, system information
│   └── help_skill.py            # Help and guidance
│
├── 📁 docs/                     # Documentation
│   ├── README.md                # Documentation index
│   ├── QUICK_START_GUIDE.md    # 5-minute guide
│   ├── HOW_TO_USE.md            # Complete user guide
│   ├── TROUBLESHOOTING.md       # Problem solving
│   ├── ACCENT_FIXES.md          # Accent handling details
│   ├── FIXES_APPLIED.md         # Technical changes
│   ├── FINAL_SOLUTION.md        # Complete overview
│   ├── MICROPHONE_ISSUE_SOLUTION.md  # Mic troubleshooting
│   ├── PROJECT_STRUCTURE.md     # This file
│   ├── START_ASSISTANT.md       # Getting started
│   ├── TEST_COMMANDS.txt        # Command reference
│   └── FINAL_STEPS.txt          # Step-by-step instructions
│
├── 📁 tests/                    # Testing and diagnostic tools
│   ├── test_microphone_volume.py        # Test mic levels
│   ├── test_speech_recognition.py       # Test recognition
│   ├── select_microphone.py             # Find best microphone
│   ├── test_all_microphones.py          # Test all mics
│   ├── test_voice_assistant_microphone.py
│   ├── voice_calibration.py             # Voice training
│   ├── train_voice_auto.py              # Auto voice training
│   └── ...
│
├── 📁 examples/                 # Example and demo files
│   ├── run_demo.py              # Demo script
│   └── main_keyboard.py         # Keyboard-only demo
│
├── 📄 Main Application Files
│   ├── main_pushtotalk.py       # ⭐ Push-to-talk mode (RECOMMENDED)
│   ├── main_combined.py         # Combined keyboard + voice
│   ├── main_hybrid.py           # Keyboard-only mode
│   └── main.py                  # Original voice-only mode
│
├── 📄 Configuration Files
│   ├── requirements.txt         # Python dependencies
│   ├── setup.py                 # Package setup
│   └── .gitignore               # Git ignore rules
│
├── 📄 Documentation Files
│   ├── README.md                # Main project README
│   ├── CHANGELOG.md             # Version history
│   ├── CONTRIBUTING.md          # Contribution guidelines
│   └── LICENSE                  # MIT License
│
└── 📄 Other Files
    ├── QUICK_START.md           # Quick start (legacy)
    └── venv/                    # Virtual environment (not in git)
```

---

## 📝 File Descriptions

### Main Application Files

#### `main_pushtotalk.py` ⭐ **RECOMMENDED**
- **Purpose:** Push-to-talk voice assistant
- **Best for:** All users, all microphones
- **Features:** Hold button to speak, type commands
- **Reliability:** Highest

#### `main_combined.py`
- **Purpose:** Combined keyboard and continuous voice
- **Best for:** Users who want both input methods
- **Features:** Type OR click "Start Listening"
- **Reliability:** High (good VAD required)

#### `main_hybrid.py`
- **Purpose:** Keyboard-only mode
- **Best for:** No microphone or testing
- **Features:** Type all commands
- **Reliability:** 100% (no audio needed)

#### `main.py`
- **Purpose:** Original voice-only mode
- **Best for:** Good microphones only
- **Features:** Continuous listening
- **Reliability:** Medium (depends on mic quality)

---

### Core Components

#### Audio Module (`audio/`)
**input_handler.py** (408 lines)
- Audio capture from microphone
- Voice Activity Detection (VAD)
- Audio buffering and processing
- Sample rate detection and conversion
- Noise filtering
- 28,000x audio boost

**output_handler.py** (408 lines)
- Text-to-speech synthesis
- Audio playback
- Voice customization
- Multiple TTS engines

#### Core Algorithms (`core/`)
**trie.py** (337 lines)
- Advanced Trie data structure
- Aho-Corasick multi-pattern matching
- Fuzzy matching with Levenshtein distance
- Wake word detection
- O(m) keyword matching

**state_machine.py** (~300 lines)
- Finite State Machine for dialogue
- Event-driven state transitions
- Context management

**scheduler.py** (~400 lines)
- Priority Heap implementation
- Task scheduling with priorities
- Recurring task support
- Reminder management

**cache.py** (~200 lines)
- LRU Cache implementation
- O(1) cache operations
- Multiple cache strategies

**graph_search.py** (~500 lines)
- Graph-based file system representation
- BFS/DFS algorithms
- Application discovery
- Path finding

#### NLP Module (`nlp/`)
**speech_to_text.py** (446 lines)
- Multi-engine speech recognition
- Google Speech API integration
- PocketSphinx offline recognition
- Audio preprocessing
- Confidence scoring
- Caching

**intent_classifier.py** (~300 lines)
- Hybrid ML intent classification
- Entity extraction
- Pattern matching
- Context awareness

**text_processor.py** (~200 lines)
- Text normalization
- Tokenization
- Stopword removal

---

### Skills Module (`skills/`)

Each skill follows the same pattern:
1. Inherit from `BaseSkill`
2. Implement `can_handle()` - Check if skill applies
3. Implement `execute()` - Execute the skill
4. Return `SkillResult` - Success/failure with message

**Skill Files:**
- `base_skill.py` - Framework (SkillManager, SkillRegistry)
- `reminder_skill.py` - Set and manage reminders
- `file_skill.py` - File search and operations
- `app_skill.py` - Launch and control applications
- `info_skill.py` - Time, date, system information
- `help_skill.py` - Show help and capabilities

---

### Documentation (`docs/`)

**For Users:**
- `QUICK_START_GUIDE.md` - 5-minute quick start
- `HOW_TO_USE.md` - Complete usage guide
- `TEST_COMMANDS.txt` - All available commands
- `TROUBLESHOOTING.md` - Problem solving

**For Developers:**
- `FIXES_APPLIED.md` - All technical improvements
- `PROJECT_STRUCTURE.md` - This file
- `README.md` - Documentation index

**Technical Details:**
- `ACCENT_FIXES.md` - Accent handling implementation
- `FINAL_SOLUTION.md` - Complete technical overview
- `MICROPHONE_ISSUE_SOLUTION.md` - Mic troubleshooting

---

### Tests (`tests/`)

**Diagnostic Tools:**
- `test_microphone_volume.py` - Test mic levels
- `select_microphone.py` - Find best microphone
- `test_speech_recognition.py` - Test recognition

**Calibration Tools:**
- `voice_calibration.py` - Voice training
- `train_voice_auto.py` - Automatic training

**Unit Tests:**
- Various test files for components

---

## 📊 Code Statistics

### By Module

| Module | Files | Lines | Purpose |
|--------|-------|-------|---------|
| audio/ | 2 | ~800 | Audio I/O |
| core/ | 5 | ~2000 | Algorithms |
| nlp/ | 3 | ~1000 | NLP |
| skills/ | 6 | ~1500 | Skills |
| **Total** | **16** | **~5300** | **Core code** |

### Main Files

| File | Lines | Purpose |
|------|-------|---------|
| main_pushtotalk.py | ~300 | Push-to-talk mode |
| main_combined.py | ~350 | Combined mode |
| main_hybrid.py | ~400 | Keyboard mode |
| main.py | ~560 | Voice mode |

---

## 🔗 Dependencies

### Core Dependencies
```
speech_recognition>=3.10.0  # Speech recognition
pyaudio>=0.2.13             # Audio I/O
numpy>=1.24.0               # Audio processing
scipy>=1.10.0               # Signal processing
```

### NLP Dependencies
```
nltk>=3.8.1                 # Natural language toolkit
scikit-learn>=1.3.0         # Machine learning
```

### Audio Processing
```
webrtcvad>=2.0.10           # Voice activity detection
pocketsphinx>=5.0.0         # Offline recognition
pyttsx3>=2.90               # Text-to-speech
```

### UI
```
customtkinter>=5.2.0        # Modern UI
```

### System
```
psutil>=5.9.0               # System information
pywin32>=305                # Windows integration (Windows only)
```

---

## 🎯 Key Files to Modify

### Adding New Features

**Add a new skill?**
→ Create file in `skills/`, inherit from `BaseSkill`

**Change audio processing?**
→ Modify `audio/input_handler.py`

**Add wake word variation?**
→ Update `core/trie.py` wake_words set

**Change UI?**
→ Modify main files (`main_pushtotalk.py`, etc.)

---

## 📖 Documentation Guide

### For Users
1. Start with: `README.md`
2. Then read: `docs/QUICK_START_GUIDE.md`
3. For details: `docs/HOW_TO_USE.md`
4. If issues: `docs/TROUBLESHOOTING.md`

### For Developers
1. Architecture: `README.md` (Architecture section)
2. Code details: `docs/FIXES_APPLIED.md`
3. Contributing: `CONTRIBUTING.md`
4. Structure: `docs/PROJECT_STRUCTURE.md` (this file)

---

## 🔄 Update Frequency

### Regular Updates
- `CHANGELOG.md` - After each release
- `requirements.txt` - When dependencies change
- `README.md` - For major features

### As Needed
- Documentation files - When features change
- Test files - When adding new tests
- Examples - When adding demos

---

**This structure keeps the project organized and easy to navigate!**

