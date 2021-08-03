from ptfuzz import *
import os

from ptrace.ptrace import *

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


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::: #


class ptfuzz:
	def __init__(self, target):
		self.tracee = target
		
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
		child_pid  = os.fork()
		self.pid = child_pid
		if (child_pid == 0):
			# executing as the child
			self.init_trace_target()
		else:
			# executing as the parent
			self.launch_tracee()
		pass
	
	
	def init_trace_target(self):
		""" Launch the process to be traced """
		print("[>>] setting up tracee")
		trace_me()
		# TODO :: Disable ASLR ?

		# replace the forked clone of main process
		# with this process, does not return
		execl(f'./{self.tracee}', self.tracee)		


	def launch_tracee(self):
		""" Launch the tracee to track coverage """
		pid_child = self.pid

		print(f"[>>] Starting trace of {pid_child}")

		# wait for trap
		status = os.waitpid(pid_child, 0)
		print(f"[>>] Waitpid returned {status}")

		start_addr = tmp_proc_bs['_start']
		end_addr = tmp_proc_bs['_end']

		self.set_anchors(start_addr, end_addr)

		print(f'[>>] child pid is {pid_child}')

		# push process forwards
		continue_exc(pid_child)

		status = os.waitpid(pid_child, 0)
		print(f"[>>] Waitpid returned {status}")
		
		if (WIFSTOPPED(status[1])):
			if (WSTOPSIG(status[1]) == 5):
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


	def set_checkpoints(self, blocks):
		""" Set dynamic breakpoints """
		print("[>>] Not implemented")


	def handle_trap():
		""" Handle trap signal from tracee """
		print("[>>] Not implemented")



# ::::::::::::::::::::::::::::::::::::::::::::::::::::::: #

""" tmp testing """

print("[>>] Starting kessel run")
ptfuzz(test_tracee).begin_trace()
print("[>>] Finished kessel run")

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::: #






'''
::::::::::::::::::::::::::::: [PTFUZZ] :::::::::::::::::::::::::::::
 		   
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