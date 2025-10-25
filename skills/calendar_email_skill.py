"""
Calendar and Email Integration skill for managing schedules and communications.
"""

import os
import json
import webbrowser
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from skills.base_skill import BaseSkill, SkillContext, SkillResult, SkillPriority


class CalendarEmailSkill(BaseSkill):
    """
    Skill for calendar and email functionality.
    Features:
    - Calendar management
    - Email integration
    - Meeting scheduling
    - Event reminders
    - Email composition
    """
    
    def __init__(self):
        super().__init__(
            name="calendar_email",
            description="Manage calendar and email functionality",
            priority=SkillPriority.NORMAL
        )
        
        # Storage paths
        self.data_dir = "data"
        self.calendar_file = os.path.join(self.data_dir, "calendar.json")
        self.email_file = os.path.join(self.data_dir, "emails.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize data files
        self._initialize_data_files()
        
    def _initialize_data_files(self):
        """Initialize data files with default values"""
        # Initialize calendar file
        if not os.path.exists(self.calendar_file):
            default_calendar = {
                "events": [
                    {
                        "id": 1,
                        "title": "Team Meeting",
                        "date": "2024-01-15",
                        "time": "10:00",
                        "duration": 60,
                        "description": "Weekly team standup meeting"
                    },
                    {
                        "id": 2,
                        "title": "Project Deadline",
                        "date": "2024-01-20",
                        "time": "17:00",
                        "duration": 0,
                        "description": "Submit project deliverables"
                    }
                ]
            }
            with open(self.calendar_file, 'w') as f:
                json.dump(default_calendar, f, indent=2)
        
        # Initialize email file
        if not os.path.exists(self.email_file):
            default_emails = {
                "emails": [
                    {
                        "id": 1,
                        "to": "john@example.com",
                        "subject": "Meeting Follow-up",
                        "body": "Thank you for the productive meeting today.",
                        "date": "2024-01-10",
                        "status": "sent"
                    }
                ]
            }
            with open(self.email_file, 'w') as f:
                json.dump(default_emails, f, indent=2)
    
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle the request."""
        user_input = context.user_input.lower()
        
        # Calendar keywords
        calendar_keywords = [
            "calendar", "schedule", "meeting", "appointment", "event",
            "add event", "create event", "schedule meeting", "my calendar",
            "today's schedule", "tomorrow's schedule", "upcoming events",
            "book meeting", "set meeting", "calendar events"
        ]
        
        # Email keywords
        email_keywords = [
            "email", "send email", "compose email", "write email",
            "check email", "my emails", "inbox", "mail",
            "email to", "send message", "compose message"
        ]
        
        has_calendar = any(keyword in user_input for keyword in calendar_keywords)
        has_email = any(keyword in user_input for keyword in email_keywords)
        
        return has_calendar or has_email
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute calendar or email functionality."""
        user_input = context.user_input.lower()
        
        try:
            # Determine the type of request
            if any(keyword in user_input for keyword in ["calendar", "schedule", "meeting", "appointment", "event"]):
                return self._handle_calendar_request(user_input)
            elif any(keyword in user_input for keyword in ["email", "mail", "compose", "send"]):
                return self._handle_email_request(user_input)
            else:
                return self._handle_general_request()
                
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error in calendar/email: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
    
    def _handle_calendar_request(self, user_input: str) -> SkillResult:
        """Handle calendar-related requests."""
        try:
            if "show" in user_input or "list" in user_input or "my calendar" in user_input:
                return self._show_calendar()
            elif "add" in user_input or "create" in user_input or "schedule" in user_input:
                return self._add_event(user_input)
            elif "today" in user_input:
                return self._show_today_schedule()
            elif "tomorrow" in user_input:
                return self._show_tomorrow_schedule()
            else:
                return self._show_calendar()
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error handling calendar request: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
    
    def _handle_email_request(self, user_input: str) -> SkillResult:
        """Handle email-related requests."""
        try:
            if "compose" in user_input or "write" in user_input or "send email" in user_input:
                return self._compose_email()
            elif "check" in user_input or "my emails" in user_input or "inbox" in user_input:
                return self._show_emails()
            else:
                return self._compose_email()
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error handling email request: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
    
    def _handle_general_request(self) -> SkillResult:
        """Handle general calendar/email requests."""
        return SkillResult(
            success=True,
            message="I can help you with calendar and email! You can:\n- View calendar: 'Show my calendar'\n- Add event: 'Schedule a meeting'\n- Compose email: 'Compose an email'\n- Check emails: 'Check my emails'",
            data={"action": "calendar_email_help"},
            execution_time=0.0,
            skill_name=self.name
        )
    
    def _show_calendar(self) -> SkillResult:
        """Show calendar events."""
        try:
            with open(self.calendar_file, 'r') as f:
                calendar_data = json.load(f)
            
            events = calendar_data.get("events", [])
            if not events:
                return SkillResult(
                    success=True,
                    message="Your calendar is empty. You can add events by saying 'Schedule a meeting' or 'Add an event'.",
                    data={"events": []},
                    execution_time=0.0,
                    skill_name=self.name
                )
            
            event_list = []
            for event in events:
                event_list.append(f"• {event['title']} on {event['date']} at {event['time']}")
            
            return SkillResult(
                success=True,
                message=f"Here are your calendar events:\n" + "\n".join(event_list),
                data={"events": events},
                execution_time=0.0,
                skill_name=self.name
            )
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error loading calendar: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
    
    def _add_event(self, user_input: str) -> SkillResult:
        """Add a new event to calendar."""
        try:
            # This is a simplified version - in reality, you'd need more sophisticated NLP
            return SkillResult(
                success=True,
                message="To add an event, please provide details like: 'Schedule a meeting with John tomorrow at 2 PM' or 'Add event Project Review on Friday at 10 AM'",
                data={"action": "add_event_prompt"},
                execution_time=0.0,
                skill_name=self.name
            )
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error adding event: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
    
    def _show_today_schedule(self) -> SkillResult:
        """Show today's schedule."""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            with open(self.calendar_file, 'r') as f:
                calendar_data = json.load(f)
            
            events = calendar_data.get("events", [])
            today_events = [event for event in events if event['date'] == today]
            
            if not today_events:
                return SkillResult(
                    success=True,
                    message="You have no events scheduled for today.",
                    data={"events": []},
                    execution_time=0.0,
                    skill_name=self.name
                )
            
            event_list = []
            for event in today_events:
                event_list.append(f"• {event['title']} at {event['time']}")
            
            return SkillResult(
                success=True,
                message=f"Today's schedule:\n" + "\n".join(event_list),
                data={"events": today_events},
                execution_time=0.0,
                skill_name=self.name
            )
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error loading today's schedule: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
    
    def _show_tomorrow_schedule(self) -> SkillResult:
        """Show tomorrow's schedule."""
        try:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            with open(self.calendar_file, 'r') as f:
                calendar_data = json.load(f)
            
            events = calendar_data.get("events", [])
            tomorrow_events = [event for event in events if event['date'] == tomorrow]
            
            if not tomorrow_events:
                return SkillResult(
                    success=True,
                    message="You have no events scheduled for tomorrow.",
                    data={"events": []},
                    execution_time=0.0,
                    skill_name=self.name
                )
            
            event_list = []
            for event in tomorrow_events:
                event_list.append(f"• {event['title']} at {event['time']}")
            
            return SkillResult(
                success=True,
                message=f"Tomorrow's schedule:\n" + "\n".join(event_list),
                data={"events": tomorrow_events},
                execution_time=0.0,
                skill_name=self.name
            )
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error loading tomorrow's schedule: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
    
    def _compose_email(self) -> SkillResult:
        """Open email composer."""
        try:
            # Open Gmail compose
            webbrowser.open("https://mail.google.com/mail/?view=cm&fs=1&to=")
            return SkillResult(
                success=True,
                message="Opening Gmail compose for you to write an email.",
                data={"action": "opened_gmail_compose"},
                execution_time=0.0,
                skill_name=self.name
            )
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Could not open email composer: {str(e)}. Please try opening Gmail manually.",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
    
    def _show_emails(self) -> SkillResult:
        """Show recent emails."""
        try:
            with open(self.email_file, 'r') as f:
                email_data = json.load(f)
            
            emails = email_data.get("emails", [])
            if not emails:
                return SkillResult(
                    success=True,
                    message="No emails found. You can compose a new email by saying 'Compose an email'.",
                    data={"emails": []},
                    execution_time=0.0,
                    skill_name=self.name
                )
            
            email_list = []
            for email in emails[-5:]:  # Show last 5 emails
                email_list.append(f"• To: {email['to']} - {email['subject']} ({email['date']})")
            
            return SkillResult(
                success=True,
                message=f"Recent emails:\n" + "\n".join(email_list),
                data={"emails": emails},
                execution_time=0.0,
                skill_name=self.name
            )
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error loading emails: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )

if __name__ == "__main__":
    # Test the skill
    skill = CalendarEmailSkill()
    context = SkillContext(
        user_input="show my calendar",
        confidence=1.0,
        entities={},
        session_id="test",
        user_id="test"
    )
    
    result = skill.execute(context)
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")
    print(f"Data: {result.data}")


