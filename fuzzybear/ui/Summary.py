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

""" Log Summary Of Fuzzing Campaign To Console """

def render_summary(campaign_data):
	""" render summary table """
	summary_table = Table(
						#title="Campaign Summary", 
						box=box.SIMPLE_HEAVY,
						collapse_padding=True,

					)

	# Display Title
	summary_table.add_column(
		"[b] Campaign Summary [/b]", 
		justify="left", 
		no_wrap=True
	)
	summary_table.add_column(" ")

	summary_table.add_row("‣ Crashing Strategy", campaign_data["crashing_strategy"])
	summary_table.add_row("‣ Total Hangs", campaign_data["hangs"])
	summary_table.add_row("‣ Explored Codepaths", campaign_data["codepaths"])
	summary_table.add_row("‣ Coverage", campaign_data["coverage"])
	summary_table.add_row("‣ Total Fuzzing Time", campaign_data["runtime"])	


	console.print(summary_table, justify="left")


"""devnotes

+ Rough plan:
    + Display table with results from stats after writing
      bad.txt
    + Note the crashing strategy

"""