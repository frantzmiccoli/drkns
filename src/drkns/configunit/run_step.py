import copy
from typing import List, Optional

from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit.StepExecutionStatus import StepExecutionStatus
from drkns.exception import UnknownStepException
from drkns.util import sh
from drkns.context.get_past_execution_status import \
    get_past_execution_status
from drkns.context.store_past_execution_status import \
    store_past_execution_status


def run_step(config_unit: ConfigUnit, step_name: str, cleanup: bool = False) \
        -> List[StepExecutionStatus]:
    """
    This function is meant to run a specific step and the previous steps if they
    haven't been run

    :param config_unit:
    :param step_name:
    :param cleanup:
    :return:
    """
    failed_previous_execution_status = _get_dependency_step_failed_status(
        config_unit, step_name, cleanup)

    if (not cleanup) and (failed_previous_execution_status is not None):
        cascaded_execution_status = _get_cascaded_failure_execution_status(
            failed_previous_execution_status, step_name)
        store_past_execution_status(
            config_unit, cascaded_execution_status, cleanup)

        return [cascaded_execution_status]

    steps = config_unit.steps
    if cleanup:
        steps = config_unit.cleanupSteps

    step = steps[step_name]
    command = '(cd "' + config_unit.directory + '"; \n' + step.command + '\n)'

    return_code, output = sh(command, detached=step.background)
    successful = return_code == 0

    step_execution_status = \
        StepExecutionStatus(config_unit.name, step_name,
                            successful=successful, output=output,
                            cleanup=cleanup)
    store_past_execution_status(config_unit, step_execution_status, cleanup)

    return [step_execution_status]


def _get_dependency_step_failed_status(
        config_unit: ConfigUnit,
        target_step_name: str,
        cleanup: bool) -> Optional[StepExecutionStatus]:

    steps = config_unit.steps
    if cleanup:
        steps = config_unit.cleanupSteps

    for step_name in steps.keys():
        past_execution_status = get_past_execution_status(
            config_unit, step_name, cleanup)

        if step_name == target_step_name:
            # we have reached the target step
            # at first execution the status will be None
            return past_execution_status

        if past_execution_status is None:
            # missing intermediate step
            past_execution_status = run_step(config_unit, step_name)[-1]

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

    config_unit_name = failed_previous_execution_status.config_unit_name
    cleanup = failed_previous_execution_status.cleanup

    return StepExecutionStatus(config_unit_name, step_name, ignored=True,
                               successful=False, cleanup=cleanup,
                               output=output)
