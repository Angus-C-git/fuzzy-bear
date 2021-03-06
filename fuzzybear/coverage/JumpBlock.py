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
		if self.is_new_path(start):
			jumpBlock = JumpBlock(start, end, self.pie, self.binaryBase)
			self.blocks[str(hex(jumpBlock.start))] = jumpBlock


	# Assuming addr is a pointer thats jumped to in the binary.
	# Unused atm.
	def is_new_path(self, addr):
		return hex(addr) not in self.blocks.keys()


	def resolve_function_context(self):
		# functions = {}
		# for fnName, fnObj in self.elf.functions.items():
		# 	address = hex(fnObj.address + self.binaryBase) if self.pie else hex(fnObj.address)
		# 	functions[address] = fnName
		# for k in self.blocks:
		# 	self.blocks[k].orient(functions)
		functionAddrList = []
		addressNameMap = {}
		for fnName, fnObj in self.elf.functions.items():
			key = hex(fnObj.address + self.binaryBase) if self.pie else hex(fnObj.address)
			addressNameMap[key] = fnName

		for fnName, fnObj in self.elf.functions.items():
			addr = fnObj.address + self.binaryBase if self.pie else fnObj.address
			functionAddrList.append(addr)
		functionAddrList.sort()
		self.build_range_finder(functionAddrList, addressNameMap)

		for key, block in self.blocks.items():
			block.set_function_context(self.which_range(block.start))

	# Assumes address list is sorted
	def build_range_finder(self, addressList, addressNameMap):
		# pprint(addressList)
		# pprint(addressNameMap)
		rangeFinder = {}
		for i in range(len(addressList)-1):
			functionRange = {'start':addressList[i],'end':addressList[i+1]-1}
			rangeFinder[addressNameMap[hex(addressList[i])]] = functionRange
		self.rangeFinder = rangeFinder
		#self.findJmp(addrMain, addrStart)

	# Give this function an address and a range finder and it will tell you which address
	# that instruction lives in.
	def which_range(self, address):
		for fnName, fnRange in self.rangeFinder.items():
			if address >= int(fnRange['start']) and address <= int(fnRange['end']):
				return fnName

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

	def set_function_context(self, fnName):
		self.function = fnName

	def reached(self):
		self.timesReached += 1

	def n_reached(self):
		return self.timesReached
