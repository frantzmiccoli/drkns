import pickle

from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.stepexecutionstatus.StepExecutionStatus import StepExecutionStatus
from drkns.context.Context import context
from drkns.context.get_unit_step_path import get_unit_step_path


def store_past_execution_status(
        config_unit: ConfigUnit,
        step_execution_status: StepExecutionStatus):
    persistence_path = get_unit_step_path(
        config_unit, step_execution_status.step_name)
    with open(persistence_path, 'wb') as persistence_file:
        pickle.dump(step_execution_status, persistence_file)

    context.cached_execution_status[persistence_path] = step_execution_status
