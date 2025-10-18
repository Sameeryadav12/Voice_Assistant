"""
Audio input handler with Voice Activity Detection (VAD) and noise reduction.
Demonstrates real-time audio processing and signal processing algorithms.
"""

import pyaudio
import numpy as np
import threading
import time
import queue
from typing import Callable, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import webrtcvad
import collections


class AudioQuality(Enum):
    """Audio quality levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class AudioConfig:
    """Audio configuration parameters."""
    sample_rate: int = 16000
    chunk_size: int = 1024
    channels: int = 1
    format: int = pyaudio.paInt16
    quality: AudioQuality = AudioQuality.MEDIUM
    vad_aggressiveness: int = 3  # 0-3, 3 is MOST aggressive (least sensitive to noise)
    silence_threshold: float = 0.003  # Even lower threshold for more sensitivity
    min_silence_duration: float = 0.5  # Half second of silence before processing
    max_recording_duration: float = 30.0


class VoiceActivityDetector:
    """
    Voice Activity Detection using WebRTC VAD and custom algorithms.
    Demonstrates signal processing and machine learning concepts.
    """
    
    def __init__(self, config: AudioConfig):
        self.config = config
        self.vad = webrtcvad.Vad(config.vad_aggressiveness)
        self.audio_buffer = collections.deque(maxlen=100)
        self.silence_frames = 0
        self.speech_frames = 0
        self.is_speaking = False
        self.energy_threshold = 3000  # Much higher - only detect loud clear speech
        self.zero_crossing_threshold = 0.1
        
    def process_frame(self, audio_frame: bytes) -> bool:
        """
        Process audio frame and determine if speech is present.
        Returns True if speech is detected.
        """
        # Convert bytes to numpy array
        audio_data = np.frombuffer(audio_frame, dtype=np.int16)
        
        # First check MAXIMUM level (must be loud enough to be speech)
        max_level = np.max(np.abs(audio_data))
        
        # Require minimum volume level to avoid background noise
        # Level 1-500 is just noise, not speech
        if max_level < 500:
            return False  # Too quiet to be speech
        
        # Now check energy level
        energy = np.mean(np.abs(audio_data))
        if energy > self.energy_threshold:
            # High energy detected, likely speech
            return True
        
        # Check if frame is valid for VAD (must be 10ms, 20ms, or 30ms)
        frame_duration_ms = len(audio_data) * 1000 / self.config.sample_rate
        
        if frame_duration_ms in [10, 20, 30]:
            try:
                # Use WebRTC VAD
                vad_result = self.vad.is_speech(audio_frame, self.config.sample_rate)
            except:
                # Fallback to energy-based detection
                vad_result = self._energy_based_detection(audio_data)
        else:
            # Use custom detection for other frame sizes
            vad_result = self._custom_vad(audio_data)
        
        # Update state
        if vad_result:
            self.speech_frames += 1
            self.silence_frames = 0
        else:
            self.silence_frames += 1
            self.speech_frames = 0
        
        # Determine if currently speaking
        self.is_speaking = self.speech_frames > 3
        
        return vad_result
    
    def _energy_based_detection(self, audio_data: np.ndarray) -> bool:
        """Energy-based voice activity detection."""
        # Calculate mean absolute energy (simpler and more direct)
        energy = np.mean(np.abs(audio_data))
        return energy > self.energy_threshold
    
    def _custom_vad(self, audio_data: np.ndarray) -> bool:
        """Custom voice activity detection algorithm."""
        # Calculate multiple features
        energy = np.mean(np.abs(audio_data))
        zero_crossings = self._calculate_zero_crossings(audio_data)
        spectral_centroid = self._calculate_spectral_centroid(audio_data)
        
        # Combine features for decision (more lenient for sensitivity)
        energy_score = 1 if energy > self.energy_threshold else 0
        zc_score = 1 if zero_crossings > self.zero_crossing_threshold else 0
        spectral_score = 1 if spectral_centroid > 500 else 0  # Lower threshold for more sensitivity
        
        # Any one positive score is enough (OR logic for maximum sensitivity)
        return sum([energy_score, zc_score, spectral_score]) >= 1
    
    def _calculate_zero_crossings(self, audio_data: np.ndarray) -> float:
        """Calculate zero crossing rate."""
        if len(audio_data) < 2:
            return 0.0
        
        # Count sign changes
        sign_changes = np.sum(np.diff(np.sign(audio_data)) != 0)
        return sign_changes / len(audio_data)
    
    def _calculate_spectral_centroid(self, audio_data: np.ndarray) -> float:
        """Calculate spectral centroid (brightness of sound)."""
        # Simple FFT-based spectral centroid
        fft = np.fft.fft(audio_data)
        magnitude = np.abs(fft[:len(fft)//2])
        
        if np.sum(magnitude) == 0:
            return 0.0
        
        freqs = np.fft.fftfreq(len(audio_data), 1/self.config.sample_rate)[:len(magnitude)]
        spectral_centroid = np.sum(freqs * magnitude) / np.sum(magnitude)
        return abs(spectral_centroid)


class AudioInputHandler:
    """
    Main audio input handler with real-time processing capabilities.
    Features:
    - Real-time audio capture
    - Voice activity detection
    - Noise reduction
    - Audio buffering
    - Callback system
    """
    
    def __init__(self, config: AudioConfig = None):
        self.config = config or AudioConfig()
        self.audio = pyaudio.PyAudio()
        self.vad = VoiceActivityDetector(self.config)
        self.is_recording = False
        self.recording_thread = None
        self.audio_queue = queue.Queue(maxsize=100)
        self.callbacks = []
        self.audio_buffer = []
        self.silence_start_time = None
        self.actual_sample_rate = self.config.sample_rate  # Will be updated when recording starts
        
    def add_callback(self, callback: Callable[[bytes], None]) -> None:
        """Add callback function for audio data."""
        self.callbacks.append(callback)
    
    def start_recording(self) -> bool:
        """Start audio recording."""
        if self.is_recording:
            return False
        
        try:
            # Find the default input device
            default_device = self.audio.get_default_input_device_info()
            print(f"[START RECORDING] Using default input device: {default_device['name']}")
            print(f"[START RECORDING] Device index: {default_device['index']}")
            print(f"[START RECORDING] Max input channels: {default_device['maxInputChannels']}")
            print(f"[START RECORDING] Default sample rate: {default_device['defaultSampleRate']}")
            
            # Use device's native sample rate if different from config
            native_sample_rate = int(default_device['defaultSampleRate'])
            if native_sample_rate != self.config.sample_rate:
                print(f"[START RECORDING] Adjusting sample rate from {self.config.sample_rate} to {native_sample_rate}")
                self.actual_sample_rate = native_sample_rate
            else:
                self.actual_sample_rate = self.config.sample_rate
            
            # Use the default input device
            self.stream = self.audio.open(
                format=self.config.format,
                channels=self.config.channels,
                rate=self.actual_sample_rate,
                input=True,
                input_device_index=default_device['index'],
                frames_per_buffer=self.config.chunk_size,
                stream_callback=self._audio_callback
            )
            
            print("[START RECORDING] Audio stream opened successfully")
            
            self.is_recording = True
            self.recording_thread = threading.Thread(target=self._recording_loop, daemon=True)
            self.recording_thread.start()
            
            print("[START RECORDING] Recording thread started")
            return True
        except Exception as e:
            import traceback
            print(f"[START RECORDING] ERROR: {e}")
            print(f"[START RECORDING] Traceback: {traceback.format_exc()}")
            return False
    
    def stop_recording(self) -> None:
        """Stop audio recording."""
        self.is_recording = False
        
        # Wait a bit for the recording thread to stop
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=1.0)
        
        # Close stream safely
        if hasattr(self, 'stream') and self.stream is not None:
            try:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
            except Exception as e:
                print(f"Error closing stream: {e}")
        
        # Clear audio buffer
        self.audio_buffer.clear()
        self.silence_start_time = None
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """PyAudio callback for real-time audio processing."""
        if self.is_recording:
            # Check audio level in callback
            audio_array = np.frombuffer(in_data, dtype=np.int16)
            max_val = np.max(np.abs(audio_array))
            if max_val > 10:  # Only log when we get some sound
                print(f"[AUDIO CALLBACK] Received audio: {len(in_data)} bytes, max level: {max_val}")
            self.audio_queue.put(in_data)
        return (in_data, pyaudio.paContinue)
    
    def _recording_loop(self) -> None:
        """Main recording loop with VAD processing."""
        chunk_count = 0
        print("[RECORDING LOOP] Starting recording loop")
        
        while self.is_recording:
            try:
                # Get audio data from queue
                audio_data = self.audio_queue.get(timeout=0.1)
                chunk_count += 1
                
                # Check audio level in queue
                audio_array = np.frombuffer(audio_data, dtype=np.int16)
                max_val = np.max(np.abs(audio_array))
                
                # Ignore very quiet audio (background noise)
                if max_val < 500:
                    # This is just background noise, skip it
                    continue
                
                # Only log when we have significant audio
                if max_val > 500:
                    print(f"[RECORDING LOOP] Chunk {chunk_count}: {len(audio_data)} bytes, max level: {max_val}")
                
                # Process with VAD
                is_speech = self.vad.process_frame(audio_data)
                print(f"[RECORDING LOOP] VAD - Speech detected: {is_speech}, level: {max_val}")
                
                if is_speech:
                    self.audio_buffer.append(audio_data)
                    self.silence_start_time = None
                    
                    # Force process if buffer gets too large (50 chunks = ~2.3 seconds)
                    if len(self.audio_buffer) >= 50:
                        print(f"[RECORDING LOOP] Buffer full at {len(self.audio_buffer)} chunks, processing...")
                        self._process_audio_buffer()
                    elif len(self.audio_buffer) % 10 == 0:  # Log every 10 chunks
                        print(f"[RECORDING LOOP] Speech buffered - total chunks: {len(self.audio_buffer)}")
                else:
                    # Handle silence
                    if self.silence_start_time is None and self.audio_buffer:
                        self.silence_start_time = time.time()
                        print(f"[RECORDING LOOP] Silence started with {len(self.audio_buffer)} chunks buffered")
                    
                    # If we have buffered audio and silence is long enough
                    # BUT only if we collected at least 20 chunks (about 0.9 seconds of speech)
                    if (self.audio_buffer and 
                        len(self.audio_buffer) >= 20 and
                        self.silence_start_time is not None and
                        time.time() - self.silence_start_time > self.config.min_silence_duration):
                        # Process buffered audio
                        print(f"[RECORDING LOOP] Silence duration exceeded, processing {len(self.audio_buffer)} chunks")
                        self._process_audio_buffer()
                    elif self.audio_buffer and len(self.audio_buffer) < 20 and self.silence_start_time is not None:
                        # If silence but not enough audio collected, clear buffer
                        if time.time() - self.silence_start_time > 1.0:
                            print(f"[RECORDING LOOP] Clearing insufficient audio ({len(self.audio_buffer)} chunks)")
                            self.audio_buffer.clear()
                            self.silence_start_time = None
                
                # Check for maximum recording duration
                if (self.audio_buffer and 
                    self.silence_start_time is not None and
                    time.time() - self.silence_start_time > self.config.max_recording_duration):
                    print(f"[RECORDING LOOP] Max recording duration exceeded, processing")
                    self._process_audio_buffer()
                
            except queue.Empty:
                # No audio in queue, continue listening
                continue
            except Exception as e:
                import traceback
                print(f"[RECORDING LOOP] ERROR: {e}")
                print(f"[RECORDING LOOP] Traceback: {traceback.format_exc()}")
                break
        
        print("[RECORDING LOOP] Recording loop ended")
    
    def _process_audio_buffer(self) -> None:
        """Process accumulated audio buffer."""
        if not self.audio_buffer:
            print("[PROCESS BUFFER] No audio buffer - returning")
            return
        
        print(f"[PROCESS BUFFER] Processing {len(self.audio_buffer)} audio chunks at {self.actual_sample_rate}Hz")
        
        # Combine audio chunks
        combined_audio = b''.join(self.audio_buffer)
        print(f"[PROCESS BUFFER] Combined audio: {len(combined_audio)} bytes")
        
        # Resample if necessary to 16000Hz for speech recognition
        if self.actual_sample_rate != 16000:
            combined_audio = self._resample_audio(combined_audio, self.actual_sample_rate, 16000)
            print(f"[PROCESS BUFFER] Resampled to 16000Hz: {len(combined_audio)} bytes")
        
        # Apply basic audio enhancement for better speech recognition
        processed_audio = self._enhance_audio_for_recognition(combined_audio)
        print(f"[PROCESS BUFFER] Enhanced audio: {len(processed_audio)} bytes")
        
        # Only notify callbacks if we have valid audio (not rejected as noise)
        if len(processed_audio) > 0:
            for callback in self.callbacks:
                try:
                    callback(processed_audio)
                except Exception as e:
                    print(f"Error in audio callback: {e}")
        else:
            print(f"[PROCESS BUFFER] Audio rejected as noise, skipping recognition")
        
        # Clear buffer
        self.audio_buffer.clear()
        self.silence_start_time = None
    
    def _resample_audio(self, audio_data: bytes, from_rate: int, to_rate: int) -> bytes:
        """Resample audio from one sample rate to another."""
        try:
            import scipy.signal as signal
            
            # Convert to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            # Calculate resampling ratio
            ratio = to_rate / from_rate
            new_length = int(len(audio_array) * ratio)
            
            # Resample using scipy
            resampled = signal.resample(audio_array, new_length)
            
            # Convert back to int16
            resampled = np.clip(resampled, -32768, 32767).astype(np.int16)
            
            return resampled.tobytes()
        except Exception as e:
            print(f"[RESAMPLE] ERROR: {e}, returning original audio")
            return audio_data
    
    def _enhance_audio_for_recognition(self, audio_data: bytes) -> bytes:
        """Enhance audio data for better speech recognition."""
        try:
            # Convert to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            # Check if audio is too quiet
            max_val = np.max(np.abs(audio_array))
            print(f"[ENHANCE AUDIO] Original audio max level: {max_val}")
            
            # Only reject if truly silent (max_val <= 0)
            # Accept all non-zero audio to accommodate low-gain microphones
            if max_val <= 0:
                print(f"[ENHANCE AUDIO] Audio is silent (max: {max_val}), rejecting")
                return b''  # Return empty bytes to skip recognition
            
            print(f"[ENHANCE AUDIO] Audio accepted (max: {max_val})")
            
            # Normalize and boost audio aggressively for low-level microphones
            if max_val > 0:
                # For very quiet mics (level < 1000), boost to near maximum
                # For normal mics (level > 1000), scale to 50%
                if max_val < 1000:
                    target_max = 28000  # 85% of max range - very aggressive boost
                    print(f"[ENHANCE AUDIO] Low-level mic detected, aggressive boost")
                else:
                    target_max = 16383  # 50% of max range
                
                audio_array = (audio_array / max_val * target_max).astype(np.int16)
                print(f"[ENHANCE AUDIO] Normalized audio from {max_val} to target {target_max}")
            
            enhanced_bytes = audio_array.tobytes()
            print(f"[ENHANCE AUDIO] Enhanced audio: {len(enhanced_bytes)} bytes")
            return enhanced_bytes
            
        except Exception as e:
            import traceback
            print(f"[ENHANCE AUDIO] ERROR: {e}")
            print(f"[ENHANCE AUDIO] Traceback: {traceback.format_exc()}")
            return audio_data
    
    def _apply_noise_reduction(self, audio_data: bytes) -> bytes:
        """Apply basic noise reduction to audio data."""
        # Convert to numpy array
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        
        # Simple high-pass filter to remove low-frequency noise
        if len(audio_array) > 1:
            # First-order high-pass filter
            alpha = 0.95
            filtered = np.zeros_like(audio_array)
            filtered[0] = audio_array[0]
            
            for i in range(1, len(audio_array)):
                filtered[i] = alpha * (filtered[i-1] + audio_array[i] - audio_array[i-1])
            
            # Normalize
            if np.max(np.abs(filtered)) > 0:
                filtered = filtered / np.max(np.abs(filtered)) * 32767
            
            audio_array = filtered.astype(np.int16)
        
        return audio_array.tobytes()
    
    def get_audio_level(self) -> float:
        """Get current audio level (0.0 to 1.0)."""
        if not self.audio_buffer:
            return 0.0
        
        # Calculate RMS level of last chunk
        last_chunk = self.audio_buffer[-1]
        audio_array = np.frombuffer(last_chunk, dtype=np.int16)
        rms = np.sqrt(np.mean(audio_array.astype(np.float32) ** 2))
        
        # Normalize to 0-1 range
        return min(rms / 32767.0, 1.0)
    
    def is_voice_detected(self) -> bool:
        """Check if voice is currently detected."""
        return self.vad.is_speaking
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        self.stop_recording()
        if hasattr(self, 'audio'):
            self.audio.terminate()


if __name__ == "__main__":
    # Demo the audio input handler
    config = AudioConfig(
        sample_rate=16000,
        chunk_size=1024,
        quality=AudioQuality.HIGH
    )
    
    handler = AudioInputHandler(config)
    
    def audio_callback(audio_data):
        print(f"Received audio data: {len(audio_data)} bytes")
    
    handler.add_callback(audio_callback)
    
    print("Starting audio recording... Press Ctrl+C to stop")
    try:
        if handler.start_recording():
            while True:
                time.sleep(0.1)
                level = handler.get_audio_level()
                voice = handler.is_voice_detected()
                print(f"Audio level: {level:.3f}, Voice detected: {voice}")
        else:
            print("Failed to start recording")
    except KeyboardInterrupt:
        print("\nStopping recording...")
    finally:
        handler.cleanup()


