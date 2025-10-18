"""
Speech-to-text processing with multiple recognition engines and optimization.
Demonstrates audio processing, machine learning integration, and performance optimization.
"""

import speech_recognition as sr
import threading
import time
import hashlib
from typing import Optional, Dict, List, Callable, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np
import io
import wave


class RecognitionEngine(Enum):
    """Available speech recognition engines."""
    GOOGLE = "google"
    GOOGLE_CLOUD = "google_cloud"
    BING = "bing"
    AZURE = "azure"
    VOSK = "vosk"
    WHISPER = "whisper"


@dataclass
class RecognitionConfig:
    """Speech recognition configuration."""
    engine: RecognitionEngine = RecognitionEngine.GOOGLE
    language: str = "en-US"
    sample_rate: int = 16000  # Audio sample rate
    timeout: float = 10.0  # Longer timeout
    phrase_timeout: float = 0.5  # Longer phrase timeout
    energy_threshold: int = 100  # Lower threshold for more sensitivity
    dynamic_energy_threshold: bool = True
    pause_threshold: float = 0.5  # Shorter pause threshold
    operation_timeout: float = None
    api_key: Optional[str] = None
    model_path: Optional[str] = None  # For Vosk


class SpeechToTextProcessor:
    """
    Advanced speech-to-text processor with multiple engines and optimizations.
    Features:
    - Multiple recognition engines
    - Audio preprocessing
    - Confidence scoring
    - Caching
    - Error handling and fallbacks
    - Real-time processing
    """
    
    def __init__(self, config: RecognitionConfig = None):
        self.config = config or RecognitionConfig()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.cache = {}
        self.callbacks = []
        self._configure_recognizer()
        self._initialize_engine()
    
    def _configure_recognizer(self) -> None:
        """Configure the speech recognizer."""
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Set recognition parameters
        self.recognizer.energy_threshold = self.config.energy_threshold
        self.recognizer.dynamic_energy_threshold = self.config.dynamic_energy_threshold
        self.recognizer.pause_threshold = self.config.pause_threshold
        self.recognizer.operation_timeout = self.config.operation_timeout
        self.recognizer.phrase_timeout = self.config.phrase_timeout
    
    def _initialize_engine(self) -> None:
        """Initialize the specified recognition engine."""
        if self.config.engine == RecognitionEngine.VOSK:
            try:
                import vosk
                if self.config.model_path:
                    self.vosk_model = vosk.Model(self.config.model_path)
                    self.vosk_recognizer = vosk.KaldiRecognizer(self.vosk_model, 16000)
                else:
                    print("Warning: Vosk model path not provided")
            except ImportError:
                print("Warning: Vosk not available, falling back to Google")
                self.config.engine = RecognitionEngine.GOOGLE
    
    def add_callback(self, callback: Callable[[str, float, Dict], None]) -> None:
        """Add callback for recognition events."""
        self.callbacks.append(callback)
    
    def recognize_audio(self, audio_data: bytes, sample_rate: int = 16000) -> Tuple[Optional[str], float, Dict]:
        """
        Recognize speech from audio data.
        Returns (text, confidence, metadata)
        """
        print(f"[RECOGNIZE_AUDIO] Starting recognition with {len(audio_data)} bytes at {sample_rate}Hz")
        
        # Generate cache key
        audio_hash = hashlib.md5(audio_data).hexdigest()
        
        # Check cache first
        if audio_hash in self.cache:
            cached_result = self.cache[audio_hash]
            print(f"[RECOGNIZE_AUDIO] Cache hit for audio hash {audio_hash[:8]}")
            self._notify_callbacks('cache_hit', cached_result)
            return cached_result['text'], cached_result['confidence'], cached_result['metadata']
        
        # Preprocess audio
        processed_audio = self._preprocess_audio(audio_data, sample_rate)
        print(f"[RECOGNIZE_AUDIO] Audio preprocessed: {len(processed_audio)} bytes")
        
        # Recognize with selected engine
        try:
            if self.config.engine == RecognitionEngine.VOSK:
                print(f"[RECOGNIZE_AUDIO] Using VOSK engine")
                result = self._recognize_with_vosk(processed_audio)
            else:
                # Use ONLY Google - Sphinx hallucinates from noise
                print(f"[RECOGNIZE_AUDIO] Using Google (Sphinx disabled - hallucinates from noise)")
                result = self._recognize_with_google(processed_audio)
            
            # Cache result
            self.cache[audio_hash] = {
                'text': result['text'],
                'confidence': result['confidence'],
                'metadata': result['metadata'],
                'timestamp': time.time()
            }
            
            # Notify callbacks
            self._notify_callbacks('recognition_success', result)
            
            print(f"[RECOGNIZE_AUDIO] Final result: text='{result['text']}', confidence={result['confidence']}")
            return result['text'], result['confidence'], result['metadata']
            
        except Exception as e:
            import traceback
            print(f"[RECOGNIZE_AUDIO] ERROR: {e}")
            print(f"[RECOGNIZE_AUDIO] Traceback: {traceback.format_exc()}")
            error_result = {
                'text': None,
                'confidence': 0.0,
                'metadata': {'error': str(e), 'engine': self.config.engine.value}
            }
            self._notify_callbacks('recognition_error', error_result)
            return None, 0.0, error_result['metadata']
    
    def recognize_from_microphone(self, timeout: float = None) -> Tuple[Optional[str], float, Dict]:
        """Recognize speech directly from microphone."""
        timeout = timeout or self.config.timeout
        
        try:
            with self.microphone as source:
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout)
                
                # Convert to bytes for processing
                audio_data = audio.get_wav_data()
                
                return self.recognize_audio(audio_data, audio.sample_rate)
                
        except sr.WaitTimeoutError:
            return None, 0.0, {'error': 'No speech detected within timeout'}
        except Exception as e:
            return None, 0.0, {'error': str(e)}
    
    def _recognize_with_google(self, audio_data: bytes) -> Dict:
        """Recognize speech using Google's engine."""
        try:
            print(f"[SPEECH RECOG] Attempting recognition with {len(audio_data)} bytes")
            
            # Convert bytes to AudioData (16-bit samples, 16kHz, mono)
            audio = sr.AudioData(audio_data, 16000, 2)
            print(f"[SPEECH RECOG] Created AudioData: {len(audio.frame_data)} bytes")
            
            # Try with show_all=False first (simpler format)
            text = self.recognizer.recognize_google(
                audio, 
                language=self.config.language,
                show_all=False
            )
            
            print(f"[SPEECH RECOG] Google result: '{text}'")
            
            # With show_all=False, we get a simple string result
            recognized_text = str(text) if text else None
            confidence = 0.8  # Default confidence
            
            return {
                'text': recognized_text,
                'confidence': confidence,
                'metadata': {
                    'engine': 'google',
                    'language': self.config.language,
                    'raw_result': text
                }
            }
            
        except sr.UnknownValueError:
            print("[SPEECH RECOG] Google couldn't understand audio")
            return {
                'text': None,
                'confidence': 0.0,
                'metadata': {'error': 'Could not understand audio', 'engine': 'google'}
            }
        except sr.RequestError as e:
            print(f"[SPEECH RECOG] Google service error: {e}")
            return {
                'text': None,
                'confidence': 0.0,
                'metadata': {'error': f'Recognition service error: {e}', 'engine': 'google'}
            }
        except Exception as e:
            print(f"[SPEECH RECOG] Unexpected error: {e}")
            return {
                'text': None,
                'confidence': 0.0,
                'metadata': {'error': f'Unexpected error: {e}', 'engine': 'google'}
            }
    
    def _recognize_with_sphinx(self, audio_data: bytes) -> Dict:
        """Recognize speech using PocketSphinx (offline)."""
        try:
            print(f"[SPEECH RECOG] Attempting Sphinx recognition with {len(audio_data)} bytes")
            
            # Create AudioData object (sample_rate=16000, sample_width=2 for 16-bit audio)
            audio = sr.AudioData(audio_data, 16000, 2)
            print(f"[SPEECH RECOG] Created AudioData for Sphinx: {len(audio.frame_data)} bytes")
            
            # Perform recognition with Sphinx
            text = self.recognizer.recognize_sphinx(audio)
            
            print(f"[SPEECH RECOG] Sphinx result: '{text}'")
            
            # Convert to string if needed
            recognized_text = str(text) if text else None
            confidence = 0.7  # Sphinx doesn't provide confidence scores
            
            return {
                'text': recognized_text,
                'confidence': confidence,
                'metadata': {
                    'engine': 'sphinx',
                    'language': self.config.language,
                    'raw_result': text
                }
            }
            
        except sr.UnknownValueError:
            print("[SPEECH RECOG] Sphinx couldn't understand audio")
            return {
                'text': None,
                'confidence': 0.0,
                'metadata': {'error': 'Could not understand audio', 'engine': 'sphinx'}
            }
        except Exception as e:
            print(f"[SPEECH RECOG] Sphinx error: {e}")
            return {
                'text': None,
                'confidence': 0.0,
                'metadata': {'error': f'Sphinx error: {e}', 'engine': 'sphinx'}
            }
    
    def _recognize_with_vosk(self, audio_data: bytes) -> Dict:
        """Recognize speech using Vosk engine."""
        try:
            if not hasattr(self, 'vosk_recognizer'):
                raise Exception("Vosk not properly initialized")
            
            # Vosk expects 16kHz mono audio
            if self.vosk_recognizer.AcceptWaveform(audio_data):
                result = self.vosk_recognizer.Result()
            else:
                result = self.vosk_recognizer.PartialResult()
            
            # Parse result
            import json
            parsed_result = json.loads(result)
            
            text = parsed_result.get('text', '')
            confidence = parsed_result.get('confidence', 0.8)
            
            return {
                'text': text,
                'confidence': confidence,
                'metadata': {
                    'engine': 'vosk',
                    'raw_result': parsed_result
                }
            }
            
        except Exception as e:
            return {
                'text': None,
                'confidence': 0.0,
                'metadata': {'error': f'Vosk recognition error: {e}', 'engine': 'vosk'}
            }
    
    def _preprocess_audio(self, audio_data: bytes, sample_rate: int) -> bytes:
        """Preprocess audio data for better recognition."""
        try:
            # Convert to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            # Normalize audio
            if np.max(np.abs(audio_array)) > 0:
                audio_array = audio_array / np.max(np.abs(audio_array)) * 32767
            
            # Apply noise reduction (simple high-pass filter)
            if len(audio_array) > 1:
                # First-order high-pass filter
                alpha = 0.95
                filtered = np.zeros_like(audio_array)
                filtered[0] = audio_array[0]
                
                for i in range(1, len(audio_array)):
                    filtered[i] = alpha * (filtered[i-1] + audio_array[i] - audio_array[i-1])
                
                audio_array = filtered.astype(np.int16)
            
            # Convert back to bytes
            return audio_array.tobytes()
            
        except Exception as e:
            print(f"Audio preprocessing error: {e}")
            return audio_data
    
    def _notify_callbacks(self, event: str, data: Dict) -> None:
        """Notify all callbacks of an event."""
        for callback in self.callbacks:
            try:
                callback(event, data)
            except Exception as e:
                print(f"Error in recognition callback: {e}")
    
    def clear_cache(self) -> None:
        """Clear the recognition cache."""
        self.cache.clear()
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        return {
            'cache_size': len(self.cache),
            'cache_hit_rate': getattr(self, '_cache_hits', 0) / max(getattr(self, '_total_requests', 1), 1)
        }
    
    def set_energy_threshold(self, threshold: int) -> None:
        """Set energy threshold for speech detection."""
        self.recognizer.energy_threshold = threshold
        self.config.energy_threshold = threshold
    
    def calibrate_microphone(self, duration: float = 1.0) -> None:
        """Calibrate microphone for ambient noise."""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=duration)


