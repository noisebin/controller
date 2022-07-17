'''
ZeroMQ CLIENT demo
    Request data from server with a timeout
    Timeout causes program to exit
'''

import sys
import zmq
import time
# from inputimeout import inputimeout, TimeoutOccurred

port = "5554"

if len(sys.argv) > 1:
    client_id =  sys.argv[1]

url = 'tcp://127.0.0.1:5554'
# client must succeed on first connect, so using an explicit interface
# client.connect("tcp://*:%s" % port)  # not cool, man

context = zmq.Context()

client = context.socket(zmq.CLIENT)
print(f"Client {client_id} sending commands to server on port {port}...")
client.connect(url)
client.setsockopt(zmq.SNDTIMEO, 300)
client.setsockopt(zmq.RCVTIMEO, 300)

for i in range (6):
    print(f'Client {client_id} sending request {i} ...')
    client.send(b'request %i' % i)
    try:
        reply = client.recv_string()
        print(f'Client {client_id} received {reply}')
    except zmq.error.Again as _e:
        print(f'Client {client_id} timeout waiting for reply')
        break  # exit the for loop
    time.sleep(0.2)

client.close()
context.term()
