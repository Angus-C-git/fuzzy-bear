from .Harness import Harness
from .utility import response_codes
from .utility.codec import detect
from .utility.mode import is_raw
from .strategies import get_generator
from .logging.logger import Logger

# highlight crashes
from colorama import Fore, Style

'''
::::::::::::::::: [Aggregator] :::::::::::::::::

    ► Takes responses (or lack of) from the
      binary and decides what changes if any 
      should be triggered in the fuzzers 
	  ecosystem
    ► Runner Class for strategies/generators 
'''

# environment args 
env_args = {
    'crash_txt': 'bad.txt',
    'crash_dir': './',
}


def write_crash(crashing_input, mode='w'):
	""" write the crashing input to a file """
	print(Fore.RED + f'\n\n   [>>] CRASH DETECTED, dropping bad.txt')
	print(Style.RESET_ALL)

	with open(
			f"{env_args['crash_dir']}{env_args['crash_txt']}", 
			mode
		) as crash:
			crash.write(crashing_input)
	

class Aggregator():
	def __init__(self, binary, input_file):
		print(f"   [>>] Running fuzzer against <{binary.split('/')[-1]}> mutating <{input_file.split('/')[-1]}>")
		self.base_file = input_file
		self.codec = detect(input_file)
		self.raw = is_raw(self.codec)
		self.logger = Logger()
		self.harness = Harness(binary, self.logger, self.raw)

		

	def run_fuzzer(self):
		Generator = get_generator(self.codec, self.base_file)

		## Tmp handler
		if (Generator is None): 
			print(f'\n   [>>] The format of {self.base_file} is not supported')
			return None

		while True:
			inputs = Generator.run()
		
			for input in inputs:
				response_code = self.harness.open_pipe(input)
				if (response_code == -11): 
					write_crash(input, 'wb') if self.raw else write_crash(input)
					exit(0)

