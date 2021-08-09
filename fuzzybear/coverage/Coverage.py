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
		# self.coverage_target = coverage_target.elf
		self.target_elf = ELF(target_path, checksec=False)
		self.pid = target_pid
		self.function_names = []


	def get_function_names(self):
		functions = self.target_elf.functions
		for name in functions.keys():
			if name not in defaults:
				self.function_names.append(name)
		return self.function_names


	def get_vmmap(self, pid):
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
		vmmap = self.get_vmmap(self.pid)
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

		for name in functions.keys():
			if name not in defaults:
				function_table[functions[name].address] = name
				self.function_names.append(name)
		
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