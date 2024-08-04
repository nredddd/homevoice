import whisper
from pydub import AudioSegment
import pyaudio
import time
import queue

# Initialize Whisper model
# model = whisper.model("large")
# model = whisper.load_model("large")

# Function to listen and process audio
def process_audio():
    # Create PyAudio object
    p = pyaudio.PyAudio()

    # Open stream from microphone (1 second of data)
    volume = 0.5     # range 0.0 to 1.0
    fs = 22050       # sampling rate, Hz, must be integer
    audio = AudioSegment(
        format="s16le",
        frame_rate=fs,
        channels=1,
        sample_width=2,
        data=p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=fs,
                    input=True).read(4096))  # read 4096 samples (1 second)

    audio_queue = queue.Queue()

    def callback(data):
        audio_data = AudioSegment(
            format="s16le",
            frame_rate=fs,
            channels=2,
            sample_width=2,
            data=data)
        audio_queue.put(audio_data.raw_data())

    stream = p.open(format=PyAudio.paInt16,
                    channels=2,
                    rate=fs,
                    input=True,
                    frames_per_buffer=4096,
                    start=False,
                    stop=False)

    # Start listening
    stream.start_stream()

    while True:
        if not audio_queue.empty():
            audio_data = audio_queue.get()
            chunks = [(chunk, chunk) for chunk in AudioSegment.silk_chunkify(audio_data)]

            for chunk in chunks:
                try:
                    result = model.transcribe(chunk)
                    print(result.text)
                except Exception as e:
                    print(f"Error transcribing: {str(e)}")
        else:
            time.sleep(0.1)

# Process audio
process_audio()