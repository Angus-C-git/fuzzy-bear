import subprocess

'''
::::::::::::::::: [Harness] :::::::::::::::::

    ► Sends data from the aggregator || or strategy
      handler to the binary
    ► Watches/Catches responses from the binary
      and sends them to the aggregator

'''


class Harness():
  def __init__(self, binary):
    self.binary = binary

  def open_pipe(self, data):
    with subprocess.Popen(
          self.binary,
          stdin  = subprocess.PIPE,
          stdout = subprocess.PIPE,
          stderr = subprocess.PIPE
    ) as pipe:
                    
      # send data as bytes to pipe
      pipe.communicate(data.encode())
      return pipe.returncode
