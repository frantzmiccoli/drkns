from typing import Collection, Tuple


from drkns.util import BColors
from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit.get_steps import get_steps
from drkns.configunit.get_hash import get_hash
from drkns.configunit.run_step import run_step
from drkns.context.get_successful_execution_date import \
    get_successful_execution_date
from drkns.context.store_successful_execution import \
    store_successful_unit_execution


def run(config_unit: ConfigUnit, name_or_index: str = None) \
        -> Tuple[bool, Collection[str]]:
    if name_or_index is None:
        steps = get_steps(config_unit)
    else:
        if name_or_index.isdigit():
            name_or_index = config_unit.steps.keys()[int(name_or_index)]
        steps = [name_or_index]

    for step_name in steps:
        _run_step(config_unit, step_name)

    output_elements = []
    successful = True
    for step_name, status in config_unit.execution_history.items():
        message = step_name + ': '
        if status.ignored:
            message += BColors.WARNING + 'Ignored' + BColors.ENDC
            successful = False
        elif not status.successful:
            message += BColors.FAIL + 'Error' + BColors.ENDC
            successful = False
        else:
            message += BColors.OKBLUE + 'OK' + BColors.ENDC

        output_elements.append(message)

    return successful, output_elements


def _run_step(config_unit: ConfigUnit, full_name: str) -> str:
    name = full_name
    current_config_unit = config_unit
    parts = name.split('.')
    name = parts[-1]
    while len(parts) > 1:
        dependency_name = parts.pop(0)
        current_config_unit = \
            current_config_unit.dependencies[dependency_name]

    successful_execution_date = get_successful_execution_date(
        current_config_unit)

    if successful_execution_date is not None:
        return config_unit.name + ' @ ' + get_hash(config_unit) + \
               ' successfully ran at ' + \
               successful_execution_date.strftime('%Y-%m-%d-%H:%M:%S')

    target_step_name = parts.pop(0)
    step_execution_status = run_step(current_config_unit, target_step_name)
    config_unit.execution_history[full_name] = step_execution_status

    if name == list(current_config_unit.steps.keys())[-1]:
        # last step completed ?
        if step_execution_status.successful:
            store_successful_unit_execution(current_config_unit)
