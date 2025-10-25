"""
Information skill for providing time, date, and system information.
"""

import os
import platform
import psutil
from datetime import datetime
from typing import Dict, Any
from skills.base_skill import BaseSkill, SkillContext, SkillResult, SkillPriority


class InfoSkill(BaseSkill):
    """
    Skill for providing information like time, date, and system stats.
    """
    
    def __init__(self):
        super().__init__(
            name="info",
            description="Provide time, date, and system information",
            priority=SkillPriority.HIGH
        )
        self.triggers = ["time", "date", "what", "when", "info", "information", "system", "tell"]
        self.required_entities = []
        self.optional_entities = []
    
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle information queries."""
        user_input = context.user_input.lower()
        
        # Time queries - more flexible
        time_keywords = ["time", "hour", "clock", "what time", "what's the time", "current time", "tell me the time"]
        if any(keyword in user_input for keyword in time_keywords):
            return True
        
        # Date queries  
        date_keywords = ["date", "day", "today", "month", "year"]
        if any(keyword in user_input for keyword in date_keywords):
            return True
        
        # System info queries
        system_keywords = ["system info", "system information", "computer info", "pc info", "specs"]
        if any(keyword in user_input for keyword in system_keywords):
            return True
        
        return False
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute information query."""
        user_input = context.user_input.lower()
        
        try:
            # Handle time queries
            if any(word in user_input for word in ["time", "hour", "clock"]):
                return self._get_time()
            
            # Handle date queries
            elif any(word in user_input for word in ["date", "day", "today"]) and "time" not in user_input:
                return self._get_date()
            
            # Handle system info queries
            elif any(word in user_input for word in ["system info", "system information", "computer", "pc info", "specs"]):
                return self._get_system_info()
            
            else:
                return SkillResult(
                    success=False,
                    message="I'm not sure what information you're looking for.",
                    data={},
                    execution_time=0.0,
                    skill_name=self.name,
                    error="Unknown query type"
                )
        
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Sorry, I couldn't get that information: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _get_time(self) -> SkillResult:
        """Get current time."""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")  # 12-hour format with AM/PM
        
        return SkillResult(
            success=True,
            message=f"The current time is {time_str}",
            data={'time': time_str, 'datetime': str(now)},
            execution_time=0.0,
            skill_name=self.name
        )
    
    def _get_date(self) -> SkillResult:
        """Get current date."""
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")  # Like: "Monday, January 15, 2024"
        
        return SkillResult(
            success=True,
            message=f"Today is {date_str}",
            data={'date': date_str, 'datetime': str(now)},
            execution_time=0.0,
            skill_name=self.name
        )
    
    def _get_system_info(self) -> SkillResult:
        """Get system information."""
        try:
            # Get system information
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            system_info = {
                'os': f"{platform.system()} {platform.release()}",
                'processor': platform.processor(),
                'cpu_usage': f"{cpu_percent}%",
                'memory_total': f"{memory.total / (1024**3):.1f} GB",
                'memory_used': f"{memory.used / (1024**3):.1f} GB",
                'memory_percent': f"{memory.percent}%",
                'disk_total': f"{disk.total / (1024**3):.1f} GB",
                'disk_used': f"{disk.used / (1024**3):.1f} GB",
                'disk_percent': f"{disk.percent}%"
            }
            
            message = f"System Information:\n"
            message += f"OS: {system_info['os']}\n"
            message += f"CPU Usage: {system_info['cpu_usage']}\n"
            message += f"Memory: {system_info['memory_used']} / {system_info['memory_total']} ({system_info['memory_percent']})\n"
            message += f"Disk: {system_info['disk_used']} / {system_info['disk_total']} ({system_info['disk_percent']})"
            
            return SkillResult(
                success=True,
                message=message,
                data=system_info,
                execution_time=0.0,
                skill_name=self.name
            )
        
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Could not retrieve system information: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )


