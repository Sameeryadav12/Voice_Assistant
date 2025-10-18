"""
Sigma Voice Assistant - Combined Mode
This version has BOTH keyboard input AND voice listening!
"""

import sys
import os
import time
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import customtkinter as ctk
from typing import Optional, Dict, Any
import queue
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import core components
from core.trie import KeywordMatcher
from core.state_machine import DialogueStateMachine, EventType, StateType
from core.scheduler import PriorityScheduler
from core.cache import CacheManager
from core.graph_search import FileSystemGraph

# Import audio components
from audio.input_handler import AudioInputHandler, AudioConfig
from audio.output_handler import AudioOutputHandler, TTSConfig, VoiceGender, SpeechRate

# Import NLP components
from nlp.speech_to_text import SpeechToTextProcessor, RecognitionConfig, RecognitionEngine
from nlp.intent_classifier import HybridIntentClassifier, IntentType
from nlp.text_processor import TextProcessor

# Import skills
from skills.base_skill import SkillManager, SkillRegistry, SkillContext
from skills.reminder_skill import ReminderSkill, RecurringReminderSkill
from skills.file_skill import FileSearchSkill, FileManagementSkill
from skills.app_skill import AppLauncherSkill, SystemControlSkill
from skills.help_skill import HelpSkill
from skills.info_skill import InfoSkill


