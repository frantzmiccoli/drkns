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
            steps = self._get_steps_to_run(config_unit)
        else:
            if name_or_index.isdigit():
                name_or_index = config_unit.steps.keys()[int(name_or_index)]
            steps = [name_or_index]

        for step_name in steps:
            self._run(step_name)

        output_elements = []
        successful = True
        for step_name, status in self.execution_history.items():
            message = step_name + ': '
            if not status.successful:
                message += BColors.FAIL + 'Error' + BColors.ENDC
                successful = False
            else:
                message += BColors.OKGREEN + 'OK' + BColors.ENDC

            output_elements.append(message)

        return successful, output_elements

    def _run(self, config_unit: ConfigUnit, name: str) -> str:
        current_config_unit = config_unit
        parts = name.split(':')
        if len(parts) == 2:
            dependency_name = parts.pop(0)
            current_config_unit = config_unit.dependencies[dependency_name]

        successful_execution_date = \
            self._context.get_unit_successful_execution_date(config_unit)

        if successful_execution_date is not None:
            return config_unit.name + ' @ ' + config_unit.get_hash() + \
                   ' successfully ran at ' + \
                   successful_execution_date.strftime('%Y-%m-%d-%H:%M:%S')

        target_step_name = parts.pop(0)
        step_execution_status = current_config_unit.run_step(target_step_name)
        self.execution_history[name] = step_execution_status

    @staticmethod
    def _get_steps_to_run(config_unit: ConfigUnit, ignore_dependency=False)\
            -> Collection[str]:
        steps = []

        considered_prefixes_and_config_units = [(None, config_unit)]

        while not len(considered_prefixes_and_config_units):
            current_prefix, config_unit = \
                considered_prefixes_and_config_units.pop(0)

            for dependency_name in config_unit.dependencies.keys():
                if ignore_dependency:
                    break

                prefix = dependency_name

                if current_prefix is not None:
                    prefix = current_prefix + ':' + dependency_name + ':'

                prefix_and_config_unit = \
                    (prefix, config_unit.dependencies[dependency_name])
                considered_prefixes_and_config_units.append(
                    prefix_and_config_unit)

            if current_prefix is None:
                current_prefix = ''

            unit_steps = [current_prefix + step_name
                          for step_name in config_unit.steps.keys()]
            steps = unit_steps + steps

        return steps
