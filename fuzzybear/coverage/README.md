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
├── ptfuzz
│   ├── __init__.py
│   ├── ptfuzz.py
│   ├── ptrace
│   │   ├── __init__.py
│   │   ├── _libc.py
│   │   ├── _ptconstants.py
│   │   ├── ptrace.py
│   │   ├── _registers.py
│   │   └── utility
│   │       ├── arch.py
│   │       └── breakpoints.py
│   └── README.md
└── README.md
```

## Operation

The coverage module utilizes a homegrown sub-module `ptfuzz` which acts as a pythonic wrapper for the `ptrace` syscall. See [ptfuzz](./ptfuzz/README.md).

## Support

The coverage module largely relies on the [`ptrace`](https://man7.org/linux/man-pages/man2/ptrace.2.html) syscall exposed by the linux kernel. Hence only linux based kernels are fully supported, it is possible that BSD is supported. 