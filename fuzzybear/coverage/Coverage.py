from pwn import *
from pwnlib.gdb import corefile



from capstone import *

# import gdb
# proc = process('../../tests/components/coverage/complex')

test_binary = "../../tests/components/coverage/complex"
simple_binary = "../../tests/components/coverage/simple"

# ================================================================= #

import ptrace

class Coverage:
    """ handler class for coverage ops """
    def __init__(self, coverage_target):
        self.coverage_target = coverage_target


    def gen_code_paths(self):
        """ establish all paths through target """
        pass


    def start(self, tracee_pid):
        """ begin coverage ops"""
    
        ptrace.attach_tracer(tracee_pid)


'''todos

+ resolve target architecture

'''

# ================================================================= #




_default_symbols = [
    '_start',
    '_init',
    'stack_chk_fail'

]

def dump_symbols():
    
    elf = ELF(simple_binary)
    print(elf.symbols, "\n\n")
    print("Functions: \n", elf.functions.keys(), "\n\n")
    
    
    # process.corefile(test_binary)
    proc = process(simple_binary)
    #gdb.corefile(proc)
    # prog_state = proc.corefile
    # print(f"EIP @: {hex(prog_state.eip)}")
    # proc.sendline('A' * 300)
    # # proc.recvuntil('function1\n')
    # # proc.sendline('test')
    # # proc.sendline('0')    
    # # proc.recvuntil('function2\n')

    # # dump a corefile at the current point
    # # core is written to disk @ cwd so will
    # # need cleanup
    # prog_state = proc.corefile
    # print(f"EIP @: {hex(prog_state.eip)}")

    # print(f"STACK :: {prog_state.stack}")
    # print(f"Registers :: {prog_state.registers}")

    # pid = gdb.attach(
    #     proc, 
    #     gdbscript='''
    #             disassemble main 
                 
    #             break main
    #             detach
    #             quit
    #             ''',
    #     api=True
    # )
    # print(pid)

    #print(proc.recvline())
    # gdb_instance = gdb.

    gdb_pipe = gdb.attach(
        proc, 
        gdbscript="""
                break main
                """, 
        api=True
    )
    print("[>>] Opened PIPE :: ", gdb_pipe)

    pid, gdb_inst = gdb_pipe
    print("[>>] Opened GDB instance ::", gdb_inst)
    # option dead on this arch?
    # gdb_inst.start_recording()

    proc.sendline('a' * 500)
    # record = gdb_inst.current_recording()
    
    # print(dir(record))
    # # print(record.begin)
    # gdb_inst.stop_recording()
    # print(record.method)

    
    # # proc.recvuntil('\n')
    # # print("EVENTS :: ", gdb_inst.events)
    # print(gdb_inst.breakpoints())
    # for bp in gdb_inst.breakpoints():
    #     # print(dir(bp))
    #     print(f'{bp.number} hit {bp.hit_count} times') 

   

    # for bp in gdb_inst.breakpoints():
    #     # print(dir(bp))
    #     print(f'{bp.number} hit {bp.hit_count} times')    
    

# ================================================================= #
blocks = [
    {
        '_start': [],    # opcodes for start
        'block_num': 0   # block number
    }, 
    {
        'main' : [],     # opcodes for main
        'block_num': 0   # block number
    }
]

def gen_code_paths():
    """ Dump binaries code paths """
    # elf = ELF(test_binary)
    elf = ELF(simple_binary)
    
    # TODO :: Dynamic arch detection
    target_bin_conf = Cs(CS_ARCH_X86, CS_MODE_32)
    target_bin_conf.detail = True
    
    # executable code lives in .text section
    opcodes = elf.section('.text')

    current_block = 0
    last_block = 0
    for op in target_bin_conf.disasm(opcodes, 0x1000):
        print("0x%x:\t%s\t%s" %(op.address, op.mnemonic, op.op_str))
        if len(op.groups) > 0:
            print(f"Block{'':5}{op.groups}")
            # if (op.groups[0] != last_block):
            #     current_block += 1
            #     last_block = op.groups[0]
            
            
            # if (current_block == 0):
            #     blocks[current_block]['block_num'] = op.groups[0]
            #     blocks[current_block]['_start'].append(op.op_str)
            # else:
            #     blocks[current_block] = {
            #         'block_num': op.groups[0],
            #     }
                
    print(blocks)


# ================================================================= #


def stop_event_handler(event):
    print("[>>] ", event)


def test_gdb():
    proc = process(simple_binary)

    gdb_pipe = gdb.attach(
        proc, 
        gdbscript="""
                break main
                c
                """, 
        api=True
    )
    print("[>>] Opened PIPE :: ", gdb_pipe)

    pid, gdb_inst = gdb_pipe
    print("[>>] Opened GDB instance ::", gdb_inst)

    gdb_inst.events.stop.connect(stop_event_handler)
    
    print("[>>] event hander connected")
    proc.sendline('a' * 5)
    # proc.interactive()
    gdb_inst.events.stop.disconnect(stop_event_handler)
    print("[>>] Event handler disconnect")


def gdb_debugger_test():
    # proc = process(simple_binary)

    gdb_pipe = gdb.debug(
        simple_binary, 
        gdbscript="""
                break main
                c
                """, 
        api=True
    )
    print("[>>] Opened PIPE :: ", gdb_pipe)

    gdb_inst = gdb_pipe
    print("[>>] Opened GDB instance ::", gdb_inst)

    gdb_inst.events.stop.connect(stop_event_handler)
    
    print("[>>] event hander connected")
    #proc.sendline('a' * 5)
    # proc.interactive()
    gdb_inst.events.stop.disconnect(stop_event_handler)
    print("[>>] Event handler disconnect")    



# ================================================================= #

"""notes

+ ptrace is very handy
+ was assumed that this would only work
  through a C wrapper / binding
+ looks like it may be possible to do it 
  directly through python, ish making it a 
  very compelling approach 
+ also libs like:
    + ptracer
    + python-ptrace

+ Example C interface
    + github.com/pinterest/ptracer/blob/master/ptracer/ptrace/_ptrace.c
"""

import ctypes
import sys
import os

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


def ptrace_tests():
    """ interface to ptrace syscall """
    pass


# ================================================================= #


# ================================================================= #
# test_gdb()
# gdb_debugger_test()
# dump_symbols()
# gen_code_paths()

# ================================================================= #
"""devnotes

+ We can dump corefiles for the running binary to detect the state
  of registers namely EIP which is critical to getting coverage information
+ pwntools corefile function is a wrapper around gdbs corefile method and
  can be called inline while the binary runs
+ There is overhead associated with this method of course
+ The method can be quite unreliable

+ UPDATE :: capstone is very much faster than gdb and 
            more effective since we dont need to mess
            with pipes for static analysis
+ TODO :: Detect code blocks and function names
    + Convert into data structure to use for tree and coverage

+ Can proably use groups to work out the blocks


=== Approach === 

+ Use capstone & symbols table (via pwntools) to perform
  static analysis on the binary dumping blocks and function
  names
+ Create a tree of the function blocks 

+ Use ptrace to set breakpoints on the previously collected
  function names and addresses
+ Log breakpoints that are hit to track coverage
    + Need to explore how ptrace interacts with breakpoints
     and when events need to occur / the responsibility of the
     harness and aggregator 

"""