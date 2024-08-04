import pyaudio
import numpy as np

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050
SILENCE_THRESHOLD = 500  # Adjust this value to change sensitivity
SILENCE_DURATION = 1  # 1 second of silence to stop recording

def is_silent(data_chunk):
    if (max(data_chunk) < SILENCE_THRESHOLD):
        print(max(data_chunk))
        return max(data_chunk) < SILENCE_THRESHOLD

def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    print("Recording... (speak into the microphone)")
    frames = []
    silent_chunks = 0
    
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        
        if is_silent(np.frombuffer(data, dtype=np.int16)):
            silent_chunks += 1
            if silent_chunks > SILENCE_DURATION * (RATE / CHUNK):
                break
        else:
            silent_chunks = 0
    
    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return b''.join(frames)



def main():
    playback = pyaudio.PyAudio()
    stream = playback.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
    
    print("Playback starting. Press Ctrl+C to stop.")
    try:
        while True:
            audio_data=record_audio()
            # stream.write(audio_data)
    except KeyboardInterrupt:
        print("\nPlayback stopped.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()