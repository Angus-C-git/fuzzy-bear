from pwn import *
from capstone import *
from pprint import pprint
import re

from rich.tree import Tree
from rich import print

from .symbols import defaults

# from ptfuzz.ptfuzz import PtFuzz


def update_coverage(address):
    """ Update coverage data """
    # TODO :: resolve function/blockname, send to UI event
    # handler
    print(f"[>>] Updating coverage, hit {hex(address)}")
    print("[>>] Not implemented")


'''Ideas:
	- Once you have code blocks working properly
	- You should be able to detect if you some sort of cyclic behavior	
'''

# TODO :: Finish implementing


class Coverage:
    """ handler class for coverage ops """

    def __init__(self, target_path, target_pid=None):
        self.target_elf = ELF(target_path, checksec=False)
        self.pid = target_pid
        self.function_names = []
        self.jumps = 0

    def get_function_names(self):
        functions = self.target_elf.functions
        for name in functions.keys():
            if name not in defaults:
                self.function_names.append(name)
        return self.function_names

    def get_vmmap(self):
        """ pulls the vmmap for target pid """
        with open(f'/proc/{self.pid}/maps', 'r') as mmap:
            vmmap = mmap.readlines()

        if len(vmmap):
            return vmmap
        else:
            print("[>>] vmmap lookup failed, is the process halted?")
            exit(1)

    def get_binary_base(self, vmmap):
        """ obtains the binaries base from vmmap """
        # First line of vmmap gives address for the start of binary.
        line = vmmap[0]
        self.binary_base = int(line[:line.index('-')], 0x10)

    # TODO :: Need to make sure this is is reliable

    def get_libc_base(self, vmmap):
        """ Search for first line that references libc. """

        for i in range(len(vmmap)):
            if 'libc' in vmmap[i]:
                line = vmmap[i]
                self.libc_base = int(line[:line.index('-')], 0x10)
                return

    def rebase(self):
        """ rebase binary for given pid """
        vmmap = self.get_vmmap()
        self.get_binary_base(vmmap)
        self.get_libc_base(vmmap)

    def gen_instruction_set(self, generator):
        instructions = []
        for i in generator:
            instructions.append(i)
        return instructions

    def find_jmp(self, addr_start, blockStart, ops):
        if not self.jumpBlocks.isNewPath(blockStart):
            return
        blockStart = blockStart
        for i in range(len(ops)-1):
            #print("0x%x:\t%s\t%s" %(ops[i].address, ops[i].mnemonic, ops[i].op_str))
            if 'j' in ops[i].mnemonic and not (
                    re.search('r..', ops[i].op_str) or
                    re.search('e..', ops[i].op_str)
            ):
                if ops[i].address >= blockStart:
                    self.jumpBlocks.add(blockStart, ops[i].address)
                    blockStart = ops[i+1].address
            try:
                key = hex(int(ops[i].op_str, 0x10))
                if 'call' in ops[i].mnemonic and key in self.addressNameMap and self.addressNameMap[key] == 'exit':
                    self.jumpBlocks.add(blockStart, ops[i].address)
            except:
                pass

    def gen_code_paths(self):
        """ generate all code paths through the target """

        self.rebase()

        functionAddrList = []
        addressNameMap = {}
        elf = self.coverage_target
        for fnName, fnObj in elf.functions.items():
            addressNameMap[hex(fnObj.address)] = fnName
        # TODO :: Need to make all of this code much nicer
        self.addressNameMap = addressNameMap
        for fnName, addr in elf.plt.items():
            addressNameMap[hex(addr)] = fnName

        pprint(self.addressNameMap)
        for fnName, fnObj in elf.functions.items():
            functionAddrList.append(fnObj.address)
        functionAddrList.sort()

        addr_start = self.coverage_target.symbols['_start']
        addr_main = self.coverage_target.symbols['main']
        target = Cs(CS_ARCH_X86, CS_MODE_32)
        target.detail = True
        elf = self.coverage_target
        opcodes = elf.section('.text')
        generator = target.disasm(opcodes, addr_start)
        ops = self.gen_instruction_set(generator)

    def get_function_calls(self):
        """ Get the function calls for the binary as a lookup table"""
        self.rebase()

        self.jumpBlocks = JumpBlocks(self.binary_base, self.coverage_target)

        self.target_elf.address = self.binary_base
        functions = self.target_elf.functions

        self.entry_point = self.target_elf.symbols['_start']
        self.exit_point = self.target_elf.symbols['_end']

        addr_main = self.coverage_target.symbols['main']

        function_table = {
            # address : name
        }

        for name in functions.keys():
            if name not in defaults:
                function_table[functions[name].address] = name
                self.function_names.append(name)

        self.find_jmp(self.entry_point, self.exit_point, ops)
        self.find_jmp(self.entry_point, addr_main, ops)
        self.jumpBlocks.resolveFunctionContext()
        print(self.jumpBlocks)
        return function_table


# ================================================================= #


'''dev notes

+ Some code reuse here, WIP

'''
