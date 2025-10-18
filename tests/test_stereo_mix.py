"""
Test Stereo Mix device for audio capture.
"""

import pyaudio
import numpy as np
import time

def test_stereo_mix():
    """Test Stereo Mix device."""
    print("=== STEREO MIX TEST ===")
    
    p = pyaudio.PyAudio()
    
    try:
        # Find Stereo Mix device
        stereo_mix_device = None
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if "stereo mix" in info['name'].lower() and info['maxInputChannels'] > 0:
                stereo_mix_device = i
                print(f"Found Stereo Mix: Device {i} - {info['name']}")
                break
        
        if stereo_mix_device is None:
            print("No Stereo Mix device found")
            return
        
        # Test Stereo Mix
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        
        print("Testing Stereo Mix... Play some audio on your computer...")
        
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=stereo_mix_device,
            frames_per_buffer=CHUNK
        )
        
        frames = []
        for i in range(int(RATE / CHUNK * 3)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        
        # Analyze audio
        audio_data = b''.join(frames)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        max_val = np.max(np.abs(audio_array))
        avg_val = np.mean(np.abs(audio_array))
        
        print(f"Stereo Mix audio levels - Max: {max_val}, Average: {avg_val:.1f}")
        
        if max_val > 100:
            print("Stereo Mix is working!")
            return stereo_mix_device
        else:
            print("Stereo Mix too quiet")
            
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        p.terminate()
    
    return None

if __name__ == "__main__":
    test_stereo_mix()

