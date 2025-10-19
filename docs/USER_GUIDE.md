# 📖 Jarvis Voice Assistant - User Guide

## Welcome to Jarvis Voice Assistant!

This comprehensive guide will help you get the most out of your voice assistant. Whether you're a beginner or an advanced user, you'll find everything you need here.

---

## 🚀 Getting Started

### First Time Setup

1. **Install the application** (see [Installation Guide](INSTALLATION.md))
2. **Run the professional UI:**
   ```bash
   python main_professional_ui.py
   ```
3. **Test your microphone** (optional):
   ```bash
   python tests/test_microphone_volume.py
   ```

### Understanding the Interface

The professional UI has two main panels:

#### Left Panel - Conversation
- **Chat bubbles** show your conversation with Jarvis
- **Auto-scrolling** - automatically shows new messages
- **Clear button** - start fresh conversation

#### Right Panel - Controls
- **🎤 HOLD TO SPEAK** - Green button for voice commands
- **Text input** - Type commands directly
- **Quick Actions** - One-click common commands
- **Settings** - Adjust voice and volume

---

## 🎤 Voice Commands

### How to Use Voice Mode

1. **Hold** the green "🎤 HOLD TO SPEAK" button
2. **Speak clearly** your command
3. **Release** the button when done
4. **Wait** for Jarvis to process and respond

### Wake Words

Always start your commands with one of these:
- "Hey Jarvis"
- "Jarvis"
- "Assistant"

**Examples:**
- ✅ "Hey Jarvis, what time is it?"
- ✅ "Jarvis, open calculator"
- ❌ "What time is it?" (missing wake word)

---

## ⌨️ Text Commands

### How to Use Text Mode

1. **Click** in the text input field
2. **Type** your command
3. **Press Enter** or click "📤 Send"
4. **Get instant response**

**Example:**
```
Type: Hey Jarvis, what time is it?
Press: Enter
Result: Current time displayed
```

---

## ⚡ Quick Actions

Click any quick action button for instant commands:

| Button | Command | Description |
|--------|---------|-------------|
| ⏰ **What time is it?** | `Hey Jarvis, what time is it?` | Get current time |
| 💻 **System info** | `Hey Jarvis, show system information` | View system details |
| ⏲️ **Set reminder** | `Hey Jarvis, set a reminder for 5 minutes` | Create reminder |
| 🔢 **Open calculator** | `Hey Jarvis, open calculator` | Launch calculator |

---

## 🎯 Available Commands

### Time & Information

| Command | Example | Response |
|---------|---------|----------|
| Get current time | "Hey Jarvis, what time is it?" | "The current time is 2:30 PM" |
| Get current date | "Hey Jarvis, what's the date?" | "Today is October 18, 2025" |
| System information | "Hey Jarvis, show system information" | CPU, memory, disk details |

### Reminders

| Command | Example | Response |
|---------|---------|----------|
| Set reminder | "Hey Jarvis, set a reminder for 5 minutes" | "Reminder set for 2:35 PM" |
| Set reminder with message | "Hey Jarvis, remind me to call John in 10 minutes" | "Reminder set: Call John at 2:40 PM" |
| List reminders | "Hey Jarvis, what reminders do I have?" | Shows upcoming reminders |

### Applications

| Command | Example | Response |
|---------|---------|----------|
| Open calculator | "Hey Jarvis, open calculator" | "Opened calculator" |
| Launch notepad | "Hey Jarvis, launch notepad" | "Opened notepad" |
| Open browser | "Hey Jarvis, open chrome" | "Opened Chrome browser" |
| Start command prompt | "Hey Jarvis, start cmd" | "Opened command prompt" |

### File Operations

| Command | Example | Response |
|---------|---------|----------|
| Search files | "Hey Jarvis, search for documents" | Lists matching files |
| Find specific files | "Hey Jarvis, find files with test in the name" | Shows test files |
| Search by content | "Hey Jarvis, search for reports" | Finds files containing "reports" |

### Help & Information

| Command | Example | Response |
|---------|---------|----------|
| Show capabilities | "Hey Jarvis, what can you do?" | Lists all available commands |
| Get help | "Hey Jarvis, help" | Shows help information |

---

## 🎨 Interface Guide

### Status Indicator

The pulsing dot in the top-right shows Jarvis's current state:

| Color | State | Description |
|-------|-------|-------------|
| ⚪ Gray | Idle | Ready to receive commands |
| 🟢 Green | Listening | Recording your voice |
| 🟡 Yellow | Processing | Understanding your command |
| 🔵 Blue | Speaking | Generating response |
| 🔴 Red | Error | Something went wrong |

### Chat Bubbles

- **Purple bubbles** (right side) - Your messages
- **Gray bubbles** (left side) - Jarvis's responses
- **Auto-scrolling** - Always shows latest messages
- **Timestamps** - Each message is timestamped

