from pwn import *
from capstone import *
from pprint import pprint
from FunctionCall import FunctionCalls, FunctionCall
from JumpBlock import JumpBlocks, JumpBlock
import re

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

'''Ideas:
	- Once you have code blocks working properly
	- You should be able to detect if you some sort of cyclic behaviour	
'''

# TODO :: Finish implementing
class Coverage:
	""" handler class for coverage ops """
	def __init__(self, coverage_target):
		self.coverage_target = coverage_target.elf
		self.pid = coverage_target.pid
		# Trying this since /proc/pid is being created but all the files are empty

	def getVmmap(self, pid):
		f = open(f'/proc/{pid}/maps', 'r')
		vmmap = f.readlines()
		# for l in vmmap:
		# 	print(l)
		return vmmap

	# First line of vmmap gives address for the start of binary.
	def getBinaryBase(self, vmmap):
		line = vmmap[0]
		
		self.binaryBase = int(line[:line.index('-')],0x10)

	# Search for first line that references libc. 
	# Need to make sure this is is reliable
	def getLibcBase(self, vmmap):
		for i in range(len(vmmap)):
			if 'libc' in vmmap[i]:
				line = vmmap[i]
				self.libcBase = int(line[:line.index('-')],0x10)
				return

	
	def dubstep(self):
		vmmap = self.getVmmap(self.pid)
		self.getBinaryBase(vmmap)
		self.getLibcBase(vmmap)
		# self.getHeapBase(vmmap)

	def gen_code_paths(self):
		""" establish all paths through target """
		target = Cs(CS_ARCH_X86, CS_MODE_32)
		target.detail = True

		elf = self.coverage_target
		
		# executable code lives in .text section
		opcodes = elf.section('.text')

		addrMain = elf.symbols['main']
		addrStart = elf.symbols['_start'] #  <-- make sure this is what we want

		# Find binaryBase and libcBase (unnecesary atm)
		self.dubstep()

		# We start storing from after main() since I don't think jumps before main are
		# relevant for code coverage? Although maybe we need to include GOT stuffs ?
		i = 0
		j = 0
		startOfNextBlock = 0
		for op in target.disasm(opcodes, addrStart):
			# This excludes insturctions that jump to a register since its a trek to find out the address
			# actually being jumped to.
			if 'j' in op.mnemonic and not re.search('r..', op.op_str) and not re.search('e..', op.op_str):
				#print("0x%x:\t%s\t%s" %(op.address, op.mnemonic, op.op_str))
				if i == 0:
					jumpBlocks = JumpBlocks(self.binaryBase, elf)
					jumpBlocks.add(addrMain, op.address)
					startOfNextBlock = int(op.op_str,0x10) 
				else:
					jumpBlocks.add(startOfNextBlock, op.address)
					startOfNextBlock = int(op.op_str,0x10) 
				i += 1
			# Can probably more efficiently write this conditional.
			if 'call' in op.mnemonic and not re.search('r..', op.op_str) and not re.search('e..', op.op_str):
				#print("0x%x:\t%s\t%s" %(op.address, op.mnemonic, op.op_str))
				if j == 0:
					functionCalls = FunctionCalls(self.binaryBase, elf)
				functionCalls.add(hex(op.address), hex(int(op.op_str, 0x10)))
				j += 1

		functionCalls.resolveFunctionNames()
		print('printing function calls')
		print(functionCalls)

		print('printng jumpBlocks')
		print(jumpBlocks)
				

	def start(self, tracee_pid):
		""" begin coverage ops"""
		pass

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
	'stack_chk_fail'

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
