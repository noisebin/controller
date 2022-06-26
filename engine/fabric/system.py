import sys, signal
from fabric.logging import Logger
from fabric.configuration import Configuration
from fabric.device_switch import Switch  # must come first, due to pin factory initialiser
from fabric.device_ultrasonic import Ultrasonic
from fabric.sqlite_events import SQLiteEventStream
from datetime import datetime
from time import sleep
from dotmap import DotMap

from inspect import ismethod, getmembers
from pprint import pprint, pformat

cfg = Configuration()
log = Logger()  # or Logger(cfg.params) if they weren't already injected during main.assemble()

# event_stream = SQLiteEventStream()  # pass database filename from cfg

class System(object):
    _instance = None

    def __new__(cls):
        # Initialise the System singleton object
        if cls._instance is None:
            cls._instance = super(System, cls).__new__(cls)

            log.debug(f'Created System singleton ID {id(log)}')

            setattr(cls._instance,'name',cfg.name)
            setattr(cls._instance,'input',DotMap({}))
            setattr(cls._instance,'control',DotMap({}))
            setattr(cls._instance,'action',DotMap({}))

        return cls._instance

    def signal_handler(self, signal, frame):
        print('\nSignal caught.  Hold on ...')
        sleep(0.3)
        sys.exit(0)         # hands over to the finally: clause

    def build(self):
        log.info(f'Configuring {len(cfg.devices)} devices:')
        for d in cfg.devices:
            if (d['device_type'] == 'switch'):
                n = d['name']
                self.input[n] = DotMap({})
                node = self.input[n]
                s = Switch(d,node) # and embed device in System object
                # log.debug(f'Switch device: {n} ID {id(s)} constructed as {pformat(getmembers(s))}')

                node['name'] = n
                node['device_type'] = d['device_type']
                node['device'] = s
                node['pin'] = d['gpio']
                node['status'] = 'built'
                node['value'] = s.sample
                node['measure'] = s.measure
                node['sampled_at'] = datetime.now()

                log.debug(f'Switch device: {d["name"]} ID {id(s)} constructed as {pformat(node)}')

            elif d['device_type'] == 'ultrasonic':
                n = d['name']
                self.input[n] = DotMap({})
                node = self.input[n]
                s = Ultrasonic(d,node) # and embed device in System object
                # log.debug(f'Switch device: {n} ID {id(s)} constructed as {pformat(getmembers(s))}')

                node['name'] = n
                node['device_type'] = d['device_type']
                node['device'] = s
                node['pin'] = node['trigger_gpio'] = d['trigger_gpio']
                node['echo_gpio'] = d['echo_gpio']
                node['status'] = 'built'
                node['value'] = s.sample
                node['measure'] = s.measure
                node['sampled_at'] = datetime.now()

                log.debug(f'Ultrasonic device: {d["name"]} ID {id(s)} constructed as {pformat(node)}')

    def measure_all(self):
        global cfg, log

        # log.debug(f'Measuring all from: {pformat(self.input)}')
        for nom, inp in self.input.items(): #         for k, v in e.items():
            # d = self.input[nom]
            # log.debug(f'\nInput being measured is {nom}: {pformat(d)}')

            d = self.input[nom].device  # device object
            log.debug(f'Input device {nom} is a: {pformat(d)}')
            if ((d.measure is not None) and ismethod(d.measure)):
                d.measure()
                # log.debug(f'Performed {nom}.measure')
            else:
                log.debug(f'No measure() for {nom}')
            pass

    def plan():
        cfg = Configuration()
        log = Logger(cfg.params)

        pass

    def actions():
        cfg = Configuration()
        log = Logger(cfg.params)

        pass
