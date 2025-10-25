"""
Progress Bar Widget Component
Provides smooth progress indication for long operations
"""

import customtkinter as ctk
from typing import Optional

class ProgressBarWidget(ctk.CTkFrame):
    """Animated progress bar with smooth transitions"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Progress state
        self.current_progress = 0
        self.max_progress = 100
        self.is_visible = False
        
        # Create progress bar frame
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.pack(fill="x", padx=10, pady=5)
        
        # Progress label
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Processing...",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        )
        self.progress_label.pack(side="left")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            width=200,
            height=8,
            progress_color="#007acc",
            fg_color="#2d2d2d"
        )
        self.progress_bar.pack(side="right", padx=(10, 0))
        self.progress_bar.set(0)
        
        # Initially hidden
        self.hide()
    
    def show(self, message: str = "Processing..."):
        """Show the progress bar"""
        self.progress_label.configure(text=message)
        self.progress_frame.pack(fill="x", padx=10, pady=5)
        self.is_visible = True
    
    def hide(self):
        """Hide the progress bar"""
        self.progress_frame.pack_forget()
        self.is_visible = False
    
    def set_progress(self, progress: int, message: Optional[str] = None):
        """Set progress value (0-100)"""
        if progress < 0:
            progress = 0
        elif progress > 100:
            progress = 100
        
        self.current_progress = progress
        self.progress_bar.set(progress / 100.0)
        
        if message:
            self.progress_label.configure(text=message)
        
        # Auto-hide when complete
        if progress >= 100:
            self.after(1000, self.hide)  # Hide after 1 second
    
    def increment_progress(self, amount: int = 10, message: Optional[str] = None):
        """Increment progress by amount"""
        new_progress = self.current_progress + amount
        self.set_progress(new_progress, message)
    
    def reset(self):
        """Reset progress to 0"""
        self.set_progress(0, "Processing...")

if __name__ == "__main__":
    # Test the progress bar widget
    root = ctk.CTk()
    root.title("Progress Bar Test")
    
    # Create test frame
    test_frame = ctk.CTkFrame(root)
    test_frame.pack(padx=20, pady=20)
    
    # Create progress bar
    progress_bar = ProgressBarWidget(test_frame)
    progress_bar.pack(pady=10)
    
    # Test buttons
    buttons_frame = ctk.CTkFrame(test_frame)
    buttons_frame.pack(pady=10)
    
    def test_show():
        progress_bar.show("Loading...")
        progress_bar.set_progress(50)
    
    def test_hide():
        progress_bar.hide()
    
    def test_complete():
        progress_bar.show("Completing...")
        progress_bar.set_progress(100, "Complete!")
    
    ctk.CTkButton(buttons_frame, text="Show Progress", command=test_show).pack(side="left", padx=5)
    ctk.CTkButton(buttons_frame, text="Hide Progress", command=test_hide).pack(side="left", padx=5)
    ctk.CTkButton(buttons_frame, text="Complete", command=test_complete).pack(side="left", padx=5)
    
    root.mainloop()



