'''
BASE CLASS

Default broad strategy for fuzzing that supplies bad strings by default.

    ► Other strategy classes inherit from this base class 
    ► Implements default methods like bitshifting, flipping and non data/format 
      specific operations 
    ► Inherit this class to build others

'''

class Strategy():
  def __init__(self) -> None:
      pass

