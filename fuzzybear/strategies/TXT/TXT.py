'''

::::::::::::::::: [TXT] :::::::::::::::::

    ► Generator and mutator for plaintext 

'''
import random
from .. import Strategy
'''
class TextFileInputGenerator(Strategy.Strategy, Strategy.Integers):
    def __init__(self):
        Strategy.Strategy.__init__(self)
        Strategy.Integers.__init__(self)
'''


class TextFile():
    def __init__(self, contents):
        self.contents = contents
        self.lines = []
        self.recentMutations = [] # <-- for fuzzing guided by run time introspection
        for line in self.contents:
            self.lines.append(line)
        self.mutations = []
    
    def append(self, line):
        self.lines.append(str(line))

    def insert(self, pos, line):
        self.lines.insert(pos, line)
    
    def prepend(self, line):
        self.insert(line, 0)

    def mutateLine(self, lineNum, newLine):
        # Should have some cooler shit here.
        self.lines[lineNum] = newLine
    
    def doubleLineLength(self, lineNum):
        self.lines[lineNum] *= 2

    def extendLine(self, lineNum, length):
        pass

    def addControlCharacters(self, lineNum, num=3):
        for i in range(num):
            randomChar = chr(random.randint(0, 0x20))
            randomPlace = random.randint(0, len(self.lines)-1)
            self.lines[lineNum] = self.lines[lineNum][:randomPlace] + randomChar + self.lines[lineNum][randomPlace:]

    def injectWhiteSpace(self):
        lineNum = random.randrange(0, len(self.lines))
        if len(self.lines[lineNum]) == 0: 
            return
        posNum  = random.randrange(0, len(self.lines[lineNum]))
        self.lines[lineNum] = self.lines[lineNum][:posNum] + ' '*lineNum + self.lines[lineNum][posNum:]
        

    def injectBlankLines(self):
        lineNum = random.randrange(0, len(self.lines))
        self.lines.insert(lineNum, '\n\n\r\n   \n\n  \n\r')
        self.lines.insert(lineNum, '')

    def bitFlip(self, s):
        pass 

    def remove(self, pos):
        # Might want to return an error code.
        self.lines.remove(self.lines[pos])

    def removeSpecificLine(self, line):
        # Might want to return an error code.
        self.lines.remove(line) 
    
    def updateRecentMutation(self, mutation):
        # some sort of logging logic
        pass

    def __str__(self):
        ret = ""
        for l in self.lines:
            ret += l
        return ret


class TXT(Strategy.Strategy):

    def __init__(self, sample_input):
        Strategy.Strategy.__init__(self)
        try:
            with open(sample_input) as f:
                self.textfile = TextFile(f.readlines())
        except e:
            # propper error logic goes here.
            print('errrooooooooor')
            raise e

    def run(self):
        randCounter = random.randrange(0, 10)
        self.textfile.append(next(self.string('overflow')))
        yield str(self.textfile)

        randNum = random.randrange(0, len(self.textfile.lines))
        self.textfile.mutateLine(randNum, next(self.string('badchars', 200)))
        yield str(self.textfile)

        if randCounter == 7:
            randNum = random.randrange(0, len(self.textfile.lines))
            self.textfile.doubleLineLength(randNum)
            yield str(self.textfile)

        for i in range(5):
            randNum = random.randrange(0, len(self.textfile.lines))
            self.textfile.addControlCharacters(randNum, 10)
        yield str(self.textfile)

        self.textfile.append(next(self.string('fuzz', 1000)))
        yield str(self.textfile)

        if randCounter == 2:
            self.textfile.injectWhiteSpace()
            yield str(self.textfile)

        if randCounter == 9:
            self.textfile.injectBlankLines()
            yield str(self.textfile)

'''devnotes
- I basically just do random shit in the run method. Will definitely need to be more heuristic
in order to find more obscure bugs.
'''
