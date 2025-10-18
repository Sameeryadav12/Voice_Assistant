#!/usr/bin/env python3
"""
Sigma Voice Assistant - Demo Script
A demonstration script showing the capabilities of the voice assistant.
"""

import sys
import os
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def demo_commands():
    """Demonstrate available commands"""
    print("=" * 60)
    print("Sigma Voice Assistant - Demo Commands")
    print("=" * 60)
    print("Here are some example commands you can try:")
    print()
    
    commands = [
        ("Time & Date", [
            "Hey Sigma, what time is it?",
            "Hey Sigma, what's the date?",
            "Hey Sigma, show system information"
        ]),
        ("Reminders", [
            "Hey Sigma, set a reminder for 5 minutes",
            "Hey Sigma, remind me to call John in 10 minutes",
            "Hey Sigma, what reminders do I have?"
        ]),
        ("Applications", [
            "Hey Sigma, open calculator",
            "Hey Sigma, launch notepad",
            "Hey Sigma, open chrome",
            "Hey Sigma, start command prompt"
        ]),
        ("File Operations", [
            "Hey Sigma, search for documents",
            "Hey Sigma, find files with test in the name",
            "Hey Sigma, search for reports"
        ]),
        ("Help", [
            "Hey Sigma, what can you do?",
            "Hey Sigma, help"
        ])
    ]
    
    for category, cmd_list in commands:
        print(f"📋 {category}:")
        for cmd in cmd_list:
            print(f"   • {cmd}")
        print()
    
    print("=" * 60)
    print("To try these commands:")
    print("1. Run: python main_professional_ui.py")
    print("2. Hold the green button and speak a command")
    print("3. Or type commands in the text field")
    print("=" * 60)

def demo_features():
    """Demonstrate key features"""
    print("\n🎯 Key Features:")
    print("• Push-to-Talk Mode - Hold button to speak")
    print("• Auto-Scrolling Conversation - Automatic scrolling")
    print("• Chat Bubbles - WhatsApp-style interface")
    print("• Quick Actions - One-click common commands")
    print("• Real-time Status - Animated status indicators")
    print("• Modern UI - Professional dark theme")
    print("• 8 Functional Skills - Time, reminders, files, apps, etc.")
    print("• Advanced NLP - Natural language processing")
    print("• Performance Optimized - Fast and efficient")

def main():
    """Run the demo"""
    demo_commands()
    demo_features()
    
    print("\n🚀 Ready to start?")
    print("Run: python main_professional_ui.py")
    print("\nFor more information, see:")
    print("• README.md - Project overview")
    print("• docs/USER_GUIDE.md - Complete user guide")
    print("• docs/TROUBLESHOOTING.md - Problem solving")

if __name__ == "__main__":
    main()