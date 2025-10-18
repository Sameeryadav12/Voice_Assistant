#!/usr/bin/env python3
"""
Sigma Voice Assistant - Keyboard Mode Example
A simple example showing how to use the voice assistant in keyboard-only mode.
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main_hybrid import SigmaVoiceAssistant

def main():
    """Run the keyboard mode example"""
    print("=" * 60)
    print("Sigma Voice Assistant - Keyboard Mode Example")
    print("=" * 60)
    print("This example demonstrates keyboard-only mode.")
    print("Type commands instead of speaking them.")
    print("Type 'quit' or 'exit' to stop.")
    print("=" * 60)
    
    # Create assistant instance
    assistant = SigmaVoiceAssistant()
    
    try:
        # Run the assistant
        assistant.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please check the troubleshooting guide for help.")

if __name__ == "__main__":
    main()