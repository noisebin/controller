import sys
import argparse
import json
import logging
from fabric.logging import Logger

from inspect import getmembers
from pprint import pformat

LOGLEVELS = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']


class Configuration(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = cfg = super(Configuration, cls).__new__(cls)

            # Buffer log messages - we don't have a logger yet.
            Logger.enqueue(f'Created Configuration singleton ID {id(cfg)}')

            Logger.enqueue(f'Command line args: {pformat(sys.argv)}')

            parser = argparse.ArgumentParser()

            parser.add_argument("-c", "--config",    help="Specify a configuration file") # , type=int)
            parser.add_argument("-l", "--log-level", help="Enable logging to console",    choices=LOGLEVELS)
            parser.add_argument("-o", "--output",    help="Enable console output",        action="store_true")
            parser.add_argument("-r", "--run-length",help="Run length count (default=3)", type=int)
            parser.add_argument("-s", "--silent",    help="Disable sound output",         action="store_true")
            parser.add_argument("-v", "--version",   help="Display version information",  action="store_true")

            args = parser.parse_args()
            setattr(cls._instance,'args',vars(args))

            interactive_console = False

            if (args.output):
                setattr(cls._instance,'params',{'console' : True})
                interactive_console = True
                Logger.enqueue("console output option specified, enabling log messages to stdout")

            # print(f'Console flag: {interactive_console}')

            config_fn="config.json"    # default
            if (args.config):          # unless a different file has been specified
                try:
                    with open(args.config) as fhandle:
                        config_fn = args.config
                        fhandle.close()

                except IOError as err:
                    sys.exit(f"Error reading the file {0}: {1}",args.config, err)

            try:
                with open(config_fn, "r") as fhandle:
                    props = json.load(fhandle)
                    for p in props:
                        setattr(cls._instance,p,props.get(p))

            except IOError as err:
                sys.exit(f"Error reading the file {0}: {1}",config_fn, err)

            Logger.enqueue(f'Initialised cfg.params before Logger() is: {pformat(cfg.params)}')

            log = Logger(settings=cfg.params)
            # log = Logger({ 'console': interactive_console, 'logfile': cfg.params['logfile'], 'log_level': logging.DEBUG })

            log_level = logging.DEBUG      # default
            if (cfg.params['log_level'] is not None):
                log_level = cfg.params['log_level']
                Logger.enqueue(f'Configured log level as specified: {log_level}')
                setattr(cls._instance,'log_level',log_level)
                if (log_level in LOGLEVELS):
                    log.setLevel(log_level)

            else:
                Logger.enqueue(f'Configured log level as (default) DEBUG')
                log.setLevel(logging.DEBUG)

            if (args.log_level):
                log.setLevel(args.log_level)

            Logger.enqueue(f"Loaded configuration from {config_fn}")
            Logger.enqueue(f"Initial configuration is: {pformat(vars(cfg))}")
            # Logger.enqueue(f"Initial configuration is: {pformat(cfg.__dict__)}")

            log.info('------- NoiseBin -------')
            Logger.flush()

        return cls._instance
