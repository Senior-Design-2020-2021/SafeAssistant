import subprocess
import datetime
import time

#recordCommand = "arecord -fdat -d 5 to_txt.wav"

#time before speech is cutoff, whether user is speaking or not

def transcribe():
	timeOut = 8
	recordCommand = "timeout " + str(timeOut) + "s rec to_txt.wav silence 1 0 0% 1 3.0 1%"
	recording = subprocess.call(recordCommand, shell = True)
	firstCheckpoint = datetime.datetime.now()
	voiceTranscribing = subprocess.Popen("./deepspeech --model deepspeech-0.9.3-models.tflite --scorer deepspeech-0.9.3-models.scorer --audio to_txt.wav", shell = True, stdout=subprocess.PIPE)
	secondCheckpoint = datetime.datetime.now()
	processingTime = secondCheckpoint - firstCheckpoint
	voiceTranscription = voiceTranscribing.stdout.read()
	voiceTranscriptionProcessed = voiceTranscription.decode("utf-8")
	return voiceTranscriptionProcessed
