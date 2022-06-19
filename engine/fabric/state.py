'''
StateMachine
    Passive singleton that contains the 'current' state of the system
'''
from fabric.logging import Logger
from fabric.configuration import Configuration 
from dotmap import DotMap

cfg = Configuration()  # not used yet
    
class StateMachine(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = state = super(StateMachine, cls).__new__(cls)
            
            # Initialise the State object

            log = Logger()  # or Logger(cfg.params) if they weren't already injected during main.assemble()
            log.info(f'Created StateMachine singleton ID {id(log)}')
            
            s = { 'input': {'leftbutton': False, 'rightbutton': False } }
            state.data = DotMap(s)
            
        return cls._instance
