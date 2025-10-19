# 🏗️ Architecture Overview

This document provides a high-level overview of the Jarvis Voice Assistant architecture and design decisions.

## 📊 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   UI Layer      │    │  Core Engine    │    │  Audio Layer    │
│                 │    │                 │    │                 │
│ • CustomTkinter │◄──►│ • State Machine │◄──►│ • PyAudio       │
│ • Chat Bubbles  │    │ • Scheduler     │    │ • WebRTC VAD    │
│ • Push-to-Talk  │    │ • Cache         │    │ • Resampling    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  NLP Pipeline   │    │  Skill System   │    │  File System    │
│                 │    │                 │    │                 │
│ • STT Engine    │    │ • Base Skill    │    │ • Graph Search  │
│ • Intent Class  │    │ • 8 Skills      │    │ • File Discovery│
│ • Text Process  │    │ • Plugin Arch   │    │ • App Launcher  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🧩 Core Components

### 1. UI Layer (`main_professional_ui.py`)
- **CustomTkinter** - Modern UI framework
- **Chat Interface** - WhatsApp-style conversation bubbles
- **Push-to-Talk** - Hold button to speak
- **Real-time Status** - Animated status indicators

### 2. Core Engine (`core/`)
- **State Machine** - Dialogue flow management
- **Scheduler** - Priority-based task scheduling
- **Cache** - LRU cache for performance
- **Trie** - O(m) keyword matching

### 3. Audio Layer (`audio/`)
- **PyAudio** - Audio I/O operations
- **WebRTC VAD** - Voice activity detection
- **Resampling** - Audio format conversion
- **Enhancement** - Noise reduction and normalization

### 4. NLP Pipeline (`nlp/`)
- **Speech-to-Text** - Google/Sphinx recognition
- **Intent Classification** - ML-based intent detection
- **Text Processing** - Preprocessing and normalization

### 5. Skill System (`skills/`)
- **Base Skill** - Abstract skill interface
- **8 Functional Skills** - Time, reminders, files, apps, etc.
- **Plugin Architecture** - Extensible skill system

## 🔄 Data Flow

```
User Input → Audio Capture → VAD → Buffer → Resample → STT → NLP → Intent → Skill → Response → UI
```

## 📁 Directory Structure

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
└── 📖 README.md              # Project overview
```

## 🎯 Design Patterns

- **Plugin Architecture** - Extensible skill system
- **Observer Pattern** - Event-driven callbacks
- **Strategy Pattern** - Multiple recognition engines
- **Factory Pattern** - Skill creation and registration
- **Singleton Pattern** - Resource management

## ⚡ Performance Optimizations

- **LRU Caching** - O(1) cache operations
- **Priority Scheduling** - O(log n) task management
- **Trie Matching** - O(m) wake word detection
- **Audio Resampling** - Efficient audio processing
- **Memory Management** - Automatic cleanup

## 🔧 Configuration

- **Environment Variables** - Runtime configuration
- **Settings Panel** - User-configurable options
- **Audio Settings** - Microphone and volume control
- **UI Settings** - Theme and display options

## 🧪 Testing Strategy

- **Unit Tests** - Individual component testing
- **Integration Tests** - Component interaction testing
- **UI Tests** - User interface testing
- **Performance Tests** - System performance testing
- **Audio Tests** - Audio processing pipeline testing

## 📚 Documentation

- **User Guide** - End-user documentation
- **API Reference** - Developer documentation
- **Troubleshooting** - Problem-solving guide
- **Performance Guide** - Optimization tips
- **Contributing Guide** - Development guidelines

---

*For detailed technical information, see [API Reference](docs/API_REFERENCE.md)*
