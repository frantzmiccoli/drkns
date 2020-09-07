from paver.easy import sh, BuildFailure
from typing import Optional

from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit.StepExecutionStatus import StepExecutionStatus
from drkns.exception import UnknownStepException


def run_step(config_unit: ConfigUnit, step_name: str) -> StepExecutionStatus:
    failed_previous_execution_status = _get_step_run_check(config_unit, step_name)

    if failed_previous_execution_status is not None:
        output = 'Previous failure of ' \
                 + failed_previous_execution_status.step_name
        return StepExecutionStatus(step_name, False, output)

    command = '(cd "' + config_unit.directory + '"; \n' + \
              config_unit.steps[step_name] + \
              '\n)'

    output = None
    try:
        output = sh(command, capture=True)
        successful = True
    except BuildFailure:
        successful = False

    step_execution_status = \
        StepExecutionStatus(step_name, successful, output)
    config_unit.steps_execution_status[step_name] = step_execution_status

    return step_execution_status


def _get_step_run_check(config_unit: ConfigUnit, target_step_name: str) \
        -> Optional[StepExecutionStatus]:
    for step_name in config_unit.steps.keys():
        if step_name == target_step_name:
            return None

        if not (step_name in config_unit.steps_execution_status):
            # missing intermediate step
            run_step(config_unit, step_name)

        step_execution_status = config_unit.steps_execution_status[step_name]
        if not step_execution_status.successful:
            return step_execution_status

    message = 'Unknown step ' + target_step_name + ' in ' + config_unit.name
    raise UnknownStepException(message)
