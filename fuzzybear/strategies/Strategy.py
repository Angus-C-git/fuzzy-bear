
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