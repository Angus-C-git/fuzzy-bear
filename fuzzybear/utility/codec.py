'''
This module attempts to determine the format of the 
supplied sample input.
'''
import magic

def detect(file):
    print(f'   [DEBUG] Attempting to resolve codec for {file}')

    mime_type = magic.from_file(file, mime=True)
    print(f'   [DEBUG] Type guess is {mime_type}')
    return mime_type.split('/')[-1]


'''devnotes

TODO

    - [ ] This code will not survive conditions where the
          input file resembles a supported codec but does
          not contain the associated magic number for that
          codec
    - [ ] This will require the implementation of a weighted
          passing algorithm which attempts to determine what
          the best supported format choice is

'''