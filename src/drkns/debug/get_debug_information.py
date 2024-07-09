from typing import List, Tuple, Optional

from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.exception import UnexpectedBranchException
from drkns.runner.get_execution_plan import get_execution_plan
from drkns.configunit.get_hash import get_hash
from drkns.context.get_past_execution_status import get_past_execution_status
from drkns.stepexecutionstatus.StepExecutionStatus import StepExecutionStatus


def get_debug_information(config_unit: ConfigUnit):
    execution_plan = get_execution_plan(config_unit)
    output_elements = [
        _get_hash_debug_information(execution_plan),
        _get_execution_plan_debug_information(execution_plan)
    ]

    return '\n\n'.join(output_elements)


def _get_hash_debug_information(
    execution_plan: List[Tuple[ConfigUnit, str, str]]
) -> str:
    names_to_hashes = {}

    for (config_unit, _, _) in execution_plan:
        if config_unit.name in names_to_hashes:
            continue

        names_to_hashes[config_unit.name] = get_hash(config_unit)

    lines = ['* ' + name + ': \n\t' + unit_hash
             for name, unit_hash in names_to_hashes.items()]
    lines.insert(0, 'Config hashes:')
    return '\n'.join(lines)


def _get_execution_plan_debug_information(
        execution_plan: List[Tuple[ConfigUnit, str, str]]
        ) -> str:
    lines = []

    for (config_unit, step_name, prefixed_step_name) in execution_plan:
        status = get_past_execution_status(config_unit, step_name)
        line = _get_line_for_status(status, prefixed_step_name)

        lines.append(line)

    lines.insert(0, 'Execution plan:')
    return '\n'.join(lines)


def _get_line_for_status(
    status: Optional[StepExecutionStatus],
    prefixed_step_name: str
) -> str:
    line = '* ' + prefixed_step_name + ': \n\t'

    if status is not None:
        line += 'previous execution as '
        if status.successful:
            line += 'successful'
        else:
            if status.ignored:
                line += 'ignored'
            else:
                line += 'execution error'

            if status.hash is None:
                raise UnexpectedBranchException()

            line += ' ' + status.hash

    else:
        line += '---'

    return line