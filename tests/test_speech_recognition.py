"""
Simple test for speech recognition to debug the None issue.
"""

import sys
import os
import time

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nlp.speech_to_text import SpeechToTextProcessor, RecognitionConfig, RecognitionEngine

def test_speech_recognition():
    """Test speech recognition with different configurations."""
    print("=== TESTING SPEECH RECOGNITION ===")
    
    try:
        # Test 1: Google engine with default settings
        print("\n--- Test 1: Google Engine ---")
        config = RecognitionConfig()
        config.engine = RecognitionEngine.GOOGLE
        processor = SpeechToTextProcessor(config)
        
        # Create a simple test audio (1 second of silence)
        import numpy as np
        sample_rate = 16000
        duration = 1.0
        silence = np.zeros(int(sample_rate * duration), dtype=np.int16)
        test_audio = silence.tobytes()
        
        print(f"Created test audio: {len(test_audio)} bytes")
        text, confidence, metadata = processor.recognize_audio(test_audio)
        
        print(f"Result: text='{text}', confidence={confidence}")
        print(f"Metadata: {metadata}")
        
        # Test 2: Try with actual speech-like audio
        print("\n--- Test 2: Speech-like Audio ---")
        # Create a simple tone (440 Hz for 0.5 seconds)
        t = np.linspace(0, 0.5, int(sample_rate * 0.5), False)
        tone = np.sin(2 * np.pi * 440 * t) * 0.1  # Low volume
        tone = (tone * 32767).astype(np.int16)
        speech_audio = tone.tobytes()
        
        print(f"Created speech-like audio: {len(speech_audio)} bytes")
        text2, confidence2, metadata2 = processor.recognize_audio(speech_audio)
        
        print(f"Result: text='{text2}', confidence={confidence2}")
        print(f"Metadata: {metadata2}")
        
        # Test 3: Try with microphone recording
        print("\n--- Test 3: Microphone Test ---")
        print("Speak 'Hello' into your microphone...")
        
        import pyaudio
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        
        print("Recording for 3 seconds...")
        frames = []
        for i in range(int(RATE / CHUNK * 3)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        mic_audio = b''.join(frames)
        print(f"Recorded audio: {len(mic_audio)} bytes")
        
        # Check if we got any sound
        audio_array = np.frombuffer(mic_audio, dtype=np.int16)
        max_val = np.max(np.abs(audio_array))
        print(f"Max audio value: {max_val}")
        
        if max_val > 100:
            text3, confidence3, metadata3 = processor.recognize_audio(mic_audio)
            print(f"Result: text='{text3}', confidence={confidence3}")
            print(f"Metadata: {metadata3}")
        else:
            print("No sound detected in microphone recording")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_speech_recognition()

