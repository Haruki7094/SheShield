import os
import aubio
import numpy as np
import pyaudio

# Define the directory where the audio files are located
audio_dir = "C:/Users/DELL/Documents/sheshield"

# Create a list of audio file names in the directory
audio_files = [f for f in os.listdir(audio_dir) if f.endswith(".wav")]

# Define the PyAudio and aubio instances
p = pyaudio.PyAudio()
pitch_o = aubio.pitch("yin", 2048, 2048//2, 44100)

# Define the minimum pitch difference required for a match to be considered valid
min_pitch_diff = 5

# Continuously listen for audio input from the microphone
while True:
    print("Listening...")
    # Open the microphone stream
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, frames_per_buffer=2048)
    # Wait for the stream to stabilize
    for i in range(10):
        data = stream.read(2048)
    # Listen for audio input from the user
    data = stream.read(2048)
    # Convert the audio data to a numpy array
    samples = np.frombuffer(data, dtype=aubio.float_type)
    # Get the pitch of the audio input using aubio
    pitch = pitch_o(samples)[0]
    # Use the pitch to compare to each audio file in the directory
    for audio_file in audio_files:
        # Open the audio file and get its pitch
        file_path = os.path.join(audio_dir, audio_file)
        audio_samples, audio_sample_rate = aubio.source(file_path, 0, 2048).read()
        audio_pitch = pitch_o(audio_samples)[0]
        # Calculate the absolute difference between the input pitch and the file pitch
        pitch_diff = abs(pitch - audio_pitch)
        # If the difference is below the minimum threshold, consider it a match
        if pitch_diff <= min_pitch_diff:
            print("Match found:", audio_file)
    # Close the microphone stream
    stream.stop_stream()
    stream.close()

# Terminate the PyAudio instance
p.terminate()
