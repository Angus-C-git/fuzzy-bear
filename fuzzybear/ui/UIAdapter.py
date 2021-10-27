'''
Handles UI events and feeds data to components.

'''
from rich.live import Live
from time import sleep, time
from rich.console import Console, RenderGroup

from fuzzybear.ui.Dashboard import Dashboard, init_layout
from fuzzybear.ui.Summary import render_summary
from fuzzybear.ui.Logs import Logs
from fuzzybear.ui.Stats import Stats
from fuzzybear.ui.Clock import Clock


class UIAdapter():
    """ stores progress states for components """

    def __init__(self):
        self.clock = Clock()
        self.logger = Logs(self.clock)
        self.stats = Stats(self.clock)

    def run_display(self):
        """ 
        return a runner for the dashboard 
        display 
        """
        return Live(
            init_layout(
                self.events,
                self.strategy_progress,
                self.overall_progress,
                self.coverage_paths,
                self.logger,
                self.stats
            ),
            refresh_per_second=6,
            screen=True
        )

    def register_strategies(self, events):
        self.events = events
        self.dashboard = Dashboard(events)
        self.strategy_progress = self.dashboard.strategy_progress
        self.overall_progress = self.dashboard.overall_progress

        # tmp return
        return self.dashboard

    def update_strategies(self, events):
        self.events = events

    def get_events(self):
        return self.events

    def register_coverage(self, coverage_paths):
        self.coverage_paths = coverage_paths

    def update_logs(self, log_msg):
        """ feed logging panel """
        # TODO seed diffrent log types
        self.logger.add_startup_log(log_msg)

    def update_stats(self, stat, value):
        """ feed stats panel """
        # self.stats.update_stats(stat, value)
        pass

    def update_clock(self):
        self.stats.update_clock()

    def update_unique_crashes(self):
        self.stats.update_unique_crashes()
