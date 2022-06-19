import os
import sys
import logging
from fabric.sqlite_logs import SQLiteLogger

# from fabric.configuration import Configuration 
# cfg = Configuration()

class Logger(object):
    _instance = None
    def __new__(cls,settings={ 'console' : False }):
        if cls._instance is None:
            cls._instance = log = logging.getLogger('nb')
                        
            log.setLevel(logging.DEBUG)

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
            
            sql_handler = SQLiteLogger(database = log_database, table = log_table, attributes_list = attributes_list)
            sql_handler.setLevel(logging.INFO)
            sql_handler.setFormatter(formatter)

            # create file handler which logs all the way down to debug messages
            if (('logfile' in settings) and (settings['logfile'] is not None)):
                logfile = settings['logfile']
            else:
                logfile = 'noisebin.log'
                            
            fh = logging.FileHandler(logfile)
            fh.setLevel(logging.DEBUG)

            # create console handler with a higher log level
            if (('console' in settings) and (settings['console'] is True)):
                ch = logging.StreamHandler(sys.stdout)
                ch.setLevel(logging.INFO)

            # add formatter to the file and console handlers
            fh.setFormatter(formatter)
            if (settings['console']): ch.setFormatter(formatter)

            # add the handlers to the logger
            log.addHandler(fh)
            log.addHandler(sql_handler)
            if (settings['console']): 
                log.addHandler(ch)

            log.info(f'-------- NoiseBin --------')    
            # it'd be nice to override the formatter to omit %(module)s.%(funcName)s and make this more prominent in the log TODO
            
            log.debug(f'Created Logger singleton ID {id(log)}')

        return cls._instance
