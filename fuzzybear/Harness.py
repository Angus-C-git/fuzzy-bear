import subprocess
from .coverage.ptfuzz.ptrace.ptrace import trace_me, attach, detach
from .coverage.ptfuzz.ptfuzz import PtFuzz
from .coverage.Coverage import Coverage


from os import execl, fork, waitpid, WIFSTOPPED, WSTOPSIG
'''
::::::::::::::::: [Harness] :::::::::::::::::

		► Sends data from the aggregator || or strategy
			handler to the binary
		► Watches/Catches responses from the binary
			and sends them to the aggregator

'''
def init_trace_target(self):
	""" Launch the process to be traced """
	print("[>>] setting up tracee")
	trace_me()

	# replace the forked clone of main process
	# with this process, does not return
	execl(f'./{self.tracee}', self.tracee)		

class Harness():
	def __init__(self, binary):
		self.binary = binary

	def open_pipe(self, data):
		with subprocess.Popen(
					self.binary,
					stdin  = subprocess.PIPE,
					stdout = subprocess.PIPE,
					stderr = subprocess.PIPE,
					preexec_fn = trace_me()
		) as pipe:
			alive = pipe.poll()
			# Do coverage here
			print(f"[>>] Starting coverage spool up ...")
			print(f"[>>] Poll returned {alive}")
			# print(f"[>>] Attempting attach {pipe.pid}")
			# attach(pipe.pid)
			# print(f"[>>] Attached to {pipe.pid}")
			# print("Waiting ...")
			# status = waitpid(pipe.pid, 0)
			# print(f"[>>] Waitpid returned {status}")
			# detach(pipe.pid)
			
			print(f"[>>] Tracee {pipe.pid}")
			coverage_ops = Coverage(self.binary, pipe.pid)
			call_table = coverage_ops.get_function_calls()
			entry = coverage_ops.entry_point
			exit = coverage_ops.exit_point
			print(f"[>>] Entry/exit points: {hex(entry)}/{hex(exit)}")
			print(call_table)
			coverage_runner = PtFuzz(None, pipe.pid, entry, exit)
			
			coverage_runner.launch_tracee()
			# coverage_runner.init_trace_target()

			# send data as bytes to pipe
			# pipe.communicate(data.encode())
			return pipe.returncode