class ContinuousRecognizer:
    """
    Continuous speech recognition for real-time processing.
    """
    
    def __init__(self, processor: SpeechToTextProcessor):
        self.processor = processor
        self.is_listening = False
        self.listen_thread = None
        self.callbacks = []
    
    def start_listening(self) -> bool:
        """Start continuous listening."""
        if self.is_listening:
            return False
        
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        return True
    
    def stop_listening(self) -> None:
        """Stop continuous listening."""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=1.0)
    
    def _listen_loop(self) -> None:
        """Main listening loop."""
        while self.is_listening:
            try:
                text, confidence, metadata = self.processor.recognize_from_microphone(timeout=1.0)
                
                if text and confidence > 0.5:  # Only process high-confidence results
                    self._notify_callbacks('speech_recognized', {
                        'text': text,
                        'confidence': confidence,
                        'metadata': metadata
                    })
                
            except Exception as e:
                print(f"Error in continuous recognition: {e}")
                time.sleep(0.1)
    
    def add_callback(self, callback: Callable[[str, Dict], None]) -> None:
        """Add callback for recognition events."""
        self.callbacks.append(callback)
    
    def _notify_callbacks(self, event: str, data: Dict) -> None:
        """Notify all callbacks of an event."""
        for callback in self.callbacks:
            try:
                callback(event, data)
            except Exception as e:
                print(f"Error in continuous recognition callback: {e}")


if __name__ == "__main__":
    # Demo the speech-to-text processor
    config = RecognitionConfig(
        engine=RecognitionEngine.GOOGLE,
        language="en-US",
        timeout=5.0
    )
    
    processor = SpeechToTextProcessor(config)
    
    def recognition_callback(event, data):
        print(f"Recognition event: {event}")
        if 'text' in data:
            print(f"Recognized: {data['text']}")
            print(f"Confidence: {data['confidence']:.2f}")
    
    processor.add_callback(recognition_callback)
    
    print("Speech recognition demo")
    print("Speak something into your microphone...")
    
    # Test microphone recognition
    text, confidence, metadata = processor.recognize_from_microphone()
    
    if text:
        print(f"Recognized: {text}")
        print(f"Confidence: {confidence:.2f}")
        print(f"Metadata: {metadata}")
    else:
        print("No speech recognized or error occurred")
        print(f"Error: {metadata.get('error', 'Unknown error')}")
    
    # Show cache stats
    print(f"Cache stats: {processor.get_cache_stats()}")
