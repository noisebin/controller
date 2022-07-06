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
from fabric.data_entity import DataEntity
from fabric.logging import Logger
from fabric.configuration import Configuration
from fabric.event import Event
from fabric.metric import Metric
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

   def sample(self):
       node = self.system_node  # this device, in the System context

       # node.driver.value  - attribute we set at creation, threshold crossings
       # driver.value is represented as:
       #   if distance > threshold_distance: result is OUT_OF_RANGE
       #   else result is IN_RANGE

       v = node.driver.value
       if (v): sample_value = 'IN_RANGE'
       else: sample_value = 'OUT_OF_RANGE'

       log.info(f'Sample of {node.name}.value is: {sample_value}')

       return v

   def measure(self):
       node = self.system_node  # this device, in the System context

       # ---- current distance to visitor, if any
       v = node.metric['distance'] = node.driver.distance    # gpiozero method, immediate data
       log.info(f'Metric {node.name}.distance: {v}')

       try:
           ATTRIBUTES={'timestamp': 'TIMESTAMP', 'device_type': 'TEXT', 'name': 'TEXT', 'pin': 'TEXT', 'state': 'INTEGER'}
           event_source = DataEntity(
               table='event',
               attributes=ATTRIBUTES
               )
       except sqlite3.Warning as msg:
           log.warn(f'Error creating event stream. {msg}')
           return  # we should complain, one feels TODO

       # log.debug(f'DataEntity \'event\' is: {pformat(vars(event_source))}')

       interval={}
       # ---- number of events in the last 5 seconds
       interval['t5sec'] = datetime.now() + timedelta(seconds=-5)

       # ---- number of events in the last 60 seconds
       interval['t60sec'] = datetime.now() + timedelta(seconds=-60)

       # ---- number of events in the last 86400 seconds (24 hours)
       interval['t24hours'] = datetime.now() + timedelta(days=-1)

       # ---- number of events in the last 30 days
       interval['t30days'] = datetime.now() + timedelta(days=-30)

       for t in interval:
           print(f'threshold {t} begins {pformat(interval[t])}')
           query = (f'SELECT count(*) AS \'{t}\' FROM event WHERE device_type = \'{self.system_node.device_type}\' \
                    AND name = \'{self.system_node.name}\' AND timestamp > \'{interval[t]}\'')
           # log.debug(query)
           result = event_source.query(query)
           # log.debug(f'Event query result: {pformat(result)}')

           if (result):
               count=result[0][0]
               node.metric[t] = count
               log.info(f'Metric {node.name}.{t}: {count}')
           else:
               log.debug(f'Query for metric {node.name}.{t} produced no result')

       node['sampled_at'] = datetime.now()
       
       # try:
       metric_data = Metric(self.system_node)
       # except sqlite3.Warning as msg:
       #     log.warn(f'Error creating event stream. {msg}')
       #     return  # we should complain, one feels TODO

       metric_data.store()
