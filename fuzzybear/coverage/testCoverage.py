from Coverage import Coverage
from pwn import *

# Make sure this path is right for you.
elf = ELF('./test')
#'/home/lucas/Comp/UNSW/2021/term2/6447/week3/wargame/bin/formatrix

c = Coverage(elf)
c.gen_code_paths()