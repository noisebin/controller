from fabric.logging import Logger
from fabric.configuration import Configuration 
from fabric.devices import Switch, Led
from fabric.sqlite_events import SQLiteEventStream
from datetime import datetime
from dotmap import DotMap

from inspect import getmembers  # Only used in disabled debugging statement
from pprint import pprint, pformat

cfg = Configuration()
log = Logger()  # or Logger(cfg.params) if they weren't already injected during main.assemble()

event_stream = SQLiteEventStream()  # pass database filename from cfg

class System(object):
    _instance = None

    def __new__(cls):
        # Initialise the System singleton object
        if cls._instance is None:
            cls._instance = super(System, cls).__new__(cls)
            
            log.debug(f'Created System singleton ID {id(log)}')
            
            setattr(cls._instance,'input',DotMap({}))
            setattr(cls._instance,'control',DotMap({}))
            setattr(cls._instance,'action',DotMap({}))

        return cls._instance
        
    def set(self,name,value):
        # Is this method useless?
        
        # print(f'Handling request to set {name} as {value}')
        pass

    def build(self):
        log.info(f'Configuring {len(cfg.devices)} devices:')
        for d in cfg.devices:
            if (d['device_type'] == 'switch'):
                n = d['name']
                self.input[n] = DotMap({})
                node = self.input[n]
                s = Switch(d,node) # and embed device in System object

                node['device_type'] = d['device_type']
                node['pin'] = d['gpio']
                node['status'] = 'built'
                node['value'] = s.sample()
                node['sampled_at'] = datetime.now()
                
                log.debug(f'Switch device: {d["name"]} ID {id(s)} constructed as {pformat(node)}')

                # s.test()       
                # Cannot set inputs that are real pins, only Mock pins.
                # Even with Mocks, this animates and gets the resulting 'state' but does not alert.
                # May be useless, get removed.  TODO

        # store events into the event queue, and log them.
                    