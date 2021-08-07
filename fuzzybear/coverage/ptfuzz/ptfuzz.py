from os import execl, fork, waitpid, WIFSTOPPED, WSTOPSIG
from .ptrace.ptrace import trace_me, continue_exc, pokedata, gen_breakpoint, SIG_TRAP

"""
 ____ _____ _____ _   _ __________
|  _ \_   _|  ___| | | |__  /__  /
| |_) || | | |_  | | | | / /  / / 
|  __/ | | |  _| | |_| |/ /_ / /_ 
|_|    |_| |_|    \___//____/____|
                                  

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


:::::::::::::::::: ptfuzz ::::::::::::::::::


begin_trace(tracee):
	Should it be prog name or a pid

set_checkpoints(blocks):
	Set coverage checkpoints in the target of
	process

	@blocks: Array of symbols or addresses

TODO: Docs 

"""



# ::::::::::::::::::::::::::::::::::::::::::::::::::::::: #

""" tmp testing """

# TODO :: get from static or dynamic analysis
tmp_proc_bs = {
	'_start': 0x80490a0,
	'_end': 0x804b2e8
}

test_tracee = 'tmp_tests/linear'


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


class PtFuzz:
	def __init__(self, target=None, pid=None, entry=None, exit=None, dynamic_bps=None):
		self.tracee = target
		self.pid = pid
		self.entry = entry
		self.exit = exit
		self.dynamic_breakpoints = dynamic_bps

		
	def begin_trace(self):
		""" 
		launches the target process as a child of the current
		process and then replaces the fork of the parent
		process with that child.

		TODO :: this will require refactoring of the harness to
		utilise 
		"""
		print(f"[>>] Attempting trace on {self.tracee}")

		# make child
		child_pid  = fork()
		self.pid = child_pid
		if (child_pid == 0):
			# executing as the child
			self.init_trace_target()
		else:
			# executing as the parent
			self.launch_tracee()
	
	
	def init_trace_target(self):
		""" Launch the process to be traced """
		print("[>>] setting up tracee")
		trace_me()

		# replace the forked clone of main process
		# with this process, does not return
		execl(f'./{self.tracee}', self.tracee)		


	def launch_tracee(self):
		""" Launch the tracee to track coverage """
		pid_child = self.pid

		print(f"[>>] Starting trace of {pid_child}")
		# continue_exc(pid_child)

		# wait for trap
		status = waitpid(pid_child, 0)
		print(f"[>>] Waitpid returned {status}")

		# TODO :: resolve dynamically
		start_addr = self.entry #tmp_proc_bs['_start']
		end_addr = self.exit  #tmp_proc_bs['_end']

		self.set_anchors(start_addr, end_addr)
		
		self.set_checkpoints()

		print(f'[>>] child pid is {pid_child}')

		# push process forwards
		continue_exc(pid_child)

		status = waitpid(pid_child, 0)
		print(f"[>>] Waitpid returned {status}")
		
		if (WIFSTOPPED(status[1])):
			if (WSTOPSIG(status[1]) == SIG_TRAP):
				print(f"[>>] Hit breakpoint!")
				print("[>>] Handling trap signal ...")
				print(f"[>>] ;) Not implemented")
				print(f"[>>] initial trap cycle complete\n\n")
			else:
				print(f"[>>] Something else stopped the process")
		else:
			print(f"[>>] Something horrible occurred, {status[1]}")

		# TODO :: set checkpoint breakpoints

	
	def set_anchors(self, _start, _end):
		""" Set entry and exit point breakpoints """
		pid_child = self.pid
		print(f"[>>] Setting start/end point at {hex(_start)}/{hex(_end)}")
		
		start_bp = gen_breakpoint(_start)
		end_bp = gen_breakpoint(_start)

		print(f"[>>] Start breakpoint: {hex(start_bp)}")
		print(f"[>>] End breakpoint: {hex(end_bp)}")

		pokedata(pid_child, _start, start_bp)
		pokedata(pid_child, _end, end_bp)


	def set_checkpoints(self):
		""" Set dynamic breakpoints """
		pid_child = self.pid
		print(f"[>>] Setting dynamic breakpoints")
		for bp in self.dynamic_breakpoints.keys():
			print(f"[>>] Setting dynamic bp {hex(bp)}")
			bp_addr = gen_breakpoint(bp)
			pokedata(pid_child, bp, bp_addr)



	def handle_trap():
		""" Handle trap signal from tracee """
		print("[>>] Not implemented")



# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


""" tmp testing """

# print("[>>] Starting kessel run")
# PtFuzz(test_tracee).begin_trace()
# print("[>>] Finished kessel run")

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::







'''
:::::::::::::::::::::::: [PTFUZZ: internals] ::::::::::::::::::::::::
 		   
process   --- pid --> begin_trace(pdi) --> set_traps(blocks) --
       												 	      | 	
															  |
				 					 <--- handle_trap() <------
										  |	   ^  |
										  |___/   |
										          |
												  V
									   update_coverage()

_ begin_trace(tracee) _

	+ Handels starting trace on tracee

_ set_anchors(blocks) _

	+ Sets breakpoints at the start of 
	  each block in a program

_ handle_trap() _

	+ Primary utility method for fuzzing
	+ Recives trap signals from the process
	+ Updates coverage information
	+ Restores register states modified to 
	  set the blocks breakpoints
	+ The coverage handler higher up
	 takes care of saving the progressing
	 input to a corpus 

'''