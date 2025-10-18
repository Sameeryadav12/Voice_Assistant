"""
Windows Microphone Configuration Helper
This script will help you configure your microphone correctly.
"""

import subprocess
import os
import sys
import time

def open_sound_settings():
    """Open Windows Sound Settings directly to the microphone page."""
    print("="*70)
    print("WINDOWS MICROPHONE CONFIGURATION HELPER")
    print("="*70)
    print()
    print("I will now open your Windows Sound Settings.")
    print("Please follow these EXACT steps:")
    print()
    print("="*70)
    print("STEP-BY-STEP INSTRUCTIONS")
    print("="*70)
    print()
    
    print("STEP 1: When the Settings window opens")
    print("   - You'll see 'Sound' settings")
    print("   - Scroll down to find 'Input' section")
    print()
    
    print("STEP 2: Under 'Input', you'll see your microphone")
    print("   - Current: 'Microphone Array (Realtek(R) Au'")
    print("   - OR: 'External Microphone (Realtek(R))'")
    print()
    
    print("STEP 3: Move the volume slider")
    print("   - Drag it ALL THE WAY to the RIGHT (100%)")
    print("   - Speak and watch the blue bar move")
    print()
    
    print("STEP 4: Click 'Device properties'")
    print("   - This is RIGHT UNDER the volume slider")
    print("   - A new page opens")
    print()
    
    print("STEP 5: On Device properties page")
    print("   - Find the 'Volume' slider - set to 100")
    print("   - Click 'Additional device properties' link at bottom")
    print()
    
    print("STEP 6: In the NEW window that pops up")
    print("   - Click the 'Levels' tab at the top")
    print("   - You'll see TWO sliders:")
    print("       * Microphone: Set to 100")
    print("       * Microphone Boost: Set to +20 or +30")  
    print("   - Click OK")
    print()
    
    print("STEP 7: Close all windows and test")
    print()
    print("="*70)
    
    print()
    input("Press Enter to open Sound Settings...")
    print()
    
    # Open Windows Sound Settings
    try:
        print("Opening Windows Sound Settings...")
        subprocess.Popen(['start', 'ms-settings:sound'], shell=True)
        print("Sound Settings opened!")
        print()
        print("Follow the steps above to configure your microphone.")
        print()
        
        print("="*70)
        print("AFTER YOU FINISH THE STEPS ABOVE")
        print("="*70)
        print()
        print("Run this command to test if it worked:")
        print()
        print("    python test_microphone_volume.py")
        print()
        print("You should see levels between 10,000 and 20,000 when speaking loudly.")
        print()
        print("If you still see level 1:")
        print("  1. Check if the correct microphone is selected (not 'Stereo Mix')")
        print("  2. Try unplugging and replugging your microphone")
        print("  3. Restart your computer")
        print("  4. Check if microphone is muted in the system tray")
        print()
        
    except Exception as e:
        print(f"Could not open settings automatically: {e}")
        print()
        print("Please open Sound Settings manually:")
        print("  1. Press Windows Key + I")
        print("  2. Click 'System'")
        print("  3. Click 'Sound'")
        print("  4. Follow the steps above")

if __name__ == "__main__":
    open_sound_settings()


