from .Harness import Harness
from .HarnessV2 import HarnessV2
from .utility import response_codes
from .utility import codec
from .strategies import get_generator

# highlight crash
from colorama import Fore, Style

# run UI
from .ui.UiRunner import UiRunner, init_layout
from rich.live import Live
from time import sleep
from rich.console import Console, RenderGroup

# console = Console()

'''
::::::::::::::::: [Aggregator] :::::::::::::::::

	► Takes responses (or lack of) from the
	  binary and decides what changes if any 
	  should be triggered (maybe)
	
	► Runner Class for strategies/generators 

'''

def write_crash(crashing_input):
	print(Fore.RED + f'\n\n   [>>] CRASH DETECTED, dropping bad.txt')
	print(Style.RESET_ALL)

	with open('./bad.txt', 'w') as crash:
		crash.write(crashing_input)
	
	exit(0)



class Aggregator():
	def __init__(self, binary, input_file):
		print(f"   [>>] Running fuzzer against <{binary.split('/')[-1]}> mutating <{input_file.split('/')[-1]}>")
		self.harness = Harness(binary)
		self.codec = codec.detect(input_file)
		# print(f'   [DEBUG] {self.codec}')
		self.base_file = input_file
		self.ui_runner = UiRunner()


	def run_fuzzer(self):
		# TODO :: run generator here <codec>
		# format runner 
		Generator = get_generator(self.codec, self.base_file)

		## Tmp handler
		if (Generator is None): 
			print(f'\n   [>>] The format of {self.base_file} is not supported')
			return None
		
		print(f"{'':3}[>>] Running fuzzer ...")

		DashboardUI = self.ui_runner.register_events(Generator.ui_events)



		## TMP RUNNER >> ##
		# while True:
		print("[>>] In fuzing loop")
		inputs = Generator.run()
		jobs = DashboardUI.strategy_progress.tasks
		current_job = 0
		
		with Live(init_layout(self.ui_runner.events, DashboardUI.strategy_progress, DashboardUI.overall_progress), refresh_per_second=10, screen=True):
			while not DashboardUI.overall_progress.finished:
				sleep(0.3)

				for input in inputs:
					response_code = self.harness.open_pipe(input)

					if current_job <= len(jobs):
							# current_job = 0
						if not jobs[current_job].finished:
							DashboardUI.strategy_progress.advance(jobs[current_job].id)
						else:
							current_job += 1
						
				
						completed = sum(task.completed for task in DashboardUI.strategy_progress.tasks)
						DashboardUI.overall_progress.update(DashboardUI.overall_tasks, completed=completed)

					# sleep(0.2)
					if (response_code == -11):
						write_crash(input)
