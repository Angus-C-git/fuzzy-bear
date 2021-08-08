from pwn import *
from capstone import *
from pprint import pprint
# from FunctionCall import FunctionCalls, FunctionCall
# from JumpBlock import JumpBlocks, JumpBlock
import re

from rich.tree import Tree
from rich import print

from .symbols import defaults

# from ptfuzz.ptfuzz import PtFuzz


# ================================================================= #

test_binary = "../../tests/components/coverage/complex"
simple_binary = "../../tests/components/coverage/simple"

# ================================================================= #

def update_coverage(address):
	""" Update coverage data """
	# TODO :: resolve function/blockname, send to UI event
	# handler
	print(f"[>>] Updating coverage, hit {hex(address)}")
	print("[>>] Not implemented")


tree = {
	'0': 'main'
}

def build_call_tree(branch, called_address):
	""" builds a tree of function calls """
	pass


'''Ideas:
	- Once you have code blocks working properly
	- You should be able to detect if you some sort of cyclic behavior	
'''

# TODO :: Finish implementing
class Coverage:
	""" handler class for coverage ops """
	def __init__(self, target_path, target_pid):
		# self.coverage_target = coverage_target.elf
		self.target_elf = ELF(target_path, checksec=False)
		self.pid = target_pid


	def getVmmap(self, pid):
		""" pulls the vmmap for target pid """
		with open(f'/proc/{pid}/maps', 'r') as mmap:
			vmmap = mmap.readlines()
		
		if len(vmmap):
			return vmmap
		else:
			print("[>>] vmmap lookup failed, is the process halted?")
			exit(1)


	def getBinaryBase(self, vmmap):
		""" obtains the binaries base from vmmap """
		# First line of vmmap gives address for the start of binary.
		line = vmmap[0]
		self.binaryBase = int(line[:line.index('-')],0x10)


	# TODO :: Need to make sure this is is reliable
	def getLibcBase(self, vmmap):
		""" Search for first line that references libc. """
		for i in range(len(vmmap)):
			if 'libc' in vmmap[i]:
				line = vmmap[i]
				self.libcBase = int(line[:line.index('-')],0x10)
				return

	
	def rebase(self):
		""" rebase binary for given pid """
		vmmap = self.getVmmap(self.pid)
		self.getBinaryBase(vmmap)
		self.getLibcBase(vmmap)
		# self.getHeapBase(vmmap)


	def get_function_calls(self):
		""" Get the function calls for the binary as a lookup table"""
		self.rebase()
		self.target_elf.address = self.binaryBase
		functions = self.target_elf.functions

		self.entry_point = self.target_elf.symbols['_start']
		self.exit_point = self.target_elf.symbols['_end']

		# print(f"[>>] Entry/exit points: {hex(self.entry_point)}/{hex(self.exit_point)}")

		function_table = {
			# address : name
		}

		for key in functions.keys():
			if key not in defaults:
				function_table[functions[key].address] =  key
				# print(f"{key}: {hex(functions[key].address)}")

		# print(function_table)
		return function_table

	# =================================================================


	# def gen_code_paths(self):
	# 	""" establish all paths through target """
		
	# 	# config
	# 	target = Cs(CS_ARCH_X86, CS_MODE_32)
	# 	target.detail = True
	# 	elf = self.coverage_target

		
	# 	# executable code lives in .text section
	# 	opcodes = elf.section('.text')

	# 	# get section entry/exits
	# 	addrMain = elf.symbols['main']
	# 	addrStart = elf.symbols['_start'] #  <-- make sure this is what we want
	# 	print(f"[>>] addrMain: {hex(addrMain)}")

	# 	# rebase binary	
	# 	# self.rebase()
	# 	# print(f"[>>] Binary Base: {hex(self.binaryBase)}")
		

	# 	# We start storing from after main() since I don't think jumps before main are
	# 	# relevant for code coverage? Although maybe we need to include GOT stuffs ?
	# 	i = 0
	# 	j = 0
	# 	startOfNextBlock = 0
	# 	for op in target.disasm(opcodes, addrStart):
	# 		# This excludes instructions that jump to a register since its a trek to find out the address
	# 		# actually being jumped to.
	# 		if 'j' in op.mnemonic and not re.search('r..', op.op_str) and not re.search('e..', op.op_str):
	# 			# print("0x%x:\t%s\t%s" %(op.address+self.binaryBase, op.mnemonic, hex(int(op.op_str,0x10)+self.binaryBase)))
	# 			print("0x%x:\t%s\t%s" %(op.address, op.mnemonic, hex(int(op.op_str,0x10))))
	# 			if i == 0:
	# 				jumpBlocks = JumpBlocks(self.binaryBase, elf)
	# 				startOfNextBlock = int(op.op_str,0x10) 
	# 			jumpBlocks.add(startOfNextBlock, op.address)
	# 			startOfNextBlock = int(op.op_str,0x10) 
	# 			i += 1
	# 		# Can probably more efficiently write this conditional.
	# 		if 'call' in op.mnemonic and not re.search('r..', op.op_str) and not re.search('e..', op.op_str):
	# 			#print("0x%x:\t%s\t%s" %(op.address, op.mnemonic, op.op_str))
	# 			if j == 0:
	# 				functionCalls = FunctionCalls(self.binaryBase, elf)
	# 			functionCalls.add(hex(op.address), hex(int(op.op_str, 0x10)))
	# 			j += 1

	# 	functionCalls.resolveFunctionNames()
	# 	print('printing function calls')
	# 	print(functionCalls)

	# 	jumpBlocks.resolveFunctionContext()
	# 	# print('printing jumpBlocks')
	# 	# print(jumpBlocks)


	# def start(self, tracee_pid):
	# 	""" begin coverage ops"""
	# 	pass


# ================================================================= #
""" debugging/tmp """
def print_symbols(proc):
	""" Print symbols """
	elf = ELF(proc)
	print(elf.symbols, "\n\n")
	print("Functions: \n", elf.functions.keys(), "\n\n")
	print('\n\n')


_default_symbols = [
	'_start',
	'_init',
	'stack_chk_fail',
	'__libc_csu_init',
	'__libc_csu_fini',
	'__stack_chk_fail_local'
]

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


# print_symbols(simple_binary)

# ================================================================= #
