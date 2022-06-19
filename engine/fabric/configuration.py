import argparse
import json
from fabric.logging import Logger 

class Configuration(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = cfg = super(Configuration, cls).__new__(cls)
            
            # Buffer log messages - we don't have a logger yet.
            buffer = []
            buffer.append(f'backlog: Created Configuration singleton ID {id(cfg)}')

            parser = argparse.ArgumentParser()

            parser.add_argument("-s", "--silent",      help="Disable sound output",     action="store_true")
            parser.add_argument("-l", "--log_console", help="Enable logging to stdout", action="store_true")
            parser.add_argument("-c", "--config",      help="Specify a configuration file", type=int)

            args = parser.parse_args()
            
            interactive_console = False
            if (args.log_console):
                setattr(cls._instance,'params',{'console' : True})
                interactive_console = True
                buffer.append("backlog: log_console arg specified, enabling log messages to stdout")
            
            # print(f'Console flag: {interactive_console}')
            log = Logger({ 'console': interactive_console })
            for msg in buffer:
                log.debug(msg)

            config_fn="config.json"    # default
            if (args.config):          # unless a different file has been specified
                try:
                    with open(args.config) as fhandle:
                        config_fn = args.config
                        fhandle.close()

                except IOError as err:
                    print(f"Error reading the file {0}: {1}",args.config, err)
                    exit

            try:
                with open(config_fn, "r") as fhandle:
                    props = json.load(fhandle)
                    for p in props:
                        setattr(cls._instance,p,props.get(p))
                        
            except IOError as err:
                print(f"Error reading the file {0}: {1}",config_fn, err)
                exit
            
            log.debug(f"Loaded configuration from {config_fn}")
        return cls._instance
