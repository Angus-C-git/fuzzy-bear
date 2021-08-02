import ctypes
# from pty import fork
from ptrace._ptconstants import *
from ptrace._libc import *
from ptrace._registers import *

from os import execl, waitpid, WIFSTOPPED, WSTOPSIG, execv


""" 
>-> pythonic interface to ptrace <-<

	► Exposed via libc and utilizing ctypes
	► Work in progress

"""

""" NOTE :: these need to be ported to constants """
# ===============================================

PID = None

# int $3
TRAP_CODE = 0xCC

ADDRESS_MASK_x86 = 0xFFFFFF00
ADDRESS_MASK_x86_64 = 0xFFFFFFFFFFFFFF00

# ===============================================


""" debugging methods  """
def print_register_state_x86_64(registers):
	""" Print register state """
	print(f"RIP: {hex(registers.rip)}")
	print(f"RBP: {hex(registers.rbp)}")
	print(f"RBX: {hex(registers.rbx)}")
	print(f"RCX: {hex(registers.rcx)}")
	print(f"RDX: {hex(registers.rdx)}")
	print(f"RSI: {hex(registers.rsi)}")
	print(f"RDI: {hex(registers.rdi)}")
	print(f"origi_rax: {hex(registers.orig_rax)}")
	print(f"RAX: {hex(registers.rax)}")


def print_register_state_x86(registers):
	""" Print register state """
	print(f"EIP: {hex(registers.eip)}")

	print(f"EBX: {hex(registers.ebx)}")
	print(f"ECX: {hex(registers.ecx)}")
	print(f"EDX: {hex(registers.edx)}")
	print(f"ESI: {hex(registers.esi)}")
	print(f"EDI: {hex(registers.edi)}")
	print(f"EBP: {hex(registers.ebp)}")
	print(f"EAX: {hex(registers.eax)}")
	print(f"DS: {hex(registers.eax)}")
	print(f"origi_rax: {hex(registers.orig_eax)}")
	print(f"EFLAGS: {hex(registers.eflags)}")
	
	# dropped other registers

def print_symbols(proc):
	""" Print symbols """
	elf = ELF(proc)
	print(elf.symbols, "\n\n")
	print("Functions: \n", elf.functions.keys(), "\n\n")
	print('\n\n')


def update_coverage(address):
	""" Update coverage data """
	# TODO :: resolve function/blockname
	print(f"Updating coverage, hit {hex(address)}")


# ===============================================

def breakpoints_state(tmp_function_name):
	state = {
		'_start': 0x80490cc,
		'main': 0x80491cc,
		'function1': 0x80491cc,
		'_end': 0x804b2cc
	}
	return state[tmp_function_name]



# NOTE :: TMP hardcodes for simple
def save_register_state(tmp_function_name):
	""" Save register state """
	state = {
		'_start': 0x80490a0,
		'main': 0x80491e9,
		'function1': 0x80491b6,
		'_end': 0x804b2e8
	}

	return state[tmp_function_name]


def restore_register_state(bp_addr, original_address):
	""" Restore register state """
	res = LIBC.ptrace(PTRACE_POKEDATA, PID, bp_addr, original_address)
	print(f"[>>] Restore returned {res}")


def dump_register_state():
	""" Dump register state """
	print(f"[>>] Dumping {PID} register state")

	# TMP patchwork 
	_registers = Registers_x86()
	_data = Registers_x86()

	LIBC.ptrace(PTRACE_GETREGS, PID, 0, ctypes.byref(_registers))
	print(_registers)
	# TODO :: make dynamic
	print_register_state_x86(_registers)
	# _data = LIBC.ptrace(PTRACE_PEEKDATA, PID, ctypes.c_void_p(_registers.rip), 0)
	# print(_data)



def continue_exc(pid):
	""" Continue execution after breaking """
	print(f"[>>] Continuing execution of {pid} ...")
	res = LIBC.ptrace(PTRACE_CONT, pid, 0, 0)
	print(f"[>>] Continue returned {res}")
	
	# print(f"[>>] Rolling back instruction ptr ...")

	if (res):
		print(f"[>>] Continue failed with error code {res}")


def breakpoint(addr, arch='x86'):
	""" Swap out the last byte with trap"""
	if (arch == 'x86'):
		return ((addr & ADDRESS_MASK_x86) | TRAP_CODE)
	else:
		return ((addr & ADDRESS_MASK_x86_64) | TRAP_CODE)



