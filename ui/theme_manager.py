"""
Advanced Theme Manager for Jarvis Voice Assistant
Provides multiple professional color schemes and theme switching
"""

import customtkinter as ctk
from typing import Dict, Any, Tuple
from enum import Enum

class ThemeType(Enum):
    """Available theme types"""
    PROFESSIONAL_DARK = "professional_dark"
    PROFESSIONAL_LIGHT = "professional_light"
    CYBER_PUNK = "cyber_punk"
    OCEAN_BLUE = "ocean_blue"
    FOREST_GREEN = "forest_green"
    SUNSET_ORANGE = "sunset_orange"

class ThemeManager:
    """Manages themes and color schemes for the UI"""
    
    def __init__(self):
        self.current_theme = ThemeType.PROFESSIONAL_DARK
        self.themes = self._initialize_themes()
        
    def _initialize_themes(self) -> Dict[ThemeType, Dict[str, Any]]:
        """Initialize all available themes"""
        return {
            ThemeType.PROFESSIONAL_DARK: {
                "name": "Professional Dark",
                "colors": {
                    "bg_primary": "#0f0f0f",
                    "bg_secondary": "#1a1a1a", 
                    "bg_tertiary": "#2a2a2a",
                    "accent": "#ffffff",
                    "accent_hover": "#e0e0e0",
                    "text_primary": "#ffffff",
                    "text_secondary": "#cccccc",
                    "text_accent": "#ffffff",
                    "success": "#00ff00",
                    "warning": "#ffff00",
                    "error": "#ff0000",
                    "border": "#333333"
                },
                "appearance_mode": "dark"
            },
            
            ThemeType.PROFESSIONAL_LIGHT: {
                "name": "Sunshine Bright",
                "colors": {
                    "bg_primary": "#fff8dc",
                    "bg_secondary": "#ffeb3b",
                    "bg_tertiary": "#ffc107",
                    "accent": "#ff5722",
                    "accent_hover": "#e64a19",
                    "text_primary": "#8d4004",
                    "text_secondary": "#b8860b",
                    "text_accent": "#ff5722",
                    "success": "#4caf50",
                    "warning": "#ff9800",
                    "error": "#f44336",
                    "border": "#ffc107"
                },
                "appearance_mode": "light"
            },
            
            ThemeType.CYBER_PUNK: {
                "name": "Matrix Green",
                "colors": {
                    "bg_primary": "#001100",
                    "bg_secondary": "#003300",
                    "bg_tertiary": "#005500",
                    "accent": "#00ff00",
                    "accent_hover": "#00cc00",
                    "text_primary": "#00ff00",
                    "text_secondary": "#00cc00",
                    "text_accent": "#00ff00",
                    "success": "#00ff00",
                    "warning": "#ffff00",
                    "error": "#ff0000",
                    "border": "#00ff00"
                },
                "appearance_mode": "dark"
            },
            
            ThemeType.OCEAN_BLUE: {
                "name": "Purple Dream",
                "colors": {
                    "bg_primary": "#2d1b69",
                    "bg_secondary": "#4a148c",
                    "bg_tertiary": "#6a1b9a",
                    "accent": "#e1bee7",
                    "accent_hover": "#ce93d8",
                    "text_primary": "#ffffff",
                    "text_secondary": "#e1bee7",
                    "text_accent": "#e1bee7",
                    "success": "#4caf50",
                    "warning": "#ff9800",
                    "error": "#f44336",
                    "border": "#9c27b0"
                },
                "appearance_mode": "dark"
            }
        }
    
    def get_current_theme(self) -> Dict[str, Any]:
        """Get the current theme configuration"""
        return self.themes[self.current_theme]
    
    def get_current_colors(self) -> Dict[str, str]:
        """Get the current theme colors"""
        return self.get_current_theme()["colors"]
    
    def set_theme(self, theme: ThemeType) -> None:
        """Set the active theme"""
        if theme in self.themes:
            self.current_theme = theme
            # Apply the theme to CustomTkinter
            theme_config = self.get_current_theme()
            ctk.set_appearance_mode(theme_config["appearance_mode"])
            
    def get_available_themes(self) -> Dict[ThemeType, str]:
        """Get all available theme names"""
        return {theme: config["name"] for theme, config in self.themes.items()}
    
    def get_accent_color(self) -> str:
        """Get the current accent color"""
        return self.get_current_colors()["accent"]
    
    def get_bg_color(self, level: str = "primary") -> str:
        """Get background color for specified level"""
        colors = self.get_current_colors()
        key = f"bg_{level}"
        return colors.get(key, colors["bg_primary"])
    
    def get_text_color(self, level: str = "primary") -> str:
        """Get text color for specified level"""
        colors = self.get_current_colors()
        key = f"text_{level}"
        return colors.get(key, colors["text_primary"])

# Global theme manager instance
theme_manager = ThemeManager()

if __name__ == "__main__":
    # Test the theme manager
    print("Theme Manager Test")
    print("Available themes:")
    for theme, name in theme_manager.get_available_themes().items():
        print(f"  - {name} ({theme.value})")
    
    print(f"\nCurrent theme: {theme_manager.get_current_theme()['name']}")
    print(f"Current accent color: {theme_manager.get_accent_color()}")
