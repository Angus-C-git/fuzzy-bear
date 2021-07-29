from pwn import *
from pwnlib.gdb import corefile

from capstone import *

# import gdb
# proc = process('../../tests/components/coverage/complex')

test_binary = "../../tests/components/coverage/complex"
simple_binary = "../../tests/components/coverage/simple"


_default_symbols = [
    '_start',
    '_init',
    'stack_chk_fail'

]

def dump_symbols():
    
    elf = ELF(test_binary)
    print(elf.symbols, "\n\n")
    print("Functions: \n", elf.functions.keys(), "\n\n")
    
    
    # process.corefile(test_binary)
    proc = process(test_binary)
    #gdb.corefile(proc)
    prog_state = proc.corefile
    print(f"EIP @: {hex(prog_state.eip)}")
    proc.recvuntil('function1\n')
    proc.sendline('test')
    # proc.sendline('0')    
    # proc.recvuntil('function2\n')

    # dump a corefile at the current point
    # core is written to disk @ cwd so will
    # need cleanup
    prog_state = proc.corefile
    print(f"EIP @: {hex(prog_state.eip)}")

    print(f"STACK :: {prog_state.stack}")
    print(f"Registers :: {prog_state.registers}")

    # pid = gdb.attach(
    #     proc, 
    #     gdbscript='''
    #             disassemble main 
                 
    #             quit
    #             ''',
    #     api=True
    # )
    # print(pid)

    # print(proc.recvline())
    # gdb_instance = gdb.

    # gdb_pipe = gdb.debug([test_binary], gdbscript="""break main""", api=True)
    

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


# dump_symbols()
gen_code_paths()


"""devnotes

+ We can dump corefiles for the running binary to detect the state
  of registers namely EIP which is critical to getting coverage information
+ pwntools corefile function is a wrapper around gdbs corefile method and
  can be called inline while the binary runs
+ There is overhead associated with this method of course
+ The method can be quite unreliable

+ UPDATE :: capstone is very much faster than gdb and 
            more effective since we dont need to mess
            with pipes
+ TODO :: Detect code blocks and function names
    + Convert into data structure to use for tree and coverage

+ Can proably use groups to work out the blocks
"""