def poketext(pid, address, value):
	""" Write to memory """
	res = LIBC.ptrace(PTRACE_POKETEXT, pid, address, value)
	print(f"[>>] POKETEXT returned {res}")
	if (res):
		print(
			f"[>>] Setting {hex(address)} failed with error code {res}"
		)



def handel_traps():
	""" Handle trap signals """
	print(f"[>>] Resuming execution from _start ...")
	continue_exc()
	# res = LIBC.ptrace(PTRACE_SINGLESTEP, PID, 0, 0)

	# restore_register_state(breakpoints_state('_start'), save_register_state('_start'))
	# print(f"[>>] Single step returned {res}")

	#TODO :: Work out why waitpid never triggers

	print(f"[>>] Listening for trap signals")
	stat = waitpid(PID, 0)

	print(f"[>>] Waitpid returned {stat}")
	# listen for trap singals while fuzzing
	while True:
		# stat = LIBC.wait()
		
		# hit bp
		if WSTOPSIG(stat[1]):
			print(f"[>>] Handling trap signal")
			dump_register_state()
			print(f"[>>] Not implemented")
		else:
			print(f"[>>] Something awful happened {WIFSTOPPED(stat[1])}")
			exit(1)

	restore_register_state()
	update_coverage()


# TODO :: deal with alignment 
def set_traps(targets):
	""" Set trap breakpoints """
	for bp_addr in targets:
		print(f"[>>] Setting trap at {hex(bp_addr)}")
		poketext(PID, bp_addr, breakpoint(bp_addr))
		




def set_entry_exit(start_addr, end_addr, pid):
	""" Set entry and exit point breakpoints """
	print(f"[>>] Setting start/end point at {hex(start_addr)}/{hex(end_addr)}")
	start_bp = breakpoint(start_addr)
	end_bp = breakpoint(end_addr)
	print(f"[>>] Start breakpoint: {hex(start_bp)}")
	print(f"[>>] End breakpoint: {hex(end_bp)}")

	poketext(pid, start_addr, start_bp)
	poketext(pid, end_addr, end_bp)



""" TMP TEST PROCESS  """
from pwn import *
test_tracee_elf = 'tmp_tests/linear'
# test_tracee = process(test_tracee_elf) 


'''
+ Looks like the process is only setting and or stopping
 at one breakpoint 

'''

def attach_tracer(pid):
		""" Attach to tracee to trace """
		global PID
		PID = pid

		LIBC.ptrace(PTRACE_ATTACH, PID, 0, 0)
		stat = waitpid(pid, 0)
		print(f"[>>] Attach stat returned {stat}")
		if WIFSTOPPED(stat[1]):
				if WSTOPSIG(stat[1]) == 19:
						
						print(f"[>>] Attached {PID}")
						set_entry_exit(0x80490a0, 0x80491e5)
						
						# set_traps([0x80491e9, 0x80491b6])
						dump_register_state()
						# handel_traps()
						# continue_exc()
						# res = LIBC.ptrace(PTRACE_SINGLESTEP, PID, 0, 0)
						dump_register_state()
						# print(f"[>>] Single step returned {res}")
						# print(f"[>>] WSTOPSIG :: {WSTOPSIG(stat[1])}")
						# proc.sendline("ls")
						stat = waitpid(pid, 0)
						# stat = LIBC.wait(5)
						print(f"[>>] Got stat {stat}")
				else:
					print(
						"[>>] stopped for some other signal ...", 
						WSTOPSIG(stat[1])
					)
					return -1





# =================================== ALT IMPLEMENTATION ===================================



tmp_proc_bs = {
	'_start': 0x80490a0,
	'_end': 0x804b2e8
}

def run_tracee():
	pass


def launch_trace_target(proc_name):
	""" Launch the process to be traced """
	trace_me_res = LIBC.ptrace(PTRACE_TRACEME, 0, 0, 0)
	if (trace_me_res < 0):
		print(f"[>>] Traceme failed with error code {trace_me_res}")

	print(f"[>>] Allowed tracing {proc_name}")
	proc_path = os.path.abspath(proc_name)
	print(f"[>>] Path to proc {proc_path}")

	# TODO :: Disable ASLR ?

	# replace the forked clone of main process
	# with this process
	execl_res = execl('./tmp_tests/linear', '/tmp_tests/linear')
	if (execl_res < 0):
		print(f"[>>] Execl failed with error code {execl_res}")



