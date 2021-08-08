from pprint import pprint
class JumpBlocks:
	def __init__(self, binaryBase, elf):
		self.blocks = {}
		self.watching = False
		self.binaryBase = binaryBase
		self.pie = 'PIE enabled' in elf.checksec()
		self.elf = elf


	# This would be used if we were to implement some sort of cycle detection
	# that's manually triggered at some point during the fuzz.
	def watch(self):
		self.watching = True


	def add(self, start, end):
		jumpBlock = JumpBlock(start, end, self.pie, self.binaryBase)
		self.blocks[str(hex(jumpBlock.start))] = jumpBlock


	# Assuming addr is a pointer thats jumped to in the binary.
	# Unused atm.
	def isNewPath(self, addr):
		return self.jumpBlocks[str(addr)] == 0


	def resolveFunctionContext(self):
		functions = {}
		for fnName, fnObj in self.elf.functions.items():
			address = hex(fnObj.address + self.binaryBase) if self.pie else hex(fnObj.address)
			functions[address] = fnName
		pprint(functions)
		for k in self.blocks:
			self.blocks[k].orient(functions)


	def __str__(self):
		string = ""
		for key, val in self.blocks.items():
			string += f'{hex(val.start)} - {hex(val.end)} in {val.function}\n'
		return string

	
class JumpBlock:
	def __init__(self, start, end, pie, binaryBase):
		self.pie = pie
		self.start = start + binaryBase if pie else start
		self.end = end + binaryBase if pie else end
		self.timesReached = 0
		self.function = "unresolved"

	def orient(self, functions):
		addresses = list(functions.keys())
		addresses.sort()
		for i in range(len(addresses)-1):
			if self.start >= int(addresses[i],0x10) and self.start <= int(addresses[i+1],0x10):
				self.function = functions[addresses[i]]

	def reached(self):
		self.timesReached += 1

	def nReached(self):
		return self.timesReached