class JumpBlocks:
	def __init__(self, binaryBase, elf):
		self.blocks = {}
		self.watching = False
		self.binaryBase = binaryBase
		self.pie = 'PIE enabled' in elf.checksec()

	# This would be used if we were to implement some sort of cycle detection
	# that's manually triggered at some point during the fuzz.
	def watch(self):
		self.watching = True

	def add(self, start, end):
		jumpBlock = JumpBlock(start, end, self.pie, self.binaryBase)
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
	def __init__(self, start, end, pie, binaryBase):
		self.pie = pie
		self.start = start + binaryBase if pie else start
		self.end = end + binaryBase if pie else end
		self.timesReached = 0

	def reached(self):
		self.timesReached += 1

	def nReached(self):
		return self.timesReached