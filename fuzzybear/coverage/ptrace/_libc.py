from . import *

""" resolve libc to expose ptrace """
LIBC_ELF_PATH = util.find_library('c')
LIBC = CDLL(LIBC_ELF_PATH, use_errno=True)

# Set ptrace constants
LIBC.ptrace.argtypes = [c_int32, c_ulonglong, c_int32, c_void_p]
LIBC.ptrace.restype = c_int32