# 📚 API Reference

This document provides detailed information about the Jarvis Voice Assistant API and its components.

## 🏗️ **Core Architecture**

### **SkillManager**
The central component that manages all skills and their execution.

```python
class SkillManager:
    def __init__(self):
        self.skills = []
        self.skill_registry = SkillRegistry(self)
    
    def register_skill(self, skill: BaseSkill) -> None:
        """Register a new skill with the manager."""
        
    def execute_best_skill(self, context: SkillContext) -> SkillResult:
        """Execute the best matching skill for the given context."""
```

### **SkillContext**
Contains the context information for skill execution.

```python
@dataclass
class SkillContext:
    user_input: str
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
```

### **SkillResult**
The result returned by skill execution.

```python
@dataclass
class SkillResult:
    success: bool
    message: str
    data: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0
    skill_name: str = ""
    error: Optional[str] = None
```

## 🎯 **Base Skill Interface**

All skills inherit from the `BaseSkill` class:

```python
class BaseSkill(ABC):
    def __init__(self, priority: SkillPriority = SkillPriority.NORMAL):
        self.name = self.__class__.__name__.lower().replace('skill', '')
        self.priority = priority
    
    @abstractmethod
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle the given context."""
        
    @abstractmethod
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute the skill with the given context."""
```

## 🧠 **Available Skills**

### **1. Web Browser Skill**
Handles web browsing and search operations.

**Commands:**
- `"search for [query]"` - Google search
- `"open [website]"` - Open specific website
- `"browse the web"` - Open Google homepage
- `"open YouTube"` - Open YouTube
- `"search images of [query]"` - Google Images search

**Methods:**
```python
def _handle_web_search(self, user_input: str) -> SkillResult
def _handle_open_website(self, user_input: str) -> SkillResult
def _handle_youtube(self, user_input: str) -> SkillResult
def _handle_image_search(self, user_input: str) -> SkillResult
```

### **2. File Management Skill**
Manages file operations and file system interactions.

**Commands:**
- `"find [file type] files"` - Search for files
- `"show files in [directory]"` - List directory contents
- `"open file [filename]"` - Open specific file
- `"create folder [name]"` - Create new folder

**Methods:**
```python
def _handle_file_search(self, context: SkillContext) -> SkillResult
def _handle_file_list(self, context: SkillContext) -> SkillResult
def _handle_file_open(self, context: SkillContext) -> SkillResult
def _handle_file_management(self, context: SkillContext) -> SkillResult
```

### **3. App Launcher Skill**
Launches and manages applications.

**Commands:**
- `"open [app name]"` - Launch application
- `"show running apps"` - List running processes
- `"close [app name]"` - Close application

**Methods:**
```python
def _handle_launch_app(self, context: SkillContext) -> SkillResult
def _handle_list_running_apps(self, context: SkillContext) -> SkillResult
def _handle_close_app(self, context: SkillContext) -> SkillResult
```

### **4. Weather & News Skill**
Provides weather information and news updates.

**Commands:**
- `"what's the weather"` - Current weather
- `"weather in [city]"` - Weather for specific city
- `"show news"` - Latest news headlines

**Methods:**
```python
def _handle_weather(self, user_input: str) -> SkillResult
def _handle_news(self, user_input: str) -> SkillResult
def _get_current_location(self) -> str
def _get_weather_data(self, location: str) -> Dict[str, Any]
```

### **5. Todo & Notes Skill**
Manages tasks and notes.

**Commands:**
- `"take a note [content]"` - Create note
- `"add task [description]"` - Add task
- `"show my tasks"` - List tasks
- `"mark task [id] as done"` - Complete task

**Methods:**
```python
def _handle_note_creation(self, user_input: str) -> SkillResult
def _handle_task_management(self, user_input: str) -> SkillResult
def _save_note(self, content: str) -> None
def _load_notes(self) -> List[Dict[str, Any]]
```

### **6. Translation Skill**
Provides language translation services.

**Commands:**
- `"translate [text] to [language]"` - Translate text
- `"how do you say [phrase] in [language]"` - Common phrases

**Methods:**
```python
def _handle_translation(self, user_input: str) -> SkillResult
def _translate_text(self, text: str, target_lang: str) -> str
def _detect_language(self, text: str) -> str
```

### **7. WhatsApp Messaging Skill**
Integrates with WhatsApp for messaging.

**Commands:**
- `"open WhatsApp"` - Open WhatsApp
- `"send message to [name]"` - Send message
- `"show message templates"` - List templates

**Methods:**
```python
def _handle_send_message(self, user_input: str) -> SkillResult
def _handle_message_templates(self, user_input: str) -> SkillResult
def _extract_person_name(self, user_input: str) -> str
def _search_person_in_whatsapp(self, person_name: str) -> None
```

## 🎨 **UI Components**

### **ThemeManager**
Manages UI themes and color schemes.

```python
class ThemeManager:
    def __init__(self):
        self.current_theme = ThemeType.PROFESSIONAL_DARK
        self.themes = self._initialize_themes()
    
    def get_theme_colors(self, theme_type: ThemeType) -> Dict[str, str]:
        """Get color scheme for specified theme."""
        
    def apply_theme(self, theme_type: ThemeType) -> None:
        """Apply theme to UI components."""
```

### **AnimatedStatusIndicator**
Provides animated visual feedback.

