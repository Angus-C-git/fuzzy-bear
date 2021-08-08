from . import *

"""
>-> ptrace registers structure <-<

    ► Supports:
        + x86_64 processes
        + x86 processes

"""

class Registers_x86_64(Structure):

    """ 64 bit user_reg_struct """
    _fields_ = (
        ('r15', c_ulonglong),
        ('r14', c_ulonglong),
        ('r13', c_ulonglong),
        ('r12', c_ulonglong),
        ('rbp', c_ulonglong),
        ('rbx', c_ulonglong),
        ('r11', c_ulonglong),
        ('r10', c_ulonglong),
        ('r9', c_ulonglong),
        ('r8', c_ulonglong),
        ('rax', c_ulonglong),
        ('rcx', c_ulonglong),
        ('rdx', c_ulonglong),
        ('rsi', c_ulonglong),
        ('rdi', c_ulonglong),
        ('orig_rax', c_ulonglong),
        ('rip', c_ulonglong),
        ('cs', c_ulonglong),
        ('eflags', c_ulonglong),
        ('rsp', c_ulonglong),
        ('ss', c_ulonglong),
        ('fs_base', c_ulonglong),
        ('gs_base', c_ulonglong),
        ('ds', c_ulonglong),
        ('es', c_ulonglong),
        ('fs', c_ulonglong),
        ('gs', c_ulonglong),
    )



class Registers_x86(Structure):
    
    """ 32 bit user_reg_struct """

    _fields_ = (
        ("ebx", c_ulong),
        ("ecx", c_ulong),
        ("edx", c_ulong),
        ("esi", c_ulong),
        ("edi", c_ulong),
        ("ebp", c_ulong),
        ("eax", c_ulong),
        ("ds", c_ushort),
        ("__ds", c_ushort),
        ("es", c_ushort),
        ("__es", c_ushort),
        ("fs", c_ushort),
        ("__fs", c_ushort),
        ("gs", c_ushort),
        ("__gs", c_ushort),
        ("orig_eax", c_ulong),
        ("eip", c_ulong),
        ("cs", c_ushort),
        ("__cs", c_ushort),
        ("eflags", c_ulong),
        ("esp", c_ulong),
        ("ss", c_ushort),
        ("__ss", c_ushort),
    )

