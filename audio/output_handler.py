"""
Audio output handler with text-to-speech synthesis and audio playback.
Demonstrates audio synthesis and playback algorithms.
"""

import pyttsx3
import threading
import queue
import time
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass
from enum import Enum
import wave
import io


class VoiceGender(Enum):
    """Voice gender options."""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"


class SpeechRate(Enum):
    """Speech rate options."""
    VERY_SLOW = 50
    SLOW = 100
    NORMAL = 200
    FAST = 300
    VERY_FAST = 400


@dataclass
class TTSConfig:
    """Text-to-speech configuration."""
    voice_gender: VoiceGender = VoiceGender.FEMALE
    speech_rate: SpeechRate = SpeechRate.NORMAL
    volume: float = 0.8  # 0.0 to 1.0
    voice_id: Optional[str] = None
    language: str = "en"
    pitch: int = 50  # 0 to 100


class AudioOutputHandler:
    """
    Advanced audio output handler with text-to-speech capabilities.
    Features:
    - Multiple TTS engines
    - Voice customization
    - Audio queuing
    - Speech synthesis optimization
    - Audio format conversion
    """
    
    def __init__(self, config: TTSConfig = None):
        self.config = config or TTSConfig()
        self.tts_engine = None
        self.audio_queue = queue.Queue()
        self.is_speaking = False
        self.speech_thread = None
        self.callbacks = []
        self._initialize_tts()
    
    def _initialize_tts(self) -> None:
        """Initialize the TTS engine."""
        try:
            self.tts_engine = pyttsx3.init()
            self._configure_voice()
        except Exception as e:
            print(f"Error initializing TTS engine: {e}")
            self.tts_engine = None
    
    def _configure_voice(self) -> None:
        """Configure voice settings."""
        if not self.tts_engine:
            return
        
        # Set speech rate
        self.tts_engine.setProperty('rate', self.config.speech_rate.value)
        
        # Set volume
        self.tts_engine.setProperty('volume', self.config.volume)
        
        # Set voice
        voices = self.tts_engine.getProperty('voices')
        if voices:
            if self.config.voice_id:
                # Use specific voice ID
                for voice in voices:
                    if voice.id == self.config.voice_id:
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            else:
                # Select voice by gender
                for voice in voices:
                    if self.config.voice_gender.value in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
    
    def speak(self, text: str, blocking: bool = False) -> bool:
        """
        Convert text to speech and play it.
        Returns True if successful.
        """
        if not self.tts_engine:
            return False
        
        if blocking:
            return self._speak_blocking(text)
        else:
            return self._speak_async(text)
    
    def _speak_blocking(self, text: str) -> bool:
        """Synchronous speech synthesis."""
        try:
            self.is_speaking = True
            self._notify_callbacks('speech_started', {'text': text})
            
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
            self.is_speaking = False
            self._notify_callbacks('speech_finished', {'text': text})
            return True
        except Exception as e:
            print(f"Error in speech synthesis: {e}")
            self.is_speaking = False
            self._notify_callbacks('speech_error', {'error': str(e)})
            return False
    
    def _speak_async(self, text: str) -> bool:
        """Asynchronous speech synthesis."""
        try:
            self.audio_queue.put(text)
            
            if not self.is_speaking:
                self._start_speech_thread()
            
            return True
        except Exception as e:
            print(f"Error queuing speech: {e}")
            return False
    
    def _start_speech_thread(self) -> None:
        """Start the speech synthesis thread."""
        if self.speech_thread and self.speech_thread.is_alive():
            return
        
        self.speech_thread = threading.Thread(target=self._speech_loop, daemon=True)
        self.speech_thread.start()
    
    def _speech_loop(self) -> None:
        """Main speech synthesis loop."""
        while True:
            try:
                # Get next text from queue
                text = self.audio_queue.get(timeout=1.0)
                
                if text is None:  # Shutdown signal
                    break
                
                # Synthesize speech
                self._speak_blocking(text)
                
            except queue.Empty:
                # No more text to speak
                self.is_speaking = False
                break
            except Exception as e:
                print(f"Error in speech loop: {e}")
                break
    
    def add_callback(self, callback: Callable[[str, Dict], None]) -> None:
        """Add callback for speech events."""
        self.callbacks.append(callback)
    
    def _notify_callbacks(self, event: str, data: Dict[str, Any]) -> None:
        """Notify all callbacks of an event."""
        for callback in self.callbacks:
            try:
                callback(event, data)
            except Exception as e:
                print(f"Error in speech callback: {e}")
    
    def stop_speaking(self) -> None:
        """Stop current speech and clear queue."""
        if self.tts_engine:
            self.tts_engine.stop()
        
        # Clear queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break
        
        self.is_speaking = False
    
    def is_speaking_now(self) -> bool:
        """Check if currently speaking."""
        return self.is_speaking
    
    def get_available_voices(self) -> list:
        """Get list of available voices."""
        if not self.tts_engine:
            return []
        
        voices = self.tts_engine.getProperty('voices')
        return [
            {
                'id': voice.id,
                'name': voice.name,
                'gender': 'male' if 'male' in voice.name.lower() else 'female',
                'languages': getattr(voice, 'languages', [])
            }
            for voice in voices
        ]
    
    def set_voice(self, voice_id: str) -> bool:
        """Set specific voice by ID."""
        if not self.tts_engine:
            return False
        
        try:
            self.tts_engine.setProperty('voice', voice_id)
            self.config.voice_id = voice_id
            return True
        except Exception as e:
            print(f"Error setting voice: {e}")
            return False
    
    def set_speech_rate(self, rate: int) -> bool:
        """Set speech rate (words per minute)."""
        if not self.tts_engine:
            return False
        
        try:
            self.tts_engine.setProperty('rate', rate)
            self.config.speech_rate = SpeechRate(rate)
            return True
        except Exception as e:
            print(f"Error setting speech rate: {e}")
            return False
    
    def set_volume(self, volume: float) -> bool:
        """Set volume (0.0 to 1.0)."""
        if not self.tts_engine:
            return False
        
        try:
            volume = max(0.0, min(1.0, volume))  # Clamp to valid range
            self.tts_engine.setProperty('volume', volume)
            self.config.volume = volume
            return True
        except Exception as e:
            print(f"Error setting volume: {e}")
            return False
    
    def speak_with_emotion(self, text: str, emotion: str = "neutral") -> bool:
        """
        Speak text with emotional inflection.
        This is a simplified implementation - real TTS engines would need
        SSML or more advanced configuration.
        """
        if emotion == "excited":
            # Increase rate and volume
            original_rate = self.config.speech_rate
            original_volume = self.config.volume
            self.set_speech_rate(min(400, self.config.speech_rate.value + 50))
            self.set_volume(min(1.0, self.config.volume + 0.2))
            result = self.speak(text)
            self.set_speech_rate(original_rate.value)
            self.set_volume(original_volume)
            return result
        elif emotion == "calm":
            # Decrease rate and volume
            original_rate = self.config.speech_rate
            original_volume = self.config.volume
            self.set_speech_rate(max(50, self.config.speech_rate.value - 50))
            self.set_volume(max(0.1, self.config.volume - 0.2))
            result = self.speak(text)
            self.set_speech_rate(original_rate.value)
            self.set_volume(original_volume)
            return result
        else:
            return self.speak(text)
    
    def save_speech_to_file(self, text: str, filename: str) -> bool:
        """Save synthesized speech to audio file."""
        if not self.tts_engine:
            return False
        
        try:
            self.tts_engine.save_to_file(text, filename)
            return True
        except Exception as e:
            print(f"Error saving speech to file: {e}")
            return False
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        self.stop_speaking()
        if self.tts_engine:
            self.tts_engine.stop()