### Quick Actions

- **One-click commands** - No need to type or speak
- **Hover effects** - Visual feedback when hovering
- **Instant execution** - Commands run immediately

---

## ⚙️ Settings

### Accessing Settings

1. Click **"⚙️ Settings"** at the bottom of the control panel
2. Adjust the sliders as needed
3. Click **"Apply Settings"** to save

### Available Settings

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| Speech Rate | 50-400 WPM | 200 | How fast Jarvis speaks |
| Volume | 0-100% | 80% | Audio output volume |

---

## 🔧 Troubleshooting

### Voice Recognition Issues

**Problem:** Jarvis doesn't understand me
- **Solution:** Speak more clearly and slowly
- **Try:** "Hey Jarvis" + pause + your command
- **Check:** Microphone is working and not muted

**Problem:** Wrong words recognized
- **Solution:** This is normal with accents - try rephrasing
- **Alternative:** Use text mode for important commands

**Problem:** "Network error" message
- **Solution:** Check your internet connection
- **Alternative:** Use keyboard mode (works offline)

### Interface Issues

**Problem:** Buttons not responding
- **Solution:** Restart the application
- **Check:** Make sure you're clicking the right button

**Problem:** Conversation not scrolling
- **Solution:** This should auto-scroll - if not, restart the app

**Problem:** Text input too small
- **Solution:** The text input is designed to be compact but usable

### Performance Issues

**Problem:** Slow response
- **Solution:** Close other applications
- **Check:** Available memory and CPU usage

**Problem:** Application crashes
- **Solution:** Restart the application
- **Check:** All dependencies are installed correctly

---

## 💡 Tips & Tricks

### Voice Commands

1. **Speak clearly** - Enunciate each word
2. **Use wake words** - Always start with "Hey Jarvis"
3. **Pause briefly** - Wait a moment after "Hey Jarvis"
4. **Hold button firmly** - Don't release too early
5. **Speak at normal volume** - Not too loud or quiet

### Text Commands

1. **Use complete sentences** - "Hey Jarvis, what time is it?"
2. **Be specific** - "Hey Jarvis, open calculator" not just "calculator"
3. **Check spelling** - Make sure words are spelled correctly
4. **Use Enter key** - Faster than clicking Send button

### Quick Actions

1. **Use frequently** - They're faster than typing
2. **Customize** - Add your own quick actions (advanced)
3. **Hover to preview** - See what each button does

---

## 🎯 Best Practices

### For Voice Commands

- **Practice with simple commands** first
- **Use consistent phrasing** - "Hey Jarvis" + command
- **Speak in quiet environment** for better recognition
- **Hold the button** until you finish speaking

### For Text Commands

- **Use the same format** as voice commands
- **Include wake words** even in text
- **Be specific** about what you want
- **Use proper grammar** for better understanding

### General Usage

- **Start simple** - Try basic commands first
- **Explore features** - Try different types of commands
- **Use quick actions** - They're designed for common tasks
- **Check status** - Watch the status indicator for feedback

---

## 📚 Advanced Usage

### Custom Commands

While you can't create custom commands yet, you can:
- **Use natural language** - Jarvis understands various phrasings
- **Combine commands** - "Hey Jarvis, what time is it and open calculator"
- **Ask for help** - "Hey Jarvis, what can you do?"

### Keyboard Shortcuts

- **Enter** - Send text command
- **Escape** - Cancel current operation (if applicable)
- **Tab** - Navigate between elements

### Multiple Modes

You can switch between modes anytime:
- **Voice mode** - Hold green button to speak
- **Text mode** - Type in the text field
- **Quick actions** - Click buttons for instant commands

---

## 🆘 Getting Help

### Built-in Help

- **"Hey Jarvis, help"** - Shows available commands
- **"Hey Jarvis, what can you do?"** - Lists capabilities
- **Settings panel** - Adjust voice and volume

### Documentation

- **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Common problems and solutions
- **[API Reference](API_REFERENCE.md)** - Technical documentation
- **[Performance Guide](PERFORMANCE.md)** - Optimization tips

### Support

- **GitHub Issues** - Report bugs and request features
- **GitHub Discussions** - Ask questions and share tips
- **Documentation** - Comprehensive guides and references

---

## 🎉 Conclusion

You now have everything you need to use Jarvis Voice Assistant effectively! 

**Remember:**
- Start with simple commands
- Use the wake word "Hey Jarvis"
- Try both voice and text modes
- Use quick actions for common tasks
- Check the status indicator for feedback

**Happy voice commanding!** 🎤✨

---

*For technical details, see [API Reference](API_REFERENCE.md)*
*For troubleshooting, see [Troubleshooting Guide](TROUBLESHOOTING.md)*
