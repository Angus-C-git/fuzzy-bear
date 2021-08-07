'''

::::::::::::::::: [TXT] :::::::::::::::::

    ► Generator and mutator for plaintext 

'''
import random
from .. import Strategy
import copy



# class TextFile():
#     def __init__(self, contents):
#         self.contents = contents
#         self.lines = []
#         self.recentMutations = [] # <-- for fuzzing guided by run time introspection
#         for line in self.contents:
#             self.lines.append(line)
#         self.mutations = []


#     def get_line(self, line_num):
#         return self.lines[line_num]

#     def append(self, line):
#         self.lines.append(str(line))


#     def insert(self, pos, line):
#         self.lines.insert(pos, line)
    

#     def prepend(self, line):
#         self.insert(line, 0)


#     def mutateLine(self, lineNum, newLine):
#         # Should have some cooler shit here.
#         self.lines[lineNum] = newLine
    

#     def doubleLineLength(self, lineNum):
#         self.lines[lineNum] *= 2
    

#     def addControlCharacters(self, lineNum, num=3):
#         for i in range(num):
#             randomChar = chr(random.randint(0, 0x20))
#             randomPlace = random.randint(0, len(self.lines)-1)
#             self.lines[lineNum] = self.lines[lineNum][:randomPlace] + randomChar + self.lines[lineNum][randomPlace:]


#     def injectWhiteSpace(self):
#         lineNum = random.randrange(0, len(self.lines))
#         if len(self.lines[lineNum]) == 0: 
#             return
#         posNum  = random.randrange(0, len(self.lines[lineNum]))
#         self.lines[lineNum] = self.lines[lineNum][:posNum] + ' '*lineNum + self.lines[lineNum][posNum:]
        

#     def injectBlankLines(self):
#         lineNum = random.randrange(0, len(self.lines))
#         self.lines.insert(lineNum, '\n\n\r\n   \n\n  \n\r')
#         self.lines.insert(lineNum, '')


#     def remove(self, pos):
#         # Might want to return an error code.
#         self.lines.remove(self.lines[pos])

#     def removeSpecificLine(self, line):
#         # Might want to return an error code.
#         self.lines.remove(line) 
    

#     def __str__(self):
#         ret = ""
#         for l in self.lines:
#             ret += l
#         return ret


def pack_txt(data):
	""" pack csv list into string """
	return "".join(data)


class TXT(Strategy.Strategy):

    def __init__(self, sample_input):
        super()
        try:
            with open(sample_input) as f:
                self.candidate_input = f.readlines()
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

        mutation = copy.deepcopy(self.candidate_input)
        # inject blank lines
        
        mutation = copy.deepcopy(self.candidate_input)
        # inject white space

        # append system words to candidate input
        mutation = copy.deepcopy(self.candidate_input)
        for sysword in super().system_words(): 
            mutation.append(sysword)
            yield pack_txt(mutation)

        # mutation = copy.deepcopy(self.textfile)
        # if randCounter == 2:
        #     mutation.injectWhiteSpace()
        #     yield str(mutation)

        # if randCounter == 9:
        #     mutation.injectBlankLines()
        #     yield str(mutation)


        # xor each character in input
        # randNum = random.randrange(0, len(self.textfile.lines))
        mutation = copy.deepcopy(self.candidate_input)
        for line in range(len(mutation)):
            mutation.append(super().xor_data(mutation[line]))
            yield pack_txt(mutation)


'''devnotes
- I basically just do random shit in the run method. Will definitely need to be more heuristic
in order to find more obscure bugs.
'''
