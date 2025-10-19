"""
Jarvis Voice Assistant - Professional Modern UI
Beautiful, animated, and user-friendly interface
"""

import sys
import os
import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
import customtkinter as ctk
from typing import Optional, Dict, Any
import queue
from datetime import datetime
import math

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import core components
from core.trie import KeywordMatcher
from core.state_machine import DialogueStateMachine, EventType, StateType
from core.scheduler import PriorityScheduler
from core.cache import CacheManager
from core.graph_search import FileSystemGraph

# Import NLP components
from nlp.intent_classifier import HybridIntentClassifier
from nlp.text_processor import TextProcessor

# Import speech recognition directly
import speech_recognition as sr

# Import skills
from skills.base_skill import SkillManager, SkillRegistry, SkillContext
from skills.reminder_skill import ReminderSkill, RecurringReminderSkill
from skills.file_skill import FileSearchSkill, FileManagementSkill
from skills.app_skill import AppLauncherSkill, SystemControlSkill
from skills.info_skill import InfoSkill
from skills.help_skill import HelpSkill


# Modern Color Palette
class Colors:
    # Primary colors
    PRIMARY = "#6366F1"  # Indigo
    PRIMARY_DARK = "#4F46E5"
    PRIMARY_LIGHT = "#818CF8"
    
    # Accent colors
    ACCENT = "#EC4899"  # Pink
    ACCENT_LIGHT = "#F472B6"
    
    SUCCESS = "#10B981"  # Green
    WARNING = "#F59E0B"  # Amber
    DANGER = "#EF4444"   # Red
    INFO = "#3B82F6"     # Blue
    
    # Neutrals
    BG_DARK = "#0F172A"      # Slate 900
    BG_MEDIUM = "#1E293B"    # Slate 800
    BG_LIGHT = "#334155"     # Slate 700
    
    TEXT_PRIMARY = "#F1F5F9"    # Slate 100
    TEXT_SECONDARY = "#CBD5E1"  # Slate 300
    TEXT_DIM = "#94A3B8"        # Slate 400
    
    BORDER = "#475569"  # Slate 600


