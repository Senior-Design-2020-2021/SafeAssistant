import snowboydecoder
import sys
import signal
import subprocess
import datetime
import time

#This script detects a hotword and then calls the voice transcription function upon detection
#Hotword detection code used from demo.py in the Snowboy github page:
#https://github.com/Kitt-AI/snowboy

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

def transcription():
    #time before speech is cutoff, whether user is speaking or not
    timeOut = 8

    #command to record speech
    recordCommand = "timeout " + str(timeOut) + "s rec to_txt.wav silence 1 0.1 1% 1 3.0 1%"
    recording = subprocess.call(recordCommand, shell = True)

    #checkpoint for processing time benchmark
    firstCheckpoint = datetime.datetime.now()

    #command to transcribe recored audio file
    voiceTranscribing = subprocess.Popen("./deepspeech --model deepspeech-0.9.3-models.tflite --scorer deepspeech-0.9.3-models.scorer --audio to_txt.wav"
    , shell = True, stdout=subprocess.PIPE)

    #second checkpoint and calulation of processing time benchmark
    secondCheckpoint = datetime.datetime.now()
    processingTime = secondCheckpoint - firstCheckpoint

    #voice transcription and benchmark output
    voiceTranscription = voiceTranscribing.stdout.read()
    voiceTranscriptionProcessed = voiceTranscription.decode("utf-8")
    print(voiceTranscriptionProcessed)
    print("Processed in " + str(processingTime.microseconds) + " microseconds.")

    print("finished")

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=transcription,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
