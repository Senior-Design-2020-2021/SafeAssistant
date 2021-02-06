# gets the time
import time

# a simple app for testing purposes

def handle(request):
    return "The time is" + time.strftime("%I %M %p") + "."

def canHandle():
    return [
        "What is the time",
        "What time is it",
        "give me the time",
        "tell me the time",
    ]