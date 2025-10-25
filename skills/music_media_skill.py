"""
Music & Media Control Skill - Advanced media playback control
Provides comprehensive control over music players and media applications.
"""

import webbrowser
import urllib.parse
import subprocess
import platform
from typing import Dict, Any, Optional
from skills.base_skill import BaseSkill, SkillContext, SkillResult, SkillPriority
import re


class MusicMediaSkill(BaseSkill):
    """
    Advanced skill for controlling music and media playback.
    Features:
    - Play music on YouTube
    - Spotify integration
    - System volume control
    - Media player control (play/pause/stop)
    - Search and play songs
    """
    
    def __init__(self):
        super().__init__(
            name="music_media",
            description="Control music playback and volume",
            priority=SkillPriority.HIGH
        )
        
        self.system = platform.system()
        
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle the request."""
        user_input = context.user_input.lower()
        
        # More flexible music keywords
        music_keywords = [
            "play", "music", "song", "audio", "spotify", "youtube music",
            "listen", "play music", "play song", "playlist", "album", "artist",
            "play track", "play audio", "music player", "media player", "stream",
            "youtube", "sound", "tune", "melody", "rhythm", "beat"
        ]
        
        # More flexible media control keywords
        control_keywords = [
            "pause", "resume", "stop", "next", "previous", "skip", "back",
            "volume", "mute", "unmute", "louder", "quieter", "sound",
            "playback", "media control", "music control", "audio control",
            "turn up", "turn down", "increase volume", "decrease volume"
        ]
        
        has_music = any(keyword in user_input for keyword in music_keywords)
        has_control = any(keyword in user_input for keyword in control_keywords)
        
        return has_music or has_control
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute music or media control command."""
        user_input = context.user_input.lower()
        
        try:
            # Volume control
            if any(word in user_input for word in ["volume", "mute", "unmute", "louder", "quieter"]):
                return self._handle_volume_control(user_input)
            
            # Play music/song
            elif "play" in user_input:
                return self._handle_play_music(user_input)
            
            # Spotify control
            elif "spotify" in user_input:
                return self._handle_spotify(user_input)
            
            # Media control (pause/resume/stop/next/prev)
            elif any(word in user_input for word in ["pause", "resume", "stop", "next", "previous"]):
                return self._handle_media_control(user_input)
            
            else:
                return SkillResult(
                    success=False,
                    message="I can play music, control volume, and manage playback. Try 'play Bohemian Rhapsody' or 'volume up'",
                    data={},
                    execution_time=0.0,
                    skill_name=self.name
                )
        
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Sorry, I encountered an error: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _handle_play_music(self, user_input: str) -> SkillResult:
        """Handle playing music."""
        # Extract song/artist name
        song = self._extract_song_name(user_input)
        
        if not song:
            return SkillResult(
                success=False,
                message="What would you like me to play?",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        # Determine platform (Spotify or YouTube)
        if "spotify" in user_input:
            # Spotify search URL
            spotify_url = f"https://open.spotify.com/search/{urllib.parse.quote(song)}"
            webbrowser.open(spotify_url)
            
            message = f"🎵 Opening '{song}' on Spotify..."
            platform_used = "Spotify"
        else:
            # YouTube Music search (more reliable for general music)
            youtube_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song + ' official audio')}"
            webbrowser.open(youtube_url)
            
            message = f"🎵 Searching YouTube for '{song}'..."
            platform_used = "YouTube"
        
        return SkillResult(
            success=True,
            message=message,
            data={"song": song, "platform": platform_used},
            execution_time=0.0,
            skill_name=self.name
        )
    
    def _handle_spotify(self, user_input: str) -> SkillResult:
        """Handle Spotify-specific commands."""
        if "play" in user_input:
            song = self._extract_song_name(user_input)
            if song:
                spotify_url = f"https://open.spotify.com/search/{urllib.parse.quote(song)}"
            else:
                spotify_url = "https://open.spotify.com"
            
            webbrowser.open(spotify_url)
            
            message = f"🎵 Opening Spotify..." if not song else f"🎵 Searching Spotify for '{song}'..."
            
            return SkillResult(
                success=True,
                message=message,
                data={"platform": "Spotify", "song": song},
                execution_time=0.0,
                skill_name=self.name
            )
        else:
            # Just open Spotify
            webbrowser.open("https://open.spotify.com")
            
            return SkillResult(
                success=True,
                message="🎵 Opening Spotify...",
                data={"platform": "Spotify"},
                execution_time=0.0,
                skill_name=self.name
            )
    
    def _handle_volume_control(self, user_input: str) -> SkillResult:
        """Handle volume control commands."""
        try:
            if self.system == "Windows":
                if "mute" in user_input and "unmute" not in user_input:
                    # Mute volume
                    subprocess.run(["powershell", "-Command", 
                                  "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"], 
                                  check=True, capture_output=True)
                    return SkillResult(
                        success=True,
                        message="🔇 Volume muted",
                        data={"action": "mute"},
                        execution_time=0.0,
                        skill_name=self.name
                    )
                
                elif "unmute" in user_input:
                    # Unmute
                    subprocess.run(["powershell", "-Command", 
                                  "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"], 
                                  check=True, capture_output=True)
                    return SkillResult(
                        success=True,
                        message="🔊 Volume unmuted",
                        data={"action": "unmute"},
                        execution_time=0.0,
                        skill_name=self.name
                    )
                
                elif any(word in user_input for word in ["up", "louder", "higher", "increase"]):
                    # Volume up (5 times for noticeable change)
                    for _ in range(5):
                        subprocess.run(["powershell", "-Command", 
                                      "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"], 
                                      check=True, capture_output=True)
                    return SkillResult(
                        success=True,
                        message="🔊 Volume increased",
                        data={"action": "volume_up"},
                        execution_time=0.0,
                        skill_name=self.name
                    )
                
                elif any(word in user_input for word in ["down", "quieter", "lower", "decrease"]):
                    # Volume down
                    for _ in range(5):
                        subprocess.run(["powershell", "-Command", 
                                      "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"], 
                                      check=True, capture_output=True)
                    return SkillResult(
                        success=True,
                        message="🔉 Volume decreased",
                        data={"action": "volume_down"},
                        execution_time=0.0,
                        skill_name=self.name
                    )
                
                else:
                    return SkillResult(
                        success=False,
                        message="I can help with 'volume up', 'volume down', 'mute', or 'unmute'",
                        data={},
                        execution_time=0.0,
                        skill_name=self.name
                    )
            
            elif self.system == "Darwin":  # macOS
                if "mute" in user_input:
                    subprocess.run(["osascript", "-e", "set volume output muted true"], check=True)
                    return SkillResult(
                        success=True,
                        message="🔇 Volume muted",
                        data={"action": "mute"},
                        execution_time=0.0,
                        skill_name=self.name
                    )
                elif "unmute" in user_input:
                    subprocess.run(["osascript", "-e", "set volume output muted false"], check=True)
                    return SkillResult(
                        success=True,
                        message="🔊 Volume unmuted",
                        data={"action": "unmute"},
                        execution_time=0.0,
                        skill_name=self.name
                    )
                elif any(word in user_input for word in ["up", "louder"]):
                    subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"], check=True)
                    return SkillResult(
                        success=True,
                        message="🔊 Volume increased",
                        data={"action": "volume_up"},
                        execution_time=0.0,
                        skill_name=self.name
                    )
                elif any(word in user_input for word in ["down", "quieter"]):
                    subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"], check=True)
                    return SkillResult(
                        success=True,
                        message="🔉 Volume decreased",
                        data={"action": "volume_down"},
                        execution_time=0.0,
                        skill_name=self.name
                    )
            
            else:  # Linux
                return SkillResult(
                    success=False,
                    message="Volume control is currently supported on Windows and macOS",
                    data={},
                    execution_time=0.0,
                    skill_name=self.name
                )
        
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Couldn't control volume: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _handle_media_control(self, user_input: str) -> SkillResult:
        """Handle media playback control (play/pause/next/previous)."""
        try:
            if self.system == "Windows":
                if "pause" in user_input or "stop" in user_input:
                    # Pause/Play toggle
                    subprocess.run(["powershell", "-Command", 
                                  "(New-Object -ComObject WScript.Shell).SendKeys([char]179)"], 
                                  check=True, capture_output=True)
                    return SkillResult(
                        success=True,
                        message="⏸️ Media paused/resumed",
                        data={"action": "pause"},
                        execution_time=0.0,
                        skill_name=self.name
                    )
                
                elif "resume" in user_input or "continue" in user_input:
                    # Play
                    subprocess.run(["powershell", "-Command", 
                                  "(New-Object -ComObject WScript.Shell).SendKeys([char]179)"], 
                                  check=True, capture_output=True)
                    return SkillResult(
                        success=True,
                        message="▶️ Media resumed",
                        data={"action": "resume"},
                        execution_time=0.0,
                        skill_name=self.name
                    )
                
                elif "next" in user_input:
                    # Next track
                    subprocess.run(["powershell", "-Command", 
                                  "(New-Object -ComObject WScript.Shell).SendKeys([char]176)"], 
                                  check=True, capture_output=True)
                    return SkillResult(
                        success=True,
                        message="⏭️ Next track",
                        data={"action": "next"},
                        execution_time=0.0,
                        skill_name=self.name
                    )
                
                elif "previous" in user_input or "back" in user_input:
                    # Previous track
                    subprocess.run(["powershell", "-Command", 
                                  "(New-Object -ComObject WScript.Shell).SendKeys([char]177)"], 
                                  check=True, capture_output=True)
                    return SkillResult(
                        success=True,
                        message="⏮️ Previous track",
                        data={"action": "previous"},
                        execution_time=0.0,
                        skill_name=self.name
                    )
            
            return SkillResult(
                success=False,
                message="Media control is currently supported on Windows",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Couldn't control media: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _extract_song_name(self, user_input: str) -> Optional[str]:
        """Extract song name from user input."""
        patterns = [
            r'play\s+(?:song\s+|music\s+)?(.+?)(?:\s+on\s+(?:spotify|youtube))?$',
            r'play\s+(?:the\s+)?song\s+(.+)',
            r'listen\s+to\s+(.+)',
            r'play\s+(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                song = match.group(1).strip()
                # Remove common filler words
                song = re.sub(r'\b(song|music|track|by|from|the)\b', '', song, flags=re.IGNORECASE)
                song = song.strip()
                if song:
                    return song
        
        return None


# Skill registration
def get_skill():
    """Factory function to get the skill instance."""
    return MusicMediaSkill()




