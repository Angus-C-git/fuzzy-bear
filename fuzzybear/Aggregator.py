from .Harness import Harness
from .utility import response_codes

'''
::::::::::::::::: [Aggregator] :::::::::::::::::

    ► Takes responses (or lack of) from the
      binary and decides what changes if any 
      should be triggered (maybe)
    
    ► Runner Class for strategies/generators 

'''

# TODO :: Some way to detect file formats


class Aggregator():
	def __init__(self, binary, input_file):
		print(f"   [DEBUG] Aggregator received <{binary.split('/')[-1]}> <{input_file.split('/')[-1]}>")
		self.harness = Harness(binary)
		self.base_file = input_file

	def run_fuzzer(self):
		# TODO :: run generator here 	<codec>
		res = self.harness.open_pipe(self.base_file)
		print(f"   [DEBUG] Aggregator received {response_codes.lookup(res)} from binary")

