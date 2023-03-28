import speech_recognition as sr

# initialize the recognizer
r = sr.Recognizer()

# define the trigger word
trigger_word = "hello"

# define the microphone as the audio source
mic = sr.Microphone()

# start listening to the microphone
with mic as source:
    print("Say something!")
    while True:
        # adjust the ambient noise threshold dynamically
        r.adjust_for_ambient_noise(source)
        
        # listen for audio and convert it to text
        audio = r.listen(source)
        text = r.recognize_google(audio)

        # check if the trigger word was detected
        if trigger_word in text.lower():
            print("Trigger word detected!")
