import time

from fabric.configuration import Configuration 
from fabric.logging import Logger
# from fabric.state import StateMachine  # absorbed into System
from fabric.system import System
# from dotmap import DotMap
from inspect import getmembers
from pprint import pprint, pformat

def assemble():
    cfg = Configuration()
    
    log = Logger(cfg.params)

    # state = StateMachine()  # absorbed into System
    
    noisebin = System()
    
    # historical: verify singleton IDs
    # log.info(f'Creating State object {s.description} of ID {id(s)}')
    # print(f'System object has ID {id(noisebin)} outside')
    
    noisebin.build()
    # Delegate device creation to per-device classes

    # print('Noisebin:')
    # pprint(getmembers(noisebin))
    # pprint(f'Noisebin: {vars(noisebin)} --')
    print
    
    print(f'noisebin.input: ', end = '')
    noisebin.input.pprint()
    # {'context': {'device_type': 'switch',
    #              'gpio': 6,
    #              'name': 'leftbutton',
    #              'state': True,
    #              'timestamp': datetime.datetime(2022, 6, 13, 22, 20, 12, 633274)},
    #  'driver': <gpiozero.LineSensor object on pin GPIO6, pull_up=False, is_active=True>}
    
    # print
    # pprint(f'State: {vars(state)}')
    
    # Also create the event, action and command queues
    # and attach them into state ... or 'system' ??
    
def run():
    pass
    
if __name__ == "__main__":

    assemble()
    
    run()
        
    exit()
