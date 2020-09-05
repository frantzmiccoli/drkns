import os
import pickle

from typing import Optional, Dict, Collection, Tuple

from drkns.util import BColors
from drkns.config.ConfigUnit import ConfigUnit
from drkns.context.Context import Context
from drkns.runner.StepExecutionStatus import StepExecutionStatus


class Runner:

    def __init__(self):
        self.execution_history: Dict[str, StepExecutionStatus] = {}

        self._context = Context()

    def run(self, config_unit: ConfigUnit, name_or_index: str = None)\
            -> Tuple[bool, Collection[str]]:
        if name_or_index is None:
            steps = config_unit.get_steps()
        else:
            if name_or_index.isdigit():
                name_or_index = config_unit.steps.keys()[int(name_or_index)]
            steps = [name_or_index]

        for step_name in steps:
            self._run(config_unit, step_name)

        output_elements = []
        successful = True
        for step_name, status in self.execution_history.items():
            message = step_name + ': '
            if not status.successful:
                message += BColors.FAIL + 'Error' + BColors.ENDC
                successful = False
            else:
                message += BColors.OKBLUE + 'OK' + BColors.ENDC

            output_elements.append(message)

        return successful, output_elements

    def _run(self, config_unit: ConfigUnit, name: str) -> str:
        current_config_unit = config_unit
        parts = name.split('.')
        name = parts[-1]
        while len(parts) > 1:
            dependency_name = parts.pop(0)
            current_config_unit = \
                current_config_unit.dependencies[dependency_name]

        successful_execution_date = \
            self._context.get_unit_successful_execution_date(
                current_config_unit)

        if successful_execution_date is not None:
            return config_unit.name + ' @ ' + config_unit.get_hash() + \
                   ' successfully ran at ' + \
                   successful_execution_date.strftime('%Y-%m-%d-%H:%M:%S')

        target_step_name = parts.pop(0)
        step_execution_status = current_config_unit.run_step(target_step_name)
        self.execution_history[name] = step_execution_status

        # last step ?
        if name == list(current_config_unit.steps.keys())[-1]:
            self._context.store_successful_unit_execution(current_config_unit)

