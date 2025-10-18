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
I'm Sigma Voice Assistant! Here's what I can do:

🗓️ **Reminders & Scheduling:**
- "Hey Sigma, remind me to call John at 3pm"
- "Hey Sigma, set a reminder for 10 minutes"
- "Hey Sigma, what reminders do I have?"

📁 **File Management:**
- "Hey Sigma, search for my documents"
- "Hey Sigma, find files with 'report' in the name"
- "Hey Sigma, open my downloads folder"

🚀 **Application Control:**
- "Hey Sigma, open calculator"
- "Hey Sigma, launch notepad"
- "Hey Sigma, start Chrome"

⚙️ **System Control:**
- "Hey Sigma, what time is it?"
- "Hey Sigma, show system information"

Just start any command with "Hey Sigma" and I'll help you!
        """
        
        return SkillResult(
            success=True,
            message=help_message.strip(),
            data={"skill_used": "help"},
            execution_time=0.0,
            skill_name=self.name
        )

