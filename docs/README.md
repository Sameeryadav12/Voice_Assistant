# Sigma Voice Assistant - Documentation

Welcome to the complete documentation for Sigma Voice Assistant!

---

## 📚 Table of Contents

### Getting Started
- **[Quick Start Guide](../README.md#quick-start)** - Get up and running in 5 minutes
- **[Installation](../README.md#installation)** - Detailed installation instructions
- **[First Steps](FINAL_STEPS.txt)** - Your first commands

### User Guides
- **[How to Use](HOW_TO_USE.md)** - Complete usage guide for all modes
- **[Test Commands](TEST_COMMANDS.txt)** - List of all available commands
- **[Push-to-Talk Guide](START_ASSISTANT.md)** - Using push-to-talk mode

### Troubleshooting
- **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Solutions to common problems
- **[Microphone Issues](MICROPHONE_ISSUE_SOLUTION.md)** - Fixing microphone problems
- **[Accent Support](ACCENT_FIXES.md)** - Understanding accent handling

### Technical Documentation
- **[Fixes Applied](FIXES_APPLIED.md)** - All improvements and bug fixes
- **[Final Solution](FINAL_SOLUTION.md)** - Complete technical overview
- **[Architecture Overview](../README.md#architecture)** - System architecture

---

## 🎮 Usage Modes

### 1. Push-to-Talk Mode (Recommended)
**File:** `main_pushtotalk.py`

**Best for:**
- All microphone types
- Noisy environments
- Accent variations
- Reliable speech capture

**How to use:**
```bash
python main_pushtotalk.py
```
- Hold button → Speak → Release → Get response

---

### 2. Combined Mode
**File:** `main_combined.py`

**Best for:**
- Users who want both keyboard and voice
- Testing different input methods
- Maximum flexibility

**How to use:**
```bash
python main_combined.py
```
- Type OR click "Start Listening" for voice

---

### 3. Hybrid Mode (Keyboard Only)
**File:** `main_hybrid.py`

**Best for:**
- No microphone available
- Quiet environments
- Maximum reliability
- Testing skills

**How to use:**
```bash
python main_hybrid.py
```
- Type all commands

---

## 🎯 Skills Documentation

### Info Skill
**Commands:**
- "Hey Sigma, what time is it?"
- "Hey Sigma, what's the date?"
- "Hey Sigma, show system information"

**Features:**
- Current time in 12-hour format
- Full date with day of week
- System stats (CPU, memory, disk)

---

### Reminder Skill
**Commands:**
- "Hey Sigma, set a reminder for 5 minutes"
- "Hey Sigma, remind me to call John in 10 minutes"
- "Hey Sigma, remind me to take a break at 3pm"
- "Hey Sigma, what reminders do I have?"

**Features:**
- Natural language time parsing
- Multiple time formats supported
- Priority-based scheduling
- Recurring reminders

---

### File Search Skill
**Commands:**
- "Hey Sigma, search for test"
- "Hey Sigma, find files with report in the name"
- "Hey Sigma, locate my documents"

**Features:**
- Graph-based file system search
- Name, content, and type search
- Fast BFS/DFS algorithms

---

### App Launcher Skill
**Commands:**
- "Hey Sigma, open calculator"
- "Hey Sigma, launch notepad"
- "Hey Sigma, open chrome"
- "Hey Sigma, start cmd"

**Supported Apps:**
- Calculator, Notepad, Chrome, Edge, Firefox
- CMD, PowerShell, Explorer
- Paint, Wordpad, Task Manager
- And more!

---

### System Control Skill
**Commands:**
- "Hey Sigma, lock computer" (safe commands only)

**Note:** Dangerous operations (shutdown/restart) show warnings only.

---

### Help Skill
**Commands:**
- "Hey Sigma, what can you do?"
- "Hey Sigma, help"

**Features:**
- Lists all capabilities
- Shows example commands
- Provides usage tips

---

## 🔧 Technical Details

### Audio Pipeline
1. **Microphone Input** → PyAudio captures audio
2. **Sample Rate Detection** → Auto-detect native rate (e.g., 44100Hz)
3. **Resampling** → Convert to 16000Hz for recognition
4. **Audio Enhancement** → 28,000x boost for quiet mics
5. **VAD Processing** → Detect speech vs noise
6. **Speech Recognition** → Google API converts to text
7. **Wake Word Detection** → Trie-based matching
8. **Intent Classification** → ML-based intent detection
9. **Skill Execution** → Route to appropriate skill
10. **Response Generation** → Return result to user

### Data Structures Used
- **Trie** - Keyword matching (O(m) time complexity)
- **Priority Heap** - Task scheduling (O(log n))
- **LRU Cache** - Result caching (O(1) access)
- **Graph** - File system navigation (BFS/DFS)
- **State Machine** - Dialogue management

---

## 🐛 Known Issues & Solutions

### Issue: Microphone Level Too Low
**Symptom:** Audio level shows 1-1000 instead of 10,000+

**Solution:**
1. Use Push-to-Talk mode (works better)
2. Enable Microphone Boost in Windows (+20dB or +30dB)
3. Run `python tests/select_microphone.py` to find best mic

---

### Issue: Wrong Words Recognized
**Symptom:** System hears "play sigma" instead of "hey sigma"

**Solution:**
- This is normal! The system accepts these variations
- 14+ wake word variations are supported
- Including: "play sigma", "hey cig", "asigma", etc.

---

### Issue: Network Errors
**Symptom:** "Could not request results" error

**Solution:**
- Check internet connection
- Google Speech API requires internet
- Use keyboard mode as backup

---

## 📖 Additional Resources

### For Users
- [HOW_TO_USE.md](HOW_TO_USE.md) - Complete user guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problem solving
- [TEST_COMMANDS.txt](TEST_COMMANDS.txt) - Command reference

### For Developers
- [FIXES_APPLIED.md](FIXES_APPLIED.md) - Technical changes
- [Architecture Docs](../README.md#architecture) - System design
- [API Reference](#) - Coming soon

### For Contributors
- [CONTRIBUTING.md](../CONTRIBUTING.md) - This file
- [Code of Conduct](#) - Coming soon
- [Development Roadmap](../README.md#roadmap) - Future plans

---

## 💬 Getting Help

### Questions?
- Check [Troubleshooting Guide](TROUBLESHOOTING.md)
- Search [GitHub Issues](https://github.com/yourusername/voice_assistant/issues)
- Ask in [Discussions](https://github.com/yourusername/voice_assistant/discussions)

### Found a Bug?
- Report in [Issues](https://github.com/yourusername/voice_assistant/issues)
- Include logs and system info
- Describe steps to reproduce

---

## 🎉 Thank You!

Your contributions make this project better for everyone!

---

**Happy Coding! 🚀**

