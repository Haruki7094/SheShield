import pyaudio
import soundfile as sf
import numpy as np

# set up audio capture parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 1024

# open audio file for comparison
data, _ = sf.read('recording.wav')
pre_existing_file = np.array(data)

# initialize pyaudio object
p = pyaudio.PyAudio()

# open audio stream for capture
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)

# initialize variables for comparing audio
buffer = np.zeros((len(pre_existing_file),))
index = 0
matched = False

# start audio capture and comparison
while True:
    # read audio data from stream
    audio_data = stream.read(CHUNK_SIZE)
    # convert audio data to numpy array
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    # add audio data to buffer
    buffer[index:index+len(audio_array)] = audio_array
    index += len(audio_array)
    # if buffer is full, compare it with pre-existing file
    if index >= len(pre_existing_file):
        diff = buffer - pre_existing_file
        rms_diff = np.sqrt(np.mean(diff ** 2))
        # print rms difference between captured audio and pre-existing file
        print("RMS difference: {}".format(rms_diff))
        # check if the audio matches
        if rms_diff < 100:
            matched = True
            break
        # reset buffer and index
        buffer = np.zeros((len(pre_existing_file),))
        index = 0

# close audio stream and pyaudio object
stream.stop_stream()
stream.close()
p.terminate()

# print the result
if matched:
    print("Audio captured through mic matches the pre-existing file.")
else:
    print("Audio captured through mic does not match the pre-existing file.")
