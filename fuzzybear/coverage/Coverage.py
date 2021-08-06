from pwn import *
from capstone import *
from pprint import pprint

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
	- 
'''
# Assume that the base addr of the binary is passed in so it 
# can resolve function names.
class FunctionCalls:
	def __init__(self, binaryBase, pid, elf=None):
		self.calls = {}
		self.binaryBase = binaryBase
		self.pid = pid
		self.elf = elf # pwntools.elf.ELF

	# Think it's better to use funcAddr as the key on the offchance
	# that the binary is stripped of symbols.
	# A potentially major problem here is that functions that are called multiple times,
	# will only have 1 entry in the dictionary since it's indexed by function address. 
	def add(self, functionCall):
		self.calls[str(functionCall.funcAddr)] = functionCall


	def resolveFunctionNames(self):
		addressNameMap = {}
		# elf.functions returns a dictionary that maps function names to function objects.
		# function object basically encapsulate some data about a function, incl its addr.
		for fnName, fnObj in self.elf.functions.items():
			addressNameMap[str(hex(fnObj.address))] = fnName
		pprint(addressNameMap)

		for key, val in self.calls.items():
			try:
				self.calls[key].setFunctionName(addressNameMap[str(key)])
			except:
				continue

	def __str__(self):
		string = ""
		for key, val in self.calls.items():
			string += f'{val.instAddr} = call {val.funcAddr} / {val.funcName}\n'
		return string

# Stored all values as strings since funcAddr will be used as a key
# so for consistency they're all strings.
class FunctionCall:
	def __init__(self, instAddr, funcAddr):
		self.instAddr = instAddr
		self.funcAddr = funcAddr
		self.funcName = None
		self.timesCalled  = 0

	def setFunctionName(self, name):
		self.funcName = name

	def called(self):
		self.timesCalled += 1

	def nCalled(self):
		return self.timesCalled


class JumpBlocks:
	def __init__(self):
		self.blocks = {}
		self.watching = False

	def watch(self):
		self.watching = True

	def add(self, jumpBlock):
		self.blocks[str(hex(jumpBlock.start))] = jumpBlock

	# Assuming addr is a pointer thats jumped to in the binary.
	def isNewPath(self, addr):
		return self.jumpBlocks[str(addr)] == 0

	def __str__(self):
		string = ""
		for key, val in self.blocks.items():
			string += f'{hex(val.start)} - {hex(val.end)}\n'
		return string

class JumpBlock:
	def __init__(self, start, end):
		self.start = start
		self.end = end
		self.timesReached = 0

	def reached(self):
		self.timesReached += 1

	def nReached(self):
		return self.timesReached

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
		#startOfInstructions = 0x80490f0
		addrMain = elf.symbols['main']
		addrStart = elf.symbols['_start']
		#print(hex(addrMain))
		current_block = 0
		last_block = 0
		i = 0
		j = 0
		startOfNextBlock = 0
		# We start storing from after main() since I don't think jumps before main are
		# relevant for code coverage? Although maybe we need to include GOT stuffs ?
		for op in target.disasm(opcodes, addrStart):
			# This finds all jump instructions in the binary. Seems to be a useful marker
			if 'j' in op.mnemonic and op.address >= addrMain and 'eax' not in op.op_str:
				#print("0x%x:\t%s\t%s" %(op.address, op.mnemonic, op.op_str))
				if i == 0:
					jumpBlocks = JumpBlocks()
					jumpBlocks.add(JumpBlock(addrMain, op.address))
					#jumpTree = JumpTree(addrMain, op.address, op.mnemonic)					
					startOfNextBlock = int(op.op_str,0x10) 
				else:
					#jumpTree.add(JumpTree(startOfNextBlock,  op.address ,op.mnemonic))
					jumpBlocks.add(JumpBlock(startOfNextBlock, op.address))
					startOfNextBlock = int(op.op_str,0x10) 
				i += 1
			if 'call' in op.mnemonic:
				print("0x%x:\t%s\t%s" %(op.address, op.mnemonic, op.op_str))
				if j == 0:
					#Will get binaryBase from /proc/{pid}/maps
					functionCalls = FunctionCalls(0x8048000, 1, elf)
				try:
					functionCalls.add(FunctionCall(hex(op.address), hex(int(op.op_str, 0x10))))
					# print('added function call')
				except:
					# if you don't call an addr, then it won't be saved in functionCalls. For example `call eax`
					# won't be stored as a function call. This can be implemented but not sure how helpful
					# it'll be.
					pass
				j += 1

		functionCalls.resolveFunctionNames()
		print(functionCalls)
		print(jumpBlocks)
		#jumpTree.show(jumpTree)
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
