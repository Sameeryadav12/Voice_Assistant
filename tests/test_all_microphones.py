"""
Test all available microphone devices to find one that works.
"""

import pyaudio
import numpy as np
import time

def test_all_microphones():
    """Test all microphone devices to find the best one."""
    print("=== TESTING ALL MICROPHONE DEVICES ===")
    
    p = pyaudio.PyAudio()
    
    try:
        # List all devices
        print("Available input devices:")
        input_devices = []
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                input_devices.append((i, info))
                print(f"  Device {i}: {info['name']}")
                print(f"    - Host API: {info['hostApi']}")
                print(f"    - Sample rate: {info['defaultSampleRate']}")
        
        print(f"\nFound {len(input_devices)} input devices")
        
        # Test each device
        best_device = None
        best_level = 0
        
        for device_id, info in input_devices:
            try:
                print(f"\n--- Testing Device {device_id}: {info['name'][:50]}... ---")
                
                # Test recording
                CHUNK = 1024
                FORMAT = pyaudio.paInt16
                CHANNELS = 1
                RATE = 16000
                
                print("Speak loudly for 2 seconds...")
                
                stream = p.open(
                    format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=device_id,
                    frames_per_buffer=CHUNK
                )
                
                frames = []
                max_levels = []
                
                for i in range(int(RATE / CHUNK * 2)):
                    data = stream.read(CHUNK)
                    frames.append(data)
                    
                    # Check audio level
                    audio_array = np.frombuffer(data, dtype=np.int16)
                    max_level = np.max(np.abs(audio_array))
                    max_levels.append(max_level)
                
                stream.stop_stream()
                stream.close()
                
                # Analyze results
                overall_max = max(max_levels)
                average_max = np.mean(max_levels)
                
                print(f"Max level: {overall_max}, Average: {average_max:.1f}")
                
                if overall_max > best_level:
                    best_level = overall_max
                    best_device = (device_id, info, overall_max)
                
                if overall_max > 100:
                    print("GOOD AUDIO LEVEL!")
                elif overall_max > 10:
                    print("Moderate audio level")
                else:
                    print("Low audio level")
                    
            except Exception as e:
                print(f"Error testing device {device_id}: {e}")
        
        # Results
        print(f"\n=== RESULTS ===")
        if best_device:
            device_id, info, level = best_device
            print(f"Best device: {device_id} - {info['name']}")
            print(f"Best audio level: {level}")
            
            if level > 100:
                print("RECOMMENDATION: Use this device for the voice assistant!")
                print(f"Device ID: {device_id}")
            else:
                print("WARNING: Even the best device has low audio levels.")
                print("This might be a hardware issue or the microphone is very quiet.")
        else:
            print("No working microphone devices found.")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        p.terminate()

if __name__ == "__main__":
    test_all_microphones()

