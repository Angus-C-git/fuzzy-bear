from .Harness import Harness

'''
::::::::::::::::: [Aggregator] :::::::::::::::::

    ► Takes responses (or lack of) from the
      binary and decides what changes if any 
      should be triggered (maybe)
    
    ► Runner Class for strategies/generators 

'''


class Aggregator():
	def __init__(self, binary, input_file):
		print(f'	[DEBUG] Aggregator received targets {binary} {input_file}')
		self.harness = Harness(binary)
