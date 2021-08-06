'''
CSV strategy driver Class

	► Generates strategies for csv based 
	  inputs
'''
from .. import Strategy
from  csv import reader
from random import randint
import copy

'''
Utility methods for CSV 
strategies
'''

MAX_ROWS = 1000
MAX_COLUMNS = 1000
ENTRIES_THRESHOLD = 10


# def ui_event(event, boost=10):
#     Strategy.ui_event(event, boost)


# random row & column number
# within the size of csv
def random_row_col(range):
	a, b = range
	return (randint(0, a - 1), randint(0, b - 1))


# TODO :: fails sometimes 
def pack_csv(data):
	return "\n".join((",".join(row_col) for row_col in data))


# TODO :: Need a way to switch
# up header preservation organically
# see dev notes
class CSV(Strategy.Strategy):
	
	# parse csv input data
	def __init__(self, sample_input):
		super()
		self.sample_input = sample_input
		self.parse_csv()


	def parse_csv(self):
		with open(self.sample_input) as csvfile:
			self.candidate_input = list(reader(csvfile))

		self.size = (len(self.candidate_input), 
					len(self.candidate_input[0]))


	def add_entries(self, preserve_header=False):
		# Generate random number of rows
		# between 0 - 1000
		rows, cols = random_row_col((MAX_ROWS, MAX_COLUMNS))

		candidate = copy.deepcopy(self.candidate_input)
		mutation = [candidate[0]] if preserve_header else candidate

		for row in range(1, rows):
			new_row = []
			for col in range(1, cols):
				new_row.append(str(col * row))     # could be anything really 

			mutation.append(new_row)

		super().ui_event('additional rows', 10)
		return mutation


	# run strategies
	def run(self):     

		row, col = random_row_col(self.size)
		mutation = copy.deepcopy(self.candidate_input)
		for emoji in super().emoji():
			mutation[row][col] = emoji   
			yield pack_csv(mutation)
			super().ui_event('emoji', 25)
		
		mutation = copy.deepcopy(self.candidate_input)
		row, col = random_row_col(self.size)
		for chonk in super().chonk():
			mutation[row][col] = chonk
			yield pack_csv(mutation)
			super().ui_event('chonk', 20)
		
		for count in range(ENTRIES_THRESHOLD):
			yield pack_csv(self.add_entries())
			
		for count in range(ENTRIES_THRESHOLD):
			yield pack_csv(self.add_entries(True))

		mutation = copy.deepcopy(self.candidate_input)
		row, col = random_row_col(self.size)
		for constant in super().max_constants():
			mutation[row][col] = constant
			yield pack_csv(mutation)
			super().ui_event('constants', 25)
	
		mutation = copy.deepcopy(self.candidate_input)
		row, col = self.size
		for r in range(row):
			for c in range(col):
				mutation[r][c] = super().xor_data(self.candidate_input[r][c])
				yield pack_csv(mutation)
				super().ui_event('xor', 1, row)

		mutation = copy.deepcopy(self.candidate_input)
		row, col = self.size
		for r in range(row):
			for c in range(col):
				mutation[r][c] = super().bit_flip(self.candidate_input[r][c])
				print(f"[>>] mutation was {mutation}")
				yield pack_csv(mutation)
				super().ui_event('bit flip', 1, row)

		mutation = copy.deepcopy(self.candidate_input)
		row, col = self.size
		for r in range(row):
			for c in range(col):
				mutation[r][c] = super().negate(self.candidate_input[r][c])
				yield pack_csv(mutation)
				super().ui_event('negate', 1, row)


'''dev_notes

 + Even tho it matters for some CSVs that the header 
 remains intact we can ignore this as it will eventually
 be resolved by the generator -> unless


 + Things like adding rows and columns could be considered
   a sub strategy because the data that goes into the extra fields
   could also be fuzzed 


+ Currently designed to run in stages where diffrent fuzz cases are applied
 random entries each time 

'''