class AnimatedButton(ctk.CTkButton):
    """Button with hover animation effects"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.original_fg_color = self.cget("fg_color")
        
    def on_enter(self, e):
        self.configure(cursor="hand2")
        
    def on_leave(self, e):
        self.configure(cursor="")


class StatusIndicator(ctk.CTkFrame):
    """Animated status indicator with pulsing effect"""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(fg_color="transparent")
        
        self.canvas = tk.Canvas(
            self, 
            width=20, 
            height=20, 
            bg=Colors.BG_MEDIUM, 
            highlightthickness=0
        )
        self.canvas.pack()
        
        self.circle = self.canvas.create_oval(5, 5, 15, 15, fill=Colors.TEXT_DIM, outline="")
        self.is_active = False
        self.animation_running = False
        
    def set_status(self, status: str):
        """Set status: idle, listening, processing, speaking"""
        self.status = status
        
        color_map = {
            "idle": Colors.TEXT_DIM,
            "listening": Colors.SUCCESS,
            "processing": Colors.WARNING,
            "speaking": Colors.INFO,
            "error": Colors.DANGER
        }
        
        color = color_map.get(status, Colors.TEXT_DIM)
        self.canvas.itemconfig(self.circle, fill=color)
        
        if status in ["listening", "processing", "speaking"]:
            if not self.animation_running:
                self.start_pulse()
        else:
            self.stop_pulse()
    
    def start_pulse(self):
        """Start pulsing animation"""
        self.animation_running = True
        self.pulse_animation(0)
        
    def stop_pulse(self):
        """Stop pulsing animation"""
        self.animation_running = False
        
    def pulse_animation(self, step):
        """Animate the pulsing effect"""
        if not self.animation_running:
            return
            
        # Calculate size based on sine wave
        scale = 0.8 + 0.2 * abs(math.sin(step * 0.1))
        base_size = 10
        size = base_size * scale
        offset = (20 - size) / 2
        
        self.canvas.coords(self.circle, offset, offset, offset + size, offset + size)
        
        # Continue animation
        self.after(50, lambda: self.pulse_animation(step + 1))


class ConversationBubble(ctk.CTkFrame):
    """Chat bubble for conversation display"""
    
    def __init__(self, parent, message: str, is_user: bool, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Configure appearance
        if is_user:
            self.configure(fg_color=Colors.PRIMARY, corner_radius=15)
            text_color = Colors.TEXT_PRIMARY
        else:
            self.configure(fg_color=Colors.BG_LIGHT, corner_radius=15)
            text_color = Colors.TEXT_PRIMARY
            
        # Message label
        self.label = ctk.CTkLabel(
            self,
            text=message,
            text_color=text_color,
            wraplength=450,
            justify="left",
            font=ctk.CTkFont(size=13)
        )
        self.label.pack(padx=15, pady=10)


class JarvisVoiceAssistantPro:
    """
    Professional Voice Assistant with Modern UI
    """
    
    def __init__(self):
        self.is_running = False
        self.is_recording = False
        self.session_id = f"session_{int(time.time())}"
        
        # Initialize components
        self._init_core_components()
        self._init_nlp_components()
        self._init_skills()
        
        # Initialize speech recognition (push-to-talk mode)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Calibrate microphone
        print("Calibrating microphone...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.recognizer.energy_threshold = 300
        print("Microphone ready!")
        
        # Initialize UI
        self.root = None
        self.setup_ui()
        
        # Event queues
        self.message_queue = queue.Queue()
        self.ui_update_queue = queue.Queue()
        
        # Start UI update loop
        self.process_ui_updates()
        
    def _init_core_components(self):
        """Initialize core components"""
        print("Initializing core components...")
        self.keyword_matcher = KeywordMatcher()
        self.state_machine = DialogueStateMachine()
        self.scheduler = PriorityScheduler(max_workers=4)
        self.cache_manager = CacheManager()
        self.fs_graph = FileSystemGraph()
        
        
    def _init_nlp_components(self):
        """Initialize NLP components"""
        print("Initializing NLP components...")
        self.intent_classifier = HybridIntentClassifier()
        self.text_processor = TextProcessor()
        
    def _init_skills(self):
        """Initialize and register skills"""
        print("Initializing skills...")
        self.skill_manager = SkillManager()
        self.skill_registry = SkillRegistry(self.skill_manager)
        
        # Register skills
        skills = [
            ReminderSkill(self.scheduler),
            RecurringReminderSkill(self.scheduler),
            FileSearchSkill(self.fs_graph),
            FileManagementSkill(),
            AppLauncherSkill(self.fs_graph),
            SystemControlSkill(),
            InfoSkill(),
            HelpSkill()
        ]
        
        for skill in skills:
            self.skill_manager.register_skill(skill)
            
        print(f"Registered {len(self.skill_manager.skills)} skills")
        
            
    def _process_user_input(self, text: str, confidence: float, metadata: Dict[str, Any]):
        """Process user input through the complete pipeline"""
        try:
            if not text or not text.strip():
                return
                
            # Add to UI
            self.ui_update_queue.put(("message", {"text": text, "is_user": True}))
            
            # Check for wake word
            if not self.keyword_matcher.detect_wake_word(text):
                return
                
            # Process through state machine
            self.state_machine.process_event(EventType.WAKE_WORD_DETECTED, {
                'user_input': text,
                'confidence': confidence
            })
            
            # Clean text (remove wake word)
            clean_text = text.lower()
            for wake_word in ["hey sigma", "sigma", "assistant"]:
                clean_text = clean_text.replace(wake_word, "").strip()
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
            context = SkillContext(
                user_input=clean_text,
                intent=intent_result.intent.value,
                entities=intent_result.entities,
                confidence=intent_result.confidence,
                session_id=self.session_id
            )
            
            # Execute appropriate skill
            result = self.skill_manager.execute_best_skill(context)
            
            # Generate response
            if result.success:
                self._respond(result.message)
            else:
                self._respond("I'm sorry, I couldn't help with that. Could you please try rephrasing?")
                
        except Exception as e:
            print(f"Error processing user input: {e}")
            import traceback
            traceback.print_exc()
            self._respond("I encountered an error. Please try again.")
            
    def _respond(self, message: str):
        """Generate response"""
        try:
            # Update UI
            self.ui_update_queue.put(("message", {"text": message, "is_user": False}))
            
            # Update state machine
            self.state_machine.process_event(EventType.RESPONSE_READY, {
                'response': message
            })
            
        except Exception as e:
            print(f"Error generating response: {e}")
            
    def setup_ui(self):
        """Setup the modern professional user interface"""
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Jarvis Voice Assistant - Professional Edition")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Configure window background
        self.root.configure(fg_color=Colors.BG_DARK)
        
        # Create main container
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create top bar
        self._create_top_bar(main_container)
        
        # Create content area
        content_container = ctk.CTkFrame(main_container, fg_color="transparent")
        content_container.pack(fill="both", expand=True, pady=(20, 0))
        
        # Create left panel (conversation)
        self._create_conversation_panel(content_container)
        
        # Create right panel (controls & info)
        self._create_control_panel(content_container)
        
        # Create bottom bar
        self._create_bottom_bar(main_container)
        
    def _create_top_bar(self, parent):
        """Create top bar with title and status"""
        top_bar = ctk.CTkFrame(parent, fg_color=Colors.BG_MEDIUM, corner_radius=15, height=80)
        top_bar.pack(fill="x", pady=(0, 10))
        top_bar.pack_propagate(False)
        
        # Left side - Title and logo
        left_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        left_frame.pack(side="left", padx=20, pady=15)
        
        title_label = ctk.CTkLabel(
            left_frame,
            text="⚡ Jarvis Assistant",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=Colors.PRIMARY_LIGHT
        )
        title_label.pack(side="left")
        
        # Right side - Status indicator
        right_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        right_frame.pack(side="right", padx=20, pady=15)
        
        self.status_indicator = StatusIndicator(right_frame)
        self.status_indicator.pack(side="left", padx=(0, 10))
        
        self.status_text = ctk.CTkLabel(
            right_frame,
            text="Idle",
            font=ctk.CTkFont(size=14),
            text_color=Colors.TEXT_SECONDARY
        )
        self.status_text.pack(side="left")
        
    def _create_conversation_panel(self, parent):
        """Create conversation panel"""
        conv_panel = ctk.CTkFrame(parent, fg_color=Colors.BG_MEDIUM, corner_radius=15)
        conv_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Header
        header = ctk.CTkFrame(conv_panel, fg_color="transparent", height=50)
        header.pack(fill="x", padx=20, pady=(15, 10))
        header.pack_propagate(False)
        
        header_label = ctk.CTkLabel(
            header,
            text="Conversation",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        header_label.pack(side="left")
        
        # Clear button
        clear_btn = ctk.CTkButton(
            header,
            text="Clear",
            width=80,
            height=30,
            corner_radius=8,
            fg_color=Colors.BG_LIGHT,
            hover_color=Colors.BG_DARK,
            command=self._clear_conversation
        )
        clear_btn.pack(side="right")
        
        # Scrollable conversation area
        self.conversation_frame = ctk.CTkScrollableFrame(
            conv_panel,
            fg_color=Colors.BG_DARK,
            corner_radius=10
        )
        self.conversation_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Welcome message - ATTRACTIVE AND ONE LINE!
        self._add_conversation_bubble("🎉 Welcome to Jarvis Voice Assistant! Hold the green button to speak or type commands below! 🚀", False)
        
    def _create_control_panel(self, parent):
        """Create control panel"""
        control_panel = ctk.CTkFrame(parent, fg_color=Colors.BG_MEDIUM, corner_radius=15, width=350)
        control_panel.pack(side="right", fill="y")
        control_panel.pack_propagate(False)
        
        # Header
        header = ctk.CTkLabel(
            control_panel,
            text="Controls",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        header.pack(pady=(20, 15))
        
        # Main action button - PUSH TO TALK
        self.main_button = AnimatedButton(
            control_panel,
            text="🎤 HOLD TO SPEAK",
            width=280,
            height=60,
            corner_radius=30,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=Colors.SUCCESS,
            hover_color="#059669"
        )
        self.main_button.pack(pady=(10, 20))
        
        # Bind push-to-talk events
        self.main_button.bind("<ButtonPress-1>", self._start_recording)
        self.main_button.bind("<ButtonRelease-1>", self._stop_recording)
        
        # Mode info
        mode_label = ctk.CTkLabel(
            control_panel,
            text="HOLD button while speaking",
            font=ctk.CTkFont(size=11),
            text_color=Colors.WARNING
        )
        mode_label.pack()
        
        # Text input section - COMPACT BUT BETTER!
        input_label = ctk.CTkLabel(
            control_panel,
            text="Type a Command",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Colors.TEXT_SECONDARY
        )
        input_label.pack(pady=(10, 5))
        
        # Text entry - BIGGER BUT NOT TOO BIG!
        self.text_entry = ctk.CTkEntry(
            control_panel,
            width=280,
            height=45,
            corner_radius=10,
            placeholder_text="Hey Jarvis, what time is it?",
            font=ctk.CTkFont(size=13),
            border_width=1,
            border_color=Colors.BORDER
        )
        self.text_entry.pack(pady=(0, 8))
        self.text_entry.bind("<Return>", lambda e: self._on_text_submit())
        
        # Send button - COMPACT!
        send_btn = AnimatedButton(
            control_panel,
            text="📤 Send",
            width=280,
            height=35,
            corner_radius=10,
            fg_color=Colors.INFO,
            hover_color=Colors.PRIMARY_DARK,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_text_submit
        )
        send_btn.pack(pady=(0, 15))
        
        # Divider
        divider = ctk.CTkFrame(control_panel, height=2, fg_color=Colors.BORDER)
        divider.pack(fill="x", padx=20, pady=10)
        
        # Quick actions - BETTER STYLING!
        actions_label = ctk.CTkLabel(
            control_panel,
            text="Quick Actions",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        actions_label.pack(pady=(10, 8))
        
        quick_actions = [
            ("What time is it?", "⏰"),
            ("System info", "💻"),
            ("Set reminder", "⏲️"),
            ("Open calculator", "🔢"),
        ]
        
        for action, emoji in quick_actions:
            btn = ctk.CTkButton(
                control_panel,
                text=f"{emoji} {action}",
                width=280,
                height=38,
                corner_radius=12,
                fg_color=Colors.BG_LIGHT,
                hover_color=Colors.PRIMARY_LIGHT,
                text_color=Colors.TEXT_PRIMARY,
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w",
                command=lambda a=action: self._quick_action(a)
            )
            btn.pack(pady=2)
        
        # Settings button (at bottom)
        settings_btn = AnimatedButton(
            control_panel,
            text="⚙️ Settings",
            width=280,
            height=35,
            corner_radius=10,
            fg_color=Colors.BG_LIGHT,
            hover_color=Colors.BG_DARK,
            command=self._show_settings
        )
        settings_btn.pack(side="bottom", pady=(10, 20))
        
    def _create_bottom_bar(self, parent):
        """Create bottom status bar"""
        bottom_bar = ctk.CTkFrame(parent, fg_color=Colors.BG_MEDIUM, corner_radius=15, height=60)
        bottom_bar.pack(fill="x", pady=(10, 0))
        bottom_bar.pack_propagate(False)
        
        # Statistics
        self.stats_label = ctk.CTkLabel(
            bottom_bar,
            text="Ready | Skills: 8 | Session: Active",
            font=ctk.CTkFont(size=12),
            text_color=Colors.TEXT_DIM
        )
        self.stats_label.pack(side="left", padx=20)
        
        # Version info
        version_label = ctk.CTkLabel(
            bottom_bar,
            text="v2.0 Professional",
            font=ctk.CTkFont(size=11),
            text_color=Colors.TEXT_DIM
        )
        version_label.pack(side="right", padx=20)
        
    def _add_conversation_bubble(self, text: str, is_user: bool):
        """Add a conversation bubble"""
        # Create container for alignment
        container = ctk.CTkFrame(self.conversation_frame, fg_color="transparent")
        container.pack(fill="x", pady=5)
        
        # Create bubble
        bubble = ConversationBubble(container, text, is_user)
        
        if is_user:
            bubble.pack(side="right", padx=(100, 10))
        else:
            bubble.pack(side="left", padx=(10, 100))
        
        # Auto-scroll to bottom after adding message
        self._scroll_to_bottom()
    
    def _scroll_to_bottom(self):
        """Automatically scroll conversation to bottom"""
        try:
            # Update the display first
            self.conversation_frame.update()
            
            # Get the canvas from the scrollable frame
            canvas = self.conversation_frame._parent_canvas
            
            # Scroll to the very bottom
            canvas.yview_moveto(1.0)
            
            # Force update
            self.conversation_frame.update()
            
        except Exception as e:
            print(f"Scroll error: {e}")
            
    def _clear_conversation(self):
        """Clear conversation history"""
        for widget in self.conversation_frame.winfo_children():
            widget.destroy()
        self._add_conversation_bubble("Conversation cleared. How can I help you?", False)
        
    def _start_recording(self, event):
        """Start recording when button is pressed (push-to-talk)"""
        if self.is_recording:
            return
        
        self.is_recording = True
        self.main_button.configure(text="🔴 RECORDING...", fg_color=Colors.DANGER)
        self.ui_update_queue.put(("status", "listening"))
        self._add_conversation_bubble("🎤 Recording... speak now!", False)
        
        # Start recording in background thread
        threading.Thread(target=self._record_audio, daemon=True).start()
    
    def _stop_recording(self, event):
        """Stop recording when button is released"""
        if not self.is_recording:
            return
        
        self.is_recording = False
        self.main_button.configure(text="🎤 HOLD TO SPEAK", fg_color=Colors.SUCCESS)
        self.ui_update_queue.put(("status", "processing"))
    
    def _record_audio(self):
        """Record audio using speech_recognition push-to-talk"""
        try:
            with self.microphone as source:
                print("Recording started...")
                
                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                
                print(f"Audio captured: {len(audio.frame_data)} bytes")
                
                # Process in background
                self.root.after(0, lambda: self._process_audio(audio))
        
        except Exception as e:
            print(f"Recording error: {e}")
            self.root.after(0, lambda: self._add_conversation_bubble(f"❌ Error: {str(e)}", False))
            self.root.after(0, lambda: self.ui_update_queue.put(("status", "idle")))
    
    def _process_audio(self, audio):
        """Process recorded audio"""
        try:
            self._add_conversation_bubble("🔄 Recognizing speech...", False)
            
            # Try Google recognition
            text = self.recognizer.recognize_google(audio, language="en-US")
            
            print(f"Recognized: '{text}'")
            
            # Process the command
            self._process_user_input(text, 1.0, {})
            
            self.ui_update_queue.put(("status", "idle"))
        
        except Exception as e:
            error_msg = "Couldn't understand - speak louder and clearer"
            if "network" in str(e).lower():
                error_msg = "Network error - check internet connection"
            
            print(f"Recognition error: {e}")
            self._add_conversation_bubble(f"❌ {error_msg}", False)
            self.ui_update_queue.put(("status", "idle"))
            
    def _on_text_submit(self):
        """Handle text input submission"""
        text = self.text_entry.get().strip()
        if text:
            self.text_entry.delete(0, tk.END)
            # Process as if it was spoken
            self._process_user_input(text, 1.0, {})
            
    def _quick_action(self, action: str):
        """Execute a quick action"""
        command = f"Hey Jarvis, {action}"
        self.text_entry.delete(0, tk.END)
        self.text_entry.insert(0, command)
        self._on_text_submit()
        
    def _show_settings(self):
        """Show settings dialog"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x400")
        settings_window.transient(self.root)
        settings_window.grab_set()
        settings_window.configure(fg_color=Colors.BG_DARK)
        
        # Header
        header = ctk.CTkLabel(
            settings_window,
            text="Settings",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        header.pack(pady=20)
        
        # Settings frame
        settings_frame = ctk.CTkFrame(settings_window, fg_color=Colors.BG_MEDIUM, corner_radius=15)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Voice settings
        voice_label = ctk.CTkLabel(
            settings_frame,
            text="Voice Settings",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        voice_label.pack(pady=(20, 10))
        
        # Speech rate
        rate_label = ctk.CTkLabel(settings_frame, text="Speech Rate:", text_color=Colors.TEXT_SECONDARY)
        rate_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        rate_slider = ctk.CTkSlider(settings_frame, from_=50, to=400, number_of_steps=35, width=400)
        rate_slider.set(200)
        rate_slider.pack(padx=20, pady=(0, 10))
        
        # Volume
        volume_label = ctk.CTkLabel(settings_frame, text="Volume:", text_color=Colors.TEXT_SECONDARY)
        volume_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        volume_slider = ctk.CTkSlider(settings_frame, from_=0, to=1, number_of_steps=100, width=400)
        volume_slider.set(0.8)
        volume_slider.pack(padx=20, pady=(0, 20))
        
        # Apply button
        apply_button = AnimatedButton(
            settings_frame,
            text="Apply Settings",
            width=200,
            height=40,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_DARK,
            command=lambda: self._apply_settings(rate_slider.get(), volume_slider.get(), settings_window)
        )
        apply_button.pack(pady=20)
        
    def _apply_settings(self, rate: float, volume: float, window):
        """Apply settings changes"""
        try:
            # Settings can be applied here if needed
            self._add_conversation_bubble("Settings saved!", False)
            window.destroy()
        except Exception as e:
            self._add_conversation_bubble(f"Error applying settings: {str(e)}", False)
            
    def process_ui_updates(self):
        """Process UI updates from queue"""
        try:
            while not self.ui_update_queue.empty():
                update_type, data = self.ui_update_queue.get_nowait()
                
                if update_type == "status":
                    self._update_status(data)
                elif update_type == "message":
                    self._add_conversation_bubble(data["text"], data["is_user"])
                    
        except queue.Empty:
            pass
        finally:
            # Schedule next update
            if self.root:
                self.root.after(100, self.process_ui_updates)
                
    def _update_status(self, status: str):
        """Update status indicator"""
        status_map = {
            "idle": "Idle",
            "listening": "Listening...",
            "processing": "Processing...",
            "speaking": "Speaking...",
            "error": "Error"
        }
        
        self.status_indicator.set_status(status)
        self.status_text.configure(text=status_map.get(status, "Unknown"))
        
        # Update stats
        cache_size = sum(stats['size'] for stats in self.cache_manager.get_all_statistics().values())
        skill_count = len(self.skill_manager.skills)
        self.stats_label.configure(text=f"{status_map.get(status, 'Unknown')} | Skills: {skill_count} | Cache: {cache_size} items")
        
    def _on_closing(self):
        """Handle application closing"""
        try:
            self.scheduler.shutdown()
            self.root.destroy()
        except Exception as e:
            print(f"Error during shutdown: {e}")
            self.root.destroy()
            
    def run(self):
        """Run the voice assistant application"""
        try:
            print("Starting Jarvis Voice Assistant Professional Edition...")
            # Welcome message already added in setup_ui
            self.root.mainloop()
        except Exception as e:
            print(f"Error running application: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Main entry point"""
    print("=" * 60)
    print("Jarvis Voice Assistant - Professional Edition")
    print("=" * 60)
    print("\nFeatures:")
    print("- Modern animated UI")
    print("- Voice and text input")
    print("- 8 intelligent skills")
    print("- Advanced NLP and ML")
    print("- Real-time status updates")
    print("\nStarting application...\n")
    
    try:
        app = JarvisVoiceAssistantPro()
        app.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

