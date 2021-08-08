'''
Handles UI events and feeds data to components.

'''
from .Dashboard import Dashboard, init_layout, coverage_tree


class UiRunner():
    """ stores progress states for components """
    
    def __init__(self):
        return
    
    def register_events(self, events):
        self.events = events
        return Dashboard(events)


    def update_events(self, events):
        # print(f"{'':3}[>>] Updating UI events")
        # print(events)
        self.events = events

    def get_events(self):
        return self.events

