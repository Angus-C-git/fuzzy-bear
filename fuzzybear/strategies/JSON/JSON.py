'''
CSV strategy driver Class
    ► Generates strategies for csv based 
      inputs
'''
from .. import Strategy
import json
from random import randint


# random row & column number
# within the size of csv
def random_row_col(range):
    a, b = range
    return (randint(0, a), randint(0, b))


def pack_csv(data):
   return "\n".join((",".join(row_col) for row_col in data))


#insert a row

#insert data at random place

#insert data for certain key

#insert key for certain value

#packing function post insertion not needed python has
#a converting function  

"""
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


    # run strategies
    def run(self):
        print(f"\n[DEBUG] mutating {self.candidate_input} \n")        

        row, col = random_row_col(self.size)
        mutation = self.candidate_input
        for emoji in super().emoji():
            mutation[row][col] = emoji   
            # print(mutation) 
            yield pack_csv(mutation)
"""       
            