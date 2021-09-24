import logging

# create logger
module_logger = logging.getLogger('nb.module')

class Useless:
    def __init__(self):
        self.logger = logging.getLogger('nb.module.useless')
        self.logger.info('Creating a Useless object')

    def beep(self):
        self.logger.info('Preparing to beep')
        print('\a')
        self.logger.info('Beeped.')

def bark():
    print('Bark! bark!')
    module_logger.info('Barked.')
