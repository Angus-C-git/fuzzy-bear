from datetime import datetime
'''
Logging and statistics collector for 
fuzzybear.

'''

class Logger:
    def __init__(self, starting_events=None):
        self.start_time = datetime.now()
        self.initial_events = [
            'starting fuzzer'
        ]

        if starting_events is not None:
            for event in starting_events:
                self.initial_events.append(event)
        
        self.statistics = {
            'hangs': 0,
            'infinite loops': 0,
            'explored code paths': 0,
            'coverage': 0,
            'aborts': 0
        }

    def register_event(self, event):
        self.last_event = event
    

    def signal(self, signal):
        try:
            self.statistics[signal] += 1
        except KeyError:
            print(f"{'':3}[>>] Stat not registered")
            return None

