"""
Interactive Skill Widget Component
Provides quick access buttons for common skills
"""

import customtkinter as ctk
from typing import Dict, Any, Optional, Callable

class SkillWidget(ctk.CTkFrame):
    """Interactive skill widget with quick action buttons"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Skill buttons
        self.skill_buttons = {}
        self.skill_callback = None
        
        # Create skill buttons frame
        self.skills_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.skills_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create skill buttons
        self._create_skill_buttons()
    
    def _create_skill_buttons(self):
        """Create skill action buttons"""
        
        # Define skills with icons and descriptions
        skills = [
            ("Weather", "🌤️", "Check weather"),
            ("Time", "🕐", "What time is it?"),
            ("Notes", "📝", "Take a note"),
            ("Search", "🔍", "Search web"),
            ("Music", "🎵", "Play music"),
            ("Memory", "🧠", "What did we talk about?")
        ]
        
        # Create buttons in a grid
        for i, (skill_name, icon, description) in enumerate(skills):
            row = i // 3
            col = i % 3
            
            # Create skill button with enhanced styling
            skill_button = ctk.CTkButton(
                self.skills_frame,
                text=f"{icon} {skill_name}",
                width=160,
                height=45,
                font=ctk.CTkFont(size=10, weight="bold"),
                command=lambda s=skill_name.lower(): self._on_skill_click(s),
                corner_radius=12,
                fg_color=["#3B8ED0", "#1F6AA5"],
                hover_color=["#36719F", "#144870"],
                border_width=1,
                border_color=["#4A90E2", "#2E5B8A"],
                text_color=["#FFFFFF", "#FFFFFF"]
            )
            skill_button.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
            
            # Store button reference
            self.skill_buttons[skill_name.lower()] = skill_button
        
        # Configure grid weights
        for i in range(3):
            self.skills_frame.grid_columnconfigure(i, weight=1)
    
    def _on_skill_click(self, skill_name: str):
        """Handle skill button click"""
        if self.skill_callback:
            # Map skill names to voice commands
            skill_commands = {
                "weather": "Hey Jarvis, what's the weather?",
                "time": "Hey Jarvis, what time is it?",
                "notes": "Hey Jarvis, take a note",
                "search": "Hey Jarvis, search for",
                "music": "Hey Jarvis, play your favorite song",
                "memory": "Hey Jarvis, what did we talk about?"
            }
            
            command = skill_commands.get(skill_name, f"Hey Jarvis, {skill_name}")
            self.skill_callback(command)
    
    def set_skill_callback(self, callback: Callable[[str], None]):
        """Set callback function for skill button clicks"""
        self.skill_callback = callback
    
    def update_skill_status(self, skill_name: str, status: str):
        """Update skill button status with smooth transitions"""
        if skill_name in self.skill_buttons:
            button = self.skill_buttons[skill_name]
            
            if status == "active":
                button.configure(
                    fg_color="#007acc", 
                    hover_color="#005a9e",
                    border_color="#0099ff"
                )
            elif status == "processing":
                button.configure(
                    fg_color="#ffc107", 
                    hover_color="#e0a800",
                    border_color="#ffd700"
                )
            elif status == "success":
                button.configure(
                    fg_color="#28a745", 
                    hover_color="#1e7e34",
                    border_color="#32cd32"
                )
            elif status == "error":
                button.configure(
                    fg_color="#dc3545", 
                    hover_color="#c82333",
                    border_color="#ff4444"
                )
            else:
                # Default state with enhanced styling
                button.configure(
                    fg_color=["#3B8ED0", "#1F6AA5"], 
                    hover_color=["#36719F", "#144870"],
                    border_color=["#4A90E2", "#2E5B8A"]
                )

if __name__ == "__main__":
    # Test the skill widget
    root = ctk.CTk()
    root.title("Skill Widget Test")
    
    # Create test frame
    test_frame = ctk.CTkFrame(root)
    test_frame.pack(padx=20, pady=20)
    
    # Create skill widget
    skill_widget = SkillWidget(test_frame, width=400, height=200)
    skill_widget.pack(pady=10)
    
    # Set callback
    def on_skill_click(command):
        print(f"Skill clicked: {command}")
    
    skill_widget.set_skill_callback(on_skill_click)
    
    # Test status updates
    def test_status():
        skill_widget.update_skill_status("weather", "active")
        skill_widget.after(2000, lambda: skill_widget.update_skill_status("weather", "success"))
    
    test_button = ctk.CTkButton(test_frame, text="Test Weather Status", command=test_status)
    test_button.pack(pady=10)
    
    root.mainloop()
