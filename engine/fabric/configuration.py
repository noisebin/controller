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

            if (args.output):
                Logger.enqueue("console output option specified, enabling log messages to stdout")

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

            cfg.params['console'] = bool(args.output)  # Overrides config file setting
            # print(f'cfg.params @configuration:66: {pformat(cfg.params)}')
            Logger.enqueue(f'Initialised cfg.params supplied to Logger() is: {pformat(cfg.params)}')
            # print(f'Initialised cfg.params before Logger() is: {pformat(cfg.params)}')

            log = Logger(settings=cfg.params)

            if (args.log_level):  # Overrides config file setting
                log_level = args.log_level
            else:
                log_level = logging.DEBUG      # default
                if ((cfg.params['log_level'] is not None) and (cfg.params['log_level'] in LOGLEVELS)):
                    log_level = cfg.params['log_level']

            Logger.enqueue(f'Configured log level as specified: {log_level}')
            setattr(cls._instance,'log_level',log_level)
            log.setLevel(log_level)

            Logger.enqueue(f"Loaded configuration from {config_fn}")
            Logger.enqueue(f"Initial configuration is: {pformat(vars(cfg))}")

            log.info('------- NoiseBin -------')
            Logger.deliver()

        return cls._instance
