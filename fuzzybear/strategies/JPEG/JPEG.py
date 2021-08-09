from .. import Strategy
import sys
import random
from pexpect import run
from pipes import quote


def debug(input, fuzzcase):
    """ debugging method writes 
    generated jpg to file"""
    f = open('origfile.jpeg', 'wb')
    f.write(input)

    f = open('fuzzcase.jpeg', 'wb')
    f.write(fuzzcase)



class JPEG(Strategy.Strategy):
    
    def __init__(self, sample_input):
        self.data = sample_input
        self.original_input = self.data
        self.parse_input()


    def parse_input(self):
        """ read bytes from our valid JPEG and return 
        them in a mutable bytearray """
        f = open(self.data, "rb").read()
        self.data = bytearray(f)


    def fuzz(self, data):
        """ attack data section """
        num_of_flips = int((len(data) - 4) * 0.0001)
        indexes = range(0x550, len(data) - 4)

        chosen_indexes = []

        # iterate selecting indexes until we've hit our num_of_flips number
        for i in range(0, num_of_flips):
            chosen_indexes.append(random.choice(indexes))
        # bytearray version
        newdata = data[:]
        chosen_indexes = chosen_indexes[:1]
        for x in chosen_indexes:
            if (0xFF in data[x-10:x+10]):
                continue
            current = data[x]
            target = random.choice(range(0,8))
            bit_flipper = 0b1 << target
            newdata[x] = current ^ bit_flipper

        return bytes(newdata)

    '''
    def very_specific_fuzz(self, data):
        markers = []
        count = 0
        for x in data:
            if (x == 0xFF):
              markers.append(count)
            count += 1
        
        target_index = markers[6]#random.choice(markers)
        #print(target_index)
        newdata = data[:]
        if (target_index < len(data) - 8):
            #size = data[target_index + 2] * 16**2 + data[target_index + 3]
            #print(hex(size))
            #i = target_index + 4
            #index = size
            #while(index > 0):
            #    newdata[i] = 0x00
            #    index -= 1
            #    i += 1
            #print(hex(newdata[target_index + 6]))
            newdata[target_index + 8] = 0x01#random.choice(range(0x00,0xFF))
            #newdata[target_index + 10] = 0x10#random.choice(range(0x00,0xFF))
        
        return bytes(newdata)
    '''

    def magic(self, data, index=None):
        """ attack magic bytes """
        newdata = data[:]
        magic_bytes = [
			[0xFF],
			[0x7F],
			[0x00],
			[0xFF, 0xFF],
			[0x00, 0x00],
			[0xFF, 0xFF, 0xFF, 0xFF],
			[0x00, 0x00, 0x00, 0x00],
			[0x80, 0x00, 0x00, 0x00],
			[0x40, 0x00, 0x00, 0x00],
			[0x7F, 0xFF, 0xFF, 0xFF]
		]
        if (index == None):
            selection = random.choice(magic_bytes)
        else:
            selection = magic_bytes[index]
        index = 50
        while(0xFF in data[index-50:index+50]):
            index = random.choice(range(50, len(data) - 50))

        count = 0
        for element in selection:
            newdata[index + count] = element
            count += 1
        return bytes(newdata)
        

	# create new jpg with mutated data
    def run(self):        
        # debug(self.data, self.fuzz(self.data))
        # debug(self.data, self.magic(self.data))
        yield self.fuzz(self.data)
        yield self.magic(self.data)
        