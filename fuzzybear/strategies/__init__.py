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
        'csv': CSV.CSV(sample_input)
    }

    return _generators[codec]
