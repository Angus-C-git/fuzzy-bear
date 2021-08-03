import ctypes
# from pty import fork
from ptrace._ptconstants import *
from ptrace._libc import ptrace
from ptrace._registers import *
from ptrace.utility.breakpoints import gen_breakpoint

from os import execl, waitpid, WIFSTOPPED, WSTOPSIG


""" 
>-> pythonic interface to ptrace for fuzzing <-<

	► Exposed via libc and utilizing ctypes
	► Not all methods supported 

"""

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

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

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::



# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def attach(target_pid):
	ptrace(PTRACE_ATTACH, target_pid, 0, 0)


def detach(target_pid):
	ptrace(PTRACE_DETACH, target_pid, 0, 0)


def pokedata(target_pid, address, value):
	res = ptrace(PTRACE_POKEDATA, target_pid, address, value)
	print(f"[>>] POKETEXT returned {res}")
	if (res < 0):
		print(
			f"[>>] Poke {hex(address)} failed, error code {res}"
		)


def peekdata(target_pid, address):
	res = ptrace(PTRACE_PEEKDATA, target_pid, address)
	if (res < 0):
		print(
			f"[>>] Peek {hex(address)} failed, error code {res}"
		)


def get_registers(target_pid):
	# TODO :: dynamic arch
	registers = Registers_x86()

	res = ptrace(PTRACE_GETREGS, target_pid, 0, byref(registers))
	if (res < 0):
		print(
			f"[>>] Get registers failed, error code {res}"
		)


def set_registers(target_pid, new_registers):
	res = ptrace(PTRACE_SETREGS, target_pid, 0, new_registers)
	if (res < 0):
		print(
			f"[>>] Set registers failed, error code {res}"
		)	


def trace_me():
	trace_me_res = ptrace(PTRACE_TRACEME, 0, 0, 0)
	if (trace_me_res < 0):
		print(f"[>>] Traceme failed with error code {trace_me_res}")


def continue_exc(pid):
	""" Continue execution after breaking """
	print(f"[>>] Continuing execution of {pid} ...")
	res = ptrace(PTRACE_CONT, pid, 0, 0)
	print(f"[>>] Continue returned {res}")
	
	# print(f"[>>] Rolling back instruction ptr ...")

	if (res):
		print(f"[>>] Continue failed with error code {res}")


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::




'''
::::::::::::::::::::::::::::: [PTRACE] :::::::::::::::::::::::::::::

+ TODO :: cleanup

+ NOTE :: pwntools process can disable ASLR

`process(process_name, aslr=False)`

+ ptrace requires pid of process so will need
	to be hooked in from harness
+ while attached the tracer can receive signals
	from the tracee and will then be able to inspect
	various aspects of the tracees state
+ NOTE :: because we will (and nearly must) set breakpoints
					on static addresses we need to pin the tracee's address 
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