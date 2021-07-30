from ptrace._ptconstants import *
from ptrace._libc import *

from os import waitpid, WIFSTOPPED, WSTOPSIG


""" 
>-> pythonic interface to ptrace <-<

    ► Exposed via libc and utilizing ctypes
    ► Work in progress

"""

""" TMP TEST PROCESS  """
from pwn import *
test_tracee = process('../../tests/components/coverage/simple') 


def attach_tracer(pid):
    """ Attach to tracee to trace """
    LIBC.ptrace(PTRACE_ATTACH, pid, 0, 0)
    stat = waitpid(pid, 0)
    if WIFSTOPPED(stat[1]):
        if WSTOPSIG(stat[1]) == 19:
            print(f"[>>] attached {pid}")
            # test intreact
            test_tracee.sendline('aa')
        else:
            print("[>>] stopped for some other signal, bad ...", WSTOPSIG(stat[1]))
            return -1


""" TMP TESTS """
print("[>>] Starting kessel run")
attach_tracer(test_tracee.pid)





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