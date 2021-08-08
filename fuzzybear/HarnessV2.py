import subprocess
from .coverage.ptfuzz.ptrace.ptrace import pokedata, set_registers, trace_me, attach, detach, continue_exc, getpid, SIG_TRAP, get_registers, Registers_x86
from .coverage.ptfuzz.ptfuzz import PtFuzz
from .coverage.Coverage import Coverage


from os import execl, fork, waitpid, WIFSTOPPED, WSTOPSIG, pipe, close, fdopen
from signal import SIGSTOP, SIGCONT


def init_trace_target(tracee):
	""" Launch the process to be traced """
	print("[>>] setting up tracee")
	trace_me()

	# replace the forked clone of main process
	# with this process, does not return
	execl(f'./{tracee}', tracee)		

class HarnessV2():
	def __init__(self, binary):
		self.binary = binary
		
	def open_pipe(self, data):
		
		# stdout_pipe, stdin_pipe = pipe()
		child_pid = fork()

		print(f"[>>] Starting coverage spool up ...")
		print(f"[>>] Child PID is {child_pid}")

		if (child_pid == 0):
			init_trace_target(self.binary)
		else:
			status = waitpid(child_pid, 0)
			print(f"[>>] Waitpid returned {status}")
			# continue_exc(child_pid)

			# ===============================================
			# test pipes
			# close(stdout_pipe)
			# data_pipe = fdopen(stdin_pipe, 'wb')
			# data_pipe.write(data.encode())
			# data_pipe.close()
			# ===============================================

			# ==============================================
			coverage_ops = Coverage(self.binary, child_pid)
			call_table = coverage_ops.get_function_calls()
			entry = coverage_ops.entry_point
			exit = coverage_ops.exit_point
			coverage_runner = PtFuzz(self.binary, child_pid, entry, exit, call_table)
			
			registers = Registers_x86()
			# ==============================================

			print(f"[>>] Starting trace on {child_pid}")

			# status = waitpid(child_pid, 0)
			# print(f"[>>] Waitpid returned {status}")

			coverage_runner.set_anchors(entry, exit)
			

			continue_exc(child_pid)
			
			status = waitpid(child_pid, 0)
			print(f"[>>] Waitpid returned {status}")

			if (WIFSTOPPED(status[1])):
				if (WSTOPSIG(status[1]) == SIG_TRAP):
					print(f"[>>] Hit breakpoint!")
					print("[>>] Handling trap signal ...")
					
					# print(f"[>>] ;) Not implemented")
					get_registers(child_pid, registers)

					print(f"[>>] initial trap cycle complete\n\n")
				else:
					print(f"[>>] Something else stopped the process")
			else:
				print(f"[>>] Something horrible occurred, {status[1]}")
			
			
			entry_breakpoint = coverage_runner.start_bp
			print(f"[>>] Look up for {hex(entry)} breakpoint was {hex(entry_breakpoint)}")

			# print(f"\n[>>] Entry bp {entry_breakpoint}")
			pokedata(child_pid, entry_breakpoint, entry)
			
			print("[>>] Restored entry BP")
			registers.eip -= 1
			print("[>>] Rolled back instruction ptr")
			set_registers(child_pid, registers)
			print("[>>] Restored registers")

			coverage_runner.set_checkpoints()
			breakpoints = coverage_runner.breakpoints
			print(f"Breakpoints :: {breakpoints}")

			print("\n")


			# send data as bytes to pipe
			# pipe.communicate(data.encode())
			# return pipe.returncode
	



