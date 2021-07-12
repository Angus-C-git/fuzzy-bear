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