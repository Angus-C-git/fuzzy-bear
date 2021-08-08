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
        #elf.data = f
        self.data = bytearray(f)

    def fuzz(self, data):

        num_of_flips = int((len(data) - 4) * 0.0001)
        indexes = range(0x550, len(data) - 4)

        chosen_indexes = []
        #index_bits = {}

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

            #print(f'Original: {bin(data[x])}\nFinal: {bin(newdata[x])}')

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
        #print(selection)
        #print(len(data))
        index = 50
        while(0xFF in data[index-50:index+50]):
            index = random.choice(range(50, len(data) - 50))
        
        #output = data[:index]
        count = 0
        for element in selection:
            newdata[index + count] = element
            #output += bytes(element)
            count += 1

        #output += data[index + count:]
        return bytes(newdata)
        #return output
        

	# create new jpg with mutated data
    def run(self):

        
        #yield self.data
        #yield self.magic(self.data)
        #f = open('origfile.jpeg', 'wb')
        #f.write(self.data)
        #f = open('new.jpeg', 'wb')
        #fuzz = self.fuzz(self.data)
        #f.write(fuzz)
        yield self.fuzz(self.data)
        yield self.magic(self.data)
        
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