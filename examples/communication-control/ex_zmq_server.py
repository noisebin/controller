'''
ZeroMQ SERVER demo
    Status: Working

'''

import zmq
import random
import sys
import time

port = "5554"

if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

# ctx = zmq.Context()

ctx = zmq.Context.instance()
url = 'tcp://127.0.0.1:5554'
# client must succeed on first connect, so using an explicit interface
# server.bind("tcp://*:%s" % port) # not cool, man

server = ctx.socket(zmq.SERVER)
server.bind(url)
print('Socket bound.')

for i in range(10):
    print(f'Listening {i}...')
    server.setsockopt(zmq.RCVTIMEO, 3000)
    try:
        msg = server.recv(copy=False)
        print(f'server recvd {msg.bytes!r} from {msg.routing_id!r}')
        rnd = random.randrange(1,20) + 15
        server.send_string(f'reply {i}: {rnd}', routing_id=msg.routing_id)
    except zmq.error.Again as _e:
        pass

    time.sleep(0.1)

server.close()
ctx.term()
