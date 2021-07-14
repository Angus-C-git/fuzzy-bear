from random import randint
from pwn import cyclic

'''
BASE CLASS

	► Other strategy classes inherit from this base class to build new strats
	► Implements default methods like bitshifting, flipping and non data/format 
	  specific operations 
	► Inherit this class to build other strategies 

'''

class Strategy():
	
	def __init__(self):
		return

	def emoji(self):
		yield '🏴‍☠️'
		yield '🔥'
		yield '👌'
		yield '😂'
		
	def chonk(self):
		yield 'A' * 50		
		yield 'A' * 500
		yield 'A' * 600
		yield 'A' * 700
		yield 'A' * 1000
		yield 'A' * 10000


	def keywords(self):
	  yield 'input'		# no this isn't a hardcoded value whattt
	  yield 'data'
	  yield 'len'  
	  

	def string(self, arg='all'):
		strings = String().genStrings(arg)
		for x in strings:
			#print(f'x = {x}')
			yield x

	

'''
STRING CLASS

	► Implemented in Base Class
	► String related arguments taken:
		'badchars', 'printf', 'overflow', 'shellstuff'

'''
class String():
	def __init__(self) -> None:
		self.printfstrs = "diouxXeEfFgGaAcspnm"
		self.printlmod = ["", "hh", 'h', 'l', 'll', 'L', 'j', 'z', 't']

	def genStrings(self, type='all'):
		strings = []

		if (type == 'all'):
			for i in range(0, 4):
				strings.append(self.fuzz(0x10**i))
		if (type == 'all' or type == 'badchars'):
			strings.append(self.badchars())
		if (type == 'all' or type == 'printf'):
			strings = self.printf(strings)
		if (type == 'all' or type == 'overflow'):
			strings = self.overflow(strings)
		if (type == 'all' or type == 'shellstuff'):
			strings = self.shellstuff(strings)

		return strings

	def fuzz(self, num=100, lowerasciibound=0, upperasciibound=128, chars=[]):
		output = ''
		for i in range (0,num):
			output += chr(randint(lowerasciibound,upperasciibound))
		return output

	def badchars(self):
		string = ""
		for i in range(0,128):
			string += chr(i)
		return string

	def printf(self, arr):
		for a in self.printfstrs:
			for b in self.printlmod:
				string = f'%{b}{a}'
				arr.append(string)
		return arr

	def overflow(self, arr):
		base = 0x10
		while (base < 0xFFFFF):
			arr.append(cyclic(base))
			base *= 0x10
		return arr

	def shellstuff(self, arr):
		stuff = ['../', '/bin/sh', '&&', '>>', '|', 'fork', 'brk', 'execve']
		for x in stuff:
			arr.append(x)
		return arr
