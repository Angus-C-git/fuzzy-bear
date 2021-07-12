# Forgive me lord

from .CSV import CSV
from .ELF import ELF
from .JPEG import JPEG
from .JSON import JSON
from .PDF import PDF
from .TXT import TXT
from .XML import XML

'''
Resolves a particular codec to a supported
generator or returns none if the appropriate
generator cannot be found.
'''
def get_generator(codec, sample_input):

    _generators = {
        'csv': CSV.CSV,
        'elf': ELF.ELF,
        'jpeg': JPEG.JPEG,
        'json': JSON.JSON,              
        'pdf': PDF.PDF,
        'plain': TXT.TXT,
        'octet-stream': TXT.TXT,       # detects plaintext3 as octet-stream
        'html': XML.XML,               # detects xml as html
        'xml': XML.XML
    }

    try: 
        return _generators[codec](sample_input)
    except KeyError: return None