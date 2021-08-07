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
		self.dubstep()
		self.jumpBlocks = JumpBlocks(self.binaryBase, self.coverage_target)
		self.jumps = 0
		# Trying this since /proc/pid is being created but all the files are empty

	def getVmmap(self, pid):
		f = open(f'/proc/{pid}/maps', 'r')
		vmmap = f.readlines()
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

	def generateAllInstructions(self, generator):
		instructions = []
		for i in generator:
			instructions.append(i)
		return instructions

	def findJmp(self, addrStart, blockStart, ops):
		if not self.jumpBlocks.isNewPath(blockStart):
			return
		blockStart = blockStart
		for i in range(len(ops)-1):
			#print("0x%x:\t%s\t%s" %(ops[i].address, ops[i].mnemonic, ops[i].op_str))
			if 'j' in ops[i].mnemonic and not re.search('r..', ops[i].op_str) and not re.search('e..', ops[i].op_str):
				#print(f'ops.address: {ops[i].address} blockStart: {blockStart}')
				if ops[i].address >= blockStart:
					self.jumpBlocks.add(blockStart, ops[i].address)
					blockStart = ops[i+1].address
			try:
				key = hex(int(ops[i].op_str, 0x10))
				if 'call' in ops[i].mnemonic and key in self.addressNameMap and self.addressNameMap[key] == 'exit':
					self.jumpBlocks.add(blockStart, ops[i].address)
					# print('\n\n=====================\n')
					# print(f'blockStart: {hex(blockStart)} currInstr: {hex(ops[i].address)}')
					# print('\n\n=====================\n')
			except:
				pass
		#	elif 'ret' in ops[i].mnemonic:
		#	 	self.jumpBlocks.add(blockStart, ops[i].address)
				#print(f'blockStart: {hex(blockStart)} current instruction address: {hex(ops[i].address)} == {ops[i].mnemonic}')

	# Need to make sure this works with PIE / ASLR
	def gen_code_paths(self):
		# addrMain = elf.symbols['main']
		#pprint(self.coverage_target.functions)
		functionAddrList = []
		addressNameMap = {}
		elf = self.coverage_target
		for fnName, fnObj in elf.functions.items():
			addressNameMap[hex(fnObj.address)] = fnName
		self.addressNameMap = addressNameMap # Need to make all of this code much nicer
		for fnName, addr in elf.plt.items():
			#print(fnName, addr)
			addressNameMap[hex(addr)] = fnName

		pprint(self.addressNameMap)
		for fnName, fnObj in elf.functions.items():
			functionAddrList.append(fnObj.address)
		functionAddrList.sort()
		#self.jumpBlocks.buildRangeFinder(functionAddrList, addressNameMap)

		addrStart = self.coverage_target.symbols['_start'] #  <-- make sure this is what we want
		addrMain = self.coverage_target.symbols['main']
		target = Cs(CS_ARCH_X86, CS_MODE_32)
		target.detail = True
		elf = self.coverage_target
		opcodes = elf.section('.text')
		#print(f'\n-------------\naddrStart {hex(addrStart)}\n----------------\n')
		generator = target.disasm(opcodes, addrStart)
		ops = self.generateAllInstructions(generator)
		
		self.findJmp(addrStart, addrStart, ops)
		self.findJmp(addrStart, addrMain, ops)
		self.jumpBlocks.resolveFunctionContext()
		print(self.jumpBlocks)

	

			# 		# Can probably more efficiently write this conditional.
			# if 'call' in op.mnemonic and not re.search('r..', op.op_str) and not re.search('e..', op.op_str):
			# 	#print("0x%x:\t%s\t%s" %(op.address, op.mnemonic, op.op_str))
			# 	if j == 0:
			# 		functionCalls = FunctionCalls(self.binaryBase, elf)
			# 	functionCalls.add(hex(op.address), hex(int(op.op_str, 0x10)))
			# 	j += 1

		#functionCalls.resolveFunctionNames()
		# print('printing function calls')
		# print(functionCalls)

				

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
