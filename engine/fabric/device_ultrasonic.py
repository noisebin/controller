'''
device_ultrasonic.py
    Device classes and helpers for ultrasonic distance measuring devices

    Builds from a Configuration spec,
    Loads into a reference address in the running System object
    Can sample input values

'''
import time
from datetime import datetime, timedelta
from copy import deepcopy
from fabric.logging import Logger
from fabric.configuration import Configuration
from fabric.event import Event
from gpiozero import Device, LineSensor, DistanceSensor

from pprint import pprint, pformat
from inspect import getmembers

IN_RANGE = True
OUT_OF_RANGE = False

cfg = Configuration()

log = Logger()


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
       node['value'] = IN_RANGE
       node['name'] = self.name

       log.debug(f'Event IN_RANGE for {pformat(node)}')

       e = Event(node)
       # log.debug(f'switch event is: {pformat(getmembers(e))}')

       e.store()

   def sense_off(self):
       node = self.system_node  # this device, in the System context

       node['sampled_at'] = datetime.now()  # sampled_at not defined
       node['value'] = OUT_OF_RANGE
       node['name'] = self.name

       log.debug(f'Event OUT_OF_RANGE for {pformat(node)}')

       e = Event(node)
       # log.debug(f'switch event is: {pformat(getmembers(e))}')

       e.store()

   # Ultrasonic relies on IN_RANGE / OUT_OF_RANGE + measure()
   def sample(self):
       node = self.system_node  # this device, in the System context

       v = node.driver.value    # gpiozero method, immediate data.
       # Should use IN_RANGE, via
       # driver.distance - in metres; driver.value = 0..1 proportion of max_distance (!)
       # if distance > threshold: result is OUT_OF_RANGE
       # else result is IN_RANGE

       log.info(f'Sample of {node.name} is: {v} metres')

       return v
   # ----------------------------------------

    def measure(self):
        global cfg, log
        node = self.system_node  # this device, in the System context

        # ---- current distance to visitor, if any
        v = node.metric['distance'] = node.driver.distance    # gpiozero method, immediate data
        log.info(f'Measured {node.name} distance is: {v}')

        try:
            ATTRIBUTES={'timestamp': 'TIMESTAMP', 'device_type': 'TEXT', 'name': 'TEXT', 'pin': 'TEXT', 'state': 'INTEGER'}
            event_source = DataEntity(
                table='event',
                attributes=ATTRIBUTES
                )
        except sqlite3.Warning as msg:
            self.log.warn(f'Error creating event stream. {msg}')
            return  # we should complain, one feels TODO

        # ---- number of events in the last 60 seconds
        interval60sec = timedelta(seconds=-60)
        t60sec = datetime.now() + interval60sec

        query = (f'SELECT * FROM event WHERE device_type = \'{self.device_type}\'
                 AND name = \'{self.name}\' WHERE timestamp > \'{t60sec}\'')
        self.log.debug(query)
        # event_source.query('SELECT * FROM event WHERE device_type = \'{self.device_type}\'
