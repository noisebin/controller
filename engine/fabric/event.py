from pprint import pprint, pformat

class Event():
    '''
    Event helpers

    Supports:
        EventStream class
    '''

    def __init__(self, device_name, e):
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

        print(f'Event args being marshalled: {device_name}: {pformat(e)}')
        self.name = device_name
        for k, v in e.items():
            if (k == 'gpio'): k = 'pin'
            if (k == 'sampled_at'): k = 'timestamp'
            if (k == 'value'): k = 'state'
            setattr(self,k,v)
