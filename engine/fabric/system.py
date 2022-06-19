from fabric.logging import Logger
from fabric.configuration import Configuration 
# from fabric.state import StateMachine  # absorbed into System
from fabric.devices import Switch, Led
from fabric.sqlite_events import SQLiteEventStream
from datetime import datetime
# from copy import   # no longer required?
# from gpiozero import LineSensor  # no longer required?
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
        
    def set(cls,name,value):
        # Is this method useless?
        # print(f'System object has ID {id(cls._instance)} inside')
        # print(f'Passed object has ID {id(cls)} inside')   
        # Same as _instance, i.e. Python injects by default.
        
        # print(f'Handling request to set {name} as {value}')
        pass

    def build(self):
        log.info(f'Configuring {len(cfg.devices)} devices:')
        for d in cfg.devices:
            if (d['device_type'] == 'switch'):
                n = d['name']
                self.input[n] = {}
                node = self.input[n]
                s = Switch(d,node) # and embed device in System object

                # c = DotMap(s.context)  # Not in use?
                node['device_type'] = d['device_type']
                node['pin'] = d['gpio']
                
                node['status'] = 'built'
                node['value'] = s.sample()
                node['sampled_at'] = datetime.now()
                node['driver'] = s.driver
                
                # s.status = node['value']  
                # cunning trick: device object can now update status directly via self.status
                # ---------- weird and fragile ------------
                # replace by giving device object a pointer to itself in System
                
                log.info(f'Switch device: {d["name"]} ID {id(s)} constructed as {pformat(node)}')

                # log.info(f'\n\n\nDriver consists of {pformat(vars(s.driver))}')
                # log.info(f'\n\n\nDriver consists of {pformat(getmembers(s.driver))}')
                s.test()       # animates but doesn't verify yet.  TODO

        # store events into the event queue, and log them.
                    