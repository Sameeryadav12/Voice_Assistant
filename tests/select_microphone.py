"""
Microphone Selector - Find and select the CORRECT microphone
"""

import speech_recognition as sr
import pyaudio
import numpy as np
import time

def list_all_microphones():
    """List all available microphones."""
    print("="*70)
    print("MICROPHONE SELECTOR")
    print("="*70)
    print()
    print("Finding all microphones on your system...")
    print()
    
    # Method 1: Using speech_recognition
    print("Available microphones:")
    print("-"*70)
    
    mic_list = sr.Microphone.list_microphone_names()
    for index, name in enumerate(mic_list):
        print(f"{index}: {name}")
    
    print()
    print("="*70)
    print("TESTING EACH MICROPHONE")
    print("="*70)
    print()
    print("I will test each microphone for 3 seconds.")
    print("SPEAK LOUDLY when testing!")
    print()
    
    audio = pyaudio.PyAudio()
    best_mic = None
    best_level = 0
    
    for index in range(len(mic_list)):
        print(f"\nTesting Microphone {index}: {mic_list[index][:50]}...")
        print("SPEAK NOW!")
        
        try:
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                input_device_index=index,
                frames_per_buffer=1024
            )
            
            max_level = 0
            for i in range(60):  # 3 seconds
                try:
                    data = stream.read(1024, exception_on_overflow=False)
                    audio_array = np.frombuffer(data, dtype=np.int16)
                    level = np.max(np.abs(audio_array))
                    max_level = max(max_level, level)
                except:
                    pass
                time.sleep(0.05)
            
            stream.stop_stream()
            stream.close()
            
            print(f"  Maximum level: {max_level}")
            
            if max_level > best_level:
                best_level = max_level
                best_mic = index
            
            if max_level > 10000:
                print(f"  SUCCESS - EXCELLENT! This microphone works great!")
            elif max_level > 5000:
                print(f"  SUCCESS - GOOD! This microphone should work.")
            elif max_level > 1000:
                print(f"  OK - Might work but volume is low")
            else:
                print(f"  FAILED - TOO QUIET - Not recommended")
        
        except Exception as e:
            print(f"  ERROR: {e}")
    
    audio.terminate()
    
    print()
    print("="*70)
    print("RESULTS")
    print("="*70)
    print()
    
    if best_mic is not None:
        print(f"BEST MICROPHONE FOUND:")
        print(f"  Index: {best_mic}")
        print(f"  Name: {mic_list[best_mic]}")
        print(f"  Maximum Level: {best_level}")
        print()
        
        if best_level > 10000:
            print("SUCCESS - This microphone is PERFECT for voice recognition!")
            print()
            print("I will save this to your configuration...")
            
            # Save to config file
            with open('mic_config.txt', 'w') as f:
                f.write(f"{best_mic}\n")
            
            print("Saved! The assistant will now use this microphone.")
            print()
            print("Run: python main_combined.py")
            print("Then click 'Start Listening' to use voice!")
            
        elif best_level > 5000:
            print("SUCCESS - This microphone should work!")
            print()
            print("Saving to configuration...")
            
            with open('mic_config.txt', 'w') as f:
                f.write(f"{best_mic}\n")
            
            print("Saved! Try using it - it might work.")
            
        else:
            print("FAILED - All microphones are too quiet.")
            print()
            print("SOLUTION: Use keyboard mode instead")
            print("Run: python main_combined.py")
            print("Then TYPE your commands (don't use voice)")
    
    else:
        print("FAILED - No working microphones found.")
        print()
        print("Use keyboard mode: python main_combined.py")


if __name__ == "__main__":
    try:
        list_all_microphones()
    except KeyboardInterrupt:
        print("\n\nStopped by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

