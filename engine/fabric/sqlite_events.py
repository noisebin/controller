import sqlite3
from fabric.logging import Logger
from fabric.configuration import Configuration
from pprint import pprint, pformat

cfg = Configuration()
log = Logger()         # Logger(cfg.params) if they weren't already injected during main.assemble()

DEFAULT_DATA_TYPE = 'TEXT'
DEFAULT_ATTRIBUTES_LIST = ['timestamp', 'device_type', 'name', 'pin', 'state'] 

class SQLiteEventStream():
    '''
    Event stream handler for SQLite
    '''
    event_table = None

    def __init__(self):
        '''
        SQLiteEventStream class constructor
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

        # Create event table if needed.  Should use a singleton because this gets re-used :(
        if (self.event_table is None):
            create_table_sql = 'CREATE TABLE IF NOT EXISTS event (timestamp TIMESTAMP, device_type TEXT, name TEXT, pin TEXT, state INTEGER);'
            # log.debug(f'Create table sql: {create_table_sql}')
            
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
        
        # log.debug(f'event.store: Extracting values from event: {vars(event)}\n')
        
        insert_sql = f'INSERT INTO event (timestamp, device_type, name, pin, state) \
            VALUES ("{event.timestamp}", "{event.device_type}", "{event.name}", "{event.pin}", {event.state});'

        # log.debug(f'event.store SQL: {insert_sql}')
        
        conn = sqlite3.connect(self.database)
        conn.execute(insert_sql)
        conn.commit()
        conn.close()
        