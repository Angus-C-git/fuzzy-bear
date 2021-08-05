from pwn import *
from capstone import *

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

'''Alternative data structure I talked about on Discord
class JumpBlocks:
	def __init__(self):
		self.jumps = {}
		self.watching = False

	def watch(self):
		self.watching = True

	def add(self, jumpBlock):
		self.jumpBlocks[str(jumpBlock.start)] = jumpBlock

	# Assuming addr is a pointer thats jumped to in the binary.
	def isNewPath(self, addr):
		return self.jumpBlocks[str(addr)] == 0
'''

class JumpBlock:
	def __init__(self, start, end):
		self.start = start
		self.end = end
		self.nReached = 0
	
	def reached(self):
		self.nReached += 1
	
	def getReached(self)
		return self.nReached


# A binary tree where the root is main, and each child is appended when a j**
# instruction is seen in the binary.

# Feel free to change whatever the fuck you want.
class JumpTree:
	# For the root node start will be the address of main(). For all subsequent nodes:
	# The start address will be wherever some previous code block jumped too. end will be
	# wherever the address that the end of this block jumps to.
	# Each jump will create a new node in the tree
	
	def __init__(self, start, end, mnemonic):
		# Hardcoded address of main(). Will need to be more robust than this more likely
		self.start = start
		self.end = end
		self.mnemonic = mnemonic
		self.right = None
		self.left = None
		self.numberTimesReached = 0

	# I memed 2521, this will probably yeet to infinity. Also not sure how helpful a tree
	# structured like this will be for just basic jump blocks
	def add(self, tree):
		if tree.start > self.start:
			if self.right is None:
				self.right = tree
			else:
				self.right.add(tree)
		else:
			if self.left is None:
				self.left = tree
			else:
				self.left.add(tree)

	def reached(self):
		self.numberTimesReached += 1
	
	def nReached(self):
		return self.numberTimesReached

	def show(self, tree):
		if tree is None:
			return
		#print(f'{hex(tree.start)} - {hex(tree.end)}')

		# mnemonic's arent being stored correctly
		print(f'{hex(tree.start)} - {hex(tree.end)}::{self.mnemonic}') 

		self.show(tree.left)
		self.show(tree.right)

# TODO :: Finish implementing
class Coverage:
	""" handler class for coverage ops """
	def __init__(self, coverage_target):
		self.coverage_target = coverage_target


	def gen_code_paths(self):
		""" establish all paths through target """
		target = Cs(CS_ARCH_X86, CS_MODE_32)
		target.detail = True

		elf = self.coverage_target
		
		# executable code lives in .text section
		opcodes = elf.section('.text')

		# No pie, so binary base should always be the same
		startOfInstructions = 0x80490f0
		addrMain = elf.symbols['main']
		print(hex(addrMain))

		current_block = 0
		last_block = 0
		i = 0
		# We start storing from after main() since I don't think jumps before main are
		# relevant for code coverage? Although maybe we need to include GOT stuffs ?
		for op in target.disasm(opcodes, startOfInstructions):
			# This finds all jump instructions in the binary. Seems to be a useful marker
			if 'j' in op.mnemonic and op.address > addrMain:
				print("0x%x:\t%s\t%s" %(op.address, op.mnemonic, op.op_str))
				if i == 0:
					jumpTree = JumpTree(addrMain, int(op.op_str,0x10), op.mnemonic)					
				else:
					jumpTree.add(JumpTree(op.address, int(op.op_str,0x10), op.mnemonic))
				i += 1
		jumpTree.show(jumpTree)
			#if len(op.groups) > 0:
				#print(f"Block{'':5}{op.groups}\n")
				
		print("[>>] Implementing......")


	def start(self, tracee_pid):
		""" begin coverage ops"""
		pass

# ================================================================= #


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
