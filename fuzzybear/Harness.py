import subprocess
from .coverage.ptfuzz.ptfuzz import PtFuzz
from .coverage.Coverage import Coverage

'''
::::::::::::::::: [Harness] :::::::::::::::::

	► Sends data from the aggregator || or strategy
		handler to the binary
	► Watches/Catches responses from the binary
		and sends them to the aggregator

'''		


class Harness():
	def __init__(self, binary, logger=None, raw=False):
		self.binary = binary
		self.raw = raw
		self.logger = logger
			

	def open_pipe(self, data):
		""" open a pipe to target process """
		with subprocess.Popen(
					self.binary,
					stdin  = subprocess.PIPE,
					stdout = subprocess.PIPE,
					stderr = subprocess.PIPE,
		) as pipe:

			if self.raw:
				# send raw bytes
				pipe.communicate(data)
			else:
				# send data as bytes to pipe
				pipe.communicate(data.encode())

			res = pipe.wait(timeout=0.5)
			if ((res is None) or res == 3 or (res < 0 and res != -11)):
				self.health_check(pipe)
			
			return pipe.returncode


	def health_check(self, pipe):
		print(f"[>>] Calling health check for {pipe.pid}")
		alive = pipe.poll() 
		if (alive is not None):
			# process has halted
			self.logger.signal('aborts')
		else:
			self.logger.signal('hangs')