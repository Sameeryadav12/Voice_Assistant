"""
Sigma Voice Assistant - Keyboard Input Version for Testing
This version accepts keyboard input instead of speech for testing purposes.
"""

import sys
import os
import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import customtkinter as ctk
from typing import Optional, Dict, Any
import queue
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import core components
from core.trie import KeywordMatcher
from core.state_machine import DialogueStateMachine, EventType, StateType
from core.scheduler import PriorityScheduler
from core.cache import CacheManager
from core.graph_search import FileSystemGraph

# Import NLP components
from nlp.intent_classifier import HybridIntentClassifier, IntentType
from nlp.text_processor import TextProcessor

# Import skills
from skills.base_skill import SkillManager, SkillRegistry
from skills.reminder_skill import ReminderSkill, RecurringReminderSkill
from skills.file_skill import FileSearchSkill, FileManagementSkill
from skills.app_skill import AppLauncherSkill, SystemControlSkill
from skills.help_skill import HelpSkill

# Import audio output
from audio.output_handler import AudioOutputHandler, TTSConfig, VoiceGender, SpeechRate


class SigmaVoiceAssistantKeyboard:
    """
    Keyboard input version of the voice assistant for testing.
    """
    
    def __init__(self):
        print("Starting Sigma Voice Assistant (Keyboard Input Mode)...")
        
        # Initialize core components
        self.keyword_matcher = KeywordMatcher()
        self.state_machine = DialogueStateMachine()
        self.scheduler = PriorityScheduler()
        self.cache_manager = CacheManager()
        self.fs_graph = FileSystemGraph()
        
        # Initialize NLP components
        self.intent_classifier = HybridIntentClassifier()
        self.text_processor = TextProcessor()
        
        # Initialize audio output
        self.audio_output = AudioOutputHandler(TTSConfig())
        
        # Initialize skills
        self.skill_manager = SkillManager()
        self._register_skills()
        
        # Initialize UI
        self.root = None
        self.is_running = False
        
        print("Components initialized successfully!")
    
    def _register_skills(self):
        """Register all available skills."""
        # Register reminder skills
        reminder_skill = ReminderSkill(self.scheduler)
        recurring_skill = RecurringReminderSkill(self.scheduler)
        self.skill_manager.register_skill(reminder_skill)
        self.skill_manager.register_skill(recurring_skill)
        
        # Register file skills
        file_search_skill = FileSearchSkill(self.fs_graph)
        file_management_skill = FileManagementSkill()
        self.skill_manager.register_skill(file_search_skill)
        self.skill_manager.register_skill(file_management_skill)
        
        # Register app skills
        app_skill = AppLauncherSkill(self.fs_graph)
        system_skill = SystemControlSkill()
        self.skill_manager.register_skill(app_skill)
        self.skill_manager.register_skill(system_skill)
        
        # Register help skill
        help_skill = HelpSkill()
        self.skill_manager.register_skill(help_skill)
        
        print(f"Registered {len(self.skill_manager.skills)} skills")
    
    def _create_ui(self):
        """Create the user interface."""
        # Configure CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Sigma Voice Assistant (Keyboard Mode)")
        self.root.geometry("800x600")
        
        # Main title
        title_label = ctk.CTkLabel(
            self.root, 
            text="Sigma Voice Assistant", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Status frame
        status_frame = ctk.CTkFrame(self.root)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = ctk.CTkLabel(
            status_frame, 
            text="Ready - Type your commands below", 
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=10)
        
        # Input frame
        input_frame = ctk.CTkFrame(self.root)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        input_label = ctk.CTkLabel(input_frame, text="Type your command:", font=ctk.CTkFont(size=12))
        input_label.pack(pady=(10, 5))
        
        self.input_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="Type 'Hey Sigma, what can you do?' or any command...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.input_entry.pack(fill="x", padx=10, pady=(0, 10))
        self.input_entry.bind("<Return>", self._on_enter_pressed)
        
        # Send button
        send_button = ctk.CTkButton(
            input_frame,
            text="Send Command",
            command=self._process_keyboard_input,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        send_button.pack(pady=(0, 10))
        
        # Conversation frame
        conversation_frame = ctk.CTkFrame(self.root)
        conversation_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        conversation_label = ctk.CTkLabel(
            conversation_frame, 
            text="Conversation", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        conversation_label.pack(pady=(10, 5))
        
        # Conversation text area
        self.conversation_text = ctk.CTkTextbox(
            conversation_frame,
            height=300,
            font=ctk.CTkFont(size=12)
        )
        self.conversation_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Control buttons
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self._clear_conversation,
            width=100
        )
        clear_button.pack(side="left", padx=5)
        
        help_button = ctk.CTkButton(
            button_frame,
            text="Help",
            command=self._show_help,
            width=100
        )
        help_button.pack(side="left", padx=5)
        
        # Stats label
        self.stats_label = ctk.CTkLabel(
            self.root, 
            text="Cache: 0 items | Skills: 6 | Executions: 0",
            font=ctk.CTkFont(size=10)
        )
        self.stats_label.pack(pady=(0, 10))
        
        # Add welcome message
        self._update_conversation("Welcome to Sigma Voice Assistant!")
        self._update_conversation("This is keyboard input mode for testing.")
        self._update_conversation("Type 'Hey Sigma, what can you do?' to start!")
        
        # Focus on input
        self.input_entry.focus()
    
    def _on_enter_pressed(self, event):
        """Handle Enter key press."""
        self._process_keyboard_input()
    
    def _process_keyboard_input(self):
        """Process keyboard input as if it were speech."""
        text = self.input_entry.get().strip()
        if not text:
            return
        
        # Clear input
        self.input_entry.delete(0, tk.END)
        
        # Process as speech input
        self._process_user_input(text, 1.0, {})
    
    def _process_user_input(self, text: str, confidence: float, metadata: Dict[str, Any]):
        """Process user input through the complete pipeline."""
        try:
            # Update UI with recognized text
            self._update_conversation(f"User: {text}")
            
            # Check for wake word
            if not self.keyword_matcher.detect_wake_word(text):
                self._respond("Please say 'Hey Sigma' first to activate the assistant.")
                return
            
            # Clean text (remove wake word)
            clean_text = text.lower()
            for wake_word in ["hey sigma", "sigma", "assistant"]:
                clean_text = clean_text.replace(wake_word, "").strip()
            
            if not clean_text:
                self._respond("Yes, I'm listening. How can I help you?")
                return
            
            # Process text
            processed_text = self.text_processor.process(clean_text)
            
            # Classify intent
            intent_result = self.intent_classifier.classify(clean_text)
            
            # Update state machine
            self.state_machine.process_event(EventType.INTENT_CLASSIFIED, {
                'intent': intent_result.intent.value,
                'confidence': intent_result.confidence,
                'entities': intent_result.entities
            })
            
            # Execute skill
            from skills.base_skill import SkillContext
            skill_context = SkillContext(
                user_input=clean_text,
                intent=intent_result.intent.value,
                entities=intent_result.entities,
                confidence=intent_result.confidence,
                session_id='keyboard_session'
            )
            skill_result = self.skill_manager.execute_best_skill(skill_context)
            
            if skill_result.success:
                self._respond(skill_result.message)
            else:
                error_msg = skill_result.error if skill_result.error else "Unknown error"
                self._respond(f"I'm sorry, I couldn't help with that. {error_msg}")
            
        except Exception as e:
            print(f"Error processing user input: {e}")
            self._respond("I'm sorry, I encountered an error. Please try again.")
    
    def _respond(self, text: str):
        """Generate and display response."""
        self._update_conversation(f"Sigma: {text}")
        
        # Update cache
        self.cache_manager.cache_speech_result("keyboard", text, 1.0)
        
        # Update stats
        self._update_stats()
    
    def _update_conversation(self, message: str):
        """Update conversation display."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.conversation_text.insert("end", f"[{timestamp}] {message}\n")
        self.conversation_text.see("end")
    
    def _update_stats(self):
        """Update statistics display."""
        try:
            cache_stats = self.cache_manager.get_cache_statistics()
            total_cache_size = sum(stats['current_size'] for stats in cache_stats.values())
            
            skill_stats = self.skill_manager.get_skill_statistics()
            total_executions = sum(stats['execution_count'] for stats in skill_stats.values())
            
            stats_text = f"Cache: {total_cache_size} items | Skills: {len(skill_stats)} | Executions: {total_executions}"
            self.stats_label.configure(text=stats_text)
        except Exception as e:
            self.stats_label.configure(text=f"Stats error: {e}")
    
    def _clear_conversation(self):
        """Clear conversation history."""
        self.conversation_text.delete("1.0", "end")
        self._update_conversation("Conversation cleared.")
    
    def _show_help(self):
        """Show help information."""
        help_text = """
Sigma Voice Assistant - Available Commands:

Wake Word Commands:
- "Hey Sigma, what can you do?"
- "Hey Sigma, what time is it?"
- "Hey Sigma, set a reminder for 5 minutes"
- "Hey Sigma, search for files"
- "Hey Sigma, open calculator"
- "Hey Sigma, what reminders do I have?"

Tips:
- Always start with "Hey Sigma"
- Speak clearly and wait for response
- Try different phrasings if something doesn't work
        """
        messagebox.showinfo("Help", help_text)
    
    def run(self):
        """Run the application."""
        self._create_ui()
        
        print("Application started. Close the window to exit.")
        self.root.mainloop()
        
        # Cleanup
        self.scheduler.shutdown()


def main():
    """Main entry point."""
    try:
        app = SigmaVoiceAssistantKeyboard()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
