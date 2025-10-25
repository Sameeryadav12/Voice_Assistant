"""
Jarvis Voice Assistant - Push-to-Talk Mode
SIMPLE & RELIABLE: Hold button to speak, release when done!
"""

import sys
import os
import time
import threading
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from typing import Dict, Any
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import core components
from core.trie import KeywordMatcher
from core.state_machine import DialogueStateMachine
from core.scheduler import PriorityScheduler
from core.cache import CacheManager
from core.graph_search import FileSystemGraph

# Import NLP
from nlp.intent_classifier import HybridIntentClassifier
from nlp.text_processor import TextProcessor

# Import skills
from skills.base_skill import SkillManager, SkillContext
from skills.reminder_skill import ReminderSkill, RecurringReminderSkill
from skills.file_skill import FileSearchSkill, FileManagementSkill
from skills.app_skill import AppLauncherSkill, SystemControlSkill
from skills.help_skill import HelpSkill
from skills.info_skill import InfoSkill

# Import speech recognition directly
import speech_recognition as sr


class PushToTalkAssistant:
    """Push-to-talk voice assistant - simple and reliable!"""
    
    def __init__(self):
        print("Starting Push-to-Talk Assistant...")
        
        # Initialize core
        self.keyword_matcher = KeywordMatcher()
        self.scheduler = PriorityScheduler()
        self.cache_manager = CacheManager()
        self.fs_graph = FileSystemGraph()
        self.intent_classifier = HybridIntentClassifier()
        self.text_processor = TextProcessor()
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        print("Calibrating microphone...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            self.recognizer.energy_threshold = 300  # Lower threshold
            self.recognizer.dynamic_energy_threshold = True
        print("Microphone calibrated!")
        
        # Initialize skills
        self.skill_manager = SkillManager()
        self._register_skills()
        
        # State
        self.root = None
        self.is_recording = False
        
        print("Components initialized!")
    
    def _register_skills(self):
        """Register all skills."""
        self.skill_manager.register_skill(ReminderSkill(self.scheduler))
        self.skill_manager.register_skill(RecurringReminderSkill(self.scheduler))
        self.skill_manager.register_skill(FileSearchSkill(self.fs_graph))
        self.skill_manager.register_skill(FileManagementSkill())
        self.skill_manager.register_skill(AppLauncherSkill(self.fs_graph))
        self.skill_manager.register_skill(SystemControlSkill())
        self.skill_manager.register_skill(HelpSkill())
        self.skill_manager.register_skill(InfoSkill())
        print(f"Registered {len(self.skill_manager.skills)} skills")
    
    def _create_ui(self):
        """Create UI."""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Jarvis - Push-to-Talk Mode")
        self.root.geometry("900x700")
        
        # Title
        title = ctk.CTkLabel(self.root, text="Jarvis Voice Assistant", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        
        # Mode info
        mode = ctk.CTkLabel(
            self.root,
            text="PUSH-TO-TALK MODE: Hold the button while speaking, release when done!",
            font=ctk.CTkFont(size=14),
            text_color="yellow"
        )
        mode.pack(pady=10)
        
        # Push-to-talk button (BIG!)
        self.talk_button = ctk.CTkButton(
            self.root,
            text="HOLD TO SPEAK",
            height=100,
            width=300,
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        self.talk_button.pack(pady=20)
        
        # Bind mouse events
        self.talk_button.bind("<ButtonPress-1>", self._start_recording)
        self.talk_button.bind("<ButtonRelease-1>", self._stop_recording)
        
        # Status
        self.status_label = ctk.CTkLabel(
            self.root,
            text="Ready - Hold button and speak!",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=10)
        
        # Keyboard input frame
        input_frame = ctk.CTkFrame(self.root)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(input_frame, text="Or type your command:", font=ctk.CTkFont(size=12)).pack(pady=5)
        
        self.input_entry = ctk.CTkEntry(input_frame, placeholder_text="Type here...", height=40, font=ctk.CTkFont(size=14))
        self.input_entry.pack(fill="x", padx=10, pady=5)
        self.input_entry.bind("<Return>", lambda e: self._process_keyboard_input())
        
        ctk.CTkButton(input_frame, text="Send", command=self._process_keyboard_input, height=35).pack(pady=5)
        
        # Conversation
        conv_frame = ctk.CTkFrame(self.root)
        conv_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(conv_frame, text="Conversation", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        self.conversation_text = ctk.CTkTextbox(conv_frame, height=250, font=ctk.CTkFont(size=12))
        self.conversation_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Welcome
        self._update_conversation("Welcome to Push-to-Talk Mode!")
        self._update_conversation("HOLD the green button while speaking, RELEASE when done!")
        self._update_conversation("Or just TYPE your commands below!")
        self._update_conversation("")
        self._update_conversation("Try: Hold button and say 'Hey Jarvis, what time is it?'")
    
    def _start_recording(self, event):
        """Start recording when button pressed."""
        if self.is_recording:
            return
        
        self.is_recording = True
        self.talk_button.configure(text="RECORDING...", fg_color="red")
        self.status_label.configure(text="Listening... speak now!")
        self._update_conversation("🎤 Recording...")
        
        # Start recording in background thread
        threading.Thread(target=self._record_audio, daemon=True).start()
    
    def _stop_recording(self, event):
        """Stop recording when button released."""
        if not self.is_recording:
            return
        
        self.is_recording = False
        self.talk_button.configure(text="HOLD TO SPEAK", fg_color="green")
        self.status_label.configure(text="Processing...")
    
    def _record_audio(self):
        """Record audio using speech_recognition."""
        try:
            with self.microphone as source:
                print("Recording started...")
                
                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                
                print(f"Audio captured: {len(audio.frame_data)} bytes")
                
                # Process in background
                self.root.after(0, lambda: self._process_audio(audio))
        
        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self._update_conversation("❌ Timeout - no speech detected"))
            self.root.after(0, lambda: self.status_label.configure(text="Ready - try again!"))
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self._update_conversation(f"❌ Error: {error_msg}"))
            self.root.after(0, lambda: self.status_label.configure(text="Ready"))
    
    def _process_audio(self, audio):
        """Process recorded audio."""
        try:
            self._update_conversation("🔄 Recognizing...")
            self.status_label.configure(text="Recognizing speech...")
            
            # Try Google recognition
            text = self.recognizer.recognize_google(audio, language="en-US")
            
            print(f"Recognized: '{text}'")
            self._update_conversation(f"👤 You said: {text}")
            
            # Process the command
            self._process_user_input(text, 1.0, {})
            
            self.status_label.configure(text="Ready - Hold button to speak again!")
        
        except sr.UnknownValueError:
            self._update_conversation("❌ Couldn't understand - speak louder and clearer")
            self.status_label.configure(text="Ready - try again!")
        except sr.RequestError as e:
            self._update_conversation(f"❌ Network error: {e}")
            self.status_label.configure(text="Ready")
        except Exception as e:
            self._update_conversation(f"❌ Error: {e}")
            self.status_label.configure(text="Ready")
    
    def _process_keyboard_input(self):
        """Process keyboard input."""
        text = self.input_entry.get().strip()
        if not text:
            return
        
        self.input_entry.delete(0, tk.END)
        self._update_conversation(f"👤 You typed: {text}")
        self._process_user_input(text, 1.0, {})
    
    def _process_user_input(self, text: str, confidence: float, metadata: Dict):
        """Process user input."""
        try:
            # Check wake word
            if not self.keyword_matcher.detect_wake_word(text):
                self._respond("Please say 'Hey Jarvis' first!")
                return
            
            # Clean text
            clean_text = text.lower()
            wake_variations = ["hey jarvis", "jarvis", "play jarvis"]
            for wake_word in wake_variations:
                clean_text = clean_text.replace(wake_word, "").strip()
            clean_text = clean_text.lstrip(',').lstrip('.').strip()
            
            if not clean_text:
                self._respond("Yes, I'm listening. How can I help?")
                return
            
            # Process
            intent_result = self.intent_classifier.classify(clean_text)
            
            skill_context = SkillContext(
                user_input=clean_text,
                intent=intent_result.intent.value,
                entities=intent_result.entities,
                confidence=intent_result.confidence,
                session_id='push_to_talk'
            )
            
            result = self.skill_manager.execute_best_skill(skill_context)
            
            if result.success:
                self._respond(result.message)
            else:
                self._respond(f"Sorry, I couldn't help with that. {result.error or ''}")
        
        except Exception as e:
            print(f"Error: {e}")
            self._respond("Sorry, I encountered an error.")
    
    def _respond(self, text: str):
        """Respond to user."""
        self._update_conversation(f"🤖 Jarvis: {text}")
    
    def _update_conversation(self, message: str):
        """Update conversation."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.conversation_text.insert("end", f"[{timestamp}] {message}\n")
        self.conversation_text.see("end")
    
    def run(self):
        """Run the assistant."""
        self._create_ui()
        self.root.mainloop()


def main():
    """Main entry point."""
    try:
        app = PushToTalkAssistant()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

