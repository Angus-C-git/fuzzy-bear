import subprocess
from .coverage.ptfuzz.ptrace.ptrace import pokedata, set_registers, trace_me, attach, detach, continue_exc, getpid, SIG_TRAP, get_registers, Registers_x86
from .coverage.ptfuzz.ptfuzz import PtFuzz
from .coverage.Coverage import Coverage


from os import execl, fork, waitpid, WIFSTOPPED, WSTOPSIG, pipe, close, fdopen
from signal import SIGSTOP, SIGCONT

# from psutil import suspend, resume
'''
::::::::::::::::: [Harness] :::::::::::::::::

		► Sends data from the aggregator || or strategy
			handler to the binary
		► Watches/Catches responses from the binary
			and sends them to the aggregator

'''	
def init_trace_target(tracee):
	""" Launch the process to be traced """
	print("[>>] setting up tracee")
	trace_me()

	# replace the forked clone of main process
	# with this process, does not return
	execl(f'./{tracee}', tracee)	


class Harness():
	def __init__(self, binary, codec=None):
		self.binary = binary
		self.codec = codec
			

	def open_pipe(self, data):
		""" open a pipe to target process """
		with subprocess.Popen(
					self.binary,
					stdin  = subprocess.PIPE,
					stdout = subprocess.PIPE,
					stderr = subprocess.PIPE,
					# preexec_fn = trace_me()
		) as pipe:
			
			"""" ptrace operations would theoretically begin here """
			# continue_exc(pipe.pid)

			if self.codec == 'jpeg':
				# send raw bytes
				pipe.communicate(data)
			else:
				# send data as bytes to pipe
				pipe.communicate(data.encode())

			return pipe.returncode