```python
class AnimatedStatusIndicator:
    def __init__(self, parent, status: str = "listening"):
        self.status = status
        self.animation_running = False
    
    def start_animation(self) -> None:
        """Start the animation loop."""
        
    def stop_animation(self) -> None:
        """Stop the animation loop."""
        
    def update_status(self, new_status: str) -> None:
        """Update the status and restart animation."""
```

## 🔧 **Configuration**

### **Skill Priority Levels**
```python
class SkillPriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
```

### **Theme Types**
```python
class ThemeType(Enum):
    PROFESSIONAL_DARK = "professional_dark"
    PROFESSIONAL_LIGHT = "professional_light"
    CYBER_PUNK = "cyber_punk"
    OCEAN_BLUE = "ocean_blue"
```

## 📊 **Data Models**

### **Note Structure**
```python
@dataclass
class Note:
    id: str
    content: str
    timestamp: datetime
    tags: List[str] = field(default_factory=list)
```

### **Task Structure**
```python
@dataclass
class Task:
    id: str
    description: str
    completed: bool = False
    priority: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
```

### **Contact Structure**
```python
@dataclass
class Contact:
    name: str
    phone: str
    email: Optional[str] = None
    notes: Optional[str] = None
```

## 🚀 **Usage Examples**

### **Creating a Custom Skill**
```python
from skills.base_skill import BaseSkill, SkillContext, SkillResult
from core.skill_priority import SkillPriority

class CustomSkill(BaseSkill):
    def __init__(self):
        super().__init__(priority=SkillPriority.NORMAL)
        self.name = "custom"
    
    def can_handle(self, context: SkillContext) -> bool:
        return "custom command" in context.user_input.lower()
    
    def execute(self, context: SkillContext) -> SkillResult:
        return SkillResult(
            success=True,
            message="Custom skill executed successfully!",
            data={"input": context.user_input},
            execution_time=0.0,
            skill_name=self.name
        )
```

### **Registering a Skill**
```python
from main_professional_ui import JarvisVoiceAssistantPro

# Initialize the assistant
app = JarvisVoiceAssistantPro()

# Create and register custom skill
custom_skill = CustomSkill()
app.skill_manager.register_skill(custom_skill)
```

### **Handling Voice Input**
```python
def process_voice_input(self, audio_data: bytes) -> str:
    """Process voice input and return transcribed text."""
    try:
        # Convert audio to text
        text = self.speech_recognizer.recognize_google(audio_data)
        
        # Create context
        context = SkillContext(
            user_input=text,
            confidence=0.9,
            metadata={"source": "voice"}
        )
        
        # Execute best matching skill
        result = self.skill_manager.execute_best_skill(context)
        
        return result.message
        
    except Exception as e:
        return f"Error processing voice input: {str(e)}"
```

## 🔍 **Error Handling**

### **Common Exceptions**
```python
class VoiceAssistantError(Exception):
    """Base exception for voice assistant errors."""
    pass

class SkillExecutionError(VoiceAssistantError):
    """Error during skill execution."""
    pass

class SpeechRecognitionError(VoiceAssistantError):
    """Error during speech recognition."""
    pass

class SkillNotFoundError(VoiceAssistantError):
    """No skill found to handle the request."""
    pass
```

### **Error Response Format**
```python
def create_error_response(error: Exception, skill_name: str) -> SkillResult:
    return SkillResult(
        success=False,
        message=f"Sorry, I encountered an error: {str(error)}",
        data={"error_type": type(error).__name__},
        execution_time=0.0,
        skill_name=skill_name,
        error=str(error)
    )
```

## 📈 **Performance Metrics**

### **Skill Execution Metrics**
- **Response Time**: Average time to execute a skill
- **Success Rate**: Percentage of successful executions
- **Error Rate**: Percentage of failed executions
- **Memory Usage**: Memory consumption per skill

### **Voice Recognition Metrics**
- **Accuracy**: Recognition accuracy percentage
- **Latency**: Time from speech to text
- **Confidence**: Average confidence score

## 🔐 **Security Considerations**

### **Input Validation**
- Sanitize all user inputs
- Validate file paths and URLs
- Check for malicious commands

### **API Security**
- Rate limiting for external APIs
- Secure storage of API keys
- Input validation for API calls

### **File System Security**
- Restrict file access to safe directories
- Validate file operations
- Prevent directory traversal attacks

## 📝 **Best Practices**

### **Skill Development**
1. **Single Responsibility**: Each skill should have one clear purpose
2. **Error Handling**: Always handle exceptions gracefully
3. **Input Validation**: Validate all inputs before processing
4. **Documentation**: Document all public methods and classes
5. **Testing**: Write comprehensive tests for all functionality

### **Performance Optimization**
1. **Lazy Loading**: Load resources only when needed
2. **Caching**: Cache frequently accessed data
3. **Async Operations**: Use async for I/O operations
4. **Memory Management**: Properly manage memory usage

### **Code Quality**
1. **Type Hints**: Use type hints for better code clarity
2. **Docstrings**: Write clear docstrings for all functions
3. **Code Style**: Follow PEP 8 style guidelines
4. **Testing**: Maintain high test coverage

---

<div align="center">

**For more information, see the [User Guide](USER_GUIDE.md) and [Contributing Guidelines](../CONTRIBUTING.md)**

</div>