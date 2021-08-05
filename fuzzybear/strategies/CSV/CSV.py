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

MAX_ROWS = 100
MAX_COLUMNS = 100
ENTRIES_THRESHOLD = 10


# def ui_event(event, boost=10):
#     Strategy.ui_event(event, boost)


# random row & column number
# within the size of csv
def random_row_col(range):
	a, b = range
	return (randint(1, a), randint(1, b))


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

		self.size = (len(self.candidate_input) - 1, 
					len(self.candidate_input[0]) - 1)


	def add_entries(self):
		# Generate random number of rows
		# between 0 - 1000
		rows, cols = random_row_col((MAX_ROWS, MAX_COLUMNS))

		candidate = copy.deepcopy(self.candidate_input)
		# TODO :: Fix header preservation
		mutation = [candidate[0]]

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


		mutation = copy.deepcopy(self.candidate_input)
		row, col = random_row_col(self.size)
		for string in super().bad_string():
			mutation[row][col] = string
			yield pack_csv(mutation)
			super().ui_event('bad strings', 10)


'''dev_notes

 + Even tho it matters for some CSVs that the header 
 remains intact we can ignore this as it will eventually
 be resolved by the generator -> unless


 + Things like adding rows and columns could be considered
   a sub strategy because the data that goes into the extra fields
   could also be fuzzed 


+ Currently designed to run in stages where diffrent fuzz cases are applied
 random entries each time 

+ TODO :: Add UI hooks


'''
