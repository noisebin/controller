import sqlite3
from fabric.logging import Logger
from fabric.configuration import Configuration 
from fabric.state import StateMachine 
# from fabric.devices import Switch, Led
# from gpiozero import LineSensor

# from inspect import getmembers
from pprint import pprint, pformat
# import re

cfg = Configuration()
log = Logger()         # Logger(cfg.params) if they weren't already injected during main.assemble()
state = StateMachine()

DEFAULT_SEPARATOR = '|'
DEFAULT_DATA_TYPE = 'TEXT'

'''    -------- Event Stream Handler --------    '''
# attributes_list = ['asctime', 'levelname', 'message'] 
# formatter = logging.Formatter("%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s","%Y-%m-%d %H:%M:%S")
# sql_handler = SQLiteLogHandler(database = log_database, table = log_table, attributes_list = attributes_list)    

DEFAULT_ATTRIBUTES_LIST = ['timestamp', 'device_type', 'name', 'pin', 'state'] 

class SQLiteEventStream():
    '''
    Event stream handler for SQLite
    '''
    event_table = None

    def __init__(self):
        '''
        SQLiteEventStreamHandler class constructor
        Parameters:
            self: instance of the class
            database: database
            table: event table name
            attributes_list: event table columns
        Returns:
            None
        '''
        
        settings = cfg.params
        if (('database' in settings) and (settings['database'] is not None)):
            self.database = settings['database']
        else:
            self.database = 'noisebin.db'
            
        if (('table' in settings) and (settings['table'] is not None)):
            self.table = settings['event_table']
        else:
            self.table = 'event'
            
        if (('attributes' in settings) and (settings['attributes'] is not None)):
            self.attributes = settings['event_attributes']
        else:
            self.attributes = DEFAULT_ATTRIBUTES_LIST

        # Create event table if needed
        if (self.event_table is None):
            create_table_sql = 'CREATE TABLE IF NOT EXISTS event (timestamp TIMESTAMP, device_type TEXT, name TEXT, pin TEXT, state INTEGER);'
            log.debug(f'Create table sql: {create_table_sql}')
            
            conn = sqlite3.connect(self.database)
            conn.execute(create_table_sql)
            conn.commit()
            conn.close()
            self.event_table = 'created'

    def store(self, event):
        '''
        Store the event
        Parameters:
            self: instance of the class
            event: event to be stored
        Returns:
            None
        '''
        
        # print(f'event.store: Extracting values from event: {vars(event)}\n')
        
        insert_sql = f'INSERT INTO event (timestamp, device_type, name, pin, state) \
            VALUES ("{event.timestamp}", "{event.device_type}", "{event.name}", "{event.pin}", {event.state});'

        log.debug(f'event.store SQL: {insert_sql}')
        # print(f'event.store SQL: {insert_sql}')
        
        conn = sqlite3.connect(self.database)
        conn.execute(insert_sql)
        conn.commit()
        conn.close()
        