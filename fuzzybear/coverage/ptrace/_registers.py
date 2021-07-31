from . import *

# class user_regs_struct(Structure):
class Registers_x86_64(Structure):
    # # 32bit registers
    # _x86_32 = {
    #     # DATA 
    #     'eax': c_int32,
    #     'ebx': c_int32,
    #     'ecx': c_int32,
    #     'edx': c_int32,

    #     # POINTERS
    #     'esp': c_int32,
    #     'ebp': c_int32,
    #     'eip': c_int32,

    #     # INDEX
    #     'esi': c_int32,
    #     'edi': c_int32,   
    # }

    # # 64bit registers
    # _x86_64 = {
    #     'r15': c_ulonglong,
    #     'r14': c_ulonglong,
    #     'r13': c_ulonglong,
    #     'r12': c_ulonglong,
    #     'r11': c_ulonglong,
    #     'r10': c_ulonglong,
    #     'r9': c_ulonglong,
    #     'r8': c_ulonglong,
    #     'rbp': c_ulonglong,
    #     'rbx': c_ulonglong,
    #     'rax': c_ulonglong,
    #     'rcx': c_ulonglong,
    #     'rdx': c_ulonglong,
    #     'rsi': c_ulonglong,
    #     'rdi': c_ulonglong,
    #     'orig_rax': c_ulonglong,
    #     'rip': c_ulonglong,
    #     'cs': c_ulonglong,
    #     'eflags': c_ulonglong,
    #     'rsp': c_ulonglong,
    #     'ss': c_ulonglong,
    #     'fs_base': c_ulonglong,
    #     'gs_base': c_ulonglong,
    #     'ds': c_ulonglong,
    #     'es': c_ulonglong,
    #     'fs': c_ulonglong,
    #     'gs': c_ulonglong,
    # }                          

    # alt 64
    _fields_ = [
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
    ]

