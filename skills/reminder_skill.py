"""
Reminder management skill using the scheduler system.
Demonstrates integration with core algorithms and practical skill implementation.
"""

import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from skills.base_skill import BaseSkill, SkillContext, SkillResult, SkillPriority
from core.scheduler import PriorityScheduler, TaskPriority, ReminderManager


class ReminderSkill(BaseSkill):
    """
    Skill for managing reminders and scheduled tasks.
    Demonstrates integration with the priority scheduler and time parsing.
    """
    
    def __init__(self, scheduler: PriorityScheduler):
        super().__init__(
            name="reminder",
            description="Manage reminders and scheduled tasks",
            priority=SkillPriority.HIGH
        )
        self.scheduler = scheduler
        self.reminder_manager = ReminderManager(scheduler)
        self.triggers = ["remind", "reminder", "schedule", "alarm", "timer"]
        self.required_entities = []  # Flexible - can work with various inputs
        self.optional_entities = ["time", "duration", "message"]
        
        # Time parsing patterns
        self.time_patterns = [
            r'\b(\d{1,2}):(\d{2})\s*(am|pm)?\b',  # 3:30, 3:30pm
            r'\b(\d{1,2})\s*(am|pm)\b',  # 3pm, 3 am
            r'\b(in|after)\s+(\d+)\s*(minute|hour|day|week|month|year)s?\b',  # in 5 minutes
            r'\b(tomorrow|today|tonight|morning|afternoon|evening)\b',
            r'\b(next|this)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b'
        ]
    
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle the context."""
        user_input = context.user_input.lower()
        
        # Check for reminder-related keywords
        reminder_keywords = ["remind", "reminder", "schedule", "alarm", "timer", "don't forget"]
        has_reminder_keyword = any(keyword in user_input for keyword in reminder_keywords)
        
        # Check for time-related keywords
        time_keywords = ["at", "in", "after", "tomorrow", "today", "tonight", "morning", "afternoon", "evening"]
        has_time_keyword = any(keyword in user_input for keyword in time_keywords)
        
        # Check for time patterns
        has_time_pattern = any(re.search(pattern, user_input, re.IGNORECASE) for pattern in self.time_patterns)
        
        return has_reminder_keyword or (has_time_keyword and has_time_pattern)
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute reminder management."""
        user_input = context.user_input.lower()
        
        # Determine if this is a query or a new reminder
        if any(keyword in user_input for keyword in ["what reminders", "my reminders", "reminder list", "show reminders"]):
            return self._handle_reminder_query(context)
        else:
            return self._handle_reminder_creation(context)
    
    def _handle_reminder_creation(self, context: SkillContext) -> SkillResult:
        """Handle creating a new reminder."""
        try:
            # Extract message and time
            message, reminder_time = self._parse_reminder_input(context.user_input)
            
            if not message:
                return SkillResult(
                    success=False,
                    message="I couldn't understand what you want to be reminded about. Please try again.",
                    data={},
                    execution_time=0.0,
                    skill_name=self.name,
                    error="No message extracted"
                )
            
            if reminder_time is None:
                return SkillResult(
                    success=False,
                    message="I couldn't understand when you want to be reminded. Please specify a time.",
                    data={},
                    execution_time=0.0,
                    skill_name=self.name,
                    error="No time extracted"
                )
            
            # Set priority based on urgency
            priority = self._determine_priority(reminder_time)
            
            # Create reminder
            reminder_id = self.reminder_manager.set_reminder(
                message=message,
                reminder_time=reminder_time,
                priority=priority
            )
            
            # Format response
            time_str = self._format_time_for_display(reminder_time)
            response = f"I've set a reminder for {time_str}: '{message}'"
            
            return SkillResult(
                success=True,
                message=response,
                data={
                    'reminder_id': reminder_id,
                    'message': message,
                    'reminder_time': reminder_time,
                    'priority': priority.value
                },
                execution_time=0.0,
                skill_name=self.name
            )
            
        except Exception as e:
            return SkillResult(
                success=False,
                message="Sorry, I had trouble setting up your reminder. Please try again.",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _handle_reminder_query(self, context: SkillContext) -> SkillResult:
        """Handle querying existing reminders."""
        try:
            # Get upcoming reminders
            reminders = self.reminder_manager.get_upcoming_reminders(limit=10)
            
            if not reminders:
                return SkillResult(
                    success=True,
                    message="You don't have any upcoming reminders.",
                    data={'reminders': []},
                    execution_time=0.0,
                    skill_name=self.name
                )
            
            # Format reminders for display
            reminder_list = []
            for reminder in reminders:
                time_str = self._format_time_for_display(reminder['scheduled_time'])
                reminder_list.append(f"• {reminder['message']} at {time_str}")
            
            response = "Here are your upcoming reminders:\n" + "\n".join(reminder_list)
            
            return SkillResult(
                success=True,
                message=response,
                data={'reminders': reminders},
                execution_time=0.0,
                skill_name=self.name
            )
            
        except Exception as e:
            return SkillResult(
                success=False,
                message="Sorry, I couldn't retrieve your reminders right now.",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _parse_reminder_input(self, user_input: str) -> tuple[Optional[str], Optional[float]]:
        """Parse user input to extract message and time."""
        user_input_lower = user_input.lower()
        
        # Parse time first
        reminder_time = self._parse_time(user_input_lower)
        
        # Extract message by removing time-related phrases
        message = user_input
        
        # Remove common prefixes
        prefixes = ["remind me to", "remind me", "don't forget to", "don't forget", "schedule", "set a reminder"]
        for prefix in prefixes:
            if user_input_lower.startswith(prefix):
                message = message[len(prefix):].strip()
                break
        
        # Remove time-related phrases from message
        time_phrases = [
            r'\bfor\s+\d+\s*(minute|hour|day|week|month|year)s?\b',
            r'\bat\s+\d{1,2}:\d{2}\s*(am|pm)?\b',
            r'\bin\s+\d+\s*(minute|hour|day|week|month|year)s?\b',
            r'\bafter\s+\d+\s*(minute|hour|day|week|month|year)s?\b',
            r'\btomorrow\b',
            r'\btoday\b',
            r'\btonight\b',
            r'\bmorning\b',
            r'\bafternoon\b',
            r'\bevening\b'
        ]
        
        for pattern in time_phrases:
            message = re.sub(pattern, '', message, flags=re.IGNORECASE)
        
        message = message.strip()
        
        # If no message but we have a time, create a generic message
        if not message and reminder_time:
            time_str = self._format_time_for_display(reminder_time)
            message = f"Reminder"
        
        return message if message else None, reminder_time
    
    def _parse_time(self, user_input: str) -> Optional[float]:
        """Parse time from user input."""
        current_time = time.time()
        
        # Pattern 1: Specific time (3:30, 3:30pm)
        time_match = re.search(r'\b(\d{1,2}):(\d{2})\s*(am|pm)?\b', user_input)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2))
            period = time_match.group(3)
            
            # Convert to 24-hour format
            if period == 'pm' and hour != 12:
                hour += 12
            elif period == 'am' and hour == 12:
                hour = 0
            
            # Calculate time for today
            today = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            reminder_time = today.timestamp()
            
            # If time has passed today, schedule for tomorrow
            if reminder_time < current_time:
                reminder_time += 24 * 3600  # Add 24 hours
            
            return reminder_time
        
        # Pattern 2: Relative time (in 5 minutes, after 2 hours, for 5 minutes)
        relative_match = re.search(r'\b(in|after|for)\s+(\d+)\s*(minute|hour|day|week|month|year)s?\b', user_input)
        if relative_match:
            amount = int(relative_match.group(2))
            unit = relative_match.group(3)
            
            # Convert to seconds
            multipliers = {
                'minute': 60,
                'hour': 3600,
                'day': 86400,
                'week': 604800,
                'month': 2592000,  # Approximate
                'year': 31536000   # Approximate
            }
            
            if unit in multipliers:
                return current_time + (amount * multipliers[unit])
        
        # Pattern 3: Tomorrow
        if 'tomorrow' in user_input:
            tomorrow = datetime.now() + timedelta(days=1)
            return tomorrow.replace(hour=9, minute=0, second=0, microsecond=0).timestamp()
        
        # Pattern 4: Today with time of day
        if 'today' in user_input:
            if 'morning' in user_input:
                return datetime.now().replace(hour=9, minute=0, second=0, microsecond=0).timestamp()
            elif 'afternoon' in user_input:
                return datetime.now().replace(hour=14, minute=0, second=0, microsecond=0).timestamp()
            elif 'evening' in user_input:
                return datetime.now().replace(hour=18, minute=0, second=0, microsecond=0).timestamp()
            elif 'tonight' in user_input:
                return datetime.now().replace(hour=20, minute=0, second=0, microsecond=0).timestamp()
        
        return None
    
    def _determine_priority(self, reminder_time: float) -> TaskPriority:
        """Determine priority based on how soon the reminder is."""
        current_time = time.time()
        time_until = reminder_time - current_time
        
        if time_until < 3600:  # Less than 1 hour
            return TaskPriority.CRITICAL
        elif time_until < 86400:  # Less than 1 day
            return TaskPriority.HIGH
        elif time_until < 604800:  # Less than 1 week
            return TaskPriority.NORMAL
        else:
            return TaskPriority.LOW
    
    def _format_time_for_display(self, timestamp: float) -> str:
        """Format timestamp for display."""
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%I:%M %p on %B %d")
    
    def cancel_reminder(self, reminder_id: str) -> bool:
        """Cancel a specific reminder."""
        return self.reminder_manager.cancel_reminder(reminder_id)
    
    def get_reminder_stats(self) -> Dict[str, Any]:
        """Get reminder statistics."""
        stats = self.scheduler.get_statistics()
        return {
            'total_tasks': stats['total_tasks'],
            'pending_tasks': stats['pending_tasks'],
            'completed_tasks': stats['completed_tasks'],
            'failed_tasks': stats['failed_tasks']
        }


