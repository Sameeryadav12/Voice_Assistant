"""
Help skill for general queries and information.
"""

from skills.base_skill import BaseSkill, SkillContext, SkillResult, SkillPriority
from typing import Dict, Any


class HelpSkill(BaseSkill):
    """
    Skill for providing help and general information.
    """
    
    def __init__(self):
        super().__init__(
            name="help",
            description="Provide help and general information",
            priority=SkillPriority.NORMAL
        )
        self.triggers = ["help", "what can you do", "capabilities", "features", "commands"]
    
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle the context."""
        user_input = context.user_input.lower()
        
        # Check for help-related keywords
        help_keywords = [
            "help", "what can you do", "capabilities", "features", 
            "commands", "how do you work", "what are you", "assistant"
        ]
        
        return any(keyword in user_input for keyword in help_keywords)
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute the help skill."""
        help_message = """
I'm Jarvis Voice Assistant! Here's what I can do:

🗓️ **Reminders & Scheduling:**
- "Hey Jarvis, remind me to call John at 3pm"
- "Hey Jarvis, set a reminder for 10 minutes"
- "Hey Jarvis, what reminders do I have?"

📁 **File Management:**
- "Hey Jarvis, search for my documents"
- "Hey Jarvis, find files with 'report' in the name"
- "Hey Jarvis, open my downloads folder"

🚀 **Application Control:**
- "Hey Jarvis, open calculator"
- "Hey Jarvis, launch notepad"
- "Hey Jarvis, start Chrome"

⚙️ **System Control:**
- "Hey Jarvis, what time is it?"
- "Hey Jarvis, show system information"

🌤️ **Weather & News:**
- "Hey Jarvis, what's the weather?"
- "Hey Jarvis, weather in London"
- "Hey Jarvis, give me the news"
- "Hey Jarvis, tech news"

📝 **Tasks & Notes:**
- "Hey Jarvis, take a note: buy groceries"
- "Hey Jarvis, add task: finish report"
- "Hey Jarvis, show my tasks"
- "Hey Jarvis, mark task 1 as done"
- "Hey Jarvis, what are my notes?"

🌐 **Web & Search:**
- "Hey Jarvis, search for Python tutorials"
- "Hey Jarvis, open YouTube"
- "Hey Jarvis, Wikipedia Albert Einstein"
- "Hey Jarvis, search images of sunset"

🎵 **Music & Media:**
- "Hey Jarvis, play Bohemian Rhapsody"
- "Hey Jarvis, volume up/down"
- "Hey Jarvis, pause music"
- "Hey Jarvis, open Spotify"

🧠 **Conversation Memory:**
- "Hey Jarvis, do you remember what we talked about?"
- "Hey Jarvis, what did I ask earlier?"
- "Hey Jarvis, conversation history"

🌍 **Translation:**
- "Hey Jarvis, translate hello to Spanish"
- "Hey Jarvis, how do you say thank you in French?"
- "Hey Jarvis, teach me basic German"

Just start any command with "Hey Jarvis" and I'll help you!
        """
        
        return SkillResult(
            success=True,
            message=help_message.strip(),
            data={"skill_used": "help"},
            execution_time=0.0,
            skill_name=self.name
        )

