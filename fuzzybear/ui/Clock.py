from datetime import datetime
from time import time, sleep


'''
::::::::::::::::: [UI:Clock] :::::::::::::::::

    ► Tracks the time for the lifespan of 
      the fuzzing campaign and returns a
      renderable string.

'''




class Clock():
    
    
    def __init__(self):
        self.start_time = time()

    
    def get_time(self):
        """
        Return the time the log was 
        emitted 
        """
        current_runtime = time() - self.start_time
        mins = int(current_runtime // 60)
        secs = int(current_runtime % 60)
        hours = int(mins // 60)
        return f'{hours}:{mins:02d}:{secs:02d}'
