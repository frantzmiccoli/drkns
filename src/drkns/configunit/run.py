from typing import Collection, Tuple

from drkns.util import BColors
from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit.StepExecutionStatus import StepExecutionStatus
from drkns.configunit.get_steps import get_steps
from drkns.configunit.run_step import run_step


def run(config_unit: ConfigUnit, name_or_index: str = None) \
        -> Tuple[bool, Collection[str]]:
    if name_or_index is None:
        steps = get_steps(config_unit)
    else:
        if name_or_index.isdigit():
            name_or_index = list(config_unit.steps.keys())[int(name_or_index)]
        steps = [name_or_index]

    execution_history = \
        {step_name: _run_step(config_unit, step_name) for step_name in steps}

    outputs = []
    statuses = []
    successful = True
    for step_name, status in execution_history.items():
        message = step_name + ': ' + BColors.BOLD
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
            output = 'Output for ' + step_name

            if status.restored:
                output += ' (restored)'

            output += ': \n' + status.output + '\n--\n\n'
            outputs.append(output)

        statuses.append(message)

    combined = []
    if len(outputs) > 0:
        combined += outputs + ['\n']

    combined += statuses

    return successful, combined


def _run_step(config_unit: ConfigUnit, full_name: str) -> StepExecutionStatus:
    current_config_unit = config_unit
    name = full_name
    parts = name.split('.')
    while len(parts) > 1:
        dependency_name = parts.pop(0)
        current_config_unit = \
            current_config_unit.dependencies[dependency_name]

    target_step_name = parts.pop(0)
    return run_step(current_config_unit, target_step_name)
