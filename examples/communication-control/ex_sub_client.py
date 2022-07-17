'''
Subscriber Client
    Opens a publishing (PUB) port and sends it 'commands' that can be remotely subscribed
    
    Connects and listens to a local 'temperature measurement' (SUB) port as a subscriber.  Logs received data.
    
    Measurements are not queued, and are discarded if no subscriber is listening, so subscriber cannot obtain past data.
    
    A publishing server program (ex_pub_server) serves this client.
'''

import sys
import zmq
import time
from inputimeout import inputimeout, TimeoutOccurred

port_result = "5556"
port_cmd = "5554"

if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

XCMD = True
# XCMD = False

XDATA = True

context = zmq.Context()

if (XCMD):  # Publisher
    # Socket to send commands via
    sock_cmd_send = context.socket(zmq.PUB)
    print(f"Sending commands to server on port {port_cmd}...")
    sock_cmd_send.bind ("tcp://*:%s" % port_cmd)
    # sock_cmd_send.bind ("tcp://localhost:%s" % port_cmd) # didn't work

if (XDATA):  # Subscriber
    # Socket to listen to server results
    sock_result_listen = context.socket(zmq.SUB)
    print(f"Collecting updates from weather server on port {port_result}...")
    sock_result_listen.connect ("tcp://localhost:%s" % port_result)
    
    # Subscribe to zipcode, default is NYC, 10001
    topicfilter = bytes("10001","utf-8")  # alt form: b"10001"
    sock_result_listen.setsockopt(zmq.SUBSCRIBE, topicfilter)

for update_nbr in range (50):
    if (XDATA):
        try:
            string = sock_result_listen.recv(flags=zmq.NOBLOCK)
            topic, messagedata = string.split()
            print(f"{topic} {messagedata}")
        except zmq.Again as e:
            print("No weather report yet")
            
    if (XCMD):
        # Scan for keyboard command, send to server    
        try:
            cmd = inputimeout(prompt='cmd: ', timeout=3)
        except TimeoutOccurred:
            cmd = 'absent'
        print(f"Input command was {cmd}")
        # if (cmd != "absent"): 
        msg = bytes(cmd,'utf-8')
        msg = f"CMD {cmd}".encode('utf-8')
        print(f"Sending command {msg}")
        sock_cmd_send.send(msg)

    time.sleep(3)
