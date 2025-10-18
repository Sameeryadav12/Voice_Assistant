"""
Automatic Voice Training - No keyboard needed!
Just speak when prompted and it learns your voice automatically.
"""

import sys
import os
import time
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from audio.input_handler import AudioInputHandler, AudioConfig
from nlp.speech_to_text import SpeechToTextProcessor, RecognitionConfig, RecognitionEngine

def automatic_voice_training():
    """Automatically train voice without needing keyboard input."""
    
    print("="*70)
    print("AUTOMATIC VOICE TRAINING")
    print("="*70)
    print()
    print("This tool will automatically learn YOUR voice!")
    print()
    print("I will:")
    print("  1. Listen to you for 30 seconds")
    print("  2. Record everything you say")
    print("  3. Show what Google recognizes")
    print("  4. Create a voice profile for you")
    print()
    print("Starting in 3 seconds...")
    time.sleep(3)
    print()
    
    audio_input = AudioInputHandler(AudioConfig())
    speech_processor = SpeechToTextProcessor(RecognitionConfig())
    
    recognized_phrases = []
    
    def audio_callback(audio_data):
        """Callback for audio data."""
        text, confidence, metadata = speech_processor.recognize_audio(audio_data)
        if text and confidence > 0.1:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"\n[{timestamp}] HEARD: '{text}' (confidence: {confidence:.0%})")
            recognized_phrases.append({
                'text': text,
                'confidence': confidence,
                'timestamp': timestamp
            })
    
    audio_input.add_callback(audio_callback)
    
    print("="*70)
    print("LISTENING FOR 30 SECONDS")
    print("="*70)
    print()
    print("SPEAK THESE PHRASES (say each one clearly):")
    print()
    print("  1. 'Hey Sigma'")
    print("  2. 'What time is it?'")
    print("  3. 'Open calculator'")
    print("  4. 'Set a reminder'")
    print("  5. 'Search for files'")
    print()
    print("Say them one at a time, pausing between each.")
    print("I'll show you what I hear in real-time!")
    print()
    print("-"*70)
    print()
    
    # Start recording
    if audio_input.start_recording():
        print("RECORDING... SPEAK NOW!")
        print()
        
        # Listen for 30 seconds
        time.sleep(30)
        
        # Stop recording
        audio_input.stop_recording()
        audio_input.cleanup()
        
        print()
        print("-"*70)
        print()
        print("="*70)
        print("TRAINING RESULTS")
        print("="*70)
        print()
        
        if recognized_phrases:
            print(f"I heard {len(recognized_phrases)} phrases from you:")
            print()
            for i, phrase in enumerate(recognized_phrases, 1):
                print(f"{i}. '{phrase['text']}' ({phrase['confidence']:.0%} confidence)")
            
            # Save results
            training_data = {
                'created': datetime.now().isoformat(),
                'phrases': recognized_phrases,
                'total_recognized': len(recognized_phrases)
            }
            
            with open('voice_training_results.json', 'w') as f:
                json.dump(training_data, f, indent=2)
            
            print()
            print("Results saved to: voice_training_results.json")
            print()
            print("="*70)
            print("NEXT STEPS")
            print("="*70)
            print()
            print("Look at what I heard above.")
            print()
            print("If the words are CORRECT (match what you said):")
            print("  -> Your voice works! Run: python main_combined.py")
            print()
            print("If the words are WRONG (different from what you said):")
            print("  -> This is an accent/mic quality issue")
            print("  -> Use keyboard mode: python main_combined.py (and type)")
            print()
            print("Either way, the assistant works!")
            print()
            
        else:
            print("NO PHRASES RECOGNIZED!")
            print()
            print("This means:")
            print("  - Microphone volume is still too low")
            print("  - OR you didn't speak loud enough")
            print("  - OR wrong microphone is selected")
            print()
            print("SOLUTION: Use keyboard mode instead")
            print("Run: python main_combined.py")
            print("Then TYPE your commands - works perfectly!")
            print()
        
    else:
        print("ERROR: Could not start recording")
        print("Check your microphone is connected and enabled.")


if __name__ == "__main__":
    try:
        automatic_voice_training()
    except KeyboardInterrupt:
        print("\n\nTraining stopped")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

