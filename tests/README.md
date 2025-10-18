# 🧪 Tests

This directory contains test files and utilities for the Sigma Voice Assistant.

## 📁 Test Files

### Audio Tests
- **[test_microphone_volume.py](test_microphone_volume.py)** - Test microphone volume levels
- **[test_speech_recognition.py](test_speech_recognition.py)** - Test speech recognition
- **[test_audio_pipeline.py](test_audio_pipeline.py)** - Test audio processing pipeline

### Device Tests
- **[test_microphone_devices.py](test_microphone_devices.py)** - List available microphones
- **[select_microphone.py](select_microphone.py)** - Interactive microphone selection
- **[test_all_microphones.py](test_all_microphones.py)** - Test all available microphones

### Calibration Tests
- **[voice_calibration.py](voice_calibration.py)** - Voice calibration utility
- **[train_my_voice.py](train_my_voice.py)** - Voice training utility
- **[train_voice_auto.py](train_voice_auto.py)** - Automated voice training

### Utility Tests
- **[test_simple.py](test_simple.py)** - Simple functionality test
- **[test_direct_recognition.py](test_direct_recognition.py)** - Direct speech recognition test
- **[test_speech_direct.py](test_speech_direct.py)** - Speech recognition test
- **[test_stereo_mix.py](test_stereo_mix.py)** - Stereo mix testing
- **[test_voice_assistant_microphone.py](test_voice_assistant_microphone.py)** - Microphone integration test

## 🚀 Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run Specific Tests
```bash
# Test microphone volume
python tests/test_microphone_volume.py

# Test speech recognition
python tests/test_speech_recognition.py

# Test audio pipeline
python tests/test_audio_pipeline.py
```

### Interactive Tests
```bash
# Select microphone
python tests/select_microphone.py

# Voice calibration
python tests/voice_calibration.py

# Train voice
python tests/train_my_voice.py
```

## 🔧 Test Configuration

### Prerequisites
- Python 3.8+
- All dependencies installed
- Working microphone (for audio tests)
- Internet connection (for speech recognition tests)

### Environment Variables
```bash
# Optional: Set test configuration
export TEST_MICROPHONE_INDEX=0
export TEST_AUDIO_LEVEL_THRESHOLD=10000
export TEST_RECOGNITION_TIMEOUT=10
```

## 📊 Test Results

### Expected Results
- **Microphone Volume**: 10,000+ when speaking
- **Speech Recognition**: Clear text output
- **Audio Pipeline**: No errors or warnings
- **Device Detection**: All microphones listed

### Troubleshooting
If tests fail:
1. Check microphone connection
2. Verify audio levels
3. Check internet connection
4. See [Troubleshooting Guide](../docs/TROUBLESHOOTING.md)

## 📚 Documentation

For more information, see:
- [User Guide](../docs/USER_GUIDE.md)
- [Troubleshooting Guide](../docs/TROUBLESHOOTING.md)
- [API Reference](../docs/API_REFERENCE.md)

---

*These tests help ensure the Sigma Voice Assistant works correctly on your system.*
