# Voice Assistant Troubleshooting Guide

## Quick Diagnosis

Run this command to identify the issue:
```bash
cd D:\Projects\voice_assistant
.\venv\Scripts\Activate.ps1
python test_microphone_volume.py
```

## Problem 1: Microphone Not Detected

**Symptoms:**
- Error: "No default input device"
- Error: "Failed to start audio recording"

**Solutions:**
1. Check microphone is plugged in
2. Windows Settings → Sound → Input → Select your microphone
3. Right-click speaker icon → Sounds → Recording tab → Enable microphone
4. Restart the application

## Problem 2: Audio Level Too Low (Current Issue)

**Symptoms:**
- Test shows level: 1-1000 (need 10,000+)
- Message: "ALMOST SILENT" or "TOO QUIET"
- Assistant captures audio but doesn't recognize speech

**Solutions (Do ALL steps):**

### Step A: Basic Volume
1. Right-click speaker icon (taskbar)
2. Click "Open Sound settings"
3. Scroll to "Input" section
4. Move volume slider to 100%
5. Speak - you should see blue bar moving significantly

### Step B: Microphone Boost (CRITICAL)
1. In Sound settings, click "Device properties"
2. Click "Additional device properties"
3. Go to "Levels" tab
4. Set Microphone: 100
5. Set Microphone Boost: +20dB or +30dB
6. Click OK
7. Click OK again

### Step C: Advanced Settings
1. In "Additional device properties"
2. Go to "Advanced" tab
3. Uncheck "Allow applications to take exclusive control"
4. Set Default Format to "1 channel, 16 bit, 16000 Hz"
5. Click OK

### Step D: Verify Fix
```bash
python test_microphone_volume.py
```
You should now see levels above 10,000 when speaking.

## Problem 3: Speech Not Recognized

**Symptoms:**
- Audio levels are good (10,000+)
- System captures audio
- But shows "Google couldn't understand audio"

**Solutions:**
1. Speak clearly and loudly
2. Say "Hey Sigma" first to activate
3. Pause briefly between wake word and command
4. Check internet connection (Google recognition needs internet)
5. Reduce background noise

Example:
```
"Hey Sigma" [pause] "what time is it?"
```

## Problem 4: Wake Word Not Detected

**Symptoms:**
- Speech recognized but nothing happens
- Message: "Wake word not detected in: [your text]"

**Solutions:**
1. Always start with "Hey Sigma"
2. Speak clearly
3. Try alternatives: "Sigma" or "Hey Assistant"

## Problem 5: Random Words Detected

**Symptoms:**
- System says words you didn't speak
- Detects "uh", "what", "but" from silence

**Solutions:**
- This is FIXED in latest version
- If still happening: Increase microphone boost further
- Background noise may be too high

## Problem 6: No Response from Assistant

**Symptoms:**
- Speech recognized
- Wake word detected
- But no response

**Solutions:**
1. Check Skills are registered (should see in console)
2. Verify TTS (text-to-speech) is working
3. Check speakers are on and unmuted
4. Look for error messages in console

## Problem 7: Application Crashes

**Symptoms:**
- Python crashes
- Window closes unexpectedly

**Solutions:**
1. Check Python version (need 3.8+)
2. Reinstall dependencies:
   ```bash
   .\venv\Scripts\Activate.ps1
   pip install --upgrade -r requirements.txt
   ```
3. Check logs for error messages
4. Run: `python main_hybrid.py` (keyboard mode) as backup

## Problem 8: Internet Connection Issues

**Symptoms:**
- "Recognition service error"
- "Request error"

**Solutions:**
1. Check internet connection
2. Google speech recognition requires internet
3. Firewall may be blocking Python
4. Try: Allow Python through Windows Firewall

## Testing Commands

### Test 1: Microphone Volume
```bash
python test_microphone_volume.py
```
**Expected**: Levels 10,000-20,000 when speaking

### Test 2: Audio Pipeline
```bash
python test_audio_pipeline.py
```
**Expected**: "Audio callback triggered: YES"

### Test 3: Hybrid Mode (No Voice)
```bash
python main_hybrid.py
```
Type commands to test without microphone

### Test 4: Full Assistant
```bash
python main.py
```
Click "Start Listening" and speak

## Understanding Error Messages

### "[ENHANCE AUDIO] Audio too quiet (max: 1), rejecting as noise"
**Meaning**: Microphone volume is too low
**Fix**: Increase microphone boost (Problem 2)

### "[SPEECH RECOG] Google couldn't understand audio"
**Meaning**: Audio captured but not clear speech
**Fix**: Speak louder, reduce noise, check internet

### "Wake word not detected in: [text]"
**Meaning**: Heard you but didn't hear "Hey Sigma"
**Fix**: Always start with "Hey Sigma"

### "[RECORDING LOOP] Buffer full at 50 chunks, processing..."
**Meaning**: Normal operation, collecting speech
**Fix**: No fix needed, working correctly

### "[PROCESS BUFFER] Audio rejected as noise, skipping recognition"
**Meaning**: Audio level below threshold (2000)
**Fix**: Increase microphone volume/boost

## Performance Tips

### For Best Recognition:
1. Speak clearly and at normal pace
2. Reduce background noise
3. Position microphone 15-30cm from mouth
4. Use push-to-talk if background is noisy
5. Speak in complete sentences

### Optimal Settings:
- Microphone Volume: 100%
- Microphone Boost: +20dB to +30dB
- Audio levels: 10,000-20,000 range
- Background noise: < 2000 level
- Internet: Stable connection

## Still Having Issues?

### Check System Requirements:
- Windows 10/11
- Python 3.8 or higher
- Working microphone
- Internet connection
- Speakers for TTS output

### Logs Location:
All output is shown in terminal/console. Look for:
- `[AUDIO CALLBACK]` - Audio capture events
- `[SPEECH RECOG]` - Recognition attempts
- `[ERROR]` - Error messages
- `[ENHANCE AUDIO]` - Audio level info

### Common Log Patterns:

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

## Emergency Fallback

If voice won't work at all, use Hybrid Mode:
```bash
python main_hybrid.py
```
This lets you TYPE commands instead of speaking them.

---

**Most Common Issue**: Microphone volume/boost too low (90% of problems)
**Second Most Common**: Not saying "Hey Sigma" first
**Third Most Common**: Background noise too loud


