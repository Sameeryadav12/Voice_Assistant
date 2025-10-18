"""
Check microphone volume and provide solutions.
"""

import pyaudio
import numpy as np
import time

def check_microphone_volume():
    """Check microphone volume levels and provide solutions."""
    print("=== MICROPHONE VOLUME CHECKER ===")
    
    p = pyaudio.PyAudio()
    
    try:
        # Find the default input device
        default_device = p.get_default_input_device_info()
        print(f"Default microphone: {default_device['name']}")
        print(f"Max input channels: {default_device['maxInputChannels']}")
        print(f"Default sample rate: {default_device['defaultSampleRate']}")
        
        # Test recording
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        
        print("\nTesting microphone volume...")
        print("Speak loudly into your microphone for 3 seconds...")
        
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        frames = []
        max_levels = []
        
        for i in range(int(RATE / CHUNK * 3)):
            data = stream.read(CHUNK)
            frames.append(data)
            
            # Check audio level
            audio_array = np.frombuffer(data, dtype=np.int16)
            max_level = np.max(np.abs(audio_array))
            max_levels.append(max_level)
            
            # Show progress
            if i % 10 == 0:
                print(f"Recording... Level: {max_level}")
        
        stream.stop_stream()
        stream.close()
        
        # Analyze results
        overall_max = max(max_levels)
        average_max = np.mean(max_levels)
        
        print(f"\n=== RESULTS ===")
        print(f"Maximum audio level: {overall_max}")
        print(f"Average audio level: {average_max:.1f}")
        
        if overall_max < 50:
            print("\n[ERROR] MICROPHONE VOLUME IS TOO LOW!")
            print("\nSOLUTIONS:")
            print("1. Check Windows microphone settings:")
            print("   - Right-click speaker icon in taskbar")
            print("   - Select 'Open Sound settings'")
            print("   - Click 'Sound Control Panel'")
            print("   - Go to 'Recording' tab")
            print("   - Double-click your microphone")
            print("   - Go to 'Levels' tab")
            print("   - Increase microphone volume to 80-100%")
            print("   - Make sure microphone is not muted")
            
            print("\n2. Check microphone permissions:")
            print("   - Go to Windows Settings > Privacy > Microphone")
            print("   - Make sure 'Allow apps to access your microphone' is ON")
            print("   - Make sure 'Allow desktop apps to access your microphone' is ON")
            
            print("\n3. Test with a different microphone:")
            print("   - Try using a headset microphone")
            print("   - Try using a USB microphone")
            
        elif overall_max < 200:
            print("\n[WARNING] MICROPHONE VOLUME IS LOW")
            print("Consider increasing microphone volume in Windows settings.")
            
        else:
            print("\n[SUCCESS] MICROPHONE VOLUME IS GOOD!")
            print("The microphone should work fine with the voice assistant.")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        p.terminate()

if __name__ == "__main__":
    check_microphone_volume()
