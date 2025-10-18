# Quick Start Guide - Get Started in 5 Minutes!

## 🚀 Super Fast Start

### Step 1: Install (2 minutes)
```bash
cd voice_assistant
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### Step 2: Run (1 minute)
```bash
python main_pushtotalk.py
```

### Step 3: Use (2 minutes)
1. **HOLD** the green button
2. **SAY**: "Hey Sigma, what time is it?"
3. **RELEASE** button
4. **GET** response!

**Done! Your voice assistant is working!** 🎉

---

## 🎮 Three Ways to Use

### Option 1: Push-to-Talk (Best!)
```bash
python main_pushtotalk.py
```
- Hold button while speaking
- Most reliable for all users
- **Recommended!**

### Option 2: Combined Mode
```bash
python main_combined.py
```
- Type OR continuous voice listening
- Click "Start Listening" for voice

### Option 3: Keyboard Only
```bash
python main_hybrid.py
```
- Type all commands
- 100% reliable, no mic needed

---

## 📝 Try These Commands

### In Any Mode (Type or Speak):

```
Hey Sigma, what time is it?
Hey Sigma, show system information
Hey Sigma, set a reminder for 5 minutes
Hey Sigma, open calculator
Hey Sigma, search for test
Hey Sigma, what can you do?
```

**All work immediately!**

---

## 🔧 If Something Doesn't Work

### Voice Not Working?
1. **Try keyboard mode** (works 100%):
   ```bash
   python main_hybrid.py
   ```
2. **Or test your mic**:
   ```bash
   python tests/test_microphone_volume.py
   ```

### Need Help?
- Read: [docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Check: [docs/HOW_TO_USE.md](HOW_TO_USE.md)

---

## ⚡ Power User Tips

### Keyboard Shortcuts
- `Enter` - Send typed command
- `Ctrl+C` in terminal - Stop assistant

### Best Voice Practices
- Speak clearly and at normal pace
- Always start with "Hey Sigma"
- Pause briefly after wake word
- Use push-to-talk for best results

### Microphone Tips
- Position mic 15-30cm from mouth
- Reduce background noise
- Enable Microphone Boost in Windows
- Test with `python tests/test_microphone_volume.py`

---

## 📊 What's Working

### ✅ All These Features Work:
- Voice input (push-to-talk)
- Keyboard input (typing)
- Time and date queries
- System information
- Reminders (multiple formats)
- File search
- Application launching (Calculator, Chrome, CMD, etc.)
- Help system
- 8 functional skills

---

## 🎯 Next Steps

1. **Explore all commands** - Try different features
2. **Set some reminders** - Test the scheduling
3. **Search for files** - Try the file search
4. **Open apps** - Launch your favorite programs
5. **Read full docs** - [docs/HOW_TO_USE.md](HOW_TO_USE.md)

---

## 📁 Important Files

- **`main_pushtotalk.py`** - Your main assistant (use this!)
- **`requirements.txt`** - Dependencies
- **`docs/`** - All documentation
- **`tests/`** - Testing utilities

---

## 💡 Pro Tips

1. **Use Push-to-Talk** - More reliable than continuous listening
2. **Type when in doubt** - Keyboard mode always works
3. **Test your mic first** - Run the mic test before voice mode
4. **Read docs** - Lots of helpful info in docs folder
5. **Check terminal** - Shows what's being recognized

---

**That's it! You're ready to use your voice assistant!** 🎤

**Run:** `python main_pushtotalk.py` and start talking to Sigma!

