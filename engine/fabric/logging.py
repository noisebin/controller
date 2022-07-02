# import os
import sys
import logging
from fabric.log_stream import LogStream
from pprint import pformat

# from fabric.configuration import Configuration
# cfg = Configuration()

class Logger(object):
    _instance = None
    _queue = []

    def __new__(cls,settings={ 'console': False, 'log_level': logging.DEBUG }):
        if cls._instance is None:
            cls._instance = log = logging.getLogger()

            # Buffer log messages - until we have this wired up correctly
            # print(f'Logging settings: {pformat(settings)}')
            cls.enqueue(f'Logging settings: {pformat(settings)}')
            cls.enqueue(f'... and a merry christmas to all')

            if (('log_level' in settings) and (settings['log_level'] is not None)):
                log_level = settings['log_level']
            else:
                log_level = logging.DEBUG

            if (('database' in settings) and (settings['database'] is not None)):
                log_database = settings['database']
            else:
                log_database = 'noisebin.db'

            if (('table' in settings) and (settings['table'] is not None)):
                log_table = settings['event_table']
            else:
                log_table = 'log'

            attributes_list = ['timestamp', 'levelname', 'message']
            formatter = logging.Formatter("%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s",
                                      "%Y-%m-%d %H:%M:%S")

            sql_handler = LogStream(database=log_database, table=log_table, attributes=attributes_list)
            sql_handler.setLevel(log_level)
            sql_handler.setFormatter(formatter)

            # create file handler which logs all the way down to debug messages
            if (('logfile' in settings) and (settings['logfile'] is not None)):
                logfile = settings['logfile']
            else:
                logfile = 'noisebin.log'

            fh = logging.FileHandler(logfile)
            fh.setLevel(log_level)

            # create console handler with a higher log level
            if (('console' in settings) and (settings['console'] is True)):
                ch = logging.StreamHandler(sys.stdout)
                ch.setLevel(log_level)

            # add formatter to the file and console handlers
            fh.setFormatter(formatter)
            if (settings['console']): ch.setFormatter(formatter)

            # add the handlers to the logger
            log.addHandler(fh)
            if (settings['console']):
                log.addHandler(ch)
            log.addHandler(sql_handler)

            # it'd be nice to override the formatter to omit %(module)s.%(funcName)s and make this more prominent in the log TODO

            cls.enqueue(f'Created Logger singleton ID {id(log)}')

        return cls._instance


    @classmethod
    def enqueue(cls, message):
        # Defer messages in situations where we are not ready to log them

        cls._queue.append(message)


    @classmethod
    def flush(cls):
        # Deliver defered messages to the log(s)

        # This design has a small potential risk of destroying /
        # mis-ordering messages in a multi-threaded process
        # because .enqueue could be cutting across this?
        # If we encounter a problem, try replacing _queue with a collections.dequeue
        # which is suposedly more efficient and fit-for-purpose

        # print(f'Hit Logger.flush, queue looks like: {pformat(cls._queue)}')

        for msg in cls._queue:
            cls._instance.debug(f'< {msg}')
        _queue = []
