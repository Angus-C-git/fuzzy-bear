'''
CSV strategy driver Class

    ► Generates strategies for csv based 
      inputs
'''
from .. import Strategy
import csv



class CSV(Strategy):
    
    # parse csv input data
    def __init__(self, sample_input):
        self.raw_data = csv.reader(sample_input)
        print(self.raw_data)



