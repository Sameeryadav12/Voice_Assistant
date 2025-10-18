"""
Direct test of speech recognition with better audio handling.
"""

import sys
import os
import time
import pyaudio
import numpy as np
import speech_recognition as sr

def test_direct_recognition():
    """Test speech recognition directly with microphone."""
    print("=== DIRECT SPEECH RECOGNITION TEST ===")
    
    # Setup audio recording
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    # Setup speech recognition
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 50  # Very low threshold
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.5
    recognizer.phrase_threshold = 0.3
    recognizer.non_speaking_duration = 0.3
    
    print("Audio settings:")
    print(f"  Energy threshold: {recognizer.energy_threshold}")
    print(f"  Pause threshold: {recognizer.pause_threshold}")
    
    # Record audio
    p = pyaudio.PyAudio()
    
    try:
        print("\nSpeak clearly: 'Hello Sigma' (3 seconds)...")
        
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        frames = []
        for i in range(int(RATE / CHUNK * 3)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        
        # Combine audio
        audio_data = b''.join(frames)
        print(f"Recorded {len(audio_data)} bytes")
        
        # Check audio levels
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        max_val = np.max(np.abs(audio_array))
        avg_val = np.mean(np.abs(audio_array))
        print(f"Audio levels - Max: {max_val}, Average: {avg_val:.1f}")
        
        if max_val < 50:
            print("Audio too quiet, trying to amplify...")
            # Amplify audio
            if max_val > 0:
                amplification = 100 / max_val
                audio_array = (audio_array * amplification).astype(np.int16)
                # Clip to prevent overflow
                audio_array = np.clip(audio_array, -32767, 32767)
                audio_data = audio_array.tobytes()
                print(f"Amplified audio - new max: {np.max(np.abs(audio_array))}")
        
        # Try recognition
        print("\nTrying speech recognition...")
        audio = sr.AudioData(audio_data, RATE, 2)
        
        try:
            text = recognizer.recognize_google(audio, show_all=False)
            print(f"SUCCESS! Recognized: '{text}'")
            
            # Test wake word detection
            if "sigma" in text.lower() or "hey sigma" in text.lower():
                print("Wake word detected!")
            else:
                print("No wake word found")
                
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Recognition service error: {e}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        p.terminate()

if __name__ == "__main__":
    test_direct_recognition()

