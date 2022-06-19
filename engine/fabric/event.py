# from inspect import getmembers
from pprint import pprint, pformat

class Event():
    '''
    Event helpers
    '''  

    def __init__(self, e):
        '''
        Parameters expected:
            {
                e['timestamp']    # timestamp, provided by the caller for accuracy
                e['device_type']  # device class
                e['name']         # user-friendly device name
                e['pin']          # GPIO pin used
                e['state']        # new status
            }

        '''

        # print(f'Event args: {pformat(e)}')
        # self.name = e['name']
        for k, v in e.items():
            if (k == 'gpio'): k = 'pin'
            setattr(self,k,v)

    # def __str__(self):
    #     return f"{self.name} is {self.age} years old"