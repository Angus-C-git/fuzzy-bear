""""
CSV strategy driver Class

	► Generates strategies for csv based 
	  inputs
"""
from .. import Strategy
from  csv import reader
from random import randint
import copy


# config
MAX_ROWS = 1000
MAX_COLUMNS = 1000
ENTRIES_THRESHOLD = 10


# def ui_event(event, boost=10):
#     Strategy.ui_event(event, boost)



def random_row_col(range):
	""" selects a random row and column with respect to size """
	a, b = range
	return (randint(0, a - 1), randint(0, b - 1))


def pack_csv(data):
	""" pack csv list into string """
	return "\n".join((",".join(row_col) for row_col in data))


class CSV(Strategy.Strategy):
	
	def __init__(self, sample_input):
		super()
		self.sample_input = sample_input
		self.parse_csv()


	def parse_csv(self):
		""" parse csv candidate file """
		with open(self.sample_input) as csvfile:
			self.candidate_input = list(reader(csvfile))

		self.size = (len(self.candidate_input), 
					len(self.candidate_input[0]))


	def add_entries(self, preserve_header=False):
		""" adds extra entries to csv file in a random range """
		rows, cols = random_row_col((MAX_ROWS, MAX_COLUMNS))

		candidate = copy.deepcopy(self.candidate_input)
		mutation = [candidate[0]] if preserve_header else candidate

		for row in range(1, rows):
			new_row = []
			for col in range(1, cols):
				# add some value
				new_row.append(str(col * row))     

			mutation.append(new_row)

		super().ui_event('additional rows', 10)
		return mutation


	def run(self):     
		""" run the CSV generator """
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


"""dev_notes

+ Currently designed to use mostly random based mutations coupled with close input 
  based mutations using field manipulation
"""
