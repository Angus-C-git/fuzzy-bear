from datetime import datetime

from rich import box
from rich.console import Console, RenderGroup
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import (
    Progress, 
    SpinnerColumn, 
    BarColumn, 
    TextColumn
)
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from rich.measure import Measurement
from rich.logging import RichHandler
from rich.live import Live

from time import sleep
import logging

console = Console()

# ======================================= #


# - CONFIG - #

LOGGER_FORMAT = "%(messages)s%"
logging.basicConfig(
    level="NOTSET",
    format=LOGGER_FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler()]
)

log = logging.getLogger("rich")


'''
Structure:
- root = main
    |
    - anchor (function): [sub_function, thing]
    |
    - anchor (function): 
        |
        - [sub_function, thing]
'''

# Coverage Tree Colors
EXPLORED = "bright_green"
UNEXPLORED = "bright_red"


def build_coverage_tree(code_paths=None):
    """ Build coverage tree """
    root = Text("main", EXPLORED)
    # root node
    paths_tree = Tree(root, guide_style="white")
    
    # code paths
    for function_name in code_paths:
        branch = paths_tree.add(Text(function_name, UNEXPLORED))

    # branch.add(Text("send_input", UNEXPLORED))
    # branch.add(Text("validate_input", UNEXPLORED))
    # paths_tree.add(Text("vuln", UNEXPLORED))

    return paths_tree
       


def tmp_stats():

    return (
"""
[ 1 ] Hangs 
[ 0 ] Aborts
"""
    )


# TODO :: finish implementing
def quote():
    """ Generate silly quotes """
    yield "Have you tried AFL?"
    yield "Are we there yet?"

# ======================================= #


class Dashboard():
    """ Display main fuzzer runtime UI """
    strategy_progress = Progress(
        "{task.description}",
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    overall_progress = Progress()

    def __init__(self, events):
        for event in events.keys():
            self.strategy_progress.add_task(
                f"[cyan]{event}", 
                total=events[event][1]
            )

        net_sum = sum(task.total for task in self.strategy_progress.tasks)
        self.overall_tasks = self.overall_progress.add_task(
            "Progress", 
            total=int(net_sum)
        )



class Banner():
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



class RowOne():
    """Display upper row of panels"""

    def __init__(self, strategy_progress, overall_progress):
        self.strategy_progress = strategy_progress
        self.overall_progress = overall_progress
        self.stat_events = tmp_stats()
        self.quote = next(quote())


    def __rich__(self) -> Table:
        progress_table = Table.grid(expand=True)
        progress_table.add_row(
            # Display overall progress bar
            Panel(
                self.overall_progress,
                title="[b]Overall Strategy Exhaustion",
                border_style="green",
                # down right
                padding=(6, 1),
                height=15,
                width=60     
            ),
            # Display inspirational 'quotes'
            Panel(
                f"'{self.quote}'{'':15}", 
                title="[b]Quotes", 
                border_style="magenta",
                padding=(6, 1),
                height=15,
                width=60 
            ),
            # Display runtime stats
            Panel(
                self.stat_events, 
                title="[b]Stats", 
                border_style="red", 
                padding=(1, 1),
                height=15,
                width=60 
            ),
        )
        return progress_table



class RowTwo():
    """ Display lower row of panels """
    logs = [
            'Fuzzer spooling up ...'
        ]

    def __init__(self, strategy_progress, functions, log_msg):
        self.strategy_progress = strategy_progress
        self.coverage_tree = build_coverage_tree(functions)
        if log_msg is not None:
            self.logs.append(log_msg)


    def __rich__(self) -> Table:
        
        progress_table = Table.grid(expand=True)
        progress_table.add_row(
            # Display strategy progress bar
            Panel(
                self.strategy_progress, 
                title="[b]Strategies",
                border_style="green",
                padding=(1, 1),
                height=20,
                width=60,
            ),
            # Display logging data
            Panel(
                f"{self.logs[-1]}", 
                title="[b]Logs", 
                border_style="cyan",
                padding=(1, 1),
                height=20,
                width=60 
            ),
            # Display current coverage data
            Panel(
                self.coverage_tree,
                title="[b]Coverage", 
                border_style="red", 
                padding=(1, 1),
                expand=True,
                height=20,
                width=60 
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
        Layout(name="RowOne", size=16),
        Layout(name="RowTwo", size=21),
    )
    
    return layout

# ======================================= #

def init_layout(
        events, 
        strategy_progress, 
        overall_progress, 
        coverage_paths, 
        log_msg=None
    ):
        layout = make_layout()

        layout["banner"].update(
            Banner()
        )  
        layout["RowOne"].update(
            RowOne(
                strategy_progress, 
                overall_progress
            )
        )                
        layout["RowTwo"].update(
            RowTwo(
                strategy_progress, 
                coverage_paths, 
                log_msg
            )
        )

        return layout


'''devnotes

 - TODO - 
+ Convert logging method to use console.log or create custom function
    + Will likely need a custom function to deal with the need for
      a renderable with multiple uncertain and changing events
+ Hookup event handlers
+ Manage component state from UiRunner
+ Make quotes generator work
+ Fix stats
___________________________________________________________________________

[-] -> half done / stalled
[X] -> done

+ Goals
    - [-] Coverage: Display tree of decisions for binary and highlight
                   discovered code paths (kinda binja graph)
    - [X] Strategies: Display progress of current strategies
    - [ ] Logging: Display messages from aggregator and other internals
            + Live feed of detections
            + Strategy changes
            + Optionally debugging
    - [ ]  Quotes: Display quotes from various sources, yield one per UI refresh
    - [ ] Stats: Display useful stats
        + [ ] Hangs
        + [ ] Loops
        + [ ] Speed (input/sec)
        + [ ] Discovered code paths
    + Overall Strategy Exhaustion: How many strategies have been exhausted
        + Does not indicate a halt in fuzzing just that all strategies have been
          exhausted in there basic forms

'''