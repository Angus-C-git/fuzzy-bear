from pwn import *
from pwnlib.gdb import corefile

# import gdb
# proc = process('../../tests/components/coverage/complex')

test_binary = "../../tests/components/coverage/complex"

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
    
    

dump_symbols()


"""devnotes

+ We can dump corefiles for the running binary to detect the state
  of registers namely EIP which is critical to getting coverage information
+ pwntools corefile function is a wrapper around gdbs corefile method and
  can be called inline while the binary runs
+ There is overhead associated with this method of course
+ The method can be quite unreliable

"""