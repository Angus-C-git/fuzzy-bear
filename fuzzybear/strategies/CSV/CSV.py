'''
CSV strategy driver Class

    ► Generates strategies for csv based 
      inputs
'''
from .. import Strategy
from  csv import reader
from random import randint


'''
Utility methods for CSV 
strategies
'''

# random row & column number
# within the size of csv
def random_row_col(range):
    a, b = range
    return (randint(0, a), randint(0, b))


def pack_csv(data):
   return "\n".join((",".join(row_col) for row_col in data))



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
        rows, cols = random_row_col((100, 100))
        # TODO :: Fix header
        mutation = [self.candidate_input[0]]
        print('\n\n', mutation)
        for row in range(1, rows):
            new_row = []
            for col in range(1, cols):
                new_row.append(str(col * row))     # could be anything really 
            
            mutation.append(new_row)

        return mutation

    # run strategies
    def run(self):
        print(f"\n[DEBUG] mutating {self.candidate_input} \n")        

        row, col = random_row_col(self.size)
        mutation = self.candidate_input
        for emoji in super().emoji():
            mutation[row][col] = emoji   
            # print(mutation) 
            yield pack_csv(mutation)
        
        row, col = random_row_col(self.size)
        for chonk in super().chonk():
            mutation[row][col] = chonk
            yield pack_csv(mutation)

        yield pack_csv(self.add_entries())


'''dev_notes

 + Even tho it matters for some CSVs that the header 
 remains intact we can ignore this as it will eventually
 be resolved by the generator 

'''