import logging
import sys
import nb_module

# create logger named 'nb'
logger = logging.getLogger('nb')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('../nb.log')
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s %(name)s.%(levelname)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('Starting up')

barker = nb_module.Useless()

barker.beep()
nb_module.bark()

logger.error('Fed up. Exiting.')
