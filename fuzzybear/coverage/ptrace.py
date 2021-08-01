import ctypes
from ptrace._ptconstants import *
from ptrace._libc import *
from ptrace._registers import *

from os import waitpid, WIFSTOPPED, WSTOPSIG


""" 
>-> pythonic interface to ptrace <-<

		► Exposed via libc and utilizing ctypes
		► Work in progress

"""


PID = None

""" debugging methods  """
def print_register_state(registers):
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



def save_register_state():
	pass


def restore_register_state():
	pass


def dump_register_state():
	""" Dump register state """
	print(f"[>>] Dumping {PID} register state")

	# TMP patchwork 
	_registers = Registers_x86_64()
	_data = Registers_x86_64()

	LIBC.ptrace(PTRACE_GETREGS, PID, 0, ctypes.byref(_registers))
	print(_registers)
	print_register_state(_registers)
	# _data = LIBC.ptrace(PTRACE_PEEKDATA, PID, ctypes.c_void_p(_registers.rip), 0)
	# print(_data)



""" TMP TEST PROCESS  """
from pwn import *
test_tracee = process('../../tests/components/coverage/complex64') 


def attach_tracer(pid):
		""" Attach to tracee to trace """
		global PID
		PID = pid

		LIBC.ptrace(PTRACE_ATTACH, PID, 0, 0)
		stat = waitpid(pid, 0)
		if WIFSTOPPED(stat[1]):
				if WSTOPSIG(stat[1]) == 19:
						print(f"[>>] attached {PID}")
						# test intreact
						test_tracee.sendlineafter('function1\n', 'aaa')
						test_tracee.recvuntil('enter a ')
						test_tracee.sendlineafter('number\n', '10')
						test_tracee.sendlineafter('hack me\n', 'A' * 200)
				else:
					print(
						"[>>] stopped for some other signal, bad ...", 
						WSTOPSIG(stat[1])
					)
					return -1


""" TMP TESTS """
print("[>>] Starting kessel run")
attach_tracer(test_tracee.pid)
dump_register_state()
print(f"[>>] Detached from {PID}")



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