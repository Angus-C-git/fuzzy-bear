'''

::::::::::::::::: [TXT] :::::::::::::::::

    ► Generator and mutator for plaintext 

'''
import random
from .. import Strategy
import copy

#config
PREPEND = 0

# helpers

def pack_txt(data):
	""" pack csv list into string """
	return "".join(data)


def pack_stream(bytes):
	""" pack csv list into string """
	return "".join(map(chr, bytes))


def values():
    v = 1
    for i in range(8):
        yield v
        v <<= 1
    # if the value is beyond 8 yield 0xff
    yield 0xFF


def xor_bytes(bytes, index, value):
    prev_byte = bytes[index]
    bytes[index] ^= value
    yield pack_stream(bytes)
    bytes[index] = prev_byte


def add_control_chars(lines, lineNum, num=10):
    for i in range(num):
        randomChar = chr(random.randint(0, 0x20))
        randomPlace = random.randint(0, len(lines)-1)
        lines[lineNum] = lines[lineNum][:randomPlace] + randomChar + lines[lineNum][randomPlace:]    
    return lines


def inject_white_space(lines):
    lineNum = random.randrange(0, len(lines))
    if not len(lines[lineNum]): return
    posNum  = random.randrange(0, len(lines[lineNum]))
    lines[lineNum] = lines[lineNum][:posNum] + ' '*lineNum + lines[lineNum][posNum:]
    return lines


def inject_blank_lines(lines):
    lineNum = random.randrange(0, len(lines))
    lines.insert(lineNum, '\n\n\r\n   \n\n  \n\r')
    lines.insert(lineNum, '')
    return lines



class TXT(Strategy.Strategy):

    def __init__(self, sample_input):
        super()
        try:
            with open(sample_input) as f:
                self.candidate_input = f.readlines()
        
            self.fuzzcases = super().strategy_cases

            num_lines = len(self.candidate_input)

            # register ui events for used fuzzcases
            self.ui_events = {
                'chonk': [0, self.fuzzcases['chonk']],
                'format strings': [0, self.fuzzcases['format_strings']],
                '2x length': [0, num_lines],
                'controll characters': [0, num_lines],
                'newlines': [0, num_lines],
                'blank space': [0, num_lines],
                'system words': [0, self.fuzzcases['system_words']],
                'xor': [0, (num_lines * 4) + 9],
                'polyglots': [0, (self.fuzzcases['polyglots'] * 3)],
                'constants': [0, self.fuzzcases['constants']],
                'large negatives': [0, (self.fuzzcases['large_negatives'])],
                'large positives': [0, self.fuzzcases['large_positives']],
            }

        except FileNotFoundError as err:
            # propper error logic goes here.
            print(f' [>>] File not found, {err}')
            exit(0)


    def run(self):
        """ run TXT generator """
        mutation = copy.deepcopy(self.candidate_input)
        for chonk in super().chonk():
            mutation.append(chonk)
            yield pack_txt(mutation)

        # append format strings to input
        for fmtstring in super().format_strings():
            mutation = copy.deepcopy(self.candidate_input)
            mutation.append(fmtstring) 
            yield pack_txt(mutation)
        
        mutation = copy.deepcopy(self.candidate_input)
        # double line length
        for line in range(len(mutation)):
            mutation[line] *= 2
            yield pack_txt(mutation)

        mutation = copy.deepcopy(self.candidate_input)
        # add control characters
        for line in range(len(mutation)):
            mutation = add_control_chars(mutation, line)
            yield pack_txt(mutation)

        mutation = copy.deepcopy(self.candidate_input)
        # inject blank lines
        for line in range(len(mutation)):
            mutation = inject_blank_lines(mutation)
            yield pack_txt(mutation)
        
        mutation = copy.deepcopy(self.candidate_input)
        # inject white space
        for line in range(len(mutation)):
            mutation = inject_white_space(mutation)
            yield pack_txt(mutation)
        
        # append system words to candidate input
        for sysword in super().system_words(): 
            mutation = copy.deepcopy(self.candidate_input)
            mutation.append(sysword)
            yield pack_txt(mutation)

        # xor parts of input file
        mutation = copy.deepcopy(self.candidate_input)
        for line in range(len(mutation)):
            mutation.append(super().xor_data(mutation[line]))
            yield pack_txt(mutation)
        
        mutation = copy.deepcopy(self.candidate_input)
        for line in range(len(mutation)):
            # append on newline
            mutation[line] = (super().xor_data(mutation[line]) + '\n')
            yield pack_txt(mutation)
            mutation = copy.deepcopy(self.candidate_input)

        mutation = copy.deepcopy(self.candidate_input)
        for line in range(len(mutation)):
            # prepend
            mutation.insert(PREPEND, super().xor_data(mutation[line]))
            yield pack_txt(mutation)

        stream = list(pack_txt(copy.deepcopy(self.candidate_input)).encode())
        for line in range(len(stream)):
            # byte by byte
            for value in values():
                for mutation in xor_bytes(stream, line, value):
                    yield mutation

        # append polyglots
        for polyglot in super().polyglots():
            mutation = copy.deepcopy(self.candidate_input)
            mutation.append(polyglot)
            yield pack_txt(mutation)

        for polyglot in super().polyglots():
            mutation = copy.deepcopy(self.candidate_input)
            for line in range(len(mutation)):
                # append on newline
                mutation[line] = polyglot + '\n'
                yield pack_txt(mutation)
        
        for polyglot in super().polyglots():
            mutation = copy.deepcopy(self.candidate_input)
            mutation.insert(PREPEND, polyglot)
            yield pack_txt(mutation)

        # append max constants
        for negative in super().max_constants():
            mutation = copy.deepcopy(self.candidate_input)
            for line in range(len(mutation)):
                mutation = copy.deepcopy(self.candidate_input)
                mutation[line] = negative + '\n'
                yield pack_txt(mutation)

        # append large negatives
        for negative in super().large_negatives():
            mutation = copy.deepcopy(self.candidate_input)
            for line in range(len(mutation)):
                mutation = copy.deepcopy(self.candidate_input)
                mutation[line] = negative + '\n'
                yield pack_txt(mutation)

        # append large positives
        for big_int in super().large_positives():
            mutation = copy.deepcopy(self.candidate_input)
            for line in range(len(mutation)):
                mutation = copy.deepcopy(self.candidate_input)
                mutation[line] = big_int + '\n'
                yield pack_txt(mutation)


'''devnotes
- Mostly tries random strategies or systematically mutates each line
'''
