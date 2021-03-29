from typing import Tuple, List

from drkns.configunit.ConfigUnit import ConfigUnit


def remove_execution_plan_redundancies(
        execution_plan: List[Tuple[ConfigUnit, str, str]]
        ) -> List[Tuple[ConfigUnit, str, str]]:
    cleaned_plan = []
    found_steps = {}
    for execution_step in execution_plan:
        step_key = _get_execution_step_key(execution_step)
        if step_key in found_steps:
            continue

        cleaned_plan.append(execution_step)
        found_steps[step_key] = True

    return cleaned_plan


def _get_execution_step_key(
        execution_step: Tuple[ConfigUnit, str, str]
        ) -> str:
    config_unit, step_name, _ = execution_step
    return config_unit.name + '.' + step_name + '@' + config_unit.directory
