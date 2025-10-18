"""
Sigma Voice Assistant - Main Application
A sophisticated voice assistant demonstrating advanced data structures and algorithms.
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

# Import audio components
from audio.input_handler import AudioInputHandler, AudioConfig
from audio.output_handler import AudioOutputHandler, TTSConfig, VoiceGender, SpeechRate

# Import NLP components
from nlp.speech_to_text import SpeechToTextProcessor, RecognitionConfig, RecognitionEngine
from nlp.intent_classifier import HybridIntentClassifier, IntentType
from nlp.text_processor import TextProcessor

# Import skills
from skills.base_skill import SkillManager, SkillRegistry
from skills.reminder_skill import ReminderSkill, RecurringReminderSkill
from skills.file_skill import FileSearchSkill, FileManagementSkill
from skills.app_skill import AppLauncherSkill, SystemControlSkill
from skills.info_skill import InfoSkill


class SigmaVoiceAssistant:
    """
    Main voice assistant application integrating all components.
    Demonstrates system architecture and component integration.
    """
    
    def __init__(self):
        self.is_running = False
        self.session_id = f"session_{int(time.time())}"
        
        # Initialize core components
        self.keyword_matcher = KeywordMatcher()
        self.state_machine = DialogueStateMachine()
        self.scheduler = PriorityScheduler(max_workers=4)
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
        self.skill_registry = SkillRegistry(self.skill_manager)
        self._register_skills()
        
        # Initialize UI
        self.root = None
        self.setup_ui()
        
        # Event queues for thread communication
        self.audio_queue = queue.Queue()
        self.response_queue = queue.Queue()
        
        # Callback setup
        self._setup_callbacks()
    
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
        
        # Register info skill
        info_skill = InfoSkill()
        self.skill_manager.register_skill(info_skill)
        
        print(f"Registered {len(self.skill_manager.skills)} skills")
    
    def _setup_callbacks(self):
        """Setup callbacks for component communication."""
        # Audio input callbacks
        self.audio_input.add_callback(self._on_audio_received)
        
        # Speech recognition callbacks
        self.speech_processor.add_callback(self._on_speech_recognized)
        
        # Audio output callbacks
        self.audio_output.add_callback(self._on_speech_completed)
    
    def _on_audio_received(self, audio_data: bytes):
        """Handle received audio data."""
        try:
            print(f"[AUDIO CALLBACK] Received {len(audio_data)} bytes of audio data")
            
            # Process audio for speech recognition
            text, confidence, metadata = self.speech_processor.recognize_audio(audio_data)
            
            print(f"[AUDIO CALLBACK] Recognition result - text: '{text}', confidence: {confidence}, metadata: {metadata}")
            
            # Only process if we have valid text (not None) - very sensitive
            if text is not None and text.strip() and confidence > 0.1:
                print(f"[AUDIO CALLBACK] Valid speech detected: '{text}' (confidence: {confidence})")
                self._process_user_input(text, confidence, metadata)
            else:
                print(f"[AUDIO CALLBACK] No valid speech detected (text: {text}, confidence: {confidence})")
        except Exception as e:
            import traceback
            print(f"[AUDIO CALLBACK] ERROR processing audio: {e}")
            print(f"[AUDIO CALLBACK] Traceback: {traceback.format_exc()}")
    
    def _on_speech_recognized(self, event: str, data: Dict[str, Any]):
        """Handle speech recognition events."""
        if event == 'recognition_success' and 'text' in data:
            self._process_user_input(data['text'], data['confidence'], data['metadata'])
    
    def _on_speech_completed(self, event: str, data: Dict[str, Any]):
        """Handle speech synthesis completion."""
        if event == 'speech_finished':
            self._update_ui_status("Ready to listen...")
    
    def _process_user_input(self, text: str, confidence: float, metadata: Dict[str, Any]):
        """Process user input through the complete pipeline."""
        try:
            # Validate input
            if text is None or not text.strip():
                print("Warning: Empty or None text received")
                return
                
            # Update UI with recognized text
            self._update_ui_conversation(f"User: {text}")
            
            # Check for wake word
            if not self.keyword_matcher.detect_wake_word(text):
                print(f"Wake word not detected in: '{text}'")
                return
            
            # Process through state machine
            self.state_machine.process_event(EventType.WAKE_WORD_DETECTED, {
                'user_input': text,
                'confidence': confidence
            })
            
            # Clean text (remove wake word) - handle None text
            if text is None:
                print("Warning: Received None text from speech recognition")
                return
                
            clean_text = text.lower()
            for wake_word in ["hey sigma", "sigma", "assistant"]:
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
            
            # Update state machine
            self.state_machine.process_event(EventType.INTENT_CLASSIFIED, {
                'intent': intent_result.intent.value,
                'confidence': intent_result.confidence,
                'entities': intent_result.entities
            })
            
            # Create skill context
            context = self._create_skill_context(clean_text, intent_result)
            
            # Execute appropriate skill
            result = self.skill_manager.execute_best_skill(context)
            
            # Generate response
            if result.success:
                self._respond(result.message)
            else:
                self._respond("I'm sorry, I couldn't help with that. Could you please try rephrasing your request?")
            
        except Exception as e:
            print(f"Error processing user input: {e}")
            self._respond("I'm sorry, I encountered an error. Please try again.")
    
    def _create_skill_context(self, text: str, intent_result) -> Any:
        """Create skill context from processed input."""
        from skills.base_skill import SkillContext
        
        return SkillContext(
            user_input=text,
            intent=intent_result.intent.value,
            entities=intent_result.entities,
            confidence=intent_result.confidence,
            session_id=self.session_id
        )
    
    def _respond(self, message: str):
        """Generate and speak response."""
        try:
            # Update UI
            self._update_ui_conversation(f"Sigma: {message}")
            
            # Speak response
            self.audio_output.speak(message)
            
            # Update state machine
            self.state_machine.process_event(EventType.RESPONSE_READY, {
                'response': message
            })
            
        except Exception as e:
            print(f"Error generating response: {e}")
    
    def setup_ui(self):
        """Setup the user interface."""
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Sigma Voice Assistant")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Create main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Sigma Voice Assistant", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Status frame
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(
            status_frame, 
            text="Initializing...", 
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=10)
        
        # Conversation frame
        conversation_frame = ctk.CTkFrame(main_frame)
        conversation_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        conversation_label = ctk.CTkLabel(
            conversation_frame, 
            text="Conversation", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        conversation_label.pack(pady=(10, 5))
        
        # Conversation text area
        self.conversation_text = scrolledtext.ScrolledText(
            conversation_frame,
            wrap=tk.WORD,
            height=15,
            font=("Arial", 11),
            bg="#2b2b2b",
            fg="white",
            insertbackground="white"
        )
        self.conversation_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Control frame
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Start/Stop button
        self.start_button = ctk.CTkButton(
            control_frame,
            text="Start Listening",
            command=self._toggle_listening,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.start_button.pack(side="left", padx=10, pady=10)
        
        # Clear button
        clear_button = ctk.CTkButton(
            control_frame,
            text="Clear",
            command=self._clear_conversation,
            font=ctk.CTkFont(size=12),
            height=40
        )
        clear_button.pack(side="left", padx=5, pady=10)
        
        # Settings button
        settings_button = ctk.CTkButton(
            control_frame,
            text="Settings",
            command=self._show_settings,
            font=ctk.CTkFont(size=12),
            height=40
        )
        settings_button.pack(side="right", padx=10, pady=10)
        
        # Stats frame
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Ready to start",
            font=ctk.CTkFont(size=10)
        )
        self.stats_label.pack(pady=5)
    
    def _update_ui_status(self, status: str):
        """Update status label."""
        if self.status_label:
            self.status_label.configure(text=status)
    
    def _add_greeting(self):
        """Add a friendly greeting when the assistant starts."""
        import random
        
        greetings = [
            "Hello! How can I help you today? I'm ready to assist with tasks, reminders, and more! 😊",
            "Hi there! What would you like me to help you with today? I'm here and listening! 🎯",
            "Good day! I'm Sigma, your personal assistant. How can I make your day better? ✨",
            "Hello! I'm here to help you stay organized and get things done. What can I do for you? 💪",
            "Hi! Ready to tackle some tasks together? Just say 'Hey Sigma' and let me know what you need! 🚀",
            "Good to see you! I can help with scheduling, files, apps, and much more. What's on your mind? 🤔",
            "Hello there! I'm powered by advanced AI and ready to assist. How can I help you today? 🧠"
        ]
        
        greeting = random.choice(greetings)
        self._update_ui_conversation(f"Sigma: {greeting}")
        
        # Also speak the greeting
        try:
            self.audio_output.speak(greeting)
        except Exception as e:
            print(f"Could not speak greeting: {e}")
    
    def _update_ui_conversation(self, message: str):
        """Update conversation text area."""
        if self.conversation_text:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.conversation_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.conversation_text.see(tk.END)
    
    def _update_ui_stats(self):
        """Update statistics display."""
        if self.stats_label:
            try:
                # Get cache stats
                cache_stats = self.cache_manager.get_all_statistics()
                total_cache_size = sum(stats['size'] for stats in cache_stats.values())
                
                # Get skill stats
                skill_stats = self.skill_manager.get_skill_statistics()
                total_executions = sum(stats['execution_count'] for stats in skill_stats.values())
                
                stats_text = f"Cache: {total_cache_size} items | Skills: {len(skill_stats)} | Executions: {total_executions}"
                self.stats_label.configure(text=stats_text)
            except Exception as e:
                self.stats_label.configure(text=f"Stats error: {e}")
    
    def _toggle_listening(self):
        """Toggle audio listening."""
        if not self.is_running:
            self._start_assistant()
        else:
            self._stop_assistant()
    
    def _start_assistant(self):
        """Start the voice assistant."""
        try:
            # Start audio input
            if not self.audio_input.start_recording():
                messagebox.showerror("Error", "Failed to start audio recording")
                return
            
            # Update UI
            self.is_running = True
            self.start_button.configure(text="Stop Listening")
            self._update_ui_status("Listening for 'Hey Sigma'...")
            self._update_ui_conversation("Sigma Voice Assistant started. Say 'Hey Sigma' to begin.")
            
            # Start stats update thread
            self._start_stats_thread()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start assistant: {e}")
    
    def _stop_assistant(self):
        """Stop the voice assistant."""
        try:
            # Stop audio input safely
            if hasattr(self, 'audio_input') and self.audio_input:
                self.audio_input.stop_recording()
            
            # Update UI
            self.is_running = False
            self.start_button.configure(text="Start Listening")
            self._update_ui_status("Stopped")
            self._update_ui_conversation("Sigma Voice Assistant stopped.")
            
        except Exception as e:
            print(f"Error stopping assistant: {e}")
            # Still update UI even if there was an error
            self.is_running = False
            self.start_button.configure(text="Start Listening")
            self._update_ui_status("Stopped")
            self._update_ui_conversation("Sigma Voice Assistant stopped.")
    
    def _start_stats_thread(self):
        """Start statistics update thread."""
        def update_stats():
            while self.is_running:
                try:
                    self.root.after(0, self._update_ui_stats)
                    time.sleep(5)  # Update every 5 seconds
                except:
                    break
        
        stats_thread = threading.Thread(target=update_stats, daemon=True)
        stats_thread.start()
    
    def _clear_conversation(self):
        """Clear conversation text area."""
        if self.conversation_text:
            self.conversation_text.delete(1.0, tk.END)
    
    def _show_settings(self):
        """Show settings dialog."""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Settings content
        settings_frame = ctk.CTkFrame(settings_window)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Voice settings
        voice_label = ctk.CTkLabel(settings_frame, text="Voice Settings", font=ctk.CTkFont(size=16, weight="bold"))
        voice_label.pack(pady=(0, 10))
        
        # Speech rate
        rate_label = ctk.CTkLabel(settings_frame, text="Speech Rate:")
        rate_label.pack(anchor="w", pady=(0, 5))
        
        rate_slider = ctk.CTkSlider(settings_frame, from_=50, to=400, number_of_steps=35)
        rate_slider.set(200)  # Default normal rate
        rate_slider.pack(fill="x", pady=(0, 10))
        
        # Volume
        volume_label = ctk.CTkLabel(settings_frame, text="Volume:")
        volume_label.pack(anchor="w", pady=(0, 5))
        
        volume_slider = ctk.CTkSlider(settings_frame, from_=0, to=1, number_of_steps=100)
        volume_slider.set(0.8)  # Default volume
        volume_slider.pack(fill="x", pady=(0, 20))
        
        # Apply button
        apply_button = ctk.CTkButton(
            settings_frame,
            text="Apply",
            command=lambda: self._apply_settings(rate_slider.get(), volume_slider.get())
        )
        apply_button.pack(pady=10)
    
    def _apply_settings(self, rate: float, volume: float):
        """Apply settings changes."""
        try:
            self.audio_output.set_speech_rate(int(rate))
            self.audio_output.set_volume(volume)
            messagebox.showinfo("Settings", "Settings applied successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply settings: {e}")
    
    def _on_closing(self):
        """Handle application closing."""
        try:
            self._stop_assistant()
            self.scheduler.shutdown()
            self.audio_input.cleanup()
            self.audio_output.cleanup()
            self.root.destroy()
        except Exception as e:
            print(f"Error during shutdown: {e}")
            self.root.destroy()
    
    def run(self):
        """Run the voice assistant application."""
        try:
            self._update_ui_status("Ready to start")
            self._update_ui_conversation("Welcome to Sigma Voice Assistant!\nClick 'Start Listening' to begin.")
            
            # Add greeting when starting
            self._add_greeting()
            self.root.mainloop()
        except Exception as e:
            print(f"Error running application: {e}")
            messagebox.showerror("Error", f"Application error: {e}")


def main():
    """Main entry point."""
    print("Starting Sigma Voice Assistant...")
    print("This application demonstrates advanced data structures and algorithms:")
    print("- Trie-based keyword matching")
    print("- Finite state machine for dialogue management")
    print("- Priority heap-based task scheduling")
    print("- LRU cache for performance optimization")
    print("- Graph-based search algorithms")
    print("- Machine learning for intent classification")
    print("- Plugin architecture for extensible skills")
    print()
    
    try:
        app = SigmaVoiceAssistant()
        app.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


