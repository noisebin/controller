'''
device_ultrasonic.py
    Device classes and helpers for ultrasonic distance measuring devices

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
from fabric.data_entity import DataEntity
import sqlite3

ATTRIBUTES={'timestamp': 'TIMESTAMP', 'device_type': 'TEXT', 'name': 'TEXT', 'pin': 'TEXT', 'state': 'INTEGER'}

# Specify preferred pin library sub-resource for gpiozero via environment:
# export GPIOZERO_PIN_FACTORY=lgpio # before program start
from gpiozero import Device, LineSensor, DistanceSensor

from pprint import pprint, pformat
from inspect import getmembers

cfg = Configuration()

log = Logger()  # or Logger(cfg.params) if they weren't already injected during main.assemble()
# log.info(f'Logging is on, console output is: {cfg.params["console"]}')
# print(f'Configuration is: {pformat(cfg.args)}')

# Pin factory initialiser singleton should go here


class Ultrasonic():
   system_node: None
   name: None

   def __init__(self, device, node):
       '''
       Ultrasonic class constructor
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

       d = DistanceSensor(
           device['echo_gpio'],
           device['trigger_gpio'],
           max_distance=device['range'],
           threshold_distance=device['threshold'],
           partial=True
           )
       d.when_in_range = self.sense_on
       d.when_out_of_range = self.sense_off  # weird but docs invert the sense of in_range ?
       node['driver'] = d

       log.debug(f'Driver {self.name} is: {node.driver}')

   def sense_on(self):
       node = self.system_node  # this device, in the System context

       node['sampled_at'] = datetime.now()  # sampled_at not defined
       node['value'] = True
       node['name'] = self.name

       log.debug(f'Event ON  for {pformat(node)}')

       e = Event(self.name, node)

       try:  # this block belongs in event.py ? TODO
           event_stream = DataEntity(
               name='event',
               attributes=ATTRIBUTES
               )
       except sqlite3.Warning as em:
           log.warn(f'Error creating event stream. {em}')
           return  # we should complain, one feels TODO

       event_stream.store(vars(e))

   def sense_off(self):
       node = self.system_node  # this device, in the System context

       node['sampled_at'] = datetime.now()  # sampled_at not defined
       node['value'] = False
       node['name'] = self.name

       log.debug(f'Event OFF for {pformat(node)}')

       e = Event(self.name, node)

       try:
           event_stream = DataEntity(
               name='event',
               attributes=ATTRIBUTES
               )
       except sqlite3.Warning as em:
           log.warn(f'Error creating event stream. {em}')
           return  # we should complain, one feels

       event_stream.store(vars(e))

   # ------------- Not In Use ---------------
   # Switch uses predefined values
   # Ultrasonic relies on in_range / out_of_range + measure()
   def sample(self):
       node = self.system_node  # this device, in the System context

       v = node.driver.value    # gpiozero method, immediate data
       log.info(f'Sample of {node.name} is: {v} metres')

       return v

   def measure(self):
       global cfg, log
       node = self.system_node  # this device, in the System context

       # log.debug(f'Measuring for {node.name} (Distance)')
       v = node.driver.distance    # gpiozero method, immediate data
       log.info(f'Observed {node.name} distance is: {v}')

