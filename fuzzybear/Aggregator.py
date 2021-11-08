from signal import signal, SIGINT

from .Harness import Harness
from .utility import response_codes
from .utility.codec import detect
from .utility.mode import is_raw
from .strategies import get_generator
from .coverage.Coverage import Coverage

# highlight crashes
from colorama import Fore, Style

# run UI
from fuzzybear.ui.UIAdapter import UIAdapter, init_layout
from rich.live import Live
from time import sleep, time
from rich.console import Console, RenderGroup
from fuzzybear.ui.Summary import render_summary

# Debugging / Quite mode
console = Console()

'''
::::::::::::::::: [Aggregator] :::::::::::::::::

	► Takes responses (or lack of) from the
	  binary and decides what changes if any 
	  should be triggered
	
	► Runner Class for strategies/generators 

'''
SEGFUALT_SIGNAL = -11


# TODO :: finish implementing
def prepare_summary(runtime, unique_crashes=0):
    """ construct campaign summary """
    console.print(
        f"{'':1}[>>] [b]Fuzzing campaign ended[/b]"
    )
    summary_data = {
        'unique_crashes': str(unique_crashes),
        'total_crashes': str(unique_crashes),
        'hangs': str(0),
        'codepaths': str(0),
        'coverage': '0%',
        'runtime': f'{str(round(runtime, 2))}s'
    }

    render_summary(summary_data)
    # exit(0)


class Aggregator():
    def __init__(
            self,
            binary,
            input_file,
            display_ui=True,
            full_logs=True,
            run_coverage=True
    ):
        self.binary = binary
        self.harness = Harness(binary)
        self.codec = detect(input_file)
        self.base_file = input_file

        self.start_clock = time()

        # if gui
        self.ui_adapter = UIAdapter()

        # if verbose
        self.log_runner = None
        self.full_logs = full_logs

        # if coverage
        self.coverage_runner = Coverage(binary)

    def end_campaign(self, signal, frame):
        """ end the campaign """
        self.gui.stop()
        self.runtime = time() - self.start_clock
        prepare_summary(
            self.runtime,
            self.ui_adapter.stats.unique_crashes
        )
        exit(0)

    def write_crash(self, crashing_input):
        """ write crashing input to file """
        crash_msg = f"[b red]CRASH DETECTED[/b red], writing [b green]crash.txt[/b green]"
        self.ui_adapter.update_logs(crash_msg)

        with open('./crash.txt', 'w') as crash:
            crash.write(crashing_input)

    def run_fuzzer(self):
        """ start the fuzzing campaign """

        # exit handler
        signal(SIGINT, self.end_campaign)
        Generator = get_generator(self.codec, self.base_file)

        # Tmp handler
        if (Generator is None):
            console.print(
                f"[b][>>] The format of [b red]{self.base_file}[/b red] is not supported")
            return None

        startup_log = f"Running fuzzer against [b green]<{self.binary.split('/')[-1]}>[/b green]" + \
            f" mutating [b green]<{self.base_file.split('/')[-1]}> [/b green]"
        self.ui_adapter.update_logs(startup_log)

        DashboardUI = self.ui_adapter.register_strategies(Generator.ui_events)
        strategy_progress = DashboardUI.strategy_progress
        overall_progress = DashboardUI.overall_progress

        coverage_paths = self.coverage_runner.get_function_names()

        self.ui_adapter.register_coverage(coverage_paths)

        ## <<-	 BETA RUNNER 	->> ##
        with self.ui_adapter.run_display() as gui:
            self.gui = gui
            while True:
                # while not DashboardUI.overall_progress.finished:
                inputs = Generator.run()
                jobs = DashboardUI.strategy_progress.tasks
                current_job = 0

                for input in inputs:
                    response_code = self.harness.open_pipe(input)

                    # push the runtime forwards (move?)
                    self.ui_adapter.update_clock()

                    if current_job < len(jobs):
                        if not jobs[current_job].finished:
                            DashboardUI.strategy_progress.advance(
                                jobs[current_job].id
                            )

                        else:
                            current_job += 1
                            # Log strategy switch ?if verbouse?
                            # self.ui_adapter.update_logs(
                            #     'Strategy done, switching'
                            # )

                        completed = sum(
                            task.completed for task in DashboardUI.strategy_progress.tasks
                        )
                        DashboardUI.overall_progress.update(
                            DashboardUI.overall_tasks, completed=completed
                        )

                    if (response_code == SEGFUALT_SIGNAL):
                        self.ui_adapter.update_unique_crashes()
                        # TODO - write unique crash files
                        self.write_crash(input)

                self.ui_adapter.update_logs(
                    'Generator cycle done'
                )

                # TODO reset ui


'''devnotes

- TODO - 

+ Update write crash to support writing
  multiple crashes over campaign lifetime
+ rest the ui on new cycles

'''
