import os
import pickle
from typing import Optional

from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.stepexecutionstatus.StepExecutionStatus import StepExecutionStatus
from drkns.context.Context import context
from drkns.context.get_unit_step_path import get_unit_step_path


def get_past_execution_status(
        config_unit: ConfigUnit,
        step_name: str) \
        -> Optional[StepExecutionStatus]:
    persistence_path = get_unit_step_path(config_unit, step_name)

    if persistence_path in context.cached_execution_status:
        return context.cached_execution_status[persistence_path]

    if os.path.exists(persistence_path):
        with open(persistence_path, 'rb') as persisted_file:
            step_execution_status = pickle.load(persisted_file)
            step_execution_status.restored = True
            context.cached_execution_status[persistence_path] =\
                step_execution_status
            return step_execution_status

    return None
