from Coverage import Coverage
from pwn import *

# Make sure this path is right for you.
#elf = ELF('./test')
path = '/home/lucas/Comp/UNSW/2021/term2/6447/week2/wargame/bin/stack-dump'
#path = './test'
p = process(path)

c = Coverage(p)
c.gen_code_paths()
