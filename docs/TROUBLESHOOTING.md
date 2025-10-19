# 🔧 Troubleshooting Guide - Jarvis Voice Assistant

This comprehensive guide helps you solve common issues with the Jarvis Voice Assistant. Follow the solutions step by step for the best results.

---

## 📋 Table of Contents

- [Quick Fixes](#-quick-fixes)
- [Voice Recognition Issues](#-voice-recognition-issues)
- [Audio Problems](#-audio-problems)
- [UI Issues](#-ui-issues)
- [Performance Problems](#-performance-problems)
- [Installation Issues](#-installation-issues)
- [Platform-Specific Issues](#-platform-specific-issues)
- [Advanced Troubleshooting](#-advanced-troubleshooting)

---

## 🚀 Quick Fixes

### Most Common Issues (90% of problems)

1. **Microphone too quiet** → Increase microphone boost to +20dB or +30dB
2. **Not saying wake word** → Always start with "Hey Jarvis"
3. **Background noise** → Reduce noise or use push-to-talk mode
4. **Internet connection** → Check internet for Google speech recognition

### Quick Test Commands

```bash
# Test microphone volume
python tests/test_microphone_volume.py

# Test speech recognition
python tests/test_speech_recognition.py

# Use keyboard mode (no microphone needed)
python main_hybrid.py
```

---

## 🎤 Voice Recognition Issues

### Problem: "Couldn't understand audio" or "Network error"

**Symptoms:**
- Audio levels are good (10,000+)
- System captures audio
- But shows "Google couldn't understand audio" or "Network error"

**Solutions:**

#### Step 1: Check Internet Connection
```bash
# Test internet connectivity
ping google.com
```

#### Step 2: Verify Speech Recognition
```bash
# Test with simple command
python tests/test_speech_direct.py
```

#### Step 3: Try Alternative Recognition
- Use push-to-talk mode: `python main_professional_ui.py`
- Use keyboard mode: `python main_hybrid.py`

#### Step 4: Check Firewall
- Allow Python through Windows Firewall
- Check antivirus isn't blocking network access

### Problem: Wrong words recognized

**Symptoms:**
- System says words you didn't speak
- Detects "uh", "what", "but" from silence

**Solutions:**
1. **Speak more clearly** - Enunciate each word
2. **Reduce background noise** - Close windows, turn off fans
3. **Use push-to-talk mode** - Hold button while speaking
4. **Check microphone quality** - Try different microphone
5. **Speak at normal pace** - Not too fast or slow

### Problem: Wake word not detected

**Symptoms:**
- Speech recognized but nothing happens
- Message: "Wake word not detected in: [your text]"

**Solutions:**
1. **Always start with "Hey Jarvis"**
2. **Speak clearly and loudly**
3. **Try alternatives:**
   - "Jarvis"
   - "Hey Assistant"
   - "Assistant"
4. **Pause briefly** after wake word

**Example:**
```
✅ "Hey Jarvis" [pause] "what time is it?"
❌ "what time is it?" (missing wake word)
```

---

## 🎵 Audio Problems

### Problem: Microphone not detected

**Symptoms:**
- Error: "No default input device"
- Error: "Failed to start audio recording"
- Error: "No microphone found"

**Solutions:**

#### Step 1: Check Hardware
1. **Verify microphone is plugged in**
2. **Check microphone is not muted**
3. **Try different USB port** (for USB microphones)
4. **Test microphone in other applications**

#### Step 2: Windows Sound Settings
1. **Right-click speaker icon** (taskbar)
2. **Click "Open Sound settings"**
3. **Scroll to "Input" section**
4. **Select your microphone** from dropdown
5. **Test microphone** - speak and watch blue bar

#### Step 3: Device Manager
1. **Open Device Manager**
2. **Expand "Audio inputs and outputs"**
3. **Right-click microphone** → "Enable device"
4. **Update drivers** if needed

### Problem: Audio level too low

**Symptoms:**
- Test shows level: 1-1000 (need 10,000+)
- Message: "ALMOST SILENT" or "TOO QUIET"
- Assistant captures audio but doesn't recognize speech

**Solutions (Do ALL steps):**

#### Step A: Basic Volume
1. **Right-click speaker icon** (taskbar)
2. **Click "Open Sound settings"**
3. **Scroll to "Input" section**
4. **Move volume slider to 100%**
5. **Speak** - you should see blue bar moving significantly

#### Step B: Microphone Boost (CRITICAL)
1. **In Sound settings, click "Device properties"**
2. **Click "Additional device properties"**
3. **Go to "Levels" tab**
4. **Set Microphone: 100**
5. **Set Microphone Boost: +20dB or +30dB**
6. **Click OK**
7. **Click OK again**

#### Step C: Advanced Settings
1. **In "Additional device properties"**
2. **Go to "Advanced" tab**
3. **Uncheck "Allow applications to take exclusive control"**
4. **Set Default Format to "1 channel, 16 bit, 16000 Hz"**
5. **Click OK**

#### Step D: Verify Fix
```bash
python tests/test_microphone_volume.py
```
**Expected:** Levels above 10,000 when speaking

### Problem: Audio feedback or echo

**Symptoms:**
- Echo or feedback when speaking
- Microphone picks up speaker output

**Solutions:**
1. **Use headphones** instead of speakers
2. **Reduce speaker volume**
3. **Move microphone away from speakers**
4. **Use push-to-talk mode** to control when listening

---

## 🖥️ UI Issues

### Problem: Interface looks broken or distorted

**Symptoms:**
- Buttons not displaying correctly
- Colors look wrong
- Layout is broken

**Solutions:**

#### Step 1: Update CustomTkinter
```bash
pip install --upgrade customtkinter
```

#### Step 2: Check Python Version
```bash
python --version
# Should be 3.8 or higher
```

#### Step 3: Clear Cache
```bash
# Clear Python cache
find . -type d -name "__pycache__" -delete
find . -name "*.pyc" -delete
```

#### Step 4: Reinstall Dependencies
```bash
pip uninstall customtkinter
pip install customtkinter
```

### Problem: Buttons not responding

**Symptoms:**
- Clicking buttons does nothing
- UI freezes or becomes unresponsive

**Solutions:**
1. **Restart the application**
2. **Check for error messages** in console
3. **Use keyboard mode** as backup: `python main_hybrid.py`
4. **Update graphics drivers**

### Problem: Conversation not scrolling

**Symptoms:**
- New messages appear but don't auto-scroll
- Have to manually scroll to see responses

**Solutions:**
1. **Restart the application** - this should auto-scroll
2. **Check if scroll bar is visible**
3. **Try clicking in conversation area**
4. **Use keyboard mode** if UI issues persist

---

## ⚡ Performance Problems

### Problem: Slow response or lag

**Symptoms:**
- Takes long time to respond to commands
- UI is slow or unresponsive
- High CPU or memory usage

**Solutions:**

#### Step 1: Check System Resources
```bash
# Check memory usage
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"

# Check CPU usage
python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%')"
```

#### Step 2: Close Other Applications
- Close unnecessary programs
- Free up memory and CPU
- Check for background processes

#### Step 3: Optimize Settings
1. **Reduce audio quality** if needed
2. **Disable animations** in settings
3. **Use keyboard mode** for better performance

#### Step 4: Restart Application
```bash
# Kill any running instances
taskkill /f /im python.exe

# Restart
python main_professional_ui.py
```

### Problem: High memory usage

**Symptoms:**
- Memory usage keeps increasing
- Application becomes slower over time
- System runs out of memory

**Solutions:**
1. **Restart application** periodically
2. **Clear conversation history** (Clear button)
3. **Close unused applications**
4. **Check for memory leaks** in logs

---

## 📦 Installation Issues

### Problem: "Module not found" errors

**Symptoms:**
- ImportError: No module named 'customtkinter'
- ImportError: No module named 'speech_recognition'
- ImportError: No module named 'numpy'

**Solutions:**

#### Step 1: Check Virtual Environment
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Check if packages are installed
pip list
```

#### Step 2: Install Missing Packages
```bash
# Install all requirements
pip install -r requirements.txt

# Or install specific package
pip install customtkinter
pip install speech_recognition
pip install numpy
```

#### Step 3: Check Python Version
```bash
python --version
# Should be 3.8 or higher
```

### Problem: Permission errors during installation

**Symptoms:**
- Permission denied errors
- Access denied when installing packages
- Administrator required

**Solutions:**
1. **Run as Administrator**
2. **Use virtual environment** (recommended)
3. **Check antivirus** isn't blocking installation
4. **Try user installation**: `pip install --user package_name`

### Problem: Package installation fails

**Symptoms:**
- pip install fails with errors
- Package compilation errors
- Network timeout errors

**Solutions:**

#### Step 1: Update pip
```bash
python -m pip install --upgrade pip
```

#### Step 2: Use different package source
```bash
pip install -i https://pypi.org/simple/ package_name
```

#### Step 3: Install pre-compiled packages
```bash
pip install --only-binary=all package_name
```

---

## 🖥️ Platform-Specific Issues

### Windows Issues

#### Problem: PyAudio installation fails
**Solution:**
```bash
# Install Microsoft Visual C++ Build Tools first
# Then install PyAudio
pip install pipwin
pipwin install pyaudio
```

#### Problem: Windows Defender blocks Python
**Solution:**
1. **Add Python to exclusions** in Windows Defender
2. **Add project folder** to exclusions
3. **Allow Python through firewall**

#### Problem: PowerShell execution policy
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### macOS Issues

#### Problem: PortAudio not found
**Solution:**
```bash
# Install PortAudio using Homebrew
brew install portaudio
pip install pyaudio
```

#### Problem: Permission denied for microphone
**Solution:**
1. **System Preferences** → **Security & Privacy**
2. **Privacy** tab → **Microphone**
3. **Check Python** or **Terminal** in the list

### Linux Issues

#### Problem: Audio system not found
**Solution:**
```bash
# Install ALSA development files
sudo apt-get install portaudio19-dev python3-pyaudio

# Or for other distributions
sudo yum install portaudio-devel python3-pyaudio
```

#### Problem: Permission denied for audio
**Solution:**
```bash
# Add user to audio group
sudo usermod -a -G audio $USER
# Log out and back in
```

---

## 🔧 Advanced Troubleshooting

### Debug Mode

Enable debug mode for detailed logging:

```python
# Add to main_professional_ui.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check System Logs

#### Windows Event Viewer
1. **Open Event Viewer**
2. **Windows Logs** → **Application**
3. **Look for Python errors**

#### Console Output
Look for these patterns in console:

**Good (Working):**
```
[ENHANCE AUDIO] Original audio max level: 15234
[SPEECH RECOG] Google result: 'hey sigma what time is it'
[AUDIO CALLBACK] Valid speech detected
```

**Bad (Too Quiet):**
```
[ENHANCE AUDIO] Original audio max level: 1
[ENHANCE AUDIO] Audio too quiet, rejecting as noise
[PROCESS BUFFER] Audio rejected as noise
```

### Performance Profiling

```python
# Add to main_professional_ui.py
import cProfile
import pstats

def profile_performance():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your code here
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
```

### Memory Leak Detection

```python
# Add to main_professional_ui.py
import tracemalloc

def check_memory():
    tracemalloc.start()
    # Your code here
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory: {current / 1024 / 1024:.1f} MB")
    print(f"Peak memory: {peak / 1024 / 1024:.1f} MB")
    tracemalloc.stop()
```

---

## 🆘 Emergency Fallback

### If Nothing Works

1. **Use keyboard mode:**
   ```bash
   python main_hybrid.py
   ```

2. **Use original mode:**
   ```bash
   python main.py
   ```

3. **Check system requirements:**
   - Windows 10/11
   - Python 3.8+
   - Working microphone
   - Internet connection
   - Speakers for TTS output

### Get Help

1. **Check GitHub Issues:** [Report bugs](https://github.com/yourusername/sigma-voice-assistant/issues)
2. **GitHub Discussions:** [Ask questions](https://github.com/yourusername/sigma-voice-assistant/discussions)
3. **Documentation:** [Read guides](docs/)
4. **Community:** [Join discussions](https://github.com/yourusername/sigma-voice-assistant/discussions)

---

## 📊 Common Error Messages

| Error Message | Meaning | Solution |
|---------------|---------|----------|
| `"No default input device"` | Microphone not detected | Check microphone connection |
| `"Audio too quiet"` | Microphone volume too low | Increase microphone boost |
| `"Google couldn't understand audio"` | Speech not clear | Speak louder, reduce noise |
| `"Wake word not detected"` | Missing "Hey Jarvis" | Always start with wake word |
| `"Network error"` | Internet connection issue | Check internet connection |
| `"Module not found"` | Missing dependency | Install required packages |
| `"Permission denied"` | Access rights issue | Run as administrator |

---

## 🎯 Prevention Tips

### Regular Maintenance
1. **Restart application** daily
2. **Clear conversation history** weekly
3. **Update dependencies** monthly
4. **Check system resources** regularly

### Best Practices
1. **Use push-to-talk mode** in noisy environments
2. **Speak clearly and at normal pace**
3. **Keep microphone clean and positioned correctly**
4. **Close unnecessary applications**
5. **Keep system updated**

---

## 📈 Performance Optimization

### System Optimization
1. **Close unnecessary programs**
2. **Disable startup programs**
3. **Update graphics drivers**
4. **Free up disk space**
5. **Defragment hard drive**

### Application Optimization
1. **Use keyboard mode** for better performance
2. **Disable animations** if needed
3. **Reduce audio quality** if necessary
4. **Clear conversation history** regularly
5. **Restart application** periodically

---

## 🎉 Success Indicators

### When Everything is Working:
- **Microphone levels:** 10,000+ when speaking
- **Speech recognition:** Clear text output
- **Wake word detection:** "Hey Jarvis" recognized
- **Response time:** < 2 seconds
- **UI responsiveness:** Smooth and fast
- **Memory usage:** < 200MB
- **CPU usage:** < 10%

### Test Commands:
```bash
# Test microphone
python tests/test_microphone_volume.py

# Test speech recognition
python tests/test_speech_recognition.py

# Test full system
python main_professional_ui.py
```

---

**Remember:** Most issues (90%) are caused by microphone volume/boost being too low. Always check this first!

For more help, see:
- [User Guide](USER_GUIDE.md)
- [API Reference](API_REFERENCE.md)
- [Performance Guide](PERFORMANCE.md)