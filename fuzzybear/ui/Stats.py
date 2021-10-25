from rich.text import Text
from rich.panel import Panel
from rich.console import Console, RenderGroup, render_group
from rich.columns import Columns
from rich.table import Table
from rich import print
from rich.spinner import Spinner, SPINNERS

console = Console()


'''stats panel


loader <emoji> < Stat Name >    < Stat Value > 

'''


class Stats():
    def __init__(self, stats):
        self.unique_crashes = 0
        self.total_crashes = 0
        self.total_hangs = 0
        self.explored_paths = 0
        self.average_speed = f'0/s'
        self.net_cycles = 0
        self.last_crash = 'N/A'           # -> [13:14:15]
        self.run_time = '0:00:00'       # -> [0:00:00]

    # TODO connect to UiAdapter
    def update_stats(self, stats):
        pass

    def render(self):
        table = Table.grid(expand=True)

        table.add_row(
            Spinner(
                'dots',
                text=f":zap: Unique Crashes"
            ),

            f"[b][[red]{self.unique_crashes}[/red]][/b]"
        )

        table.add_row(
            Spinner(
                'dots',
                text=f":atom_symbol:  Total Crashes"
            ),

            f"[b][[red]{self.total_crashes}[/red]][/b]"
        )

        table.add_row(
            Spinner(
                'dots',
                text=f":hourglass_done: Total Hangs"
            ),

            f"[b][[dark_goldenrod]{self.total_hangs}[/dark_goldenrod]][/b]"
        )

        table.add_row(
            Spinner(
                'dots',
                text=f":world_map:  Explored Paths"
            ),

            f"[b][[green]{self.explored_paths}[/green]][/b]"
        )

        table.add_row(
            Spinner(
                'dots',
                text=f":clock1: Average Speed"
            ),

            f"[b][[cyan]{self.average_speed}[/cyan]][/b]"
        )

        table.add_row(
            Spinner(
                'dots',
                text=f":cyclone: Net Cycles"
            ),

            f"[b][[magenta]{self.net_cycles}[/magenta]][/b]"
        )

        table.add_row(
            Spinner(
                'dots',
                text=f":calendar: Last Crash"
            ),

            f"[b][[medium_orchid]{self.last_crash}[/medium_orchid]][/b]"
        )

        table.add_row(
            Spinner(
                'dots',
                text=f":watch: Run Time"
            ),

            f"[b][[green]{self.run_time}[/green]][/b]"
        )

        return table
