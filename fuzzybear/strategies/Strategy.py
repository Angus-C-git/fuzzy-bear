from random import randint, randrange
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
	  

	def negate(self, data):
		try:
			yield data * -1
		except TypeError:
			try:
				yield '-' + data if ('-' not in data) else data.strip('-')
			except TypeError:
				yield data


	def string(self, arg='all'):
		strings = String().genStrings(arg)
		for x in strings:
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


class Integers():
	#MAGIC NUMBERS :) (UNSIGNED)
	CHAR_MAX = 255
	INT_MAX  = 4294967295
	INT_MAX_SIGNED = 2147483648
	BYTE_8_MAX = 18446744073709551615
	#number of ints gen:
	def __init__(self, gen_max):
		self.gen_max = gen_max

	#Returns a list ofrandom integers for a particular range
	def range(self, lower, upper):
		int_list = []
		for i in range(0, self.gen_max):
			num = randrange(lower, upper)
			if(num in int_list):
				i -= 1
			else:
				int_list.append(num)
		return int_list

	def rand_positive(self):
		int_list = []
		for i in range(0, self.gen_max):
			num = randint(0 , Integers.INT_MAX_SIGNED)
			int_list.append(num)
		#SOMETHING SHOULD BREAK IF THESE NUMBER ARE ENTERED :)
		int_list.append(Integers.INT_MAX)
		int_list.append(Integers.BYTE_8_MAX)
		return int_list

	def rand_negative(self):
		int_list = []
		for i in range(0, self.gen_max):
			num = randint(-Integers.INT_MAX_SIGNED, 0)
			int_list.append(num)
		int_list.append(0)
		int_list.append(Integers.INT_MAX)
		int_list.append(Integers.BYTE_8_MAX)
		return int_list

	def rand(self):
		int_list = []
		for i in range(0, self.gen_max):
			num = randint(-Integers.INT_MAX_SIGNED, Integers.INT_MAX_SIGNED)
			int_list.append(num)
		int_list.append(Integers.INT_MAX)
		int_list.append(Integers.BYTE_8_MAX)
		return int_list

	# def break(self):
	# 	pass


	class Floats():
		def __init__(self):
			pass

		def rand_float(self):
			pass

		def rand_large(self):
			pass

		def decimal(self):
			pass

		def rand(self):
			pass





'''devnotes

TODO

	- [ ] May need to port the strings class methods into the
	      strategies body since they cannot be used individually
		  at the moment by sub strategies
'''