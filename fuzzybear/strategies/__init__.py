# Forgive me lord

from .CSV import CSV
from .ELF import ELF
from .JPEG import JPEG
from .JSON import JSON
from .PDF import PDF
from .TXT import TXT
from .XML import XML


def get_generator(codec, sample_input):

    _generators = {
        'csv': CSV.CSV(sample_input),
        'elf': ELF.ELF(sample_input),
        'jpeg': JPEG.JPEG(sample_input),
        # 'json': JSON.JSON(sample_input),          # TODO :: merge json branch to fix
        'pdf': PDF.PDF(sample_input),
        'plain': TXT.TXT(sample_input),
        'octet-stream': TXT.TXT(sample_input),      # detects plaintext3 as octet-stream
        'html': XML.XML(sample_input)               # detects xml as html
    }

    return _generators[codec]
