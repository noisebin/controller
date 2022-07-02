'''
device_switch.py
    Device classes and helpers for switch (& similar) input devices

    Builds from a Configuration spec,
    Loads into a reference address in the running System object
    Can sample input values

'''
import time
from datetime import datetime
from copy import deepcopy
from fabric.logging import Logger
from fabric.configuration import Configuration
from fabric.event import Event
from gpiozero import Device, LineSensor, DistanceSensor

from pprint import pprint, pformat
from inspect import getmembers

cfg = Configuration()

log = Logger()

v = cfg.args['version']  # i.e. going to exit early
if (not v):              # i.e. going to build and run the noisebin system

    # if we're not on a Raspberry Pi, fake it ...
    log.debug("Testing if we need a Mock pin factory")
    try:
        from gpiozero.pins.lgpio import LGPIOFactory
        Device.pin_factory = LGPIOFactory()
    except ImportError:
        log.warn("Backfilling with Mock pin factory")
        from gpiozero.pins.mock import MockFactory
        Device.pin_factory = MockFactory()

    if (Device.pin_factory):
        log.info(f'Pin factory chosen: {Device.pin_factory}')
    else:
        log.warn('No pin factory found. Abandon ship!')
        exit()


class Switch():
    system_node: None
    name: None

    def __init__(self, device, node):
        '''
        Switch class constructor
        Parameters:
            self: instance of the class
            device: (source) device descriptor dict from the resolved global configuration
            node: (destination) reference to operating data structure within the global System object
        Attributes:
            name: human-friendly name of device
            system_node: ref to deep copy of the device driver, plus current state and metadata about same
        Returns:
            itself
        '''

        log.info(f'Building device {device}')

        self.name = device['name']
        self.system_node = node  # this device, in the System context

        p = device['gpio']
        d = LineSensor(p)
        d.when_no_line = self.sense_on
        d.when_line = self.sense_off
        node['driver'] = d

        log.debug(f'Driver {self.name} is: {node.driver}')

    def sense_on(self):
        node = self.system_node  # this device, in the System context

        node['sampled_at'] = datetime.now()  # sampled_at not defined?
        node['value'] = True
        node['name'] = self.name

        log.info(f'Observed event {self.name} ON')

        e = Event(self.name, node)
        # log.debug(f'switch event is: {pformat(getmembers(e))}')

        e.store()

    def sense_off(self):
        node = self.system_node  # this device, in the System context

        node['sampled_at'] = datetime.now()  # sampled_at not defined?
        node['value'] = False
        node['name'] = self.name

        log.info(f'Observed event {self.name} OFF')

        e = Event(self.name, node)
        # log.debug(f'switch event is: {pformat(getmembers(e))}')

        e.store()

    def sample(self):
        node = self.system_node  # this device, in the System context

        v = node.driver.value    # gpiozero method, immediate data
        log.info(f'Sample of {node.name} is: {v}')

        return v

    def measure(self):
        global cfg, log
        node = self.system_node  # this device, in the System context
        ATTRIBUTES_LIST = ['timestamp', 'device_type', 'name', 'metric', 'value']

        log.debug(f'Measures for {node.name} (None)')

class DeviceFail(Exception):
    '''Handle device failures, general case (can be extended)'''
    pass

class Led():

    def __new__(self, device):
       pass
