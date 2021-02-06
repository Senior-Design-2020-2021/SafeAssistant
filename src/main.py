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
    # settings["IP_ADDR"] = gethostbyname(gethostname())
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
    send(sd, server, msg_type="data", content="hello this is a test")


def discover_server(sd):

    # client advertisement
    sd.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    send(sd, ('<broadcast>', settings['port']), msg_type="connect")
    log("sent client advertisement")

    # turn off broadcast mode
    sd.setsockopt(SOL_SOCKET, SO_BROADCAST, 0)
    
    msg, sender = read(sd)

    if msg['type'] == 'auth challenge':
        server = sender
        log("set server as {}".format(server))
        send(sd, server, msg_type="auth reply", content="Blue")
        data, sender = read(sd)
        return server


def runServer():
    
    log("starting server")
    sd = socket(type=SOCK_DGRAM)
    sd.bind(("", settings["port"]))
    nodes = {}

    # UDP polling loop
    while True:
        
        # Receive data
        msg, sender = read(sd)

        #--------------------------
        # Parse message
        #--------------------------

        ## Client Advertisement
        if msg['type'] == "connect":
            nodes.update({sender:("challenged", time())})
            send(sd, sender, msg_type="auth challenge", content="what is your favorite color") 

        ## Client Response to Authentication request
        elif msg['type'] == "auth reply":
            if sender in nodes.keys():
                status = nodes[sender]
                if status[0] == "challenged" and time() - status[1] < settings['timeout']:
                    # highly secure authentication checks
                    if msg['content'] == "Blue":
                        # success
                        nodes[sender] = ('Authorized', time())
                        log("Added {} to list of authorized clients".format(sender))
                        send(sd, sender, msg_type="auth accept")
                    else:
                        # invalid credentials
                        nodes.pop(sender)
                        log("denied authorization to {}".format(sender))
                        send(sd, sender, msg_type="auth reject", content='invalid credentials')
                else:
                    # expired challenge
                    nodes.pop(sender)
                    send(sd, sender, msg_type="auth reject", content="expired challenge")

        ## if message is not an authentication message
        else:
            # check authentication
            if sender in nodes.keys():
                status = nodes[sender]
                if status[0] == "Authorized" and time() - nodes[sender][1] < settings['timeout']:
                    ## process application data
                    if msg['type'] == 'data':
                        log("got some data: {}".format(msg['content']))

                else:
                    send(sd, sender, msg_type="auth reject", content="not authenticated")
            else:
                send(sd, sender, msg_type="auth reject", content="not authenticated")

def send(sd, dst, msg_type, content=None):
    """ a simple send function that incorporates loging"""
    data = {"type":msg_type, "content":content}
    sd.sendto(json.dumps(data).encode('utf-8'), dst)
    log("sent to {}: {}".format(dst, data))

def read(sd):
    """ 
    a function that reads from the given socket, logs the data and 
    returns a message object and a tuple representing the sender
    """
    data, sender = sd.recvfrom(1024)
    msg = json.loads(data.decode('utf-8'))

    log("received from {}: {}".format(sender, msg))
    return msg, sender

def log(message):
    """ for convenient reporting of app status"""
    print("[{}] {}".format(settings['mode'].upper(), message))


if __name__ == '__main__':
    startUp()