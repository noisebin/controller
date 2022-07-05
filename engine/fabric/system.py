import sys, signal
from fabric.logging import Logger
from fabric.configuration import Configuration
from fabric.device_switch import Switch  # must come first, due to pin factory initialiser
from fabric.device_ultrasonic import Ultrasonic

from datetime import datetime
from time import sleep
from dotmap import DotMap

from inspect import ismethod, getmembers
from pprint import pprint, pformat

class System(object):
    _instance = None
    cfg = None
    log = None

    def __new__(cls):
        # Initialise the System singleton object
        if cls._instance is None:
            cls._instance = self = super(System, cls).__new__(cls)

            self.cfg = Configuration()
            self.log = Logger()

            self.log.debug(f'Created System singleton ID {id(self.log)}')

            setattr(cls._instance,'name',self.cfg.name)
            setattr(cls._instance,'input',DotMap({}))
            setattr(cls._instance,'control',DotMap({}))
            setattr(cls._instance,'action',DotMap({}))

        return cls._instance

    def signal_handler(self, signal, frame):
        sys.stderr.write('\nSignal caught.  Hold on ...')
        self.log.debug('Exiting on receipt of signal') # might need a try block TODO
        sleep(0.3)
        sys.exit(0)         # th-th-th-that's all, folks

    def build(self):
        self.log.info(f'Configuring {len(self.cfg.devices)} devices:')
        for d in self.cfg.devices:
            if (d['device_type'] == 'switch'):
                n = d['name']
                self.input[n] = DotMap({})
                node = self.input[n]
                s = Switch(d,node) # and embed device in System object
                # self.log.debug(f'Switch device: {n} ID {id(s)} constructed as {pformat(getmembers(s))}')

                node['name'] = n
                node['device_type'] = d['device_type']
                node['device'] = s
                node['pin'] = d['gpio']
                node['status'] = 'built'
                node['value'] = s.sample()           # set an initial value
                node['sample_fn'] = s.sample         # function to call for future samples
                node['measure_fn'] = s.measure       # function to call for future measurements
                node['metric'] = {}
                node['sampled_at'] = datetime.now()

                self.log.debug(f'Switch device: {d["name"]} ID {id(s)} constructed as {pformat(node)}')

            elif d['device_type'] == 'ultrasonic':
                n = d['name']
                self.input[n] = DotMap({})
                node = self.input[n]
                s = Ultrasonic(d,node) # and embed device in System object
                # self.log.debug(f'Switch device: {n} ID {id(s)} constructed as {pformat(getmembers(s))}')

                node['name'] = n
                node['device_type'] = d['device_type']
                node['device'] = s
                node['pin'] = node['trigger_gpio'] = d['trigger_gpio']
                node['echo_gpio'] = d['echo_gpio']
                node['status'] = 'built'

                # node['value'] = s.sample()  # an initial value, although it's never updated?
                IN_RANGE = True ; OUT_OF_RANGE = False
                if (s.sample() > s.threshold):
                    node['value'] = OUT_OF_RANGE
                else:
                    else node['value'] = IN_RANGE

                node['sample_fn'] = s.sample
                node['measure_fn'] = s.measure
                node['metric'] = {}
                node['sampled_at'] = datetime.now()

                self.log.debug(f'Ultrasonic device: {d["name"]} ID {id(s)} constructed as {pformat(node)}')

    def measure_all(self):
        # self.log.debug(f'Measuring all from: {pformat(self.input)}')
        for nom, inp in self.input.items(): #         for k, v in e.items():

            d = self.input[nom].device  # device object
            self.log.debug(f'Input device {nom} is a sampler and a: {pformat(d)}')
            if ((d.measure is not None) and ismethod(d.measure)):
                d.measure()
                # self.log.debug(f'Conducted {nom}.measure')
            else:
                self.log.debug(f'No measure() for {nom}')
            pass

    def plan():
        pass

    def actions():
        pass
