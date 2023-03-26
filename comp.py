import os
import speech_recognition as sr
from fuzzywuzzy import fuzz

# Define the directory where the audio files are located
audio_dir = "C:/Users/DELL/Documents/sheshield"

# Create a list of audio file names in the directory
audio_files =[f for f in os.listdir(audio_dir) if f.endswith(".wav")]

# Define the SpeechRecognition recognizer and microphone instances
r = sr.Recognizer()
mic = sr.Microphone()

# Define the minimum score required for a match to be considered valid
min_score = 70

# Continuously listen for audio input from the microphone
while True:
    print("Listening...")
    with mic as source:
        # Adjust microphone for ambient noise
        r.adjust_for_ambient_noise(source)
        # Listen for audio input from the user
        audio = r.listen(source)
    # Use the SpeechRecognition library to transcribe the audio
    try:
        # Set the language to English (US)
        text = r.recognize_google(audio, language="en-US")
        print("You said:", text)
        # Compare the transcribed text to each audio file name in the directory
        for audio_file in audio_files:
            score = fuzz.ratio(text, audio_file[:-4])
            if score >= min_score:
                print("Match found:", audio_file)
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
