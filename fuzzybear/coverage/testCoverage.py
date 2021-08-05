from Coverage import Coverage
from pwn import *

# Make sure this path is right for you.
elf = ELF('../../../binaries/plaintext2')

c = Coverage(elf)
c.gen_code_paths()