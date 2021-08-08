
""" constants for ptrace requests """

PTRACE_TRACEME   = 0
PTRACE_PEEKTEXT   = 1
PTRACE_PEEKDATA   = 2
PTRACE_POKETEXT   = 4
PTRACE_POKEDATA   = 5
PTRACE_CONT       = 7
PTRACE_SINGLESTEP = 9
PTRACE_GETREGS    = 12
PTRACE_SETREGS    = 13
PTRACE_ATTACH     = 16
PTRACE_DETACH     = 17


"""
>-> Ptrace Request Constants <-<

PTRACE_TRACEME:                   
    Signal to parent that this process is expecting to be traced

PTRACE_PEEKTEXT, PTRACE_PEEKDATA: 
    Read  a word at the address addr in the tracee's memory

PTRACE_POKETEXT, PTRACE_POKEDATA:
    Copy the word data to the address addr in the tracee's memory

PTRACE_CONT:
    Continue execution of the tracee

PTRACE_SINGLESTEP:
    Move forward one instruction in the tracee
    
PTRACE_GETREGS:
    Dump the tracee's register state 

PTRACE_SETREGS
    Set the tracee's register state

PTRACE_ATTACH:
    Attach to tracee from parent

PTRACE_DETACH:
    Stop tracing a tracee
"""
