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

'''
 Log Summary Of Fuzzing Campaign To Console
 '''


def render_summary(campaign_data):
    """ render summary table """
    summary_table = Table(
        box=box.SIMPLE_HEAVY,
        collapse_padding=True,
        padding=(1, 40),
        pad_edge=False,
    )

    # Display Title
    summary_table.add_column(
        "[b]Campaign Summary [/b]",
        justify="left",
        no_wrap=True,
    )
    summary_table.add_column(" ", justify="left", no_wrap=True)

    summary_table.add_row(
        "[b]‣ :zap: Unique Crashes",
        campaign_data["unique_crashes"]
    )
    summary_table.add_row(
        "[b]‣ :atom_symbol:  Total Crashes",
        campaign_data["total_crashes"]
    )
    summary_table.add_row(
        "[b]‣ :hourglass_done: Total Hangs",
        campaign_data["hangs"]
    )
    summary_table.add_row(
        "[b]‣ :world_map:  Explored Codepaths",
        campaign_data["codepaths"]
    )
    summary_table.add_row(
        "[b]‣ :scales:  Coverage",
        campaign_data["coverage"]
    )
    summary_table.add_row(
        "[b]‣ :watch: Total Fuzzing Time",
        campaign_data["runtime"]
    )

    # padding top
    console.print('\n')
    console.print(summary_table, justify="left")


"""devnotes

 - TODO - 

 + connect other stats

"""
