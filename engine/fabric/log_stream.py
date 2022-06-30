import sqlite3
import logging
from inspect import getmembers
from pprint import pprint, pformat

DEFAULT_SEPARATOR = '|'
DEFAULT_DATA_TYPE = 'TEXT'

#WARNING: attributes must be choosen from https://docs.python.org/3/library/logging.html#formatter-objects
DEFAULT_ATTRIBUTES_LIST = ['timestamp', 'levelname', 'name', 'message']


class LogStream(logging.Handler):
    '''
    Logging handler for SQLite
    Based on Yarin Kessler's sqlite_handler.py https://gist.github.com/ykessler/2662203#file_sqlite_handler.py
    '''

    def __init__(self, database, table, attributes_list):
        '''
        SQLiteLogHandler class constructor
        Parameters:
            self: instance of the class
            database: database
            table: log table name
            attributes_list: log table columns
        Returns:
            None
        '''

        super().__init__() # for python 3.X
        self.database = database
        self.table = table
        self.attributes = attributes_list

        # Create log table if needed
        create_table_sql = 'CREATE TABLE IF NOT EXISTS ' + self.table \
            + ' (' + ((' ' + DEFAULT_DATA_TYPE + ', ').join(self.attributes)) \
            + ' ' + DEFAULT_DATA_TYPE + ');'

        # print(create_table_sql)
        conn = sqlite3.connect(self.database)
        conn.execute(create_table_sql)
        conn.commit()
        conn.close()


    def emit(self, record):
        '''
        Save the log record
        Parameters:
            self: instance of the class
            record: log record to be saved
        Returns:
            None
        '''
        # Use default formatting if no formatter is set
        self.format(record)

        # print(f'Incoming record: {pformat(record.__dict__)}\n')
        # print(f'Class attributes: {pformat(self.attributes)}\n')
        # KeyError: 'timestamp'
        # Class attributes: ['timestamp', 'levelname', 'message']
        insert_sql = f'INSERT INTO log (timestamp, levelname, message) \
            VALUES ("{record.asctime}", "{record.levelname}", "{record.message}");'

        # print(insert_sql)

        conn = sqlite3.connect(self.database)
        conn.execute(insert_sql)
        conn.commit()
        conn.close()
