from fabric.logging import Logger
from fabric.data_entity import DataEntity
import sqlite3

from pprint import pprint, pformat

ATTRIBUTES={'timestamp': 'TIMESTAMP', 'device_type': 'TEXT', 'name': 'TEXT', 'metric': 'TEXT', 'value': 'INTEGER'}

class Metric():
    '''
    Metric helpers - calculate, observe, derive and store metrics
    '''
    node = None
    name = None
    how = None

    def __init__(self, node):
        '''
        Parameters:
            node:    ref to input device, or a dict containing name: slot
            (?) how:     function that observes/calculates the metric

        '''
        log = Logger()

        # log.debug(f'Metric args received: {node["name"]}: {pformat(node)}')
        self.node = node
        self.name = node['name']


    def store(self):
        '''Store a dict of metrics attached to the device node as individual SQLite records'''
        log = Logger()

        # log.debug(f'Storing {self.name}.metric: {pformat(self.node.metric)}')

        try:
            metric_stream = DataEntity(
                table='metric',
                attributes=ATTRIBUTES
                )
        except sqlite3.Warning as msg:
            log.warn(f'Error creating event stream. {msg}')
            return  # we should complain, one feels TODO

        n = self.node
        mset = self.node.metric
        if (len(mset)):
            conn = sqlite3.connect(metric_stream.database)
            for m in mset.keys():
                query = f"INSERT INTO {metric_stream.table} (timestamp, device_type, name, metric, value) \
                            VALUES ('{n.sampled_at}', '{n.device_type}', '{n.name}', '{m}', '{mset[m]}' )"
                # log.debug(f'Storing metric.{m} with {query}')

                cursor = conn.execute(query)
                conn.commit()
            conn.close()
