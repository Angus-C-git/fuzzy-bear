from pprint import pprint
# Assume that the base addr of the binary is passed in so it 
# can resolve function names.
class FunctionCalls:
	def __init__(self, binaryBase, elf=None):
		self.calls = {}
		self.binaryBase = binaryBase
		self.elf = elf # pwntools.elf.ELF
		self.pie = 'PIE enabled' in elf.checksec()

	# Think it's better to use funcAddr as the key on the offchance
	# that the binary is stripped of symbols.
	# A potentially major problem here is that functions that are called multiple times,
	# will only have 1 entry in the dictionary since it's indexed by function address. 
	def add(self, instAddr, funcAddr):
		functionCall = FunctionCall(int(instAddr,0x10), int(funcAddr,0x10), self.pie, self.binaryBase)
		self.calls[functionCall.funcAddr] = functionCall
		# TODO: 
		# - value should be a list of functionCall's, otherwise we can't record
		#   different calls to the same function.

	def resolveFunctionNames(self):
		addressNameMap = {}
		# elf.functions returns a dictionary that maps function names to function objects.
		# function object basically encapsulate some data about a function, incl its addr.
		# Here we reverse the mapping so we can index it by address.
		for fnName, fnObj in self.elf.functions.items():
			address = hex(fnObj.address + self.binaryBase) if self.pie else hex(fnObj.address)
			addressNameMap[address] = fnName
		pprint(addressNameMap)
		for key, val in self.calls.items():
			try:
				# our functionCalls data structure is indexed by function address.
				self.calls[key].setFunctionName(addressNameMap[key])
			except:
				continue



	def __str__(self):
		string = ""
		for key, val in self.calls.items():
			# Make sure you call resolveFunctionNames before printing if you want
			# to see what function names are being resolved.
			string += f'{val.instAddr} = call {val.funcAddr} / {val.funcName}\n'
		return string

# Stored all values as strings since funcAddr will be used as a key
# so for consistency they're all strings.
class FunctionCall:
	def __init__(self, instAddr, funcAddr, pie, binaryBase):
		self.instAddr = hex(instAddr + binaryBase) if pie else hex(instAddr)
		self.funcAddr = hex(funcAddr + binaryBase) if pie else hex(funcAddr)
		self.funcName = None
		self.timesCalled  = 0

	def setFunctionName(self, name):
		self.funcName = name

	def called(self):
		self.timesCalled += 1

	def nCalled(self):
		return self.timesCalled
