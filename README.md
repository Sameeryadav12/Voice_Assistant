# 🎤 Jarvis Voice Assistant - Professional Edition

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![UI](https://img.shields.io/badge/UI-modern--professional-purple)

**A sophisticated voice-controlled assistant with modern UI, advanced data structures, and natural language processing.**

[🚀 Quick Start](#-quick-start) • [📖 Documentation](docs/) • [🎯 Features](#-features) • [🛠️ Installation](#-installation) • [🤝 Contributing](docs/CONTRIBUTING.md)

</div>

---

## ✨ Features

### 🎨 **Modern Professional UI**
- **Beautiful Dark Theme** with purple/green accents
- **Push-to-Talk Interface** - Hold button to speak, release when done
- **Chat Bubbles** - WhatsApp-style conversation display
- **Auto-Scrolling** - Automatic conversation scrolling
- **Quick Actions** - One-click common commands
- **Real-time Status** - Animated status indicators
- **Responsive Design** - Clean 2-panel layout

### 🧠 **Advanced Technologies**
- **Trie-based Keyword Matching** - O(m) wake word detection
- **Finite State Machine** - Dialogue flow management
- **Priority Heap Scheduling** - Task scheduling with priorities
- **LRU Cache** - Performance optimization
- **Graph-based Search** - File system and application discovery
- **Machine Learning** - Intent classification with scikit-learn
- **Voice Activity Detection** - Smart speech detection
- **Audio Resampling** - Automatic sample rate conversion

### 🎯 **8 Functional Skills**
- ⏰ **Time & Date** - Get current time and date
- 💻 **System Info** - CPU, memory, disk information
- ⏲️ **Reminders** - Set and manage reminders
- 📁 **File Search** - Find files by name or content
- 🔢 **App Launcher** - Open applications
- 🎛️ **System Control** - Control system functions
- ❓ **Help System** - Show available commands
- 📊 **Statistics** - Real-time performance metrics

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
git clone https://github.com/yourusername/sigma-voice-assistant.git
cd sigma-voice-assistant
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
python main_professional_ui.py
```

### 🎮 Usage

#### Voice Mode (Push-to-Talk)
1. **Hold** the green "🎤 HOLD TO SPEAK" button
2. **Speak** your command: "Hey Jarvis, what time is it?"
3. **Release** the button when done
4. Watch the response appear as a chat bubble!

#### Text Mode
1. Type your command in the text field
2. Press **Enter** or click **📤 Send**
3. Get instant response!

#### Quick Actions
Click any quick action button for instant commands:
- ⏰ What time is it?
- 💻 System info
- ⏲️ Set reminder
- 🔢 Open calculator

---

## 📝 Example Commands

```bash
# Time & Information
Hey Jarvis, what time is it?
Hey Jarvis, what's the date?
Hey Jarvis, show system information

# Reminders
Hey Jarvis, set a reminder for 5 minutes
Hey Jarvis, remind me to call John in 10 minutes
Hey Jarvis, what reminders do I have?

# Applications
Hey Jarvis, open calculator
Hey Jarvis, launch notepad
Hey Jarvis, open chrome
Hey Jarvis, start command prompt

# File Operations
Hey Jarvis, search for documents
Hey Jarvis, find files with test in the name
Hey Jarvis, search for reports

# Help
Hey Jarvis, what can you do?
Hey Jarvis, help
```

---

## 🛠️ Installation

### Windows (Recommended)

1. **Download Python 3.8+** from [python.org](https://python.org)
2. **Clone this repository**
3. **Open PowerShell** in the project folder
4. **Run setup commands:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main_professional_ui.py
```

### Linux/macOS

```bash
git clone https://github.com/yourusername/sigma-voice-assistant.git
cd sigma-voice-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main_professional_ui.py
```

---

## 📁 Project Structure

```
sigma-voice-assistant/
├── 📁 audio/                  # Audio processing components
│   ├── input_handler.py      # Audio capture & VAD
│   └── output_handler.py     # Text-to-speech
├── 📁 core/                   # Core algorithms
│   ├── trie.py               # Keyword matching
│   ├── state_machine.py      # Dialogue management
│   ├── scheduler.py          # Task scheduling
│   ├── cache.py              # LRU cache
│   └── graph_search.py       # Graph algorithms
├── 📁 nlp/                    # Natural language processing
│   ├── speech_to_text.py     # Speech recognition
│   ├── intent_classifier.py  # Intent classification
│   └── text_processor.py     # Text preprocessing
├── 📁 skills/                 # Skill implementations
│   ├── base_skill.py         # Skill framework
│   ├── reminder_skill.py     # Reminders & scheduling
│   ├── file_skill.py         # File operations
│   ├── app_skill.py          # Application control
│   ├── info_skill.py         # Time, date, system info
│   └── help_skill.py         # Help system
├── 📁 docs/                   # Documentation
│   ├── USER_GUIDE.md         # Complete user guide
│   ├── TROUBLESHOOTING.md    # Problem solving
│   ├── API_REFERENCE.md      # Technical documentation
│   └── CONTRIBUTING.md       # Development guide
├── 📁 tests/                  # Testing utilities
│   ├── test_microphone_volume.py
│   └── test_speech_recognition.py
├── 🎮 main_professional_ui.py # Main application (Recommended)
├── 🎮 main_pushtotalk.py     # Push-to-talk mode
├── 🎮 main_hybrid.py         # Keyboard-only mode
├── 🎮 main.py                # Original voice-only mode
├── 📋 requirements.txt       # Dependencies
└── 📖 README.md              # This file
```

---

## 🎯 Available Modes

| Mode | File | Best For | Description |
|------|------|----------|-------------|
| **🎨 Professional UI** | `main_professional_ui.py` | Daily use, best looking | Modern UI with push-to-talk |
| **⌨️ Keyboard-Only** | `main_hybrid.py` | Most reliable, no mic needed | Type all commands |
| **🎤 Push-to-Talk** | `main_pushtotalk.py` | Precise voice control | Hold button to speak |
| **🔄 Original** | `main.py` | Continuous listening | Always listening mode |

---

## 🔧 Advanced Features

### Audio Processing
- **Sample Rate Auto-Detection** - Automatically detects and converts microphone sample rates
- **Audio Enhancement** - Works with low-gain microphones
- **Noise Filtering** - Ignores background noise below threshold
- **Voice Activity Detection** - Smart speech detection using WebRTC VAD

### Wake Word Detection
- **Multiple Variations** - Handles different pronunciations
- **Accent Support** - Recognizes "Hey Jarvis", "asigma", "hair sigma", etc.
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

### UI Issues

**Problem:** Interface looks broken
- **Solution:** Update CustomTkinter: `pip install --upgrade customtkinter`

**Problem:** Buttons not responding
- **Solution:** Restart the application

For more help, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 📚 Documentation

- **[📖 User Guide](docs/USER_GUIDE.md)** - Complete user guide
- **[🔧 Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[⚙️ API Reference](docs/API_REFERENCE.md)** - Technical documentation
- **[🤝 Contributing](docs/CONTRIBUTING.md)** - Development guidelines
- **[📊 Performance](docs/PERFORMANCE.md)** - Performance optimization guide

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

Contributions are welcome! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

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
- **CustomTkinter** - Modern UI framework
- **scikit-learn** - Machine learning library

---

## 📊 Project Statistics

- **Lines of Code:** ~6,500+
- **Skills:** 8 functional skills
- **Data Structures:** 6 advanced implementations
- **UI Modes:** 4 different interfaces
- **Wake Word Variations:** 14+ supported
- **Test Files:** 10+
- **Documentation Files:** 10+

---

## 🎯 Roadmap

### Completed ✅
- [x] Voice recognition with multiple modes
- [x] 8 functional skills
- [x] Modern professional UI
- [x] Push-to-talk mode
- [x] Auto-scrolling conversation
- [x] File search and app launching
- [x] System information and reminders

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

- **Issues:** [GitHub Issues](https://github.com/yourusername/sigma-voice-assistant/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/sigma-voice-assistant/discussions)
- **Documentation:** [docs/](docs/)

---

## ⭐ Show Your Support

If you find this project useful, please consider:
- Giving it a ⭐ on GitHub
- Sharing it with others
- Contributing improvements
- Reporting issues

---

<div align="center">

**Made with ❤️ and Python**

*A demonstration of advanced algorithms, data structures, and AI integration in a practical application.*

[🚀 Get Started](#-quick-start) • [📖 Read Docs](docs/) • [🐛 Report Issues](https://github.com/yourusername/sigma-voice-assistant/issues)

</div>