'''
  example-clock.py

  Creates a thread that gets a character from the keyboard.
      Intention is to stash the character (or eventually token) and
      raise a flag that the other thread can collect / parse / act on

  Appears to ignore 'q' being typed, but is really waiting for a line of input.

  Can break out with CTRL-C * 2

  Propose adopting sshkeyboard:
  https://sshkeyboard.readthedocs.io/en/latest/

'''

import time
import threading
 
data_ready = threading.Event()
kill_flag = threading.Event()
 
def keyboard_poller():
    global key_pressed
    loop = True
 
    while not kill_flag.isSet():
        time.sleep(0.1)
        ch = input("poll: ")
        if ch:
            key_pressed = ch
            data_ready.set()
            
    loop = False
    print("\r  ............. Ping!\r")
 
 
def main():
    curr_millis = time.time() * 1000
    prev_millis = curr_millis
 
    poller = threading.Thread(target=keyboard_poller)
    poller.start()
 
    loop = True
 
    while loop:
        curr_millis = time.time() * 1000
        if (curr_millis - prev_millis) >= 1000:
            print("Another second passed... [",time.ctime(),"]\r\r")
            prev_millis = curr_millis
            # Do some extra stuff here
 
        if data_ready.isSet():
            if key_pressed.lower() == "q":
                kill_flag.set()
                loop = False
            else:
                print("You pressed: " + key_pressed)
            data_ready.clear()
 
 
if __name__ == "__main__":
    print("Started..")
    main()
 
    print("You press q to quit ...")

    exit()
