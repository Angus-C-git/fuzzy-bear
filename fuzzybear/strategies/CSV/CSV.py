'''
CSV strategy driver Class

    ► Generates strategies for csv based 
      inputs
'''
from .. import Strategy
import csv



# random row number 10 - 1000



class CSV(Strategy.Strategy):
    
    # parse csv input data
    def __init__(self, sample_input):
        super()
        self.raw_data = csv.reader(sample_input)
        print(self.raw_data)

    

    

