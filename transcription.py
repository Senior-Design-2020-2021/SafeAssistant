import subprocess
import datetime
import time

recordCommand = "arecord -fdat -d 5 to_txt.wav"
#recordCommand = "rec to_txt.wav silence 1 0.1 3% 1 3.0 3%"
recording = subprocess.Popen(recordCommand, shell = True)
time.sleep(6)

firstCheckpoint = datetime.datetime.now()

voiceTranscribing = subprocess.Popen("./deepspeech --model deepspeech-0.9.3-models.tflite --scorer deepspeech-0.9.3-models.scorer --audio to_txt.wav"
, shell = True, stdout=subprocess.PIPE)

secondCheckpoint = datetime.datetime.now()
processingTime = secondCheckpoint - firstCheckpoint

voiceTranscription = voiceTranscribing.stdout.read()
voiceTranscriptionProcessed = voiceTranscription.decode("utf-8")
print(voiceTranscriptionProcessed)
print("Processed in " + str(processingTime.microseconds) + " microseconds.")

print("finished")