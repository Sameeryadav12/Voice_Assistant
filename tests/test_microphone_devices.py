"""
Test different microphone devices and settings.
"""

import pyaudio
import numpy as np
import time

def test_microphone_devices():
    """Test different microphone devices."""
    print("=== MICROPHONE DEVICE TEST ===")
    
    p = pyaudio.PyAudio()
    
    try:
        # List all devices
        print("Available audio devices:")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"  Device {i}: {info['name']}")
                print(f"    - Input channels: {info['maxInputChannels']}")
                print(f"    - Default sample rate: {info['defaultSampleRate']}")
                print(f"    - Host API: {info['hostApi']}")
        
        # Test different devices
        test_devices = [0, 1, 2, 6, 7, 8]  # Common input devices
        
        for device_id in test_devices:
            try:
                info = p.get_device_info_by_index(device_id)
                if info['maxInputChannels'] > 0:
                    print(f"\n--- Testing Device {device_id}: {info['name']} ---")
                    
                    # Test recording
                    CHUNK = 1024
                    FORMAT = pyaudio.paInt16
                    CHANNELS = 1
                    RATE = 16000
                    
                    stream = p.open(
                        format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=device_id,
                        frames_per_buffer=CHUNK
                    )
                    
                    print("Recording 2 seconds... Speak now!")
                    frames = []
                    for i in range(int(RATE / CHUNK * 2)):
                        data = stream.read(CHUNK)
                        frames.append(data)
                    
                    stream.stop_stream()
                    stream.close()
                    
                    # Analyze audio
                    audio_data = b''.join(frames)
                    audio_array = np.frombuffer(audio_data, dtype=np.int16)
                    max_val = np.max(np.abs(audio_array))
                    avg_val = np.mean(np.abs(audio_array))
                    
                    print(f"Audio levels - Max: {max_val}, Average: {avg_val:.1f}")
                    
                    if max_val > 200:
                        print("GOOD AUDIO LEVELS!")
                        # Try speech recognition
                        import speech_recognition as sr
                        recognizer = sr.Recognizer()
                        recognizer.energy_threshold = 50
                        
                        audio = sr.AudioData(audio_data, RATE, 2)
                        try:
                            text = recognizer.recognize_google(audio)
                            print(f"RECOGNIZED: '{text}'")
                        except:
                            print("Could not recognize speech")
                    else:
                        print("Audio too quiet")
                        
            except Exception as e:
                print(f"Error testing device {device_id}: {e}")
                
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        p.terminate()

if __name__ == "__main__":
    test_microphone_devices()

