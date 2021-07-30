# Coverage Module

Handles coverage related tasks for fuzzing including:

+ Static disassembly 
+ Code path construction
+ Coverage tracking
    + Explored code paths 
    + Unexplored code paths

```files
.
├── Coverage.py
├── __init__.py
├── ptrace
│   ├── __init__.py
│   ├── _libc.py
│   ├── _ptconstants.py
│   └── _registers.py
└── ptrace.py
```

## Operation

The coverage module implements a sub-module `ptrace` which acts as a pythonic wrapper wrapper for `ptrace`.


## Support

The coverage module largely relies on the [`ptrace`](https://man7.org/linux/man-pages/man2/ptrace.2.html) syscall exposed by the linux kernel. Hence only linux based kernels are fully supported, it is possible that BSD is supported. 