'''
devices.py
    Device classes and helpers for input & output devices
    
    Makes use of a supplied device descriptor dict of the form:
        {
            "device_type": "switch",
            "name": "leftbutton",
            "gpio": 6
        }
    We attach the descriptor ref to each instance as descriptive context.
    
'''
import time
from datetime import datetime
from copy import deepcopy
from fabric.logging import Logger
from fabric.configuration import Configuration 
from fabric.state import StateMachine   # Useful for self-validating under text()
from fabric.event import Event
from gpiozero import Device, LineSensor
from fabric.sqlite_events import SQLiteEventStream

# from inspect import getmembers
from pprint import pprint, pformat

cfg = Configuration()

log = Logger()  # or Logger(cfg.params) if they weren't already injected during main.assemble()
# log.info(f'Logging is on, console output is: {cfg.params["console"]}')
                
if (Device.pin_factory):
    log.info(f'Pin factory chosen: {Device.pin_factory}')
else:
    log.warn("Backfilling with Mock pin factory")
    from gpiozero.pins.mock import MockFactory
    Device.pin_factory = MockFactory()

class Switch():
    
    def __init__(self, device):
        '''
        Switch class constructor
        Parameters:
            self: instance of the class
            device: device descriptor dict - see above
        Attributes:
            context: deep copy of the device descriptor
        Returns:
            None
        '''

        log.info(f'Building device {device}')
        self.context = deepcopy(device)
        # log.info(f'Context is: {cls.context}')  # announced in system.build()

        p = device['gpio']
        d = LineSensor(p)
        log.debug(f'Switch driver is: {d}')
        d.when_no_line = self.sense_on
        d.when_line = self.sense_off

        self.driver = d
        # self.test()    # Currently called by system.build
        log.info(f'Driver {device["name"]} is: {self.driver}')
        # log.info(f'Driver consists of {pformat(getmembers(self.driver))}')

    def sense_on(self):
        log.info(f'{self.driver._pin} is ON')
        # log.info(f'{self.context["gpio"]} is ON')
        log.debug(f'Event ON  for {pformat(self.context)}') 

        self.status = True
        self.context['timestamp'] = datetime.now()
        self.context['state'] = True  # WHY is this being used for the SQLite event logging?
        
        c = self.context        
        # print(f'Calling context for event: {pformat(c)} <<\n')
                
        e = Event(c)
        event_stream = SQLiteEventStream()
        event_stream.store(e)

    def sense_off(self):
        log.info(f'{self.driver._pin} is OFF')
        # log.info(f'{self.context["gpio"]} is OFF')
        log.debug(f'Event OFF for {pformat(self.context)}')

        self.status = False
        self.context['timestamp'] = datetime.now()
        self.context['state'] = False  # WHY is this being used for the SQLite event logging?
        c = self.context
        # print(f'Calling context for event: {pformat(c)} <<\n')
        
        e = Event(c)
        event_stream = SQLiteEventStream()
        event_stream.store(e)
        
    def sample(self):
        v = self.driver.value
        log.info(f'Sample of {self.context["name"]} is: {v}')
        
        return v        
            
    def test(self):
        # animates the pin, but doesn't alert on failures TODO

        n = self.context["name"]
        log.debug(f'Setting {n} high')
        self.driver.pin.drive_high()
        time.sleep(0.2)
        log.info(f'{n} is now {self.status}')
        log.debug(f'Setting {n} low')
        self.driver.pin.drive_low()
        time.sleep(0.2)
        log.info(f'{n} is now {self.status}')        
        log.debug(f'Setting {n} high')
        self.driver.pin.drive_high()
        time.sleep(0.2)
        log.info(f'{n} is now {self.status}')
        
class Led():
    
    def __new__(self, device):
       pass