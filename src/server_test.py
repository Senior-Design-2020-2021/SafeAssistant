# a test script of the client server setup
import os
import json
import argparse
from time import sleep, time
from socket import socket, gethostbyname, gethostname, \
                   SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST 

#======================================================
settings = {}
with open("config.json", "r") as fd:
    settings = json.loads(fd.read())
    settings["IP_ADDR"] = gethostbyname(gethostname())
#======================================================
CONFIG_PATH = "config.json"
#======================================================

def startUp():
   
    if settings['mode'] == 'hub':
        pid = os.fork()
        if pid == 0:
            settings['mode'] = 'Client'
            runClient()
        else:
            settings['mode'] = 'Server'
            runServer()
    
    elif settings['mode'] == 'Client':
        runClient()
    elif settings['mode'] == 'Server':
        runServer()

def runClient():
    """ The startup for the client side process"""
    log("starting client")
    sd = socket(type=SOCK_DGRAM)
    sd.bind(('', 0))

    server = discover_server(sd)
    send(sd, "DATA: hello this is a test", server)
    

def discover_server(sd):

    # client advertisement
    sd.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    send(sd, "CLIENT AVAILABLE", ('<broadcast>', settings['port']))
    log("sent client advertisement")

    # turn off broadcast mode
    sd.setsockopt(SOL_SOCKET, SO_BROADCAST, 0)
    
    data, sender = sd.recvfrom(1024)
    log("received from {}: {}".format(sender, data))

    if data.decode('utf-8').startswith("AUTH REQUEST"):
        server = sender
        log("set server as {}".format(server))
        send(sd, "AUTH: Blue", server)
        data, sender = sd.recvfrom(1024)
        log("received from {}: {}".format(sender, data))
        return server


def runServer():
    
    log("starting server")
    sd = socket(type=SOCK_DGRAM)
    sd.bind(("", settings["port"]))
    nodes = {}

    # UDP polling loop
    while True:
        
        # Receive data
        data, sender = sd.recvfrom(1024)
        print("[SERVER] received from {}: {}".format(sender, data))
        msg = data.decode('utf-8')

        #--------------------------
        # Parse message
        #--------------------------

        ## Client Advertisement
        if msg.startswith("CLIENT AVAILABLE"):
            nodes.update({sender:("challenged", time())})
            send(sd, "AUTH REQUEST: what is your favorite color", sender) 

        ## Client Response to Authentication request
        elif msg.startswith("AUTH: "):
            if sender in nodes.keys():
                status = nodes[sender]
                if status[0] == "challenged" and time() - status[1] < settings['timeout']:
                    # highly secure authentication checks
                    if data.decode('utf-8').split(' ')[1] == "Blue":
                        # success
                        nodes[sender] = ('Authorized', time())
                        log("added {} to list of Authorized clients".format(sender))
                        send(sd, "AUTH ACCEPTED", sender)
                    else:
                        # invalid credentials
                        nodes.pop(sender)
                        log("denied authorization to {}".format(sender))
                        send(sd, "AUTH DENIED: invalid credentials", sender)
                else:
                    # expired challenge
                    nodes.pop(sender)
                    send(sd, "AUTH DENIED: expired challenge", sender)

        ## application data
        elif msg.startswith("DATA: "):
            log("got some data: {}".format(msg[6:]))

def send(sd, msg, dst):
    """ a simple send function that incorporates loging"""
    sd.sendto(msg.encode('utf-8'), dst)
    log("sent to {}: {}".format(dst, msg))

def log(message):
    """ for convenient reporting of app status"""
    print("[{}] {}".format(settings['mode'].upper(), message))


if __name__ == '__main__':
    startUp()