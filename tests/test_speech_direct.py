"""
Direct speech recognition test to verify it works.
"""

import speech_recognition as sr
import pyaudio
import numpy as np
import time

def test_direct_speech_recognition():
    """Test speech recognition directly."""
    print("=== DIRECT SPEECH RECOGNITION TEST ===")
    
    # Initialize recognizer
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 50
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.5
    
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    
    try:
        # Record audio
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        RECORD_SECONDS = 3
        
        print(f"Recording for {RECORD_SECONDS} seconds...")
        print("Say 'Hey Sigma' clearly...")
        
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=0,  # Microsoft Sound Mapper
            frames_per_buffer=CHUNK
        )
        
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
            
            # Show audio level
            audio_array = np.frombuffer(data, dtype=np.int16)
            max_val = np.max(np.abs(audio_array))
            if max_val > 100:
                print(f"Audio level: {max_val}")
        
        stream.stop_stream()
        stream.close()
        
        # Combine audio
        audio_data = b''.join(frames)
        print(f"Recorded {len(audio_data)} bytes of audio")
        
        # Create AudioData
        audio = sr.AudioData(audio_data, RATE, 2)
        
        # Try recognition with different engines
        print("\n--- Testing Google Speech Recognition ---")
        try:
            text = recognizer.recognize_google(audio, show_all=False)
            print(f"Google result: '{text}'")
        except sr.UnknownValueError:
            print("Google couldn't understand audio")
        except sr.RequestError as e:
            print(f"Google service error: {e}")
        
        print("\n--- Testing Sphinx (Offline) ---")
        try:
            text = recognizer.recognize_sphinx(audio)
            print(f"Sphinx result: '{text}'")
        except sr.UnknownValueError:
            print("Sphinx couldn't understand audio")
        except Exception as e:
            print(f"Sphinx error: {e}")
        
        print("\n--- Testing with different settings ---")
        # Try with different audio format
        try:
            # Convert to 44.1kHz
            import wave
            import io
            
            # Create WAV file in memory
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(44100)  # 44.1kHz
                wav_file.writeframes(audio_data)
            
            wav_data = wav_buffer.getvalue()
            audio_44k = sr.AudioData(wav_data, 44100, 2)
            
            text = recognizer.recognize_google(audio_44k, show_all=False)
            print(f"Google (44.1kHz) result: '{text}'")
        except Exception as e:
            print(f"44.1kHz test error: {e}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        p.terminate()

if __name__ == "__main__":
    test_direct_speech_recognition()

