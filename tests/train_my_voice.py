"""
Voice Training Tool - Teach Jarvis YOUR Voice!
This creates a custom mapping of what YOU say vs what Google hears.
"""

import sys
import os
import time
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from audio.input_handler import AudioInputHandler, AudioConfig
from nlp.speech_to_text import SpeechToTextProcessor, RecognitionConfig, RecognitionEngine

class VoiceTrainer:
    """Train the system to understand YOUR specific voice/accent."""
    
    def __init__(self):
        self.audio_input = AudioInputHandler(AudioConfig())
        self.speech_processor = SpeechToTextProcessor(RecognitionConfig())
        self.voice_mappings = {}
        self.training_complete = False
        
    def train(self):
        """Run voice training."""
        print("="*70)
        print("VOICE TRAINING - Teaching Jarvis YOUR Voice!")
        print("="*70)
        print()
        print("I will show you a phrase, you say it, and I'll learn how")
        print("Google recognizes YOUR pronunciation!")
        print()
        print("This creates a custom profile just for you!")
        print()
        
        # Training phrases
        training_phrases = [
            ("Hey Jarvis", "The wake word"),
            ("what time is it", "Time query"),
            ("open calculator", "Open app"),
            ("set a reminder", "Reminder command"),
            ("search for files", "File search")
        ]
        
        print("="*70)
        print(f"TRAINING: {len(training_phrases)} phrases")
        print("="*70)
        print()
        
        for i, (phrase, description) in enumerate(training_phrases, 1):
            print(f"\n{'='*70}")
            print(f"PHRASE {i}/{len(training_phrases)}: {description}")
            print(f"{'='*70}")
            print()
            print(f"SAY THIS EXACTLY: '{phrase}'")
            print()
            print("When you're ready:")
            print("  1. Take a breath")
            print("  2. Say it clearly")
            print("  3. Wait 3 seconds")
            print()
            
            input("Press Enter when you're ready to speak...")
            print()
            print("RECORDING NOW - SAY IT!")
            print()
            
            # Record what they say
            recognized = self.record_phrase()
            
            if recognized:
                print(f"  YOU SAID:     '{phrase}'")
                print(f"  GOOGLE HEARD: '{recognized}'")
                print()
                
                if recognized.lower().strip() == phrase.lower().strip():
                    print("  PERFECT MATCH! No training needed for this phrase.")
                else:
                    print("  DIFFERENT! I'll remember this variation.")
                    # Map what Google hears → what user actually said
                    self.voice_mappings[recognized.lower().strip()] = phrase.lower().strip()
                    print(f"  Saved: '{recognized}' means '{phrase}'")
            else:
                print(f"  NO SPEECH DETECTED")
                print()
                print("  This could mean:")
                print("    - Microphone level still too low")
                print("    - Not speaking loud enough")
                print("    - Background noise too high")
                print()
                retry = input("  Try again? (yes/no): ").strip().lower()
                if retry == 'yes':
                    print()
                    print("  RECORDING AGAIN - SAY IT LOUDER!")
                    recognized = self.record_phrase()
                    if recognized:
                        print(f"  GOOGLE HEARD: '{recognized}'")
                        self.voice_mappings[recognized.lower().strip()] = phrase.lower().strip()
            
            time.sleep(0.5)
        
        # Save the mappings
        self.save_voice_profile()
        
        print()
        print("="*70)
        print("TRAINING COMPLETE!")
        print("="*70)
        print()
        print(f"Created {len(self.voice_mappings)} voice mappings for you!")
        print()
        
        if self.voice_mappings:
            print("YOUR CUSTOM VOICE PROFILE:")
            for google_hears, user_said in self.voice_mappings.items():
                print(f"  When Google hears: '{google_hears}'")
                print(f"  System knows you said: '{user_said}'")
                print()
        
        print("Voice profile saved to: voice_mappings.json")
        print()
        print("Now the assistant will understand YOUR voice better!")
        print()
        print("Run: python main_combined.py")
        print("Then use voice - it will correct Google's misunderstandings!")
        print()
        
        return len(self.voice_mappings) > 0
    
    def record_phrase(self):
        """Record a phrase and return what was recognized."""
        recognized_text = None
        
        def audio_callback(audio_data):
            nonlocal recognized_text
            text, confidence, metadata = self.speech_processor.recognize_audio(audio_data)
            if text and confidence > 0.1:
                recognized_text = text
                print(f"  [Recognized: '{text}' with {confidence:.0%} confidence]")
        
        # Clear previous callbacks and add new one
        self.audio_input.callbacks.clear()
        self.audio_input.add_callback(audio_callback)
        
        # Record for 3 seconds
        if self.audio_input.start_recording():
            print("  Listening... (speak now!)")
            time.sleep(4)  # Record for 4 seconds
            self.audio_input.stop_recording()
            time.sleep(1)  # Wait for processing
        
        return recognized_text
    
    def save_voice_profile(self):
        """Save voice profile."""
        profile = {
            'created': datetime.now().isoformat(),
            'mappings': self.voice_mappings,
            'accent_aware': True
        }
        
        try:
            with open('voice_mappings.json', 'w') as f:
                json.dump(profile, f, indent=2)
            print(f"Voice profile saved!")
        except Exception as e:
            print(f"Could not save profile: {e}")


def main():
    """Main entry point."""
    print()
    print("This tool will teach Jarvis to understand YOUR voice!")
    print()
    
    try:
        trainer = VoiceTrainer()
        success = trainer.train()
        
        if success:
            print("="*70)
            print("SUCCESS! Jarvis has learned your voice!")
            print("="*70)
        else:
            print("="*70)
            print("Training had some issues, but you can still use keyboard mode!")
            print("="*70)
    
    except KeyboardInterrupt:
        print("\n\nTraining cancelled")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

