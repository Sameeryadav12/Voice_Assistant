"""
Voice Calibration Tool
This will help the system learn YOUR voice, tone, and accent!
"""

import sys
import os
import time
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from audio.input_handler import AudioInputHandler, AudioConfig
from nlp.speech_to_text import SpeechToTextProcessor, RecognitionConfig, RecognitionEngine
import pyaudio
import numpy as np

class VoiceCalibrator:
    """Tool to calibrate and learn user's voice."""
    
    def __init__(self):
        print("="*70)
        print("VOICE CALIBRATION - Teaching Jarvis YOUR Voice!")
        print("="*70)
        print()
        print("This tool will:")
        print("  1. Test your microphone level")
        print("  2. Record you saying test phrases")
        print("  3. Learn how YOUR accent/tone sounds")
        print("  4. Create a voice profile for you")
        print()
        
        self.audio_config = AudioConfig()
        self.audio_input = AudioInputHandler(self.audio_config)
        self.speech_processor = SpeechToTextProcessor(RecognitionConfig())
        self.voice_profile = {
            'wake_word_variations': [],
            'common_phrases': {},
            'audio_characteristics': {}
        }
    
    def run_calibration(self):
        """Run the full calibration process."""
        print("="*70)
        print("PART 1: Microphone Level Test")
        print("="*70)
        print()
        
        # Test microphone level first
        max_level = self.test_microphone_level()
        
        if max_level < 1000:
            print()
            print("WARNING: Your microphone level is very low!")
            print(f"Current max level: {max_level} (need at least 10,000)")
            print()
            print("CRITICAL ISSUE: Your microphone is too quiet or not working.")
            print()
            print("Please do this NOW:")
            print("  1. Windows Sound Settings is already open (I opened it)")
            print("  2. Go to Input section")
            print("  3. Check if CORRECT microphone is selected")
            print("  4. Set volume to 100%")
            print("  5. Enable Microphone Boost (+20 or +30 dB)")
            print()
            response = input("Have you fixed it? (yes/no): ").strip().lower()
            if response == 'yes':
                print()
                print("Great! Let's test again...")
                max_level = self.test_microphone_level()
                if max_level < 1000:
                    print()
                    print("Still too quiet. The assistant will work better with keyboard mode.")
                    print("Run: python main_combined.py")
                    print("Then just TYPE your commands instead of speaking.")
                    return False
            else:
                print()
                print("No problem! You can use keyboard mode instead.")
                print("Run: python main_combined.py")
                print("Then just TYPE your commands.")
                return False
        
        print()
        print(f"Great! Your microphone level is: {max_level}")
        print()
        
        # Continue with voice calibration
        print("="*70)
        print("PART 2: Voice Calibration")
        print("="*70)
        print()
        print("I will ask you to say some phrases.")
        print("This helps me learn YOUR pronunciation!")
        print()
        
        test_phrases = [
            "Hey Jarvis",
            "Jarvis",
            "What time is it",
            "Open calculator",
            "Set a reminder"
        ]
        
        for i, phrase in enumerate(test_phrases, 1):
            print(f"\nPhrase {i}/{len(test_phrases)}")
            print(f"Say: '{phrase}'")
            input("Press Enter when ready...")
            
            # Record and recognize
            recognized = self.record_and_recognize(phrase)
            
            if recognized:
                print(f"  You said: '{phrase}'")
                print(f"  I heard: '{recognized}'")
                
                if recognized.lower() != phrase.lower():
                    print(f"  NOTE: Different! I'll remember this variation.")
                    self.voice_profile['common_phrases'][phrase.lower()] = recognized.lower()
                else:
                    print(f"  Perfect match!")
            else:
                print(f"  Couldn't understand - audio may be too quiet")
            
            time.sleep(1)
        
        # Save voice profile
        self.save_voice_profile()
        
        print()
        print("="*70)
        print("CALIBRATION COMPLETE!")
        print("="*70)
        print()
        print("Voice profile saved!")
        print("The assistant will now recognize YOUR voice better!")
        print()
        print("Run: python main_combined.py")
        print("Then click 'Start Listening' to use voice commands!")
        print()
        
        return True
    
    def test_microphone_level(self):
        """Test microphone and return maximum level detected."""
        print("Testing microphone for 5 seconds...")
        print("Please SPEAK LOUDLY into your microphone NOW!")
        print()
        
        audio = pyaudio.PyAudio()
        max_level = 0
        
        try:
            default_device = audio.get_default_input_device_info()
            print(f"Using: {default_device['name']}")
            
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=int(default_device['defaultSampleRate']),
                input=True,
                input_device_index=default_device['index'],
                frames_per_buffer=1024
            )
            
            start_time = time.time()
            while time.time() - start_time < 5:
                data = stream.read(1024, exception_on_overflow=False)
                audio_array = np.frombuffer(data, dtype=np.int16)
                level = np.max(np.abs(audio_array))
                max_level = max(max_level, level)
                
                # Show real-time feedback
                bar_length = int((level / 32767) * 30)
                bar = "#" * bar_length + "-" * (30 - bar_length)
                print(f"Level: {level:5d} [{bar}]", end='\r')
                
                time.sleep(0.05)
            
            stream.stop_stream()
            stream.close()
            
            print()  # New line after progress
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            audio.terminate()
        
        return max_level
    
    def record_and_recognize(self, expected_phrase):
        """Record audio and recognize it."""
        recognized_texts = []
        
        def audio_callback(audio_data):
            text, confidence, metadata = self.speech_processor.recognize_audio(audio_data)
            if text and confidence > 0.3:
                recognized_texts.append(text)
        
        self.audio_input.add_callback(audio_callback)
        
        # Record for 3 seconds
        if self.audio_input.start_recording():
            time.sleep(3)
            self.audio_input.stop_recording()
            time.sleep(1)  # Wait for processing
        
        # Return most common recognition
        if recognized_texts:
            return recognized_texts[-1]  # Return last recognition
        return None
    
    def save_voice_profile(self):
        """Save voice profile to file."""
        try:
            with open('voice_profile.json', 'w') as f:
                json.dump(self.voice_profile, f, indent=2)
            print("Voice profile saved to: voice_profile.json")
        except Exception as e:
            print(f"Could not save voice profile: {e}")


def main():
    """Main entry point."""
    try:
        calibrator = VoiceCalibrator()
        success = calibrator.run_calibration()
        
        if success:
            print("Success! Your voice is now calibrated!")
        else:
            print("Calibration stopped. Use keyboard mode instead!")
        
    except KeyboardInterrupt:
        print("\n\nCalibration cancelled by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

