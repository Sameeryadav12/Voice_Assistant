"""
WhatsApp and Messaging skill for sending messages and communication automation.
"""

import os
import json
import webbrowser
from datetime import datetime
from typing import Dict, Any, List, Optional
from skills.base_skill import BaseSkill, SkillContext, SkillResult, SkillPriority


class WhatsAppMessagingSkill(BaseSkill):
    """
    Skill for WhatsApp and messaging functionality.
    Features:
    - Send WhatsApp messages
    - SMS functionality (simulated)
    - Message templates
    - Contact management
    - Message scheduling
    """
    
    def __init__(self):
        super().__init__(
            name="whatsapp_messaging",
            description="Send WhatsApp messages and manage communications",
            priority=SkillPriority.HIGH
        )
        
        # Storage paths
        self.data_dir = "data"
        self.contacts_file = os.path.join(self.data_dir, "contacts.json")
        self.templates_file = os.path.join(self.data_dir, "message_templates.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize data files
        self._initialize_data_files()
        
    def _initialize_data_files(self):
        """Initialize data files with default values"""
        # Initialize contacts file
        if not os.path.exists(self.contacts_file):
            default_contacts = {
                "contacts": [
                    {"name": "Mom", "phone": "+1234567890", "whatsapp": True},
                    {"name": "Dad", "phone": "+1234567891", "whatsapp": True},
                    {"name": "John", "phone": "+1234567892", "whatsapp": True},
                    {"name": "Sarah", "phone": "+1234567893", "whatsapp": True}
                ]
            }
            with open(self.contacts_file, 'w') as f:
                json.dump(default_contacts, f, indent=2)
        
        # Initialize message templates file
        if not os.path.exists(self.templates_file):
            default_templates = {
                "templates": [
                    {"name": "greeting", "text": "Hello! How are you doing?"},
                    {"name": "meeting", "text": "Hi! Can we schedule a meeting for tomorrow?"},
                    {"name": "thanks", "text": "Thank you for your help!"},
                    {"name": "reminder", "text": "Don't forget about our appointment today."}
                ]
            }
            with open(self.templates_file, 'w') as f:
                json.dump(default_templates, f, indent=2)
    
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle the request."""
        user_input = context.user_input.lower()
        
        # WhatsApp keywords - very specific to avoid conflicts
        whatsapp_keywords = [
            "whatsapp", "send whatsapp", "whatsapp message", "open whatsapp",
            "launch whatsapp", "start whatsapp", "whatsapp app", "whatsapp web",
            "send message to", "text someone", "message someone", "send a message to",
            "send message to someone", "send a message to someone", "whatsapp message to"
        ]
        
        # Contact keywords - removed as requested
        contact_keywords = []
        
        # Template keywords
        template_keywords = [
            "template", "message template", "quick message", "predefined message",
            "show message templates", "message templates", "templates", "show templates"
        ]
        
        has_whatsapp = any(keyword in user_input for keyword in whatsapp_keywords)
        has_contact = any(keyword in user_input for keyword in contact_keywords)
        has_template = any(keyword in user_input for keyword in template_keywords)
        
        return has_whatsapp or has_contact or has_template
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute WhatsApp/messaging functionality."""
        user_input = context.user_input.lower()
        
        try:
            # Determine the type of request
            if "open whatsapp" in user_input or "launch whatsapp" in user_input or "start whatsapp" in user_input:
                return self._handle_send_message(user_input)
            elif "send message" in user_input or "send whatsapp" in user_input or "send a message" in user_input or "text someone" in user_input or "message someone" in user_input:
                return self._handle_send_message(user_input)
            elif "template" in user_input or "quick message" in user_input or "show message templates" in user_input or "message templates" in user_input:
                return self._handle_message_templates()
            else:
                return self._handle_general_messaging(user_input)
                
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error in messaging: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
    
    def _handle_send_message(self, user_input: str) -> SkillResult:
        """Handle sending messages."""
        try:
            import subprocess
            import webbrowser
            import os
            
            # Extract person's name from user input for search
            person_name = self._extract_person_name(user_input)
            
            # Method 1: Try to launch WhatsApp desktop app first
            try:
                # Try common WhatsApp desktop app paths
                whatsapp_paths = [
                    r"C:\Program Files\WhatsApp\WhatsApp.exe",
                    r"C:\Program Files (x86)\WhatsApp\WhatsApp.exe",
                    r"C:\Users\{}\AppData\Local\WhatsApp\WhatsApp.exe".format(os.getenv('USERNAME')),
                    r"C:\Users\{}\AppData\Roaming\WhatsApp\WhatsApp.exe".format(os.getenv('USERNAME')),
                    r"C:\Users\{}\AppData\Local\Microsoft\WindowsApps\WhatsApp.exe".format(os.getenv('USERNAME')),
                    r"C:\Users\{}\AppData\Local\Microsoft\WindowsApps\WhatsAppDesktop.exe".format(os.getenv('USERNAME'))
                ]
                
                # Check if WhatsApp desktop app exists
                for path in whatsapp_paths:
                    if os.path.exists(path):
                        subprocess.Popen([path])
                        if person_name:
                            # Wait a moment for WhatsApp to open, then search for the person
                            import time
                            time.sleep(2)
                            self._search_person_in_whatsapp(person_name)
                            return SkillResult(
                                success=True,
                                message=f"Opening WhatsApp desktop app and searching for '{person_name}'. You can now send your message.",
                                data={"action": "opened_whatsapp_desktop", "person": person_name},
                                execution_time=0.0,
                                skill_name=self.name
                            )
                        else:
                            return SkillResult(
                                success=True,
                                message="Opening WhatsApp desktop app for you to send messages.",
                                data={"action": "opened_whatsapp_desktop"},
                                execution_time=0.0,
                                skill_name=self.name
                            )
                
                # Try launching WhatsApp through Windows start command
                result = subprocess.run(["start", "whatsapp:"], shell=True, capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    if person_name:
                        return SkillResult(
                            success=True,
                            message=f"Opening WhatsApp desktop app. Search for '{person_name}' to send your message.",
                            data={"action": "opened_whatsapp_desktop_start", "person": person_name},
                            execution_time=0.0,
                            skill_name=self.name
                        )
                    else:
                        return SkillResult(
                            success=True,
                            message="Opening WhatsApp desktop app for you to send messages.",
                            data={"action": "opened_whatsapp_desktop_start"},
                            execution_time=0.0,
                            skill_name=self.name
                        )
            except:
                pass
            
            # Method 2: If desktop app not found, open WhatsApp Web
            try:
                webbrowser.open("https://web.whatsapp.com")
                if person_name:
                    # Wait a moment for WhatsApp Web to load, then search for the person
                    import time
                    time.sleep(3)
                    self._search_person_in_whatsapp(person_name)
                    return SkillResult(
                        success=True,
                        message=f"WhatsApp desktop app not found. Opening WhatsApp Web and searching for '{person_name}'. You can now send your message.",
                        data={"action": "opened_whatsapp_web", "person": person_name},
                        execution_time=0.0,
                        skill_name=self.name
                    )
                else:
                    return SkillResult(
                        success=True,
                        message="WhatsApp desktop app not found. Opening WhatsApp Web for you to send messages.",
                        data={"action": "opened_whatsapp_web"},
                        execution_time=0.0,
                        skill_name=self.name
                    )
            except:
                pass
            
            # If all methods fail, provide instructions
            return SkillResult(
                success=True,
                message="I couldn't automatically open WhatsApp. Please open WhatsApp manually or go to https://web.whatsapp.com to send messages.",
                data={"action": "manual_whatsapp"},
                execution_time=0.0,
                skill_name=self.name
            )
            
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Could not open WhatsApp: {str(e)}. Please try opening WhatsApp manually.",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
    
    def _extract_person_name(self, user_input: str) -> Optional[str]:
        """Extract person's name from user input."""
        # Look for patterns like "send message to nikhil", "text nikhil", "message nikhil"
        words = user_input.lower().split()
        
        # Find name after "to" or after "message"/"text"
        if "to" in words:
            to_index = words.index("to")
            if to_index + 1 < len(words):
                return words[to_index + 1].title()
        
        # Look for name after "message" or "text"
        for i, word in enumerate(words):
            if word in ["message", "text"] and i + 1 < len(words):
                return words[i + 1].title()
        
        # Look for name after "send"
        if "send" in words:
            send_index = words.index("send")
            if send_index + 1 < len(words) and words[send_index + 1] not in ["message", "text", "a"]:
                return words[send_index + 1].title()
        
        return None
    
    def _search_person_in_whatsapp(self, person_name: str):
        """Search for a person in WhatsApp using keyboard shortcuts."""
        try:
            import time
            import pyautogui
            
            # Wait for WhatsApp to be active
            time.sleep(1)
            
            # Press Ctrl+F to open search
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            
            # Type the person's name
            pyautogui.typewrite(person_name)
            time.sleep(0.5)
            
            # Press Enter to search
            pyautogui.press('enter')
            
        except Exception as e:
            # Fallback: just type the name in the current window
            try:
                import pyautogui
                pyautogui.typewrite(person_name)
            except:
                pass
    
    def _handle_add_contact(self, user_input: str) -> SkillResult:
        """Handle adding contacts."""
        # Extract name and phone from user input (simplified)
        try:
            # Look for patterns like "add contact John with phone +1234567890"
            words = user_input.lower().split()
            
            if "add contact" in user_input.lower():
                # Try to extract name and phone
                name = None
                phone = None
                
                # Find name after "add contact"
                add_index = words.index("add")
                contact_index = words.index("contact")
                if contact_index + 1 < len(words):
                    name = words[contact_index + 1]
                
                # Find phone number
                for word in words:
                    if word.startswith("+") or word.replace("-", "").replace("(", "").replace(")", "").isdigit():
                        phone = word
                        break
                
                if name and phone:
                    # Add contact to file
                    with open(self.contacts_file, 'r') as f:
                        contacts_data = json.load(f)
                    
                    new_contact = {
                        "name": name.title(),
                        "phone": phone,
                        "whatsapp": True
                    }
                    
                    contacts_data["contacts"].append(new_contact)
                    
                    with open(self.contacts_file, 'w') as f:
                        json.dump(contacts_data, f, indent=2)
                    
                    return SkillResult(
                        success=True,
                        message=f"Added contact {name.title()} with phone {phone} to your contact list.",
                        data={"action": "contact_added", "contact": new_contact},
                        execution_time=0.0,
                        skill_name=self.name
                    )
                else:
                    return SkillResult(
                        success=True,
                        message="To add a contact, please provide the name and phone number. For example: 'Add contact John with phone +1234567890'",
                        data={"action": "add_contact_prompt"},
                        execution_time=0.0,
                        skill_name=self.name
                    )
            else:
                return SkillResult(
                    success=True,
                    message="To add a contact, say 'Add contact [name] with phone [number]'. For example: 'Add contact John with phone +1234567890'",
                    data={"action": "add_contact_help"},
                    execution_time=0.0,
                    skill_name=self.name
                )
                
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error adding contact: {str(e)}. Please try again with the format: 'Add contact [name] with phone [number]'",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
    
    def _handle_list_contacts(self) -> SkillResult:
        """Handle listing contacts."""
        try:
            with open(self.contacts_file, 'r') as f:
                contacts_data = json.load(f)
            
            contacts = contacts_data.get("contacts", [])
            if not contacts:
                return SkillResult(
                    success=True,
                    message="No contacts found. You can add contacts by saying 'Add contact [name] with phone [number]'",
                    data={"contacts": []},
                    execution_time=0.0,
                    skill_name=self.name
                )
            
            contact_list = []
            for contact in contacts:
                contact_list.append(f"{contact['name']}: {contact['phone']}")
            
            return SkillResult(
                success=True,
                message=f"Here are your contacts:\n" + "\n".join(contact_list),
                data={"contacts": contacts},
                execution_time=0.0,
                skill_name=self.name
            )
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error loading contacts: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
    
    def _handle_message_templates(self) -> SkillResult:
        """Handle message templates."""
        try:
            with open(self.templates_file, 'r') as f:
                templates_data = json.load(f)
            
            templates = templates_data.get("templates", [])
            if not templates:
                return SkillResult(
                    success=True,
                    message="No message templates found.",
                    data={"templates": []},
                    execution_time=0.0,
                    skill_name=self.name
                )
            
            template_list = []
            for template in templates:
                template_list.append(f"{template['name']}: {template['text']}")
            
            return SkillResult(
                success=True,
                message=f"Here are your message templates:\n" + "\n".join(template_list),
                data={"templates": templates},
                execution_time=0.0,
                skill_name=self.name
            )
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error loading templates: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
    
    def _handle_general_messaging(self, user_input: str) -> SkillResult:
        """Handle general messaging requests."""
        return SkillResult(
            success=True,
            message="I can help you with WhatsApp messaging! You can:\n- Send messages: 'Send message to [contact]'\n- Add contacts: 'Add contact [name] with phone [number]'\n- List contacts: 'Show my contacts'\n- Use templates: 'Show message templates'",
            data={"action": "messaging_help"},
            execution_time=0.0,
            skill_name=self.name
        )

if __name__ == "__main__":
    # Test the skill
    skill = WhatsAppMessagingSkill()
    context = SkillContext(
        user_input="Send a message to John",
        confidence=1.0,
        entities={},
        session_id="test"
    )
    
    result = skill.execute(context)
