#!/usr/bin/env python3

from .. import Strategy
import sys
import random

class JPEG(Strategy.Strategy):
    
    # parse ___ input data
    def __init__(self, sample_input):
        self.data = sample_input
        self.parse_input()

    # read bytes from our valid JPEG and return them in a mutable bytearray 
    def parse_input(self):
        
        f = open(self.data, "rb").read()
        self.data = bytearray(f)

    def fuzz(self, data):

        num_of_flips = int((len(data) - 4) * 100)

        indexes = range(4, (len(data) - 4))

        chosen_indexes = []

        # iterate selecting indexes until we've hit our num_of_flips number
        for i in range(0, num_of_flips):
            chosen_indexes.append(random.choice(indexes))

        for x in chosen_indexes:
            current = (bin(data[x]).replace("0b",""))
            current = "0" * (8 - len(current)) + current
            indexes = range(0,8)
            target = random.choice(indexes)
            new_number = []

            # our new_number list now has all the digits, example: ['1', '0', '1', '0', '1', '0', '1', '0']
            for i in current:
                new_number.append(i)

            # if the number at our randomly selected index is a 1, make it a 0, and vice versa
            if new_number[target] == "1":
                new_number[target] = "0"
            else:
                new_number[target] = "1"

            # create our new binary string of our bit-flipped number
            current = ''
            for i in new_number:
                current += i

            current = int(current,2)
            data[x] = current

        output = ""
        for x in data:
            output += bin(x)
            
        return output

    def magic(self, data, index=None):

        magic_vals = [
			(1, 255),
			(1, 255),
			(1, 127),
			(1, 0),
			(2, 255),
			(2, 0),
			(4, 255),
			(4, 0),
			(4, 128),
			(4, 64),
			(4, 127)
		]
        if (index == None):
            selection = random.choice(magic_vals)
        else:
            selection = index

        length = len(data) - 8
        index = random.choice(range(0, length))

        if (selection[0] == 4 and selection[1] != 0 and selection[1] != 255):
            if (selection[1] == 128):	# 0x80000000
                data[index] = 128
                data[index + 1] = 0
                data[index + 2] = 0
                data[index + 3] = 0
            elif selection[1] == 64:   # 0x40000000
                data[index] = 64
                data[index + 1] = 0
                data[index + 2] = 0
                data[index + 3] = 0
            elif selection[1] == 127:# 0x7FFFFFFF
                data[index] = 127
                data[index + 1] = 255
                data[index + 2] = 255
                data[index + 3] = 255
        else:
            for i in range(0,selection[0]):
                data[index + i] = selection[1]
        
        output = ""
        for x in data:
            output += bin(x)

        return output

	# create new jpg with mutated data
    def run(self):
        yield self.fuzz(self.data)
        yield self.magic(self.data)