class RecurringReminderSkill(BaseSkill):
    """
    Skill for managing recurring reminders.
    Demonstrates advanced scheduling capabilities.
    """
    
    def __init__(self, scheduler: PriorityScheduler):
        super().__init__(
            name="recurring_reminder",
            description="Manage recurring reminders and periodic tasks",
            priority=SkillPriority.NORMAL
        )
        self.scheduler = scheduler
        self.reminder_manager = ReminderManager(scheduler)
        self.triggers = ["recurring", "repeat", "daily", "weekly", "monthly", "periodic"]
    
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle recurring reminders."""
        user_input = context.user_input.lower()
        recurring_keywords = ["recurring", "repeat", "daily", "weekly", "monthly", "every"]
        return any(keyword in user_input for keyword in recurring_keywords)
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute recurring reminder management."""
        try:
            # Parse recurring reminder input
            message, interval = self._parse_recurring_input(context.user_input)
            
            if not message:
                return SkillResult(
                    success=False,
                    message="I couldn't understand what you want to be reminded about.",
                    data={},
                    execution_time=0.0,
                    skill_name=self.name,
                    error="No message extracted"
                )
            
            if interval is None:
                return SkillResult(
                    success=False,
                    message="I couldn't understand the recurring schedule. Please specify daily, weekly, or monthly.",
                    data={},
                    execution_time=0.0,
                    skill_name=self.name,
                    error="No interval extracted"
                )
            
            # Create recurring reminder
            reminder_id = self.reminder_manager.set_recurring_reminder(
                message=message,
                interval=interval,
                priority=TaskPriority.NORMAL
            )
            
            response = f"I've set up a recurring reminder every {self._format_interval(interval)}: '{message}'"
            
            return SkillResult(
                success=True,
                message=response,
                data={
                    'reminder_id': reminder_id,
                    'message': message,
                    'interval': interval
                },
                execution_time=0.0,
                skill_name=self.name
            )
            
        except Exception as e:
            return SkillResult(
                success=False,
                message="Sorry, I had trouble setting up your recurring reminder.",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _parse_recurring_input(self, user_input: str) -> tuple[Optional[str], Optional[float]]:
        """Parse recurring reminder input."""
        user_input_lower = user_input.lower()
        
        # Extract message
        message = user_input
        prefixes = ["remind me to", "remind me", "don't forget to", "recurring reminder"]
        for prefix in prefixes:
            if user_input_lower.startswith(prefix):
                message = message[len(prefix):].strip()
                break
        
        # Remove recurring keywords from message
        recurring_keywords = ["daily", "weekly", "monthly", "every day", "every week", "every month"]
        for keyword in recurring_keywords:
            message = re.sub(rf'\b{keyword}\b', '', message, flags=re.IGNORECASE)
        
        message = message.strip()
        
        # Parse interval
        interval = None
        if 'daily' in user_input_lower or 'every day' in user_input_lower:
            interval = 86400  # 24 hours
        elif 'weekly' in user_input_lower or 'every week' in user_input_lower:
            interval = 604800  # 7 days
        elif 'monthly' in user_input_lower or 'every month' in user_input_lower:
            interval = 2592000  # 30 days (approximate)
        
        return message if message else None, interval
    
    def _format_interval(self, interval: float) -> str:
        """Format interval for display."""
        if interval == 86400:
            return "day"
        elif interval == 604800:
            return "week"
        elif interval == 2592000:
            return "month"
        else:
            return f"{interval} seconds"


if __name__ == "__main__":
    # Demo the reminder skills
    from voice_assistant.core.scheduler import PriorityScheduler
    
    scheduler = PriorityScheduler()
    reminder_skill = ReminderSkill(scheduler)
    recurring_skill = RecurringReminderSkill(scheduler)
    
    # Test reminder creation
    context = SkillContext(
        user_input="Remind me to call mom at 3pm",
        intent="reminder_set",
        entities={},
        confidence=0.9,
        session_id="test"
    )
    
    result = reminder_skill.execute(context)
    print(f"Reminder result: {result.message}")
    
    # Test recurring reminder
    context2 = SkillContext(
        user_input="Set a daily reminder to take medication",
        intent="recurring_reminder",
        entities={},
        confidence=0.9,
        session_id="test"
    )
    
    result2 = recurring_skill.execute(context2)
    print(f"Recurring reminder result: {result2.message}")
    
    # Show statistics
    stats = reminder_skill.get_reminder_stats()
    print(f"Reminder stats: {stats}")
    
    scheduler.shutdown()
