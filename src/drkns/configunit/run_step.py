import copy
from typing import Optional

from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit.StepExecutionStatus import StepExecutionStatus
from drkns.exception import UnknownStepException
from drkns.util import sh
from drkns.context.get_past_execution_status import \
    get_past_execution_status
from drkns.context.store_past_execution_status import \
    store_past_execution_status


def run_step(config_unit: ConfigUnit, step_name: str) -> StepExecutionStatus:
    """
    This function is meant to run a specific step and the previous steps if they
    haven't been run

    :param config_unit:
    :param step_name:
    :return:
    """
    failed_previous_execution_status = _get_dependency_step_failed_status(
        config_unit, step_name)

    if failed_previous_execution_status is not None:
        cascaded_execution_status = _get_cascaded_failure_execution_status(
            failed_previous_execution_status, step_name)
        store_past_execution_status(config_unit, cascaded_execution_status)

        return cascaded_execution_status

    step = config_unit.steps[step_name]
    command = '(cd "' + config_unit.directory + '"; \n' + step.command + '\n)'

    return_code, output = sh(command, detached=step.background)
    successful = return_code == 0

    step_execution_status = \
        StepExecutionStatus(step_name, successful=successful, output=output)
    store_past_execution_status(config_unit, step_execution_status)

    return step_execution_status


def _get_dependency_step_failed_status(
        config_unit: ConfigUnit,
        target_step_name: str) -> Optional[StepExecutionStatus]:

    for step_name in config_unit.steps.keys():
        past_execution_status = get_past_execution_status(
            config_unit, step_name)

        if step_name == target_step_name:
            # we have reached the target step
            # at first execution the status will be None
            return past_execution_status

        if past_execution_status is None:
            # missing intermediate step
            past_execution_status = run_step(config_unit, step_name)

        if past_execution_status.successful:
            continue

        # not successful
        return past_execution_status

    message = 'Unknown step ' + target_step_name + ' in ' + config_unit.name
    raise UnknownStepException(message)


def _get_cascaded_failure_execution_status(
        failed_previous_execution_status: StepExecutionStatus,
        step_name: str) -> StepExecutionStatus:

    if failed_previous_execution_status.step_name == step_name:
        # Not really cascading, this is a shared dependency that has been run
        # before
        new_status = copy.deepcopy(failed_previous_execution_status)

        return new_status

    output = 'Previous failure of ' \
             + failed_previous_execution_status.step_name

    if failed_previous_execution_status.restored:
        output += ' (restored)'

    return StepExecutionStatus(step_name, ignored=True, successful=False,
                               output=output)
