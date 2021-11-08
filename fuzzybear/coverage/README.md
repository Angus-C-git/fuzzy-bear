# Coverage Module

_Currently being rewritten_

Handles coverage related tasks for fuzzing including:

-   Static disassembly
-   Code path construction
-   Coverage tracking
    -   Explored code paths
    -   Unexplored code paths

## Operation

The coverage module utilizes a homegrown ~~sub-module `ptfuzz` which acts as a pythonic wrapper for the `ptrace` syscall. See [ptfuzz](./ptfuzz/README.md)~~ library, [ptfuzz](#), which is a W.I.P offering pythonic bindings to ptrace through a `C` wrapper and other helper and utility functions aimed at building coverage guided fuzzers or other utilities to work with ptrace.

## Support

The coverage module largely relies on the [`ptrace`](https://man7.org/linux/man-pages/man2/ptrace.2.html) syscall exposed by the linux kernel. Hence only linux based kernels are fully supported, it is possible that BSD is supported.
