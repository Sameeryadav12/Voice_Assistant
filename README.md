# 🎤 Sigma Voice Assistant

**A sophisticated voice-controlled assistant with advanced data structures, machine learning, and natural language processing.**

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Status](https://img.shields.io/badge/status-working-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

### 🎯 Core Capabilities
- **Voice Recognition** - Push-to-talk mode for accurate speech capture
- **Text Input** - Type commands for instant response
- **8 Functional Skills** - Reminders, file search, app launching, system info, and more
- **Accent Support** - Handles multiple pronunciations and accents
- **Multi-mode Operation** - Keyboard, voice, or combined modes

### 🧠 Advanced Technologies
- **Trie-based Keyword Matching** - Efficient wake word detection
- **Finite State Machine** - Dialogue flow management
- **Priority Heap Scheduling** - Task scheduling with priorities
- **LRU Cache** - Performance optimization
- **Graph-based Search** - File system and application discovery
- **Machine Learning** - Intent classification
- **Voice Activity Detection** - Smart speech detection
- **Audio Resampling** - Automatic sample rate conversion

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 (macOS and Linux support in development)
- Working microphone (optional - keyboard mode available)
- Internet connection (for Google Speech Recognition)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/voice_assistant.git
cd voice_assistant
```

2. **Create virtual environment**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the assistant**
```bash
python main_pushtotalk.py
```

---

## 🎮 Usage

### Push-to-Talk Mode (Recommended)
```bash
python main_pushtotalk.py
```
- **Hold** the green button while speaking
- **Release** when done
- Works best for all microphones!

### Combined Mode
```bash
python main_combined.py
```
- Type OR speak commands
- Continuous voice listening

### Hybrid Mode (Keyboard Only)
```bash
python main_hybrid.py
```
- Type all commands
- 100% reliable, no microphone needed

---

## 📝 Example Commands

```
Hey Sigma, what time is it?
Hey Sigma, show system information
Hey Sigma, set a reminder for 5 minutes
Hey Sigma, remind me to call John at 3pm
Hey Sigma, open calculator
Hey Sigma, open chrome
Hey Sigma, search for files
Hey Sigma, find files with report in the name
Hey Sigma, what can you do?
```

---

## 🛠️ Project Structure

```
voice_assistant/
├── audio/                  # Audio processing components
│   ├── input_handler.py   # Audio capture & VAD
│   └── output_handler.py  # Text-to-speech
├── core/                   # Core algorithms
│   ├── trie.py            # Keyword matching
│   ├── state_machine.py   # Dialogue management
│   ├── scheduler.py       # Task scheduling
│   ├── cache.py           # LRU cache
│   └── graph_search.py    # Graph algorithms
├── nlp/                    # Natural language processing
│   ├── speech_to_text.py  # Speech recognition
│   ├── intent_classifier.py # Intent classification
│   └── text_processor.py  # Text preprocessing
├── skills/                 # Skill implementations
│   ├── base_skill.py      # Skill framework
│   ├── reminder_skill.py  # Reminders & scheduling
│   ├── file_skill.py      # File operations
│   ├── app_skill.py       # Application control
│   ├── info_skill.py      # Time, date, system info
│   └── help_skill.py      # Help system
├── docs/                   # Documentation
│   ├── HOW_TO_USE.md      # User guide
│   ├── TROUBLESHOOTING.md # Problem solving
│   └── ...
├── tests/                  # Testing utilities
│   ├── test_microphone_volume.py
│   └── ...
├── examples/               # Example scripts
├── main_pushtotalk.py     # Push-to-talk mode (recommended)
├── main_combined.py       # Combined keyboard + voice
├── main_hybrid.py         # Keyboard-only mode
├── main.py                # Original voice-only mode
└── requirements.txt       # Dependencies
```

---

## 🎯 Skills Available

### 1. **Info Skill**
- Get current time
- Get current date
- View system information (CPU, memory, disk)

### 2. **Reminder Skill**
- Set reminders with natural language
- Recurring reminders
- View upcoming reminders

### 3. **File Search Skill**
- Search files by name
- Find files with specific content
- Navigate file system

### 4. **App Launcher Skill**
- Open applications (Calculator, Chrome, Notepad, etc.)
- Close applications
- List running apps

### 5. **Help Skill**
- Show available commands
- Display capabilities

---

## 🔧 Advanced Features

### Audio Processing
- **Sample Rate Auto-Detection** - Automatically detects and converts microphone sample rates
- **28,000x Audio Boost** - Works with low-gain microphones
- **Noise Filtering** - Ignores background noise below threshold
- **Voice Activity Detection** - Smart speech detection using WebRTC VAD

### Wake Word Detection
- **Multiple Variations** - Handles different pronunciations
- **Accent Support** - Recognizes "Hey Sigma", "asigma", "hair sigma", etc.
- **Trie-based Matching** - Fast O(m) keyword detection

### Intent Classification
- **Hybrid ML Approach** - Combines rule-based and ML classification
- **Entity Extraction** - Automatically extracts time, app names, filenames
- **Context Awareness** - Maintains dialogue state

---

## 🐛 Troubleshooting

### Voice Recognition Issues

**Problem:** Microphone not working
- **Solution 1:** Use keyboard mode (`python main_hybrid.py`)
- **Solution 2:** Run `python tests/select_microphone.py` to find best mic
- **Solution 3:** Enable Microphone Boost in Windows Sound Settings

**Problem:** Wrong words recognized
- **Solution:** Use Push-to-Talk mode for better accuracy
- **Reason:** Accent variations are normal - system accepts them

**Problem:** "Network error"
- **Solution:** Check internet connection (Google API needs internet)
- **Alternative:** Use keyboard mode (works offline)

For more help, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 📚 Documentation

- **[How to Use](docs/HOW_TO_USE.md)** - Complete user guide
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Fixes Applied](docs/FIXES_APPLIED.md)** - Technical details of all improvements
- **[Accent Support](docs/ACCENT_FIXES.md)** - How accent handling works

---

## 🧪 Testing

### Test Your Microphone
```bash
python tests/test_microphone_volume.py
```

### Select Best Microphone
```bash
python tests/select_microphone.py
```

### Run All Tests
```bash
python tests/test_speech_recognition.py
```

---

## 🏗️ Architecture

### Data Structures
- **Trie** - O(m) keyword matching
- **Priority Heap** - O(log n) task scheduling  
- **LRU Cache** - O(1) cache operations
- **Graph** - BFS/DFS for file system navigation
- **Finite State Machine** - Dialogue state management

### Design Patterns
- **Plugin Architecture** - Extensible skill system
- **Observer Pattern** - Event-driven callbacks
- **Strategy Pattern** - Multiple recognition engines
- **Factory Pattern** - Skill creation and registration

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **SpeechRecognition** - Python speech recognition library
- **PyAudio** - Audio I/O
- **WebRTC VAD** - Voice activity detection
- **Google Speech API** - Speech recognition engine
- **PocketSphinx** - Offline speech recognition
- **CustomTkinter** - Modern UI framework

---

## 📊 Project Statistics

- **Lines of Code:** ~5,000+
- **Skills:** 8 functional skills
- **Data Structures:** 6 advanced implementations
- **Audio Modes:** 3 (Push-to-talk, Continuous, Keyboard)
- **Wake Word Variations:** 14+ supported
- **Test Files:** 10+
- **Documentation Files:** 10+

---

## 🎯 Roadmap

### Completed ✅
- [x] Voice recognition with multiple modes
- [x] 8 functional skills
- [x] Accent support
- [x] Push-to-talk mode
- [x] Keyboard mode
- [x] File search
- [x] App launching
- [x] Reminders
- [x] System information

### Future Enhancements 🚀
- [ ] Offline speech recognition (Whisper integration)
- [ ] Multi-language support
- [ ] Voice training for personalization
- [ ] Cloud sync for reminders
- [ ] Mobile app companion
- [ ] Custom wake word training
- [ ] Voice feedback (TTS responses)

---

## 💬 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/voice_assistant/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/voice_assistant/discussions)
- **Documentation:** [docs/](docs/)

---

## ⭐ Show Your Support

If you find this project useful, please consider:
- Giving it a ⭐ on GitHub
- Sharing it with others
- Contributing improvements
- Reporting issues

---

**Made with ❤️ and Python**

*A demonstration of advanced algorithms, data structures, and AI integration in a practical application.*