def launch_tracee(pid_child):
	""" Launch the tracee to track coverage """
	print(f"[>>] Starting trace of {pid_child}")

	# trap?
	status = os.waitpid(pid_child, 0)
	print(f"[>>] Waitpid returned {status}")

	start_addr = tmp_proc_bs['_start']
	end_addr = tmp_proc_bs['_end']

	set_entry_exit(start_addr, end_addr, pid_child)

	print(f'[>>] child pid is {pid_child}')

	# cnt
	continue_exc(pid_child)

	status = os.waitpid(pid_child, 0)
	print(f"[>>] Waitpid returned {status}")
	

	if (WIFSTOPPED(status[1])):
		# print(f"[>>] Stopped for some signal")
		if (WSTOPSIG(status[1]) == 5):
			print(f"[>>] Handling trap signal!")
			# tmp_input = input("[>>] Continue? [y/n] ")
			# dump_register_state()
			print(f"[>>] ;) Not implemented")
		else:
			print(f"[>>] Something else stopped the process")
	else:
		print(f"[>>] Something horrible occurred, {status[1]}")

def alt_attach_tracer(tracee):
	# if (LIBC.ptrace(PTRACE_ATTACH, pid, 0, 0) < 0):
	# 	print(f"[>>] Attach failed for {pid}")
	print(f"[>>] Attempting trace of {tracee}")

	# make child
	child_pid  = os.fork()
	if (child_pid == 0):
		# we are the child
		launch_trace_target(tracee)
	else:
		launch_tracee(child_pid)

""" TMP TESTS """

# simple:
	# _start: 0x80490a0
	# main: 0x80491e9
	# function1: 0x80491b6
	# _end: 0x804b2e8

# linear:
	# _start

print("[>>] Starting kessel run")
print_symbols(test_tracee_elf)
# attach_tracer(test_tracee.pid)
alt_attach_tracer(test_tracee_elf)
print("[>>] Finished kessel run somehow")
# print(f"[>>] Detached from {PID}")

# ===========================================================================

'''
::::::::::::::::::::::::::::: [PTRACE] :::::::::::::::::::::::::::::
 _________
|		  |
| process | --- pid --> attach_tracer(pdi) --> set_traps(blocks) --
|_________|												 	      | 	
																  |
					 detach_tracer(pid) <--- handle_trap() <------
											  |	   ^  |
											  |___/   |
											          |
													  V
										   update_coverage()

_ attach_tracer(pid) _

	+ Handels attaching to tracee

_ set_traps(blocks) _

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

_ detach_tracer(pid) _

	+ Handels detaching from tracee
	+ Cleanup, may be unnecessary since 
	  the process terminating kills the ptrace
'''



'''devnotes


+ NOTE :: pwntools process can disable aslr

`process(process_name,aslr=False)`

+ ptrace requires pid of process so will need
	to be hooked in from harness
+ while attached the tracer can receive signals
	from the tracee and will then be able to inspect
	various aspects of the tracees state
+ NOTE :: because we will (and nearly must) set breakpoints
					on static addresses we need to pin the tracees address 
					space by dissabling ASLR  

+ Set breakpoints by inserting sigtraps in the binary at single
	instruction locations
+ can tap into /proc/mappings to defeat PIE/ASLR
+ Might need to be stopped to properly observe register changes

@ man ptrace
+ When the tracer is finished tracing, it can cause the tracee to continue executing in a normal,
	untraced mode via PTRACE_DETACH

_c ptrace:

```C
long ptrace(enum __ptrace_request request, pid_t pid,
									 void *addr, void *data);

// attach 
ptrace(PTRACE_ATTACH, pid, 0, 0);
```

__ relevant requests __

+ The value of request determines the action to be performed:
		+ PTRACE_ATTACH: Attach  to  the process specified in pid, making it a tracee of the calling process
		+ PTRACE_SEIZE: Attach  to  the process specified in pid, making it a tracee of the calling process.  
										Unlike PTRACE_ATTACH, PTRACE_SEIZE does not stop the process.
										Only a PTRACE_SEIZEd process can accept  PTRACE_INTERRUPT  and  PTRACE_LISTEN  commands

		
		+ PTRACE_PEEKTEXT, PTRACE_PEEKDATA :  Read the contents of the specified memory location (addr)
		+ PTRACE_POKETEXT:  Write the contents of the specified memory location (addr)
		+ PTRACE_GETREGSET:  Read  the tracee's registers
		+ PTRACE_SETREGSET:  Write the tracee's registers
		+ PTRACE_GETSIGINFO:  Read the tracee's signal information
		+ PTRACE_O_TRACEEXIT:  Stop  the  tracee  at exit
'''