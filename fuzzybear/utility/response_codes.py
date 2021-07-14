
response_codes = {
    0: 'normal exit',
    -11: 'segfault',
    

    '-': 'no such code'
}


def lookup(response_code):
    try: return response_codes[response_code]
    except: return response_codes['-']

