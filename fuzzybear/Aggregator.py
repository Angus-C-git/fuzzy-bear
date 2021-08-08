from .Harness import Harness
from .utility import response_codes
from .utility import codec
from .strategies import get_generator

# highlight crash
from colorama import Fore, Style

'''
::::::::::::::::: [Aggregator] :::::::::::::::::

    ► Takes responses (or lack of) from the
      binary and decides what changes if any 
      should be triggered (maybe)
    
    ► Runner Class for strategies/generators 

'''

def write_crash(crashing_input):
	print(Fore.RED + f'\n\n   [>>] CRASH DETECTED, dropping bad.txt')
	print(Style.RESET_ALL)

	with open('./bad.txt', 'w') as crash:
		crash.write(crashing_input)


class Aggregator():
	def __init__(self, binary, input_file):
		print(f"   [>>] Running fuzzer against <{binary.split('/')[-1]}> mutating <{input_file.split('/')[-1]}>")
		self.harness = Harness(binary)
		self.codec = codec.detect(input_file)
		# print(f'   [DEBUG] {self.codec}')
		self.base_file = input_file

	# TODO :: Should internals be exported
	# to standalone fuzzing class ?
	def run_fuzzer(self):
		# TODO :: run generator here <codec>
		# format runner 
		Generator = get_generator(self.codec, self.base_file)

		## Tmp handler
		if (Generator is None): 
			print(f'\n   [>>] The format of {self.base_file} is not supported')
			return None
		
		print('   [>>] Running fuzzer ...')

		## TMP RUNNER >> ##
		while True:
			inputs = Generator.run()

		
			for input in inputs:
				# print(f"	 [DEBUG] mutation was {input}")
				response_code = self.harness.open_pipe(input, self.codec)
				# print(f"\n   [DEBUG] Aggregator received {response_codes.lookup(response_code)} from binary")
				if (response_code): 
					write_crash(input)
					exit(0)				# exit on crash ? 

