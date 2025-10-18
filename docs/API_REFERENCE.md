# 🔧 API Reference - Sigma Voice Assistant

This document provides technical details about the Sigma Voice Assistant architecture, APIs, and implementation.

---

## 📋 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Core Components](#-core-components)
- [Audio Processing](#-audio-processing)
- [NLP Pipeline](#-nlp-pipeline)
- [Skill System](#-skill-system)
- [UI Framework](#-ui-framework)
- [Data Structures](#-data-structures)
- [Configuration](#-configuration)
- [Error Handling](#-error-handling)

---

## 🏗️ Architecture Overview

### System Design

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

### Design Patterns

- **Plugin Architecture** - Extensible skill system
- **Observer Pattern** - Event-driven callbacks
- **Strategy Pattern** - Multiple recognition engines
- **Factory Pattern** - Skill creation and registration
- **State Machine** - Dialogue flow management

---

## 🧩 Core Components

### 1. State Machine (`core/state_machine.py`)

Manages dialogue states and transitions.

```python
class StateMachine:
    def __init__(self):
        self.current_state = "idle"
        self.states = {
            "idle": self._idle_state,
            "listening": self._listening_state,
            "processing": self._processing_state,
            "responding": self._responding_state
        }
    
    def transition(self, new_state: str):
        """Transition to new state"""
        if new_state in self.states:
            self.current_state = new_state
            self.states[new_state]()
```

**States:**
- `idle` - Waiting for input
- `listening` - Recording audio
- `processing` - Understanding command
- `responding` - Generating response

### 2. Scheduler (`core/scheduler.py`)

Priority-based task scheduling using binary heap.

```python
class PriorityScheduler:
    def __init__(self):
        self.heap = []
        self.counter = 0
    
    def schedule_task(self, task, priority: int, delay: float = 0):
        """Schedule task with priority and optional delay"""
        heapq.heappush(self.heap, (priority, self.counter, time.time() + delay, task))
        self.counter += 1
```

**Features:**
- O(log n) insertion and extraction
- Priority-based execution
- Delayed task support
- Thread-safe operations

### 3. Cache (`core/cache.py`)

LRU cache implementation for performance optimization.

```python
class LRUCache:
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.cache = {}
        self.access_order = []
    
    def get(self, key):
        """Get value from cache, update access order"""
        if key in self.cache:
            self._update_access(key)
            return self.cache[key]
        return None
```

**Features:**
- O(1) get and put operations
- Automatic eviction of least recently used items
- Configurable capacity
- Thread-safe implementation

### 4. Trie (`core/trie.py`)

Efficient keyword matching for wake word detection.

```python
class Trie:
    def __init__(self):
        self.root = {}
        self.end_marker = "*"
    
    def insert(self, word: str):
        """Insert word into trie"""
        node = self.root
        for char in word.lower():
            if char not in node:
                node[char] = {}
            node = node[char]
        node[self.end_marker] = True
```

**Features:**
- O(m) search time where m is word length
- Case-insensitive matching
- Multiple wake word variations
- Memory efficient

---

## 🎵 Audio Processing

### Audio Pipeline

```
Microphone → PyAudio → VAD → Buffer → Resample → STT → NLP
     ↓           ↓       ↓       ↓        ↓       ↓     ↓
  Raw Audio → Chunks → Speech → Audio → 16kHz → Text → Intent
```

### Voice Activity Detection

```python
class VoiceActivityDetector:
    def __init__(self, sample_rate: int = 16000):
        self.vad = webrtcvad.Vad(2)  # Aggressiveness level 2
        self.sample_rate = sample_rate
        self.frame_duration = 30  # ms
        self.frame_size = int(sample_rate * self.frame_duration / 1000)
    
    def is_speech(self, audio_chunk: bytes) -> bool:
        """Detect if audio chunk contains speech"""
        return self.vad.is_speech(audio_chunk, self.sample_rate)
```

**Features:**
- WebRTC VAD integration
- Configurable aggressiveness
- Real-time processing
- Noise filtering

### Audio Resampling

```python
def resample_audio(audio_data: bytes, from_rate: int, to_rate: int) -> bytes:
    """Resample audio from one sample rate to another"""
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    resampled = librosa.resample(
        audio_array.astype(np.float32), 
        orig_sr=from_rate, 
        target_sr=to_rate
    )
    return resampled.astype(np.int16).tobytes()
```

**Features:**
- Automatic sample rate detection
- High-quality resampling with librosa
- Support for various input formats
- Memory efficient processing

---

## 🧠 NLP Pipeline

### Speech-to-Text

```python
class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engines = ["google", "sphinx"]
    
    def recognize(self, audio_data: bytes) -> str:
        """Convert audio to text using multiple engines"""
        try:
            # Try Google first (more accurate)
            return self.recognizer.recognize_google(audio_data)
        except:
            # Fallback to Sphinx (offline)
            return self.recognizer.recognize_sphinx(audio_data)
```

**Engines:**
- **Google Speech API** - High accuracy, requires internet
- **Sphinx** - Offline, lower accuracy
- **Hybrid approach** - Google primary, Sphinx fallback

### Intent Classification

```python
class IntentClassifier:
    def __init__(self):
        self.classifier = Pipeline([
            ("tfidf", TfidfVectorizer()),
            ("classifier", MultinomialNB())
        ])
        self.intents = ["time", "reminder", "app_launch", "file_search", "help"]
    
    def classify(self, text: str) -> str:
        """Classify user intent from text"""
        features = self.classifier.named_steps["tfidf"].transform([text])
        prediction = self.classifier.named_steps["classifier"].predict(features)
        return self.intents[prediction[0]]
```

**Features:**
- TF-IDF vectorization
- Naive Bayes classification
- Multiple intent categories
- Confidence scoring

### Text Processing

```python
class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
    
    def preprocess(self, text: str) -> str:
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        
        # Remove stop words
        words = [word for word in text.split() if word not in self.stop_words]
        
        # Lemmatize
        words = [self.lemmatizer.lemmatize(word) for word in words]
        
        return ' '.join(words)
```

**Features:**
- Text normalization
- Stop word removal
- Lemmatization
- Punctuation handling

---

## 🎯 Skill System

### Base Skill Class

```python
class BaseSkill:
    def __init__(self, name: str):
        self.name = name
        self.keywords = []
        self.description = ""
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """Check if skill can handle the intent"""
        return intent in self.keywords
    
    def execute(self, intent: str, entities: dict) -> str:
        """Execute the skill and return response"""
        raise NotImplementedError
    
    def get_help(self) -> str:
        """Return help text for this skill"""
        return self.description
```

### Skill Registration

```python
class SkillManager:
    def __init__(self):
        self.skills = {}
    
    def register_skill(self, skill: BaseSkill):
        """Register a new skill"""
        self.skills[skill.name] = skill
    
    def get_skill(self, intent: str, entities: dict) -> BaseSkill:
        """Find appropriate skill for intent"""
        for skill in self.skills.values():
            if skill.can_handle(intent, entities):
                return skill
        return None
```

### Available Skills

1. **TimeSkill** - Time and date information
2. **ReminderSkill** - Set and manage reminders
3. **AppSkill** - Launch applications
4. **FileSkill** - File search and operations
5. **InfoSkill** - System information
6. **HelpSkill** - Help and documentation

---

## 🎨 UI Framework

### CustomTkinter Integration

```python
class ProfessionalUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.setup_theme()
        self.setup_ui()
    
    def setup_theme(self):
        """Configure dark theme"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    
    def setup_ui(self):
        """Create UI components"""
        self.create_header()
        self.create_conversation_panel()
        self.create_control_panel()
```

### Color Scheme

```python
class Colors:
    # Primary colors
    PRIMARY = "#6366f1"
    PRIMARY_DARK = "#4f46e5"
    PRIMARY_LIGHT = "#818cf8"
    
    # Background colors
    BG_DARK = "#1e1e2e"
    BG_MEDIUM = "#2a2a3e"
    BG_LIGHT = "#3a3a4e"
    
    # Text colors
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#a0a0a0"
    
    # Status colors
    SUCCESS = "#10b981"
    WARNING = "#f59e0b"
    DANGER = "#ef4444"
    INFO = "#3b82f6"
```

### Animation System

```python
class AnimatedButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        """Hover animation"""
        self.configure(fg_color=self.hover_color)
    
    def _on_leave(self, event):
        """Leave animation"""
        self.configure(fg_color=self.fg_color)
```

---

## 📊 Data Structures

### Graph Search (`core/graph_search.py`)

```python
class FileSystemGraph:
    def __init__(self, root_path: str):
        self.graph = {}
        self.root = root_path
        self.build_graph()
    
    def build_graph(self):
        """Build graph representation of file system"""
        for root, dirs, files in os.walk(self.root):
            for name in files + dirs:
                path = os.path.join(root, name)
                self.graph[path] = {
                    'type': 'file' if os.path.isfile(path) else 'dir',
                    'size': os.path.getsize(path) if os.path.isfile(path) else 0,
                    'modified': os.path.getmtime(path)
                }
    
    def search(self, query: str) -> List[str]:
        """Search for files matching query"""
        results = []
        query_lower = query.lower()
        for path, metadata in self.graph.items():
            if query_lower in path.lower():
                results.append(path)
        return sorted(results, key=lambda x: self.graph[x]['modified'], reverse=True)
```

**Features:**
- BFS/DFS traversal
- Metadata caching
- Fuzzy matching
- Performance optimization

---

## ⚙️ Configuration

### Environment Variables

```bash
# Audio settings
AUDIO_SAMPLE_RATE=16000
AUDIO_CHUNK_SIZE=2048
VAD_AGGRESSIVENESS=2

# Speech recognition
STT_ENGINE=google
STT_LANGUAGE=en-US
STT_TIMEOUT=10

# UI settings
UI_THEME=dark
UI_ANIMATIONS=true
UI_AUTO_SCROLL=true

# Performance
CACHE_SIZE=100
MAX_CONCURRENT_TASKS=5
```

### Configuration Class

```python
class Config:
    def __init__(self):
        self.audio = AudioConfig()
        self.speech = SpeechConfig()
        self.ui = UIConfig()
        self.performance = PerformanceConfig()
    
    def load_from_file(self, filepath: str):
        """Load configuration from JSON file"""
        with open(filepath, 'r') as f:
            config = json.load(f)
            self._update_from_dict(config)
    
    def save_to_file(self, filepath: str):
        """Save configuration to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
```

---

## 🚨 Error Handling

### Exception Hierarchy

```python
class SigmaError(Exception):
    """Base exception for Sigma Voice Assistant"""
    pass

class AudioError(SigmaError):
    """Audio processing errors"""
    pass

class RecognitionError(SigmaError):
    """Speech recognition errors"""
    pass

class SkillError(SigmaError):
    """Skill execution errors"""
    pass

class UIError(SigmaError):
    """UI-related errors"""
    pass
```

### Error Recovery

```python
def safe_execute(func, *args, **kwargs):
    """Execute function with error recovery"""
    try:
        return func(*args, **kwargs)
    except AudioError as e:
        logger.error(f"Audio error: {e}")
        return "Audio error - please check your microphone"
    except RecognitionError as e:
        logger.error(f"Recognition error: {e}")
        return "Couldn't understand - please try again"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "Something went wrong - please try again"
```

---

## 📈 Performance Metrics

### Monitoring

```python
class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'recognition_time': [],
            'response_time': [],
            'memory_usage': [],
            'cpu_usage': []
        }
    
    def record_metric(self, metric_name: str, value: float):
        """Record performance metric"""
        if metric_name in self.metrics:
            self.metrics[metric_name].append(value)
    
    def get_average(self, metric_name: str) -> float:
        """Get average value for metric"""
        if metric_name in self.metrics and self.metrics[metric_name]:
            return sum(self.metrics[metric_name]) / len(self.metrics[metric_name])
        return 0.0
```

### Optimization

- **Caching** - LRU cache for frequent operations
- **Lazy loading** - Load components on demand
- **Threading** - Background processing for heavy operations
- **Memory management** - Automatic cleanup of unused objects

---

## 🔌 Extensibility

### Adding New Skills

```python
class CustomSkill(BaseSkill):
    def __init__(self):
        super().__init__("custom")
        self.keywords = ["custom", "special"]
        self.description = "Custom skill for special operations"
    
    def execute(self, intent: str, entities: dict) -> str:
        """Implement custom functionality"""
        return "Custom skill executed successfully"

# Register the skill
skill_manager.register_skill(CustomSkill())
```

### Adding New UI Components

```python
class CustomWidget(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.setup_widget()
    
    def setup_widget(self):
        """Setup custom widget components"""
        pass
```

---

## 📚 Dependencies

### Core Dependencies

```
customtkinter>=5.2.0
speechrecognition>=3.10.0
pyaudio>=0.2.11
webrtcvad>=2.0.10
librosa>=0.10.0
numpy>=1.24.0
scipy>=1.10.0
scikit-learn>=1.3.0
nltk>=3.8.1
```

### Optional Dependencies

```
pygame>=2.1.0  # For audio feedback
matplotlib>=3.6.0  # For visualizations
pandas>=1.5.0  # For data analysis
```

---

## 🧪 Testing

### Unit Tests

```python
def test_trie_insertion():
    trie = Trie()
    trie.insert("hello")
    assert trie.search("hello") == True
    assert trie.search("world") == False

def test_voice_activity_detection():
    vad = VoiceActivityDetector()
    # Test with sample audio data
    assert vad.is_speech(sample_audio) == True
```

### Integration Tests

```python
def test_full_pipeline():
    assistant = SigmaVoiceAssistant()
    response = assistant.process_command("Hey Sigma, what time is it?")
    assert "time" in response.lower()
```

---

## 📖 Conclusion

This API reference provides comprehensive technical documentation for the Sigma Voice Assistant. The system is designed with modularity, extensibility, and performance in mind.

**Key Features:**
- **Modular Architecture** - Easy to extend and modify
- **Advanced Algorithms** - Efficient data structures and algorithms
- **Real-time Processing** - Low-latency audio and text processing
- **Error Recovery** - Robust error handling and recovery
- **Performance Monitoring** - Built-in metrics and optimization

For more information, see:
- [User Guide](USER_GUIDE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Performance Guide](PERFORMANCE.md)
