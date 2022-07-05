# import os
import sys
import logging
from fabric.log_stream import LogStream
from pprint import pformat
from inspect import currentframe, stack
from os.path import basename
import re

# from fabric.configuration import Configuration
# cfg = Configuration()

class Logger(object):
    _instance = None
    _queue = []
    settings = {}

    def __new__(cls, *args, **kwargs):
        # the initial instantiation call carries a hand-carved dict of
        # parameters, as soon as they can be determined from args
        # and the config file.  Subsequent calls bypass everything
        # and return the previously built instance of the object
        
        if cls._instance is None:
            cls._instance = log = logging.getLogger()

            cls.enqueue(f'Logger kwargs: {pformat(kwargs)}')

            current_frame = currentframe()
            caller_frame = current_frame.f_back
            call_stack = stack()
            class_string = str(stack()[1][0].f_locals['cls'])[1:-1]
            caller_line = call_stack[1][0].f_lineno
            s = re.split("\s+", str(caller_frame))
            cls.enqueue(f'Logger caller: {class_string} from {basename(s[4][1:-2])}:{caller_line}')

            if ((kwargs) and (kwargs['settings'])):
                settings = cls.settings = kwargs['settings']
                cls.enqueue(f'Logger assigned settings: {settings}')
            else:
                sys.stderr.write('Unexpected error, exiting.  Log:\n')
                for msg in cls._queue:
                    sys.stderr.write(f'  < {msg}\n')
                sys.exit(f'Logger given no configuration settings.  Aark.')

            # exit()
            # Buffer log messages - until we have this wired up correctly.
            # A real instance would have dangerous side effects like recursion,
            # so we employ class methods + vars to pool messages before the
            # eventual singleton dispatches them.
            cls.enqueue(f'Logging settings: {pformat(settings)}')

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
    def deliver(cls):
        # Deliver defered messages to the log(s)

        # This design has a small potential risk of destroying /
        # mis-ordering messages in a multi-threaded process
        # because .enqueue could be cutting across this?
        # If we encounter a problem, try replacing _queue with a collections.dequeue
        # which is suposedly more efficient and fit-for-purpose

        for msg in cls._queue:
            cls._instance.debug(f'< {msg}')
        _queue = []
