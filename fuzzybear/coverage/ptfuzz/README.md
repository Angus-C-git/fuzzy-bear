# ptfuzz

The **ptfuzz** module is a pythonic interface to the `ptrace` unix sys call specifically targeted at fuzzing. It exposes the methods necessary to collect coverage information from a binary in blackbox settings as well as the ability to fuzz programs entirely in memory, only forking once, by saving and restoring register state in the target program.

It aims to provide an easy way to harness the power of `ptrace` for fuzzing through simple abstracted methods. Being written in python also has advantages for portability and easy of use/extensibility.


## Usage



## Internals



## Architectures 

Currently the module only supports `x86` and `x86_64` trace targets  however extending this support is nearly as simple as adding the necessary registers and types to the `ptfuzz/registers` file. Assuming that the `ptrace` syscall is supported on the architecture the port should be simple. 