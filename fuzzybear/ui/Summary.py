from rich import box
from rich.console import Console, RenderGroup
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.measure import Measurement
from rich.live import Live
from time import sleep

console = Console()

""" Log Summary Of Fuzzing Campagin To Console """



"""devnotes

+ Rough plan:
    + Display table with results from stats after writing
      bad.txt
    + Note the crashing strategy

"""