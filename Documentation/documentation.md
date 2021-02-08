# Safe Assistant User Documentation

A guide for installing and using the Safe Assistant system

## Contents

Installation Guide (link)
User Guide (link)
FAQ (link)

## Installation Guide

Safe Assistant was designed to be highly configurable and adaptable to the user’s needs, but we have included some directions and troubleshooting  for setting the system up in the recommended configuration.

### Set up Hardware

Safe Assistant can run on any platform that supports Python 3, but we recommend using a unix based system such as a raspberry PI running ubuntu or similar. Instructions to set up a raspberry PI with ubuntu are included [here](https://ubuntu.com/tutorials/how-to-install-ubuntu-desktop-on-raspberry-pi-4#1-overview). 

### Set up Software

All of the necessary files needed to run Safe Assistant are included in a packaged folder (link coming soon). To run Safe Assistant, a user will need to download this folder into a directory on their computer. In that same directory, a user should run the following 
`python3 setup.py` This will pull third party Python packages that Safe Assistant relies on to work properly.

When setting up a new voice assistant device. Make sure to change the value of the `“mode”` setting in `config.json` to the role of “client”, “server”, or “hub”. The server is the main device that hosts the assistant software. There should always be only one of these. The devices that actually communicate with the user are in client mode. There can be many of these connected to a single server. If the device hosting the server also functions as a client device, then the mode should be set to “hub”.

When a safe assistant device starts up, it immediately determines its role based on the ‘mode’ setting, and connects to other devices on the network. For a client device to work properly, the server must be started first. The safe assistant software can be started by running `python3 main.py` in the safe assistant folder

### Install applications

Place any application python files into the “applications” folder in the Safe Assistant. The Safe Assistant will automatically load every application within the folder upon startup.

## User Guide


### Wake Word Detection

The user will activate Safe Assistant by speaking the wake word to it (to be determined). SafeAssistant will then play an audible noise to signal that it is listening for further instructions. 

### Issuing Commands

After the tone SafeAssistant plays immediately following the wake word, a user can begin speaking commands to Safe Assistant. Safe Assistant will record audio until no commands are heard for 3 seconds.

### Command Processing

After issuing a command to the Safe Assistant, the system will process your request. This can take several seconds, depending on the hardware being used; lower-end hardware (such as a raspberry pi) will take a bit longer than a more powerful desktop computer.

### Receiving Information

Once processing for your command is complete, the Safe Assistant will speak back the results of your command. This confirms that your action was successfully processed!

In the case that your action could not be successfully processed or the Safe Assistant could not recognize your command, the Safe Assistant will inform you by speaking.

### Changing Voice, Volume, and Speed

The Safe Assistant allows the user to alter its voice, volume, and speed. To do this, change the “voice,” “volume,” and “speed” variables within the setup file. These changes will take place upon restart of the Safe Assistant system.

## FAQ

### Q: What happens with my voice data when I speak a command?
A: Voice recordings are never sent over a network. After you speak the wake word, the voice recording for your command is saved locally in a temporary file on your PC for it to be transcribed. After transcription, only the text data is used for intent processing. This text data may be sent over the local network to your server hub for faster intent processing, but it will never leave your local network. 

### Q: How will Safe Assistant improve speech recognition without keeping our voice recordings?
A: Voice Assistant relies on Mozilla’s Deepspeech for speech recognition. Mozilla relies on voluntary voice recording donations through their [Common Voice program](https://commonvoice.mozilla.org/en) to improve their software. 

### Q: How can we be sure that Deepspeech is safe if it was written by a third party?
A: We are confident Deepspeech is safe. However, anyone can browse the publicly available source code on the [Deepspeech Github page](https://github.com/mozilla/DeepSpeech) to verify the integrity of the software. 

### Q: What if I have further questions about the security or operations of Safe Assistant?
A: Unlike other voice assistants, Safe Assistant is completely open source. You can verify how our software works by looking at the source code on our [Github page](https://github.com/Senior-Design-2020-2021/SafeAssistant) . Additionally, feel free to leave questions or bugs here for us to take a look at. 
