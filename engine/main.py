import time

from fabric.configuration import Configuration 
from fabric.logging import Logger
from fabric.system import System
from inspect import getmembers
from pprint import pprint, pformat

def assemble():
    cfg = Configuration()
    
    log = Logger(cfg.params)

    noisebin = System()
    
    noisebin.build()
    # Delegate device creation to per-device classes

    print(f'noisebin.input: ', end = '')
    noisebin.input.pprint()
    
    # Also create the event, action and command queues
    # and attach them into state ... or 'system' ??
    
def run():
    pass
    
if __name__ == "__main__":

    assemble()
    
    run()
        
    exit()