class SigmaVoiceAssistantCombined:
    """
    Combined voice assistant with BOTH keyboard and voice input!
    """
    
    def __init__(self):
        print("Starting Sigma Voice Assistant (Combined Mode)...")
        
        # Initialize core components
        self.keyword_matcher = KeywordMatcher()
        self.state_machine = DialogueStateMachine()
        self.scheduler = PriorityScheduler()
        self.cache_manager = CacheManager()
        self.fs_graph = FileSystemGraph()
        
        # Initialize audio components
        self.audio_config = AudioConfig()
        self.audio_input = AudioInputHandler(self.audio_config)
        self.tts_config = TTSConfig(voice_gender=VoiceGender.FEMALE, speech_rate=SpeechRate.NORMAL)
        self.audio_output = AudioOutputHandler(self.tts_config)
        
        # Initialize NLP components
        self.recognition_config = RecognitionConfig(engine=RecognitionEngine.GOOGLE)
        self.speech_processor = SpeechToTextProcessor(self.recognition_config)
        self.intent_classifier = HybridIntentClassifier()
        self.text_processor = TextProcessor()
        
        # Initialize skills
        self.skill_manager = SkillManager()
        self._register_skills()
        
        # State
        self.root = None
        self.is_voice_listening = False
        
        # Setup callbacks
        self._setup_callbacks()
        
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
        
        # Register info skill
        info_skill = InfoSkill()
        self.skill_manager.register_skill(info_skill)
        
        print(f"Registered {len(self.skill_manager.skills)} skills")
    
    def _setup_callbacks(self):
        """Setup callbacks for component communication."""
        # Audio input callback
        self.audio_input.add_callback(self._on_audio_received)
    
    def _on_audio_received(self, audio_data: bytes):
        """Handle received audio data from voice."""
        try:
            print(f"[VOICE] Received {len(audio_data)} bytes of audio")
            
            # Process audio for speech recognition
            text, confidence, metadata = self.speech_processor.recognize_audio(audio_data)
            
            print(f"[VOICE] Recognition result: '{text}' (confidence: {confidence})")
            
            # Only process if we have valid text
            if text is not None and text.strip() and confidence > 0.1:
                print(f"[VOICE] Valid speech detected: '{text}'")
                self._process_user_input(text, confidence, metadata, source="voice")
            else:
                print(f"[VOICE] No valid speech detected")
        except Exception as e:
            import traceback
            print(f"[VOICE] ERROR: {e}")
            print(f"[VOICE] Traceback: {traceback.format_exc()}")
    
    def _process_user_input(self, text: str, confidence: float, metadata: Dict[str, Any], source: str = "keyboard"):
        """Process user input through the complete pipeline."""
        try:
            # Update UI with recognized text
            self._update_conversation(f"User ({source}): {text}")
            
            # Check for wake word
            if not self.keyword_matcher.detect_wake_word(text):
                self._respond("Please say 'Hey Sigma' first to activate the assistant.")
                return
            
            # Clean text (remove wake word and variations)
            clean_text = text.lower()
            wake_word_variations = [
                "hey sigma", "sigma", "assistant",
                "play sigma", "hey cig", "cig", "say sigma",
                "hey cigma", "cigma", "hey sig", "sig",
                "a sigma", "hey signal", "signal",
                "hey seema", "seema"
            ]
            for wake_word in wake_word_variations:
                clean_text = clean_text.replace(wake_word, "").strip()
            
            # Remove leading punctuation
            clean_text = clean_text.lstrip(',').lstrip('.').lstrip('!').lstrip('?').strip()
            
            if not clean_text:
                self._respond("Yes, I'm listening. How can I help you?")
                return
            
            # Process text
            processed_text = self.text_processor.process(clean_text)
            
            # Classify intent
            intent_result = self.intent_classifier.classify(clean_text)
            
            # Execute skill
            skill_context = SkillContext(
                user_input=clean_text,
                intent=intent_result.intent.value,
                entities=intent_result.entities,
                confidence=intent_result.confidence,
                session_id='combined_session'
            )
            skill_result = self.skill_manager.execute_best_skill(skill_context)
            
            if skill_result.success:
                self._respond(skill_result.message)
            else:
                error_msg = skill_result.error if skill_result.error else "Unknown error"
                self._respond(f"I'm sorry, I couldn't help with that. {error_msg}")
            
        except Exception as e:
            import traceback
            print(f"Error processing user input: {e}")
            print(traceback.format_exc())
            self._respond("I'm sorry, I encountered an error. Please try again.")
    
    def _respond(self, text: str):
        """Generate and display response."""
        self._update_conversation(f"Sigma: {text}")
        self.cache_manager.cache_speech_result("combined", text, 1.0)
        self._update_stats()
    
    def _create_ui(self):
        """Create the user interface."""
        # Configure CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Sigma Voice Assistant - Combined Mode")
        self.root.geometry("900x750")
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Main title
        title_label = ctk.CTkLabel(
            self.root, 
            text="Sigma Voice Assistant", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Mode indicator
        mode_label = ctk.CTkLabel(
            self.root,
            text="Combined Mode: Type commands OR use voice (Click Start Listening)",
            font=ctk.CTkFont(size=12),
            text_color="green"
        )
        mode_label.pack(pady=(0, 10))
        
        # Status frame
        status_frame = ctk.CTkFrame(self.root)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = ctk.CTkLabel(
            status_frame, 
            text="Ready - Type or speak your commands", 
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=10)
        
        # Voice control frame
        voice_frame = ctk.CTkFrame(self.root)
        voice_frame.pack(fill="x", padx=20, pady=5)
        
        voice_label = ctk.CTkLabel(voice_frame, text="Voice Control:", font=ctk.CTkFont(size=12, weight="bold"))
        voice_label.pack(side="left", padx=10, pady=10)
        
        self.voice_button = ctk.CTkButton(
            voice_frame,
            text="Start Listening",
            command=self._toggle_voice_listening,
            height=40,
            width=150,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.voice_button.pack(side="left", padx=10, pady=10)
        
        self.voice_status_label = ctk.CTkLabel(
            voice_frame,
            text="Voice: OFF",
            font=ctk.CTkFont(size=12),
            text_color="red"
        )
        self.voice_status_label.pack(side="left", padx=10)
        
        # Quick commands frame
        quick_frame = ctk.CTkFrame(self.root)
        quick_frame.pack(fill="x", padx=20, pady=5)
        
        quick_label = ctk.CTkLabel(quick_frame, text="Quick Commands:", font=ctk.CTkFont(size=12, weight="bold"))
        quick_label.pack(pady=(10, 5))
        
        buttons_frame = ctk.CTkFrame(quick_frame)
        buttons_frame.pack(pady=(0, 10))
        
        # Quick command buttons
        commands = [
            ("What can you do?", "Hey Sigma, what can you do?"),
            ("Time", "Hey Sigma, what time is it?"),
            ("Set Reminder", "Hey Sigma, set a reminder for 5 minutes"),
            ("Open Calculator", "Hey Sigma, open calculator")
        ]
        
        for i, (btn_text, command) in enumerate(commands):
            btn = ctk.CTkButton(
                buttons_frame,
                text=btn_text,
                command=lambda cmd=command: self._send_quick_command(cmd),
                width=150,
                height=30
            )
            btn.grid(row=0, column=i, padx=5, pady=5)
        
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
            height=250,
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
        
        test_mic_button = ctk.CTkButton(
            button_frame,
            text="Test Microphone",
            command=self._test_microphone,
            width=150
        )
        test_mic_button.pack(side="left", padx=5)
        
        # Stats label
        self.stats_label = ctk.CTkLabel(
            self.root, 
            text="Cache: 0 items | Skills: 8 | Executions: 0",
            font=ctk.CTkFont(size=10)
        )
        self.stats_label.pack(pady=(0, 10))
        
        # Add welcome message
        self._update_conversation("Welcome to Sigma Voice Assistant (Combined Mode)!")
        self._update_conversation("You can TYPE commands OR click 'Start Listening' to use your voice!")
        self._update_conversation("Try clicking a quick command button or type in the field below!")
        
        # Focus on input
        self.input_entry.focus()
    
    def _toggle_voice_listening(self):
        """Toggle voice listening on/off."""
        if not self.is_voice_listening:
            # Start voice listening
            if self.audio_input.start_recording():
                self.is_voice_listening = True
                self.voice_button.configure(text="Stop Listening")
                self.voice_status_label.configure(text="Voice: ACTIVE", text_color="green")
                self.status_label.configure(text="Listening for 'Hey Sigma'...")
                self._update_conversation("Voice listening activated! Say 'Hey Sigma' followed by your command.")
            else:
                messagebox.showerror("Error", "Failed to start microphone. Please check your microphone settings.")
        else:
            # Stop voice listening
            self.audio_input.stop_recording()
            self.is_voice_listening = False
            self.voice_button.configure(text="Start Listening")
            self.voice_status_label.configure(text="Voice: OFF", text_color="red")
            self.status_label.configure(text="Voice stopped - You can still type commands")
            self._update_conversation("Voice listening stopped. You can still type commands!")
    
    def _send_quick_command(self, command):
        """Send a quick command."""
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, command)
        self._process_keyboard_input()
    
    def _on_enter_pressed(self, event):
        """Handle Enter key press."""
        self._process_keyboard_input()
    
    def _process_keyboard_input(self):
        """Process keyboard input."""
        text = self.input_entry.get().strip()
        if not text:
            return
        
        # Clear input
        self.input_entry.delete(0, tk.END)
        
        # Process as user input
        self._process_user_input(text, 1.0, {}, source="keyboard")
    
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
    
    def _test_microphone(self):
        """Show microphone test information."""
        msg = """Microphone Test:

To test your microphone volume, run this in PowerShell:
python test_microphone_volume.py

Your microphone should show levels above 10,000 when speaking.

If levels are too low:
1. Right-click speaker icon
2. Open Sound settings
3. Increase microphone volume to 100%
4. Enable Microphone Boost (+20dB or +30dB)
"""
        messagebox.showinfo("Microphone Test", msg)
    
    def _on_closing(self):
        """Handle window closing."""
        try:
            if self.is_voice_listening:
                self.audio_input.stop_recording()
            self.scheduler.shutdown()
            self.audio_input.cleanup()
            self.audio_output.cleanup()
            self.root.destroy()
        except Exception as e:
            print(f"Error during shutdown: {e}")
            self.root.destroy()
    
    def run(self):
        """Run the application."""
        self._create_ui()
        
        print("Application started. You can type commands or use voice!")
        self.root.mainloop()
        
        # Cleanup
        if self.is_voice_listening:
            self.audio_input.stop_recording()
        self.scheduler.shutdown()


def main():
    """Main entry point."""
    try:
        app = SigmaVoiceAssistantCombined()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

