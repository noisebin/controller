from fabric.logging import Logger
from fabric.data_entity import DataEntity
import sqlite3

from pprint import pprint, pformat

ATTRIBUTES={'timestamp': 'TIMESTAMP', 'device_type': 'TEXT', 'name': 'TEXT', 'pin': 'TEXT', 'state': 'INTEGER'}


class Event():
    '''
    Event helpers

    Supports:
        EventStream class
    '''

    def __init__(self, device_name, e):
        '''
        Parameters expected:
            {
                e['timestamp']    # timestamp, provided by the caller for accuracy
                e['device_type']  # device class
                e['name']         # user-friendly device name
                e['pin']          # GPIO pin used
                e['state']        # new status
            }
            Some rearrangement may be necessary to achieve this.
        '''
        self.log = Logger()
        log.debug(f'Event args being marshalled: {device_name}: {pformat(e)}')
        self.name = device_name
        for k, v in e.items():
            if (k == 'gpio'): k = 'pin'
            if (k == 'sampled_at'): k = 'timestamp'
            if (k == 'value'): k = 'state'
            setattr(self,k,v)

    def store(self):
        self.log.debug(f'Storing switch event: {pformat(vars(self))}')

        try:
            event_stream = DataEntity(
                table='event',
                attributes=ATTRIBUTES
                )
        except sqlite3.Warning as msg:
            self.log.warn(f'Error creating event stream. {msg}')
            return  # we should complain, one feels TODO

        event_stream.store(vars(self))
