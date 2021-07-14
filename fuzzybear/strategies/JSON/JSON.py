#!/usr/bin/env python3
from .. import Strategy
import json
import random
from random import randint


def insert(key,value,json_obj):
    json_obj[key] = value

#given a value replace it
def replace_val(find,replace,json_obj):
    for item in json_obj.items():
        if item[1] == find:
            #print(item)
            json_obj[item[0]] = replace
            
# random entry within dictionary
def random_entry(json_obj):
    itt = list(json_obj.items())
    entry = random.choice(itt)
    return entry

def thicc_file(num_entries):
    thiccboi = {}
    for i in range(0,num_entries):
        thiccboi[i] = []

        for l in range(1,50):
            thiccboi[i].append(l)

    return thiccboi


class JSON(Strategy.Strategy):
    
    # parse csv input data
    def __init__(self, sample_input):
        super()
        self.sample_input = sample_input
        print(sample_input)
        with open(sample_input) as jsonfile:
            self.candidate_input = json.load(jsonfile)
        
        self.size = len(self.candidate_input)

    """
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
    """
    # run strategies
    def run(self):
        print(f"\n[DEBUG] mutating {self.candidate_input} \n")        
        
        mutation = self.candidate_input
        rand_entry = random_entry(mutation)

        for emoji in super().emoji():
            if (type(rand_entry[1]) is list): 
                rand_entry[1][0] = emoji
            else:
                mutation[rand_entry[1]] = emoji 

            yield json.dumps(mutation)

        rand_entry_count = randint(1,100)
        mutation = thicc_file(rand_entry_count)
        yield json.dumps(mutation)

    
