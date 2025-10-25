# 🔧 Troubleshooting Guide

This guide helps you resolve common issues with the Jarvis Voice Assistant.

## 🚨 **Quick Fixes**

### **Application Won't Start**
1. **Check Python Version**: Ensure Python 3.8+ is installed
2. **Install Dependencies**: Run `pip install -r requirements.txt`
3. **Check Permissions**: Run as administrator if needed
4. **Restart Computer**: Sometimes a restart helps

### **Voice Recognition Not Working**
1. **Check Microphone**: Ensure microphone is connected and working
2. **Allow Microphone Access**: Grant permission when prompted
3. **Speak Clearly**: Speak at normal volume and pace
4. **Reduce Background Noise**: Use in quiet environment

### **Commands Not Recognized**
1. **Use Wake Word**: Always start with "Hey Jarvis"
2. **Speak Clearly**: Enunciate words clearly
3. **Check Command**: Verify the command is supported
4. **Try Rephrasing**: Use alternative phrasings

## 🐛 **Common Issues**

### **Issue: "ModuleNotFoundError"**
**Symptoms**: Application crashes with import errors

**Solutions**:
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Check Virtual Environment**:
   ```bash
   # Activate virtual environment
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Update pip**:
   ```bash
   python -m pip install --upgrade pip
   ```

### **Issue: "Microphone not detected"**
**Symptoms**: No audio input, microphone errors

**Solutions**:
1. **Check Microphone Connection**:
   - Ensure microphone is properly connected
   - Check if microphone is working in other applications

2. **Allow Microphone Access**:
   - Windows: Go to Settings > Privacy > Microphone
   - macOS: System Preferences > Security & Privacy > Microphone
   - Linux: Check audio permissions

3. **Test Microphone**:
   ```python
   import speech_recognition as sr
   r = sr.Recognizer()
   with sr.Microphone() as source:
       print("Speak now...")
       audio = r.listen(source)
   ```

### **Issue: "I couldn't help with that"**
**Symptoms**: Commands not being recognized

**Solutions**:
1. **Check Wake Word**:
   - Always start with "Hey Jarvis"
   - Try "Jarvis" or "Assistant"

2. **Speak Clearly**:
   - Speak at normal volume
   - Enunciate words clearly
   - Reduce background noise

3. **Check Command Format**:
   - Use supported commands
   - Check spelling and grammar
   - Try alternative phrasings

### **Issue: "Application crashes on startup"**
**Symptoms**: Application closes immediately after starting

**Solutions**:
1. **Check Python Version**:
   ```bash
   python --version
   # Should be 3.8 or higher
   ```

2. **Install Missing Dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Check System Requirements**:
   - Windows 10/11, macOS 10.14+, or Linux
   - 4GB RAM minimum
   - 1GB free disk space

4. **Run in Debug Mode**:
   ```bash
   python -u main_professional_ui.py
   ```

### **Issue: "Theme switching causes crashes"**
**Symptoms**: Application crashes when changing themes

**Solutions**:
1. **Update CustomTkinter**:
   ```bash
   pip install --upgrade customtkinter
   ```

2. **Check Theme Files**:
   - Ensure theme files are not corrupted
   - Reinstall if necessary

3. **Use Default Theme**:
   - Start with Professional Dark theme
   - Change themes gradually

### **Issue: "WhatsApp not opening"**
**Symptoms**: WhatsApp commands not working

**Solutions**:
1. **Check WhatsApp Installation**:
   - Ensure WhatsApp desktop app is installed
   - Check installation path

2. **Try Alternative Methods**:
   - Use WhatsApp Web as fallback
   - Check browser permissions

3. **Update Dependencies**:
   ```bash
   pip install --upgrade pyautogui
   ```

### **Issue: "Weather showing wrong location"**
**Symptoms**: Weather shows incorrect location

**Solutions**:
1. **Check Internet Connection**:
   - Ensure stable internet connection
   - Check firewall settings

2. **Update Location Services**:
   - Allow location access
   - Check IP geolocation

3. **Specify Location**:
   - Use "weather in [city]" command
   - Check city name spelling

### **Issue: "File operations not working"**
**Symptoms**: File commands not executing

**Solutions**:
1. **Check File Permissions**:
   - Ensure read/write permissions
   - Run as administrator if needed

2. **Check File Paths**:
   - Use correct file paths
   - Avoid special characters

3. **Update Dependencies**:
   ```bash
   pip install --upgrade psutil
   ```

## 🔍 **Debugging Steps**

### **Step 1: Check Logs**
1. **Run with Verbose Output**:
   ```bash
   python -u main_professional_ui.py
   ```

2. **Check Console Output**:
   - Look for error messages
   - Note any warnings

3. **Check Log Files**:
   - Look for log files in the project directory
   - Check system event logs

### **Step 2: Test Components**
1. **Test Voice Recognition**:
   ```python
   import speech_recognition as sr
   r = sr.Recognizer()
   with sr.Microphone() as source:
       print("Speak now...")
       audio = r.listen(source)
       text = r.recognize_google(audio)
       print(f"You said: {text}")
   ```

2. **Test Text-to-Speech**:
   ```python
   import pyttsx3
   engine = pyttsx3.init()
   engine.say("Hello, this is a test")
   engine.runAndWait()
   ```

3. **Test Skills**:
   ```python
   from skills.weather_news_skill import WeatherNewsSkill
   skill = WeatherNewsSkill()
   context = SkillContext("what's the weather")
   result = skill.execute(context)
   print(result.message)
   ```

### **Step 3: System Diagnostics**
1. **Check System Resources**:
   - CPU usage
   - Memory usage
   - Disk space

2. **Check Network Connection**:
   - Internet connectivity
   - API access
   - Firewall settings

3. **Check Audio System**:
   - Microphone functionality
   - Speaker functionality
   - Audio drivers

## 🛠️ **Advanced Troubleshooting**

### **Performance Issues**
1. **Close Other Applications**:
   - Free up system resources
   - Close unnecessary programs

2. **Check System Requirements**:
   - Ensure minimum requirements are met
   - Consider upgrading hardware

3. **Optimize Settings**:
   - Reduce voice recognition sensitivity
   - Disable unnecessary features

### **Memory Issues**
1. **Check Memory Usage**:
   ```python
   import psutil
   print(f"Memory usage: {psutil.virtual_memory().percent}%")
   ```

2. **Restart Application**:
   - Close and reopen the application
   - Clear memory cache

3. **Update Dependencies**:
   - Update all packages
   - Check for memory leaks

### **Network Issues**
1. **Check Internet Connection**:
   ```bash
   ping google.com
   ```

2. **Check API Access**:
   - Test weather API
   - Test translation API
   - Check firewall settings

3. **Use Offline Mode**:
   - Disable internet-dependent features
   - Use local functionality only

## 📞 **Getting Help**

### **Before Asking for Help**
1. **Check This Guide**: Look for your issue in this guide
2. **Search Issues**: Check GitHub issues for similar problems
3. **Try Solutions**: Attempt the suggested solutions
4. **Gather Information**: Collect error messages and logs

### **When Reporting Issues**
1. **Include System Information**:
   - Operating system and version
   - Python version
   - Application version

2. **Describe the Problem**:
   - What you were trying to do
   - What happened instead
   - Error messages received

3. **Include Logs**:
   - Console output
   - Error messages
   - System logs

4. **Provide Steps to Reproduce**:
   - Detailed steps to reproduce the issue
   - Expected vs actual behavior

### **Contact Information**
- **GitHub Issues**: [Report Issues](https://github.com/yourusername/jarvis-voice-assistant/issues)
- **GitHub Discussions**: [Community Help](https://github.com/yourusername/jarvis-voice-assistant/discussions)
- **Email**: support@jarvis-assistant.com

## 🔄 **Recovery Options**

### **Reset to Default Settings**
1. **Delete Configuration Files**:
   - Remove `config.json`
   - Remove `settings.json`

2. **Reinstall Dependencies**:
   ```bash
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   ```

3. **Fresh Installation**:
   - Delete project directory
   - Clone repository again
   - Follow installation guide

### **Backup and Restore**
1. **Backup Data**:
   - Save notes and tasks
   - Export configuration
   - Backup custom skills

2. **Restore Data**:
   - Import saved data
   - Restore configuration
   - Reinstall custom skills

## 📋 **Prevention Tips**

### **Regular Maintenance**
1. **Update Dependencies**:
   - Check for updates monthly
   - Update Python packages
   - Keep system updated

2. **Clean Up**:
   - Remove old log files
   - Clear temporary files
   - Clean up unused data

3. **Monitor Performance**:
   - Check system resources
   - Monitor application performance
   - Watch for errors

### **Best Practices**
1. **Use Virtual Environment**:
   - Isolate dependencies
   - Avoid conflicts
   - Easy cleanup

2. **Regular Backups**:
   - Backup important data
   - Save configuration
   - Keep copies of customizations

3. **Stay Updated**:
   - Follow project updates
   - Read release notes
   - Participate in community

---

<div align="center">

**Need more help? Check the [User Guide](USER_GUIDE.md) or [API Reference](API_REFERENCE.md)**

</div>