from random import randint, randrange
from pwn import cyclic

'''
BASE CLASS

	► Other strategy classes inherit from this base class to build new strats
	► Implements default methods like bitshifting, flipping and non data/format 
	  specific operations 
	► Inherit this class to build other strategies 

	► TODO :: Should be a factory model
'''

GEN_MAX = 100

# tmp UI manager
tmp_cumulative = 0

class Strategy():
	
	CHAR_MAX = 255
	INT_MAX  = 4294967295
	INT_MAX_SIGNED = 2147483648
	BYTE_8_MAX = 18446744073709551615

	def __init__(self):
		return


	def ui_event(self, event, boost=10):
		""" handels triggering strategy progress for UI """
		global tmp_cumulative
		tmp_cumulative += boost
		""" handels triggering strategy progress for UI """
		print(f'   [>>] Updating {event} progress %{tmp_cumulative} done')
		if tmp_cumulative >= 100:
			tmp_cumulative = 0



	def emoji(self):
		""" Meme fuzzcases """
		yield '🏴‍☠️'
		yield '🔥'
		yield '👌'
		yield '😂'


	def chonk(self):
		""" Overflow fuzzcases """
		yield cyclic(100)	
		yield cyclic(500)
		yield cyclic(1000)
		yield cyclic(4000)
		yield cyclic(10000)


	def keywords(self):
		""" Use grammas to fuzz keywords """
		yield 'input'	
		yield 'data'
		yield 'len'
		yield 'trivial'
		yield 'size'
		yield 'length'
		yield 'max'
		yield 'min'  
	  

	def negate(self, data):
		""" Negate the given data """
		try:
			yield data * -1
		except TypeError:
			try:
				yield '-' + data if ('-' not in data) else data.strip('-')
			except TypeError:
				yield data


	def format_strings(self, data='', offset=1):
		""" Format string fuzzcases """
		yield data + '%p'
		yield data + '%n'
		yield data + '%d'
		yield data + '%s'
		yield data + '%x'
		yield data + '%@'
		yield data + '%hn'
		yield data + '%hhn'
		yield data + f'\x00\x00\x00\x01%{offset}$n'
		yield data + f'%99999$hn'
	

	def system_words(self, data='', arg=''):
		""" System keyword fuzzcases """
		yield f'{data}/bin/sh{arg}'
		yield f'{data}/bin/bash{arg}'
		yield f'{data}/bin/zsh{arg}'
		yield f'{data}fork{arg}'
		yield f'{data}exec{arg}'
		yield f'{data}brk{arg}'
		yield f'{data}exit{arg}'
		yield f'{data}>>{arg}'
		yield f'{data}|{arg}'


	def system_paths(self, data=''):
		""" System path fuzzcases """
		yield data + '/dev/null'
		yield data + '/etc/passwd'
		yield data + '/dev/random'
		yield data + '/dev/urandom'
		yield data + '\\..\\..\\'
		yield data + '../' * 25
		yield data + '..%' * 25


	def polyglots(self, data=''):
		""" Polyglot fuzzcases """
		yield data + """javascript:/*--></title></style></textarea></script>
		</xmp><svg/onload='+/"/+/onmouseover=1/+/[*/[]/+alert(1)//'>"""

		yield data + """jaVasCript:/*-/*`/*\`/*'/*"/*%0D%0A%0d%0a*/(/* */oNcliCk=alert() )//
		</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3ciframe/<iframe/oNloAd=alert()//>\x3e""" 

		yield data + """<script>/*<![CDATA[*/alert(1)///*]]>*/</script>"""

		yield data + """${{<%[%'"}}%\""""

		yield data + """'/**/"# -- """

	
	def rand_int_range(self, lower, upper):
		""" Gen random integers in a range """
		int_list = []
		for i in range(0, self.gen_max):
			num = randrange(lower, upper)
			if(num in int_list):
				i -= 1
			else:
				int_list.append(num)
		yield int_list


	def rand_positive(self):
		""" Gen random positive integers """
		int_list = []
		for i in range(0, self.gen_max):
			num = randint(0 , self.INT_MAX_SIGNED)
			int_list.append(num)
		#SOMETHING SHOULD BREAK IF THESE NUMBER ARE ENTERED :)
		int_list.append(self.INT_MAX)
		int_list.append(self.BYTE_8_MAX)
		yield  int_list


	def rand_negative(self):
		""" Gen random negative integers """
		int_list = []
		for i in range(0, self.gen_max):
			num = randint(-self.INT_MAX_SIGNED, 0)
			int_list.append(num)
		int_list.append(0)
		int_list.append(self.INT_MAX)
		int_list.append(self.BYTE_8_MAX)
		yield int_list

	def rand(self):
		""" Gen random integers """
		int_list = []
		for i in range(0, self.gen_max):
			num = randint(-self.INT_MAX_SIGNED, Integers.INT_MAX_SIGNED)
			int_list.append(num)
		int_list.append(self.INT_MAX)
		int_list.append(self.BYTE_8_MAX)
		yield  int_list


	def max_constants(self):
		""" Maximal constant fuzzcases """
		yield '255'
		yield '4294967295'
		yield '2147483648'
		yield '18446744073709551615'


	def xor_data(self, data):
		""" XOR each char in a string """
		return ''.join(chr(ord(char) ^ 0xFF) for char in data)


	def bit_flip(self, data):
		""" Bitflip fuzzcases, expects a integer value """
		try:
			return  ~int(data)
		except:
			print(f"{'':4}[DEBUG] {data} is not a number")
			return data


	def byte_flip(self, data):
		""" Byteflip fuzzcases """
		try:
			return ''.join(chr(~ord(char)) for char in data)
		except:
			return ''.join(str(~ord(char)) for char in data)


