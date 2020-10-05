from typing import Optional, Collection, Tuple, List, Dict

from drkns.util import BColors
from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit.StepExecutionStatus import StepExecutionStatus
from drkns.configunit.get_steps import get_steps
from drkns.configunit.run_step import run_step
from drkns.configunit.cleanup import cleanup


class Runner:

    def __init__(self):
        self._past_config_unit_triggered_execution = False
        self._past_config_unit: Optional[ConfigUnit] = None

    def run(self, config_unit: ConfigUnit, name_or_index: str = None) \
            -> Tuple[bool, Collection[str]]:
        if name_or_index is None:
            steps = get_steps(config_unit)
        else:
            if name_or_index.isdigit():
                name_or_index = \
                    list(config_unit.steps.keys())[int(name_or_index)]
            steps = [name_or_index]

        execution_history = []
        for step_name in steps:
            execution_history += self._run_step(config_unit, step_name)

        execution_history += self._cleanup_if_needed(None)

        return self._get_successful_flag_and_combined_output(execution_history)

    def _run_step(self, config_unit: ConfigUnit, full_name: str)\
            -> List[StepExecutionStatus]:
        current_config_unit = config_unit
        name = full_name
        parts = name.split('.')
        while len(parts) > 1:
            dependency_name = parts.pop(0)
            current_config_unit = \
                current_config_unit.dependencies[dependency_name]

        statuses = self._cleanup_if_needed(current_config_unit)

        target_step_name = parts.pop(0)
        statuses += run_step(current_config_unit, target_step_name)
        if not statuses[-1].restored:
            self._past_config_unit_triggered_execution = True

        return statuses

    def _cleanup_if_needed(self, current_config_unit: Optional[ConfigUnit]) \
            -> List[StepExecutionStatus]:
        if self._past_config_unit == current_config_unit:
            return []

        statuses = []
        if self._past_config_unit is not None:
            if self._past_config_unit_triggered_execution:
                statuses = cleanup(self._past_config_unit)
            self._past_config_unit_triggered_execution = False

        self._past_config_unit = current_config_unit

        return statuses

    @staticmethod
    def _get_successful_flag_and_combined_output(
            execution_history: List[StepExecutionStatus]) -> Tuple[
            bool, Collection[str]]:
        outputs = []
        statuses = []
        successful = True
        for status in execution_history:
            message = status.name() + ': ' + BColors.BOLD
            if status.ignored:
                message += BColors.WARNING + 'Ignored' + BColors.ENDC
                successful = False
            elif not status.successful:
                message += BColors.FAIL + 'Error' + BColors.ENDC
                successful = False
            else:
                message += BColors.OKBLUE + 'OK' + BColors.ENDC

            if status.restored:
                message += ' (restored)'

            if not status.successful:
                output = 'Output for ' + status.name()

                if status.restored:
                    output += ' (restored)'

                output += ': \n' + status.output + '\n--\n\n'
                outputs.append(output)

            statuses.append(message)

        combined_output = []
        if len(outputs) > 0:
            combined_output += outputs + ['\n']

        combined_output += statuses

        return successful, combined_output
