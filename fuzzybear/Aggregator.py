from .Harness import Harness
from .utility import response_codes
from .utility import codec
from .strategies import get_generator
from .coverage.Coverage import Coverage

# highlight crash
from colorama import Fore, Style

# run UI
from .ui.UiRunner import UiRunner, init_layout
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


def write_crash(crashing_input):
	""" write crashing input to file """
	console.print(
		f"{'':1}[>>] [b red]CRASH DETECTED[/b red], writing [b green]crash.txt[/b green]"
	)

	with open('./crash.txt', 'w') as crash:
		crash.write(crashing_input)
	

# TODO :: finish implementing	
def prepare_summary(crashing_strategy, runtime, unique_crashes=0):
	""" construct campaign summary """
	console.print(
		f"{'':1}[>>] [b]Fuzzing campaign ended[/b]"
	)
	summary_data = {
		'crashing_strategy': crashing_strategy,
		'unique_crashes': str(unique_crashes),
		'total_crashes': str(unique_crashes),
		'hangs': str(0),
		'codepaths': str(0),
		'coverage': '0%',
		'runtime': f'{str(round(runtime, 2))}s'
	}

	render_summary(summary_data)


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
		self.codec = codec.detect(input_file)
		self.base_file = input_file		
		
		self.start_clock = time()

		# if gui
		self.ui_runner = UiRunner()
		
		# if verbose
		self.log_runner = None
		self.full_logs = full_logs

		# if coverage
		self.coverage_runner = Coverage(binary)
	

	def run_fuzzer(self):
		Generator = get_generator(self.codec, self.base_file)

		## Tmp handler
		if (Generator is None): 
			console.print(f"[b][>>] The format of [b red]{self.base_file}[/b red] is not supported")
			return None
		
		startup_log = f"Running fuzzer against [b green]<{self.binary.split('/')[-1]}>[/b green]" + \
					  f" mutating [b green]<{self.base_file.split('/')[-1]}> [/b green]"

		DashboardUI = self.ui_runner.register_events(Generator.ui_events)
		strategy_progress = DashboardUI.strategy_progress
		overall_progress = DashboardUI.overall_progress

		coverage_paths = self.coverage_runner.get_function_names()

		## <<-	 TMP RUNNER 	->> ##

		# while True:
		inputs = Generator.run()
		jobs = DashboardUI.strategy_progress.tasks
		current_job = 0
		
		with Live(
				init_layout(
					self.ui_runner.events, 
					strategy_progress, 
					overall_progress,
					coverage_paths,
					startup_log
				), 
				refresh_per_second=6, 
				screen=True
			) as gui:
				while not DashboardUI.overall_progress.finished:					
					
					for input in inputs:
						
						response_code = self.harness.open_pipe(input)

						if current_job < len(jobs):
							
							if not jobs[current_job].finished:
								DashboardUI.strategy_progress.advance(jobs[current_job].id)
							else:
								# Log strategy switch if verbouse
								if self.full_logs:
									pass
									# DashboardUI. = 'Strategy done, switching'
									
								current_job += 1
							
							completed = sum(task.completed for task in DashboardUI.strategy_progress.tasks)
							DashboardUI.overall_progress.update(DashboardUI.overall_tasks, completed=completed)

						if (response_code == -11):
							gui.stop()
							write_crash(input)
							self.runtime = time() - self.start_clock
							prepare_summary(
								jobs[current_job].description,
								self.runtime,
								unique_crashes=1
							)
							exit(0)
					
					
					# DEBUG
					# sleep(0.6)
					
					# Kill the gui on next iteration
					# gui.stop()

		# Display summary on exit
		self.runtime = time() - self.start_clock
		prepare_summary(
			"None",
			self.runtime
		)


'''devnotes

- TODO - 

+ Port live render to another file
+ Use UiRunner to handle events and manage
  UI component updates
+ Add the ability to cycle the UI to run
  'forever'
+ Update write crash to support writing
  multiple crashes over campaign lifetime

'''