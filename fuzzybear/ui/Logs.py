from datetime import datetime

from rich.console import Console, RenderGroup
from rich.console import group


'''
::::::::::::::::: [UI:Logs] :::::::::::::::::

	► Custom logging render for the logs
      system Dashboard component
'''

# - CONFIG - #

# Number of logs to render
# at a given time
MAX_RECENT_LOGS = 5


class Logs():
	
	logs = []

	def __init__(self, starting_log):
		self.logs.append(starting_log)

	
	def add_log(self, log):
		self.logs.append(log)
		if len(self.logs) > MAX_RECENT_LOGS:
			# pop the oldest log
			self.logs.pop(0)


	def construct_renderable(self):
		# construct the renderable
		pass
			

'''devnotes

- NOTE - 

+ Want logs to have a format similar to the following

[0:00] Running Fuzzer against <json1>, input corpus <json1.txt>

+ Potentially have a few defined log formats for example:
      + startup log - take in target and corups
      + event log - take in event type and message
      + error log - take in error type and message
      + debug log - take in debug message

+ Since the UI is re-rendered on each update will need
  to be able to support a system which maintains a list
  of the last x logs (that fit on the UI) and be able
  to return a renderable of those logs
'''