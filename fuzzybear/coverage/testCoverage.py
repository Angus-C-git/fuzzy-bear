from Coverage import Coverage
from pwn import *

# Make sure this path is right for you.
#elf = ELF('./test')
# path = '/home/lucas/Comp/UNSW/2021/term2/6447/week2/wargame/bin/stack-dump'
# path = './test'
TESTS_PATH = '../../tests/components/coverage/codepaths'

# target_binary = f'{TESTS_PATH}/test'
# target_binary = f'{TESTS_PATH}/simple'
# target_binary = f'{TESTS_PATH}/complex'
target_binary = f'{TESTS_PATH}/regular'


proc = process(target_binary)

# inspect binary in gdb to check if offsets work
# gdb.attach(proc.pid)


coverage_runner = Coverage(proc, proc.pid)
coverage_runner.gen_code_paths()
