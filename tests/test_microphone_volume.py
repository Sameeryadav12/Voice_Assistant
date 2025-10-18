"""
Microphone Volume Test Tool
This will help you adjust your microphone to the right volume level.
"""

import pyaudio
import numpy as np
import time

def test_microphone():
    """Test microphone and show volume levels in real-time."""
    
    print("=" * 60)
    print("MICROPHONE VOLUME TEST")
    print("=" * 60)
    print()
    print("This tool will help you adjust your microphone volume.")
    print()
    print("GOAL: Get audio levels above 10,000 when speaking")
    print("      (Ideal range: 10,000 - 20,000)")
    print()
    print("If levels are too low:")
    print("  1. Right-click speaker icon in taskbar")
    print("  2. Click 'Open Sound settings'")
    print("  3. Scroll to 'Input' section")
    print("  4. Click on your microphone")
    print("  5. Increase volume to 100%")
    print("  6. Click 'Device properties' -> 'Additional device properties'")
    print("  7. Go to 'Levels' tab")
    print("  8. Set microphone to 100% AND microphone boost to +20dB or +30dB")
    print()
    print("Starting test in 3 seconds...")
    time.sleep(3)
    print()
    
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    
    try:
        # Get default input device
        default_device = audio.get_default_input_device_info()
        print(f"Using microphone: {default_device['name']}")
        print(f"Sample rate: {int(default_device['defaultSampleRate'])} Hz")
        print()
        print("SPEAK NOW! Say 'Hey Sigma, what time is it?' loudly and clearly")
        print("Press Ctrl+C to stop")
        print()
        print("-" * 60)
        
        # Open stream
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=int(default_device['defaultSampleRate']),
            input=True,
            input_device_index=default_device['index'],
            frames_per_buffer=1024
        )
        
        max_level_seen = 0
        good_count = 0
        test_duration = 30  # Test for 30 seconds
        start_time = time.time()
        
        while time.time() - start_time < test_duration:
            # Read audio
            data = stream.read(1024, exception_on_overflow=False)
            audio_array = np.frombuffer(data, dtype=np.int16)
            
            # Calculate level
            max_val = np.max(np.abs(audio_array))
            max_level_seen = max(max_level_seen, max_val)
            
            # Determine status
            if max_val > 15000:
                status = "EXCELLENT!"
                bar_length = 50
                good_count += 1
            elif max_val > 10000:
                status = "GOOD!"
                bar_length = 40
                good_count += 1
            elif max_val > 5000:
                status = "TOO QUIET"
                bar_length = 25
            elif max_val > 2000:
                status = "WAY TOO QUIET"
                bar_length = 15
            else:
                status = "ALMOST SILENT"
                bar_length = 5
            
            # Calculate bar
            bar_chars = int((max_val / 32767) * bar_length)
            bar = "#" * bar_chars + "-" * (bar_length - bar_chars)
            
            # Print level
            elapsed = int(time.time() - start_time)
            remaining = test_duration - elapsed
            print(f"[{remaining:2d}s] Level: {max_val:5d} {bar} {status}", end='\r')
            
            time.sleep(0.05)
        
        stream.stop_stream()
        stream.close()
        
        print()
        print()
        print("=" * 60)
        print("TEST RESULTS")
        print("=" * 60)
        print(f"Maximum level recorded: {max_level_seen}")
        print(f"Good readings: {good_count} / {test_duration * 20}")
        print()
        
        if max_level_seen > 15000:
            print("SUCCESS - PERFECT! Your microphone is configured correctly!")
            print("  You can now use the voice assistant.")
            print()
            print("  Run: python main.py")
        elif max_level_seen > 10000:
            print("SUCCESS - GOOD! Your microphone should work.")
            print("  For best results, try to increase volume a bit more.")
            print()
            print("  Run: python main.py")
        elif max_level_seen > 5000:
            print("FAILED - TOO QUIET! Increase microphone volume.")
            print("  Enable microphone boost in Windows sound settings.")
        elif max_level_seen > 2000:
            print("FAILED - WAY TOO QUIET! Your microphone volume is very low.")
            print("  You MUST increase it to at least 100% + enable boost.")
        else:
            print("FAILED - ALMOST SILENT! The microphone is barely picking up anything.")
            print("  Check:")
            print("    - Is the correct microphone selected?")
            print("    - Is it muted?")
            print("    - Is it plugged in properly?")
        
        print()
        
    except KeyboardInterrupt:
        print("\n\nTest stopped by user")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        audio.terminate()

if __name__ == "__main__":
    test_microphone()