class AudioPlayer:
    """
    Simple audio player for playing pre-recorded audio files.
    """
    
    def __init__(self):
        self.is_playing = False
        self.playback_thread = None
    
    def play_file(self, filename: str, blocking: bool = False) -> bool:
        """Play an audio file."""
        if blocking:
            return self._play_blocking(filename)
        else:
            return self._play_async(filename)
    
    def _play_blocking(self, filename: str) -> bool:
        """Synchronous audio playback."""
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            return True
        except Exception as e:
            print(f"Error playing audio file: {e}")
            return False
    
    def _play_async(self, filename: str) -> bool:
        """Asynchronous audio playback."""
        try:
            self.playback_thread = threading.Thread(
                target=self._play_blocking, 
                args=(filename,), 
                daemon=True
            )
            self.playback_thread.start()
            return True
        except Exception as e:
            print(f"Error starting audio playback: {e}")
            return False
    
    def stop_playback(self) -> None:
        """Stop current audio playback."""
        try:
            import pygame
            pygame.mixer.music.stop()
        except:
            pass
        
        self.is_playing = False


if __name__ == "__main__":
    # Demo the audio output handler
    config = TTSConfig(
        voice_gender=VoiceGender.FEMALE,
        speech_rate=SpeechRate.NORMAL,
        volume=0.8
    )
    
    handler = AudioOutputHandler(config)
    
    def speech_callback(event, data):
        print(f"Speech event: {event}, Data: {data}")
    
    handler.add_callback(speech_callback)
    
    print("Available voices:")
    voices = handler.get_available_voices()
    for voice in voices[:3]:  # Show first 3 voices
        print(f"  {voice['name']} ({voice['gender']})")
    
    print("\nTesting speech synthesis...")
    
    # Test basic speech
    handler.speak("Hello! I am Jarvis, your voice assistant.")
    
    # Test emotional speech
    time.sleep(2)
    handler.speak_with_emotion("I'm excited to help you today!", "excited")
    
    # Test calm speech
    time.sleep(2)
    handler.speak_with_emotion("Let me help you in a calm and peaceful way.", "calm")
    
    # Wait for speech to finish
    while handler.is_speaking_now():
        time.sleep(0.1)
    
    print("Speech synthesis demo completed.")
    handler.cleanup()




