
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

