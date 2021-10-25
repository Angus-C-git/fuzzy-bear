from datetime import datetime
from time import time, sleep

from rich.text import Text
from rich.console import Console, RenderGroup, render_group
from rich import print

console = Console()


'''
::::::::::::::::: [UI:Logs] :::::::::::::::::

	► Custom logging render for the logs
      system Dashboard component
'''

# - CONFIG - #

# Number of logs to render
# at a given time
MAX_RECENT_LOGS = 8


class Logs():

    logs = []

    def __init__(self):
        self.start_time = time()

    # TODO :: TMP METHOD, handled in logging.py

    def get_time(self):
        """
        Return the time the log was 
        emitted 
        """
        current_runtime = time() - self.start_time
        mins = int(current_runtime // 60)
        secs = int(current_runtime % 60)
        hours = int(mins // 60)
        return f'{hours}:{mins:02d}:{secs:02d}'

    def add_startup_log(self, log):

        self.logs.append(
            f'[b green][{self.get_time()}][/b green] {log}'
        )

        if len(self.logs) > MAX_RECENT_LOGS:
            # pop the oldest log
            self.logs.pop(0)

    def add_event_log(self, event_log):
        if len(self.logs) > MAX_RECENT_LOGS:
            # pop the oldest log
            self.logs.pop(0)

        self.logs.append(event_log)

    def add_debug_log(self, debug_log):
        pass

    def add_error_log(self, error_log):
        pass

    @render_group()
    def construct_renderable(self):
        """ 
        Build a render group of
        the most recent logs to display 
        on the logs panel
        """
        for log in self.logs:
            # log_group.update(log)
            yield log


'''devnotes

- NOTE - 

+ Want logs to have a format similar to the following

[0:00] Running Fuzzer against <json1>, input corpus <json1.txt>

+ Potentially have a few defined log formats for example:
      + startup log - take in target and corups
      + event log - take in event type and message
      + error log - take in error type and message
      + debug log - take in debug message

+ Each log type will have associated colour

+ Since the UI is re-rendered on each update will need
  to be able to support a system which maintains a list
  of the last x logs (that fit on the UI) and be able
  to return a renderable of those logs
'''
