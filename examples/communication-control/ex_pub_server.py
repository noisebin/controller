'''
Publishing Server
Status: Working

    Opens a publishing (PUB) port and generates random 'temperature measurements' that can be remotely subscribed
    
    Connects and listens to a local (SUB) command port as a subscriber.  Logs received commands.
    
    Measurements are not queued, and are discarded if no subscriber is listening.

    A client program (ex_sub_client) operates to complement the server.
'''

import zmq
import random
import sys
import time

port_result = "5556"
port_cmd = "5554"

if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

XCMD = True
# XCMD = False

XDATA = True

context = zmq.Context()

if (XDATA):  # Publisher
    # Socket for publishing temperature results on
    socket_send_result = context.socket(zmq.PUB)
    socket_send_result.bind("tcp://*:%s" % port_result)
    print(f"Sending temperature updates from server on port {port_result}...")

if (XCMD):  # Subscriber
    # Socket for incoming commands
    socket_cmd_listen = context.socket(zmq.SUB)
    print(f"Receiving commands from client on port {port_cmd}...")
    # Doesn't work for SUB(?): socket_cmd_listen.bind ("tcp://*:%s" % port_cmd)
    socket_cmd_listen.connect ("tcp://localhost:%s" % port_cmd)
    topicfilter = bytes("CMD",'utf-8')
    socket_cmd_listen.setsockopt(zmq.SUBSCRIBE, topicfilter)

print("Meditating ...")    
time.sleep(5)

runstate = True
while runstate:
    if (XDATA):
        # topic = random.randrange(9999,10005)
        topic = 10001
        messagedata = random.randrange(1,20) + 15
        msg = f"{topic} {messagedata}".encode('utf-8')
        print("Sending ",msg)
        socket_send_result.send(msg)
    
    if (XCMD):
        cmd = ""
        socks=[]
        print("Peeking at port")
        
        try:
            cmd = socket_cmd_listen.recv(zmq.NOBLOCK)
            params = cmd.decode('utf-8').split()
            inst = params.pop(0)
            print(f"Received {inst} {params} command")  # Received CMD ['exit'] command
            if (params.pop(0) == 'exit'): runstate = False
        except zmq.Again as e:
             print("Nothing happening on cmd port")

    time.sleep(3)

print('Exiting gracefully.')
