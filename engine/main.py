from time import sleep
import signal
from fabric.configuration import Configuration
from fabric.logging import Logger
from fabric.system import System
from inspect import getmembers
from pprint import pprint, pformat

noisebin = None

def assemble():
    cfg = Configuration()
    log = Logger(settings={'breakfast': 'eggs'})
    # print(f'cfg contains: {pformat(getmembers(cfg))}')

    if (cfg.args['version']):
        v =f'Version {cfg.code_version}: \'{cfg.scope}\''
        print(v)  # Version, then exit
        log.info(v)
        log.info(' ::::::: Done.')
        exit()

    log.info(' ::::::: Build system code')

    global noisebin     # send to __main__ context var
    noisebin = System() # minimal constructor
    noisebin.build()    # the real work of assembling a system object
                        # Delegates device creation to per-device classes
    noisebin.connect()  # Find a network, Open command socket + queue

    # print(f'cfg contains: {pformat(getmembers(cfg))}')

    # print(f'noisebin contains: {pformat(getmembers(noisebin))}')

def run():
    cfg = Configuration()
    log = Logger()

    global noisebin  # yeah, that one.

    signal.signal(signal.SIGINT, noisebin.signal_handler)  # pull red cord to stop

    run = 1
    if (cfg.args['run_length']):
        run_length = cfg.args['run_length']
    else:
        run_length = 3

    while run != run_length + 1:
        log.debug(f'run cycle {run} of {run_length}')
        log.info(' ::::::: Perform defined measurements')
        noisebin.measure_all()

        log.info(' ::::::: Analyse and plan')
        noisebin.plan

        log.info(' ::::::: Perform specified actions')
        noisebin.actions
        sleep(0.5)
        run += 1

    log.info(' ::::::: Shut down')


if __name__ == "__main__":

    # print('Zero', flush=True)
    assemble()

    run()

    exit()
