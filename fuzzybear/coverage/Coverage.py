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

		current_block = 0
		last_block = 0
		for op in target.disasm(opcodes, 0x1000):
			print("0x%x:\t%s\t%s" %(op.address, op.mnemonic, op.op_str))
			if len(op.groups) > 0:
				print(f"Block{'':5}{op.groups}")

		print("[>>] Not implemented")


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
