"""
Animated Status Indicator Component
Provides smooth animations for status changes
"""

import customtkinter as ctk
import math
from typing import Dict, Any, Optional

class AnimatedStatusIndicator(ctk.CTkFrame):
    """Animated status indicator with smooth transitions"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Animation state
        self.is_animating = False
        self.animation_step = 0
        self.max_animation_steps = 20
        self.animation_speed = 50  # milliseconds
        
        # Status colors
        self.status_colors = {
            "idle": "#6c757d",      # Gray
            "listening": "#007acc",  # Blue
            "processing": "#ffc107", # Yellow
            "speaking": "#28a745",   # Green
            "error": "#dc3545"       # Red
        }
        
        # Current status
        self.current_status = "idle"
        
        # Create the indicator circle
        self.canvas = ctk.CTkCanvas(
            self,
            width=20,
            height=20,
            highlightthickness=0,
            bg="#2d2d2d"  # Fixed color instead of dynamic
        )
        self.canvas.pack(expand=True, fill="both")
        
        # Draw initial indicator
        self._draw_indicator()
    
    def _draw_indicator(self):
        """Draw the status indicator circle"""
        self.canvas.delete("all")
        
        # Get current color
        color = self.status_colors.get(self.current_status, "#6c757d")
        
        # Calculate animation effect
        if self.is_animating and self.current_status in ["listening", "processing"]:
            # Pulsing effect
            pulse_factor = 0.8 + 0.4 * math.sin(self.animation_step * 0.3)
            size = int(8 * pulse_factor)
            alpha = int(255 * (0.6 + 0.4 * pulse_factor))
        else:
            # Static indicator
            size = 8
            alpha = 255
        
        # Draw the circle
        x, y = 10, 10  # Center of canvas
        self.canvas.create_oval(
            x - size, y - size,
            x + size, y + size,
            fill=color,
            outline="",
            width=0
        )
    
    def set_status(self, status: str, animate: bool = True):
        """Set the status with optional animation"""
        if status not in self.status_colors:
            return
        
        self.current_status = status
        
        if animate and status in ["listening", "processing"]:
            self._start_animation()
        else:
            self._stop_animation()
        
        self._draw_indicator()
    
    def _start_animation(self):
        """Start the pulsing animation"""
        if not self.is_animating:
            self.is_animating = True
            self.animation_step = 0
            self._animate_step()
    
    def _stop_animation(self):
        """Stop the animation"""
        self.is_animating = False
    
    def _animate_step(self):
        """Perform one animation step"""
        if self.is_animating:
            self.animation_step += 1
            self._draw_indicator()
            # Schedule next animation frame
            self.after(self.animation_speed, self._animate_step)

if __name__ == "__main__":
    # Test the animated status indicator
    root = ctk.CTk()
    root.title("Animated Status Test")
    
    # Create test frame
    test_frame = ctk.CTkFrame(root)
    test_frame.pack(padx=20, pady=20)
    
    # Create status indicator
    status_indicator = AnimatedStatusIndicator(test_frame, width=40, height=40)
    status_indicator.pack(pady=10)
    
    # Test buttons
    buttons_frame = ctk.CTkFrame(test_frame)
    buttons_frame.pack(pady=10)
    
    def test_status(status):
        status_indicator.set_status(status, animate=True)
    
    ctk.CTkButton(buttons_frame, text="Idle", command=lambda: test_status("idle")).pack(side="left", padx=5)
    ctk.CTkButton(buttons_frame, text="Listening", command=lambda: test_status("listening")).pack(side="left", padx=5)
    ctk.CTkButton(buttons_frame, text="Processing", command=lambda: test_status("processing")).pack(side="left", padx=5)
    ctk.CTkButton(buttons_frame, text="Speaking", command=lambda: test_status("speaking")).pack(side="left", padx=5)
    ctk.CTkButton(buttons_frame, text="Error", command=lambda: test_status("error")).pack(side="left", padx=5)
    
    root.mainloop()
