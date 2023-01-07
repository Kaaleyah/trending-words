import azure.cognitiveservices.speech as speechsdk
import time
import sys
import csv
from collections import Counter

# Azure configuration
speech_key, service_region = "API_KEY", "REGION"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Video file
soundFile = input("Enter the sound file name (It must be WAV file): ")
videoInput = speechsdk.AudioConfig(filename=soundFile)

# Speech recognition
speechRecognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=videoInput)

def stop_cb(evt):
    """callback that stops continuous recognition upon receiving an event `evt`"""
    print('CLOSING on {}'.format(evt))
    speechRecognizer.stop_continuous_recognition()

def recognized(evt):
    print('RECOGNIZED: {}'.format(evt))

    with open("text.txt", "a") as f:
        f.write(evt.result.text)

def countWords():
    with open("text.txt", "r") as f:
        text = f.read()

    words = text.split()

    words = [word for word in words if word.isalpha()]
    words = [word.lower() for word in words]

    wordCount = Counter(words)

    with open("data.csv", "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["Word"])

        for word in words:
            writer.writerow([word])

def finished(evt):
    print('SESSION STOPPED {}'.format(evt))
    countWords()
    
    sys.exit(0)

# Connect callbacks to the events fired by the speech recognizer
#speechRecognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
speechRecognizer.recognized.connect(recognized)
speechRecognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
speechRecognizer.session_stopped.connect(finished)
speechRecognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

# stop continuous recognition on either session stopped or canceled events
speechRecognizer.session_stopped.connect(stop_cb)
speechRecognizer.canceled.connect(stop_cb)

# Start continuous speech recognition
speechRecognizer.start_continuous_recognition()

while True:
    # This is just an example. The actual code will depend on your specific application.
    # You can use a loop or other mechanism to keep the program running until the user
    # indicates that they want to stop the program.
    time.sleep(1)