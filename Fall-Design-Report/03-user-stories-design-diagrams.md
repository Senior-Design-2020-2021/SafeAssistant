# User Stories and Design Diagrams

## User Stories

1. As a privacy-conscious user, I want a home voice assistant that keeps all of my voice data on the local network so that I have total control over my own voice data.
2. As a privacy-conscious user, I want the ability to specify what applications can and can’t do with my data
3. As a privacy-conscious user, I want the project code and ecosystem to be open source so that I can verify the trustworthiness and security of the voice assistant 
4. As a voice assistant user, I want the ability to add new functions to my voice assistant so that the software can continue to meet all of my needs
5. As a consumer, I want hardware that can support the basic functionalities of a voice assistant.

## Design Diagrams

Level 0

![Level 0](level0.png)

The Level 0 diagram reflects the general flow of information from the user to the device. In this architecture, The only communication to the internet is done by installed applications which can be verified by the user. In addition, users can grant permission on an app by app basis.

Level 1

![Level 1](level1.png)

The Level 1 diagram reflects the control flow of the program, and indicates the major portions of the process, and where the code is being executed.

Level 2

![Level 2](level2.png)

The Level 2 diagram shows a more granular breakdown of the code components involved in the process. This details the way the assistant hub will route control to the various installed applications and communicate with the edge nodes. Additionally the dotted lines represent logical security relate boundaries. There will be security measures in place to protect and verify communication between the client, the server, and third party code.

---

[⭠ Previous Page](02-project-description.md) | [Next Page ⭢](04-project-tasks-and-timeline.md)
