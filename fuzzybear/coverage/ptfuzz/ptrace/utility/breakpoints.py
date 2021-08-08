# int $3
TRAP_CODE = 0xCC

ADDRESS_MASK_x86 = 0xFFFFFF00
ADDRESS_MASK_x86_64 = 0xFFFFFFFFFFFFFF00


def gen_breakpoint(addr, arch='x86'):
	""" Swap out the last byte with trap"""
	if (arch == 'x86'):
		return ((addr & ADDRESS_MASK_x86) | TRAP_CODE)
	else:
		return ((addr & ADDRESS_MASK_x86_64) | TRAP_CODE)