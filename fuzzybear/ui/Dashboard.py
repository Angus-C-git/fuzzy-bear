from datetime import datetime

from rich import box
from rich.console import Console, RenderGroup
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from rich.measure import Measurement
from rich.live import Live
from time import sleep

console = Console()

# ======================================= #


"""
    TMP DUMMY VARIABLES TO SIMULATE ELEMENTS

    TODO :: fill out function stubs
"""
# strategy_progress = Progress(
#     "{task.description}",
#     SpinnerColumn(),
#     BarColumn(),
#     TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
# )

# strategy_progress.add_task("[green]Max Constants")
# strategy_progress.add_task("[magenta]Bad Strings", total=200)
# strategy_progress.add_task("[cyan]Large fields", total=400)

# total = sum(task.total for task in strategy_progress.tasks)
# overall_progress = Progress()
# overall_task = overall_progress.add_task("Progress", total=int(total))





"""
Structure:
- root = main
    |
    - anchor (function): [sub_function, thing]
    |
    - anchor (function): 
        |
        - [sub_function, thing]

"""

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


def quotes():
    yield "Have you tried AFL?"
    yield "Are we there yet?"

# ======================================= #


class Dashboard():
    strategy_progress = Progress(
        "{task.description}",
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    overall_progress = Progress()

    def __init__(self, events):
        for event in events.keys():
            self.strategy_progress.add_task(f"[cyan] {event}", total=events[event][1])

        net_sum = sum(task.total for task in self.strategy_progress.tasks)
        self.overall_tasks = self.overall_progress.add_task("Progress", total=int(net_sum))



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



class Header():
    """Display upper row of panels"""


    def __init__(self, strategy_progress, overall_progress):
        self.strategy_progress = strategy_progress
        self.overall_progress = overall_progress
        self.stat_events = tmp_stats()


    def __rich__(self) -> Table:
        # super()
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
                f"'{next(quotes())}'{'':15}", 
                title="[b]Quotes", 
                border_style="magenta",
                padding=(6, 1),
                height=15,
                width=60 
            ),
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



class Footer():
    """ Display lower row of panels """

    # TMP samples
    time_stamp = '0:00'
    log_msg = "Fuzzing ..."

    def __init__(self, strategy_progress, functions):
        self.strategy_progress = strategy_progress
        self.coverage_tree = build_coverage_tree(functions)

    def __rich__(self) -> Table:
        # super()
        progress_table = Table.grid(expand=True)
        progress_table.add_row(
            Panel(
                # super().strategy_progress,
                self.strategy_progress, 
                title="[b]Strategies",
                border_style="green",
                padding=(1, 1),
                height=20,
                width=60,
            ),
            # Display logging data
            Panel(
                f"[{self.time_stamp}]{'':3}{self.log_msg}{'':10}\n[0:10]{'':3}'detecting hang'", 
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
        Layout(name="header", size=16),
        Layout(name="footer", size=21),
    )
    return layout

# ======================================= #

def init_layout(events, strategy_progress, overall_progress, coverage_paths):
    layout = make_layout()

    layout["banner"].update(Banner())  
    layout["header"].update(Header(strategy_progress, overall_progress))                
    layout["footer"].update(Footer(strategy_progress, coverage_paths))

    return layout

# ======================================= #

# TODO :: Move to method and tie in event handlers
# probably an update method

# with Live(init_layout(), refresh_per_second=10, screen=True):
#     while not overall_progress.finished:
#         sleep(0.1)
#         for job in strategy_progress.tasks:
#             if not job.finished:
#                 strategy_progress.advance(job.id)

#         completed = sum(task.completed for task in strategy_progress.tasks)
#         overall_progress.update(overall_task, completed=completed)

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

+ Rendering the code paths will be a interesting and should be done
    recursively 
'''