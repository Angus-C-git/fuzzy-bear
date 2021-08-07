#!/usr/bin/env python3

from .. import Strategy
import sys
import random
from pexpect import run
from pipes import quote

class JPEG(Strategy.Strategy):
    
    # parse ___ input data
    def __init__(self, sample_input):
        self.data = sample_input
        self.original_input = self.data
        self.parse_input()

    # read bytes from our valid JPEG and return them in a mutable bytearray 
    def parse_input(self):
        
        f = open(self.data, "rb").read()
        self.data = f
        #self.data = bytearray(f)

    def fuzz(self, data):

        num_of_flips = int((len(data) - 4) * 0.01)

        indexes = range(32, (len(data) - 4))

        #chosen_indexes = []
        index_bits = {}

        # iterate selecting indexes until we've hit our num_of_flips number
        for i in range(0, num_of_flips):
            #chosen_indexes.append(random.choice(indexes))
            index_bits[str(random.choice(indexes))] = 0

        # bytearray version
        #for x in chosen_indexes:
        for x in index_bits:
            current = data[x]
            target = random.choice(range(0,8))
            bit_flipper = 0b1 << target
            #data[x] = current ^ bit_flipper
            index_bits[x] = current ^ bit_flipper

        first = 4
        last = 4
        output = data[:32]
        for i in range(32, len(data) - 4):
            last = i
            if (str(i) in index_bits):
                output += data[first:last] + index_bits[str(i)]
                first = i
        output += data[first:last] + data[len(data) - 4:]
            
        #return bytes(data)
        return output

    def magic(self, data, index=None):

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
            selection = index

        index = random.choice(range(32, len(data) - 4))
        
        output = data[:index]
        count = 0
        for element in magic_bytes[selection]:
            #data[index + count] = element
            output += bytes(element)
            count += 1

        output += data[index + count:]
        #return bytes(data)
        return output
        

	# create new jpg with mutated data
    def run(self):

        #yield self.original_input
        for i in range(0, 10):
            yield self.magic(self.data, i)
        for i in range(0, 10):
            yield self.fuzz(self.data)
        '''
        counter = 0
        while counter < 100000:
            picked_function = random.randint(0,2)
            if picked_function == 0:
                mutated = self.magic(self.data)
                self.create_new(mutated)
                self.exif(counter,mutated)
            else:
                mutated = self.fuzz(self.data)
                self.create_new(mutated)
                self.exif(counter,mutated)
            counter += 1
        '''
    '''
        # create new jpg with mutated data
    def create_new(self, data):

        f = open("mutated.jpeg", "wb+")
        f.write(self.data)
        f.close()

    def exif(self, counter, data):

        command = "cat mutated.jpeg > ./tests/complete/jpg1 -verbose"

        out, returncode = run("sh -c " + quote(command), withexitstatus=1)
        if b'Seg' in out:
            print(out)
            f = open("crashes/crash.{}.txt".format(str(counter)), "wb+")
            f.write(data)

        if (counter % 100 == 0):
            print(counter)

    '''