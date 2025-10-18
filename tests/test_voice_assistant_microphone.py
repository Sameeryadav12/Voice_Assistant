"""
Test the exact same microphone settings as the voice assistant.
"""

import pyaudio
import numpy as np
import time

def test_voice_assistant_microphone():
    """Test microphone with exact voice assistant settings."""
    print("=== TESTING VOICE ASSISTANT MICROPHONE SETTINGS ===")
    
    p = pyaudio.PyAudio()
    
    try:
        # Use EXACT same settings as voice assistant
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        INPUT_DEVICE_INDEX = 0  # Microsoft Sound Mapper - Input
        
        print(f"Settings:")
        print(f"  - Device: {INPUT_DEVICE_INDEX} (Microsoft Sound Mapper - Input)")
        print(f"  - Sample rate: {RATE}")
        print(f"  - Channels: {CHANNELS}")
        print(f"  - Chunk size: {CHUNK}")
        print(f"  - Format: {FORMAT}")
        
        print(f"\nRecording for 3 seconds... SPEAK LOUDLY NOW!")
        
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=INPUT_DEVICE_INDEX,
            frames_per_buffer=CHUNK
        )
        
        frames = []
        max_levels = []
        
        for i in range(int(RATE / CHUNK * 3)):
            data = stream.read(CHUNK)
            frames.append(data)
            
            # Check audio level (same as voice assistant)
            audio_array = np.frombuffer(data, dtype=np.int16)
            max_level = np.max(np.abs(audio_array))
            max_levels.append(max_level)
            
            # Show progress
            if i % 10 == 0:
                print(f"  Chunk {i}: Max level = {max_level}")
        
        stream.stop_stream()
        stream.close()
        
        # Analyze results
        overall_max = max(max_levels)
        average_max = np.mean(max_levels)
        
        print(f"\n=== RESULTS ===")
        print(f"Maximum audio level: {overall_max}")
        print(f"Average audio level: {average_max:.1f}")
        
        if overall_max > 500:
            print("[SUCCESS] Audio levels are good for voice recognition!")
        elif overall_max > 100:
            print("[WARNING] Audio levels are moderate - might work")
        else:
            print("[ERROR] Audio levels are too low - this is the problem!")
        
        # Test speech recognition with this audio
        if overall_max > 50:
            print(f"\nTesting speech recognition with this audio...")
            
            # Combine all audio
            combined_audio = b''.join(frames)
            
            # Try speech recognition
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = 50
            
            audio = sr.AudioData(combined_audio, RATE, 2)
            try:
                text = recognizer.recognize_google(audio, show_all=False)
                print(f"[SUCCESS] Recognized: '{text}'")
                
                # Test wake word detection
                if "sigma" in text.lower() or "hey sigma" in text.lower():
                    print("[SUCCESS] Wake word would be detected!")
                else:
                    print("[INFO] No wake word detected (but speech recognition works)")
                    
            except sr.UnknownValueError:
                print("[WARNING] Could not understand audio")
            except sr.RequestError as e:
                print(f"[ERROR] Recognition service error: {e}")
        else:
            print("Skipping speech recognition test - audio too quiet")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        p.terminate()

if __name__ == "__main__":
    test_voice_assistant_microphone()

