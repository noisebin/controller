'''
loop.py

  Read keypresses (and releases) in non-blocking manner.
  Plan: extend this to capture a full command line, similar to readline
'''

from pynput import keyboard
import time

runstate = True

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))

    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    global runstate
    
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        runstate = False
        # Stop listener
        return False

def main():
    
    # Collect events until released ... in a non-blocking fashion:
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

if __name__ == "__main__":
    print("Started main ...")
    main()
 
    while runstate:
        time.sleep(3)                              #  Delay of n seconds
        print("[",time.ctime(),"]\r")
        
    print("Bailing out ...")
    exit()