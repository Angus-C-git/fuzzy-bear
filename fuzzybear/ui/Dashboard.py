from datetime import datetime

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

# ======================================= #


"""
    TMP DUMMY VARIABLES TO SIMULATE STRATEGIES

    TODO :: fill out function stubs
"""
strategy_progress = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
)
strategy_progress.add_task("[green]Max Constants")
strategy_progress.add_task("[magenta]Bad Strings", total=200)
strategy_progress.add_task("[cyan]Large fields", total=400)

total = sum(task.total for task in strategy_progress.tasks)
overall_progress = Progress()
overall_task = overall_progress.add_task("Progress", total=int(total))

# ======================================= #

""" UI Event Handlers """

def update_strategies() -> None:
    # Update current strategy progress

    # Update Overall progress
    pass


def update_quote() -> str:
    # update current quote
    pass


def update_stats() -> None:
    # update current stats
    pass


def log_event(event) -> None:
    # update logs
    pass


def update_coverage() -> None:
    # update coverage
    pass


# ======================================= #



class Banner:
    """Display banner block"""
    def __rich__(self) -> Panel:
        banner = Table(
            box=box.SIMPLE_HEAVY, 
            expand=True, 
            collapse_padding=True
        )
        banner.add_column(
            f"v1.0{'':15}", 
            justify="left"
        )
        banner.add_column(
            "[b]Fuzzy Bear[/b]", 
            justify="center", 
            no_wrap=True
        )
        banner.add_column(
            datetime.now().ctime().replace(":", "[blink]:[/]"), 
            justify="right", 
            no_wrap=True
        )
        return Panel(banner, style="green", box=box.SIMPLE_HEAD)    



class Header:
    """Display upper row of panels"""
    def __rich__(self) -> Table:
        progress_table = Table.grid(expand=True)
        progress_table.add_row(
            Panel(
                overall_progress,
                title="[b]Overall Strategy Exhaustion",
                border_style="green",
                # down right
                padding=(4, 10),     
            ),
            # Display inspirational 'quotes'
            Panel(
                f"'Have you tried AFL?'{'':15}", 
                title="[b]Quotes", 
                border_style="magenta",
                padding=(4, 3),
            ),
            Panel(
                strategy_progress, 
                title="[b]Stats", 
                border_style="red", 
                padding=(3, 2)
            ),
        )
        return progress_table



class Footer:
    """ Display lower row of panels """

    # TMP samples
    time_stamp = '0:00'
    log_msg = "Fuzzing csv1 ..."

    def __rich__(self) -> Table:
        progress_table = Table.grid(expand=True)
        progress_table.add_row(
            Panel(
                strategy_progress,
                title="[b]Strategies",
                border_style="green",
                padding=(3, 2),
            ),
            # Display logging data
            Panel(
                f"[{self.time_stamp}]{'':3}{self.log_msg}{'':10}", 
                title="[b]Logs", 
                border_style="cyan",
                padding=(4, 3),
            ),
            # Display current coverage data
            Panel(
                strategy_progress, 
                title="[b]Coverage", 
                border_style="red", 
                padding=(3, 2),
                expand=True
            ),
        )
        return progress_table

# ======================================= #

""" Initialise Dashboard """

def make_layout() -> Layout:
    """ Define the layout """
    
    # layout anchor
    layout = Layout(name="root")

    # main components
    layout.split_column(
        Layout(name="banner", size=5),
        Layout(name="header", size=12),
        Layout(name="footer", size=12),
    )
    return layout

# ======================================= #

# TODO :: Move to method
layout = make_layout()

layout["banner"].update(Banner())  
layout["header"].update(Header())                
layout["footer"].update(Footer())

# ======================================= #

# TODO :: Move to method and tie in event handlers
with Live(layout, refresh_per_second=10, screen=True):
    while not overall_progress.finished:
        sleep(0.1)
        for job in strategy_progress.tasks:
            if not job.finished:
                strategy_progress.advance(job.id)

        completed = sum(task.completed for task in strategy_progress.tasks)
        overall_progress.update(overall_task, completed=completed)

# ======================================= #

'''devnotes

+ Convert logging method to use console.log or create custom function
+ Hookup event handlers
+ Tie in Live handler

+ Rough plan
    + Coverage: Display tree of decisions for binary and highlight
      discovered code paths (kinda binja graph)
    + Strategies: Display progress of current strategies
    + Logging: Display messages from aggregator and other internals
        + Live feed of detections
        + Strategy changes
        + Optionally debugging
    + Quotes: Display quotes from various sources, yield one per UI refresh
    + Stats: Display useful stats
        + [ ] Hangs
        + [ ] Loops
        + [ ] Speed (input/sec)
        + [ ] Discovered code paths
    + Overall Strategy Exhaustion: How many strategies have been exhausted
        + Does not indicate a halt in fuzzing just that all strategies have been
          exhausted in there basic forms
'